"""
Account, checkout and chat endpoints for the teammate's frontend.

That UI (GutGraph-Website/index.html + script.js) was built against a backend that
never made it into the repo — only its compiled ``db.cpython-310.pyc`` and
``llm_service.cpython-310.pyc`` came along with the upload. This module rebuilds
the contract the frontend actually calls, and nothing more:

    POST /api/auth/send-otp        {email}                          -> {dev_otp}
    POST /api/auth/verify-otp      {email, otp}                     -> {verified}
    GET  /api/auth/generate-random                                  -> {username, password}
    POST /api/auth/register        {email, username, password}      -> {user, profile}
    POST /api/auth/login           {identifier, password}           -> {user, profile}
    POST /api/user/profile         {user_id, medical_history[], ...}-> {profile}
    GET  /api/user/profile?user_id=N                                -> {profile}
    POST /api/checkout/calculate   {user_id, items[], coupon_code}   -> bill
    POST /api/chat                 {user_id, message}               -> {reply}
    GET  /api/chat/history?user_id=N                                -> [{role, content, ts}]

The SQLite schema is the one recovered from the uploaded ``gutgraph.db``
(users / profiles / otps / chat_history / bills) so a database from that build
opens here unchanged. Money rules mirror the frontend's own cart math, which the
invoice rows in that database confirm: 10% campus discount, CGST+SGST at 2.5%
each on the discounted amount, delivery waived (list value ₹40).

Two honest caveats:
  * Passwords are stored as a bare sha256 hex digest. That is what the uploaded
    rows look like (64 hex chars), it is not a salted KDF, and it should be
    replaced with argon2/bcrypt before this is exposed to anyone real.
  * OTP delivery is dev-mode: the code is returned in the response because the
    frontend prints it on screen. Wire a mailer before this leaves the LAN.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import random
import secrets
import sqlite3
import time
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from agent import llm

DB_PATH = pathlib.Path(__file__).resolve().with_name("gutgraph.db")
OTP_TTL_SECONDS = 300
VERIFIED_TTL_SECONDS = 900
PRODUCT_CURRENCY = "₹"

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS profiles (
    user_id INTEGER PRIMARY KEY,
    medical_history TEXT DEFAULT '[]',
    current_situation TEXT DEFAULT '',
    allergies TEXT DEFAULT '[]',
    dietary_pref TEXT DEFAULT 'Vegetarian',
    spice_tolerance TEXT DEFAULT 'Medium',
    medications TEXT DEFAULT '',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS otps (
    email TEXT PRIMARY KEY,
    otp TEXT NOT NULL,
    expires_at REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS bills (
    bill_id TEXT PRIMARY KEY,
    user_id INTEGER,
    items_json TEXT NOT NULL,
    subtotal REAL NOT NULL,
    discount REAL NOT NULL,
    tax REAL NOT NULL,
    total REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

router = APIRouter(prefix="/api", tags=["gutgraph"])

# email -> expiry, for the gap between "verify OTP" and "register"
_verified: Dict[str, float] = {}


# --------------------------------------------------------------------------- #
# storage
# --------------------------------------------------------------------------- #
@contextmanager
def _db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _db() as conn:
        conn.executescript(SCHEMA)


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def _public_user(row: sqlite3.Row) -> Dict[str, Any]:
    return {"id": row["id"], "email": row["email"], "username": row["username"]}


def _profile_dict(row: Optional[sqlite3.Row]) -> Dict[str, Any]:
    if row is None:
        return {
            "medical_history": [],
            "current_situation": "",
            "allergies": [],
            "dietary_pref": "Vegetarian",
            "spice_tolerance": "Medium",
            "medications": "",
        }
    def _list(raw: Any) -> List[str]:
        try:
            val = json.loads(raw) if isinstance(raw, str) else (raw or [])
        except (TypeError, ValueError):
            return []
        return val if isinstance(val, list) else []

    return {
        "medical_history": _list(row["medical_history"]),
        "current_situation": row["current_situation"] or "",
        "allergies": _list(row["allergies"]),
        "dietary_pref": row["dietary_pref"] or "Vegetarian",
        "spice_tolerance": row["spice_tolerance"] or "Medium",
        "medications": row["medications"] or "",
    }


def _profile_for(conn: sqlite3.Connection, user_id: int) -> Dict[str, Any]:
    row = conn.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,)).fetchone()
    return _profile_dict(row)


# --------------------------------------------------------------------------- #
# payloads
# --------------------------------------------------------------------------- #
class EmailIn(BaseModel):
    email: str


class VerifyIn(BaseModel):
    email: str
    otp: str


class RegisterIn(BaseModel):
    email: str
    username: str
    password: str


class LoginIn(BaseModel):
    identifier: str
    password: str


class ProfileIn(BaseModel):
    user_id: int
    medical_history: List[str] = []
    current_situation: str = ""
    allergies: List[str] = []
    dietary_pref: str = "Vegetarian"
    spice_tolerance: str = "Medium"
    medications: str = ""


class CartItemIn(BaseModel):
    id: str
    name: str
    price: float
    quantity: int


class CheckoutIn(BaseModel):
    user_id: Optional[int] = None
    items: List[CartItemIn]
    coupon_code: Optional[str] = None


class ChatIn(BaseModel):
    user_id: Optional[int] = None
    message: str


# --------------------------------------------------------------------------- #
# auth
# --------------------------------------------------------------------------- #
@router.post("/auth/send-otp")
def send_otp(body: EmailIn):
    email = body.email.strip().lower()
    if "@" not in email or "." not in email.split("@")[-1]:
        raise HTTPException(status_code=400, detail="Please enter a valid email address.")
    otp = f"{secrets.randbelow(900000) + 100000}"
    with _db() as conn:
        conn.execute(
            "INSERT INTO otps (email, otp, expires_at) VALUES (?, ?, ?) "
            "ON CONFLICT(email) DO UPDATE SET otp = excluded.otp, expires_at = excluded.expires_at",
            (email, otp, time.time() + OTP_TTL_SECONDS),
        )
    return {
        "ok": True,
        "email": email,
        "dev_otp": otp,
        "expires_in": OTP_TTL_SECONDS,
        "delivery": "dev",  # no mailer configured; the UI prints this on screen
    }


@router.post("/auth/verify-otp")
def verify_otp(body: VerifyIn):
    email = body.email.strip().lower()
    with _db() as conn:
        row = conn.execute("SELECT * FROM otps WHERE email = ?", (email,)).fetchone()
        if row is None or row["expires_at"] < time.time() or row["otp"] != body.otp.strip():
            raise HTTPException(status_code=400, detail="Invalid or expired OTP code.")
        conn.execute("DELETE FROM otps WHERE email = ?", (email,))
    _verified[email] = time.time() + VERIFIED_TTL_SECONDS
    return {"ok": True, "verified": True, "email": email}


_ADJECTIVES = ["Curcumin", "Haldi", "Zesty", "Bifido", "Microbe", "Spice",
               "Botanical", "Kombucha", "Chaas", "Ferment", "Flavour"]
_NOUNS = ["Sage", "Guru", "Alchemist", "Crafter", "Knight", "Explorer",
          "Master", "Botanist", "Pioneer", "Scholar"]


@router.get("/auth/generate-random")
def generate_random():
    return {
        "username": f"{random.choice(_ADJECTIVES)}{random.choice(_NOUNS)}_{random.randint(10, 99)}",
        "password": f"Gut#{random.choice(_ADJECTIVES)}{random.randint(100, 999)}",
    }


@router.post("/auth/register")
def register(body: RegisterIn):
    email = body.email.strip().lower()
    username = body.username.strip()
    if not (email and username and body.password):
        raise HTTPException(status_code=400, detail="Email, username and password are all required.")
    if not _verified.pop(email, 0) > time.time():
        # the UI's step 1 must have passed; re-verify rather than silently trusting
        raise HTTPException(status_code=400, detail="Please verify your email code first.")
    with _db() as conn:
        try:
            cur = conn.execute(
                "INSERT INTO users (email, username, password_hash) VALUES (?, ?, ?)",
                (email, username, hash_password(body.password)),
            )
        except sqlite3.IntegrityError as exc:
            dup = "email" if "users.email" in str(exc) else "username"
            raise HTTPException(status_code=409, detail=f"That {dup} is already registered.") from exc
        user_id = int(cur.lastrowid or 0)
        conn.execute("INSERT OR IGNORE INTO profiles (user_id) VALUES (?)", (user_id,))
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        profile = _profile_for(conn, user_id)
    return {"user": _public_user(row), "profile": profile}


@router.post("/auth/login")
def login(body: LoginIn):
    ident = body.identifier.strip()
    with _db() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE lower(email) = ? OR lower(username) = ?",
            (ident.lower(), ident.lower()),
        ).fetchone()
        if row is None or row["password_hash"] != hash_password(body.password):
            raise HTTPException(status_code=401, detail="Invalid credentials. Please try again.")
        profile = _profile_for(conn, row["id"])
    return {"user": _public_user(row), "profile": profile}


# --------------------------------------------------------------------------- #
# profile ("lifetime gut memory")
# --------------------------------------------------------------------------- #
@router.post("/user/profile")
def save_profile(body: ProfileIn):
    with _db() as conn:
        exists = conn.execute("SELECT 1 FROM users WHERE id = ?", (body.user_id,)).fetchone()
        if exists is None:
            raise HTTPException(status_code=404, detail="Unknown user_id.")
        conn.execute(
            """
            INSERT INTO profiles (user_id, medical_history, current_situation, allergies,
                                  dietary_pref, spice_tolerance, medications, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id) DO UPDATE SET
                medical_history = excluded.medical_history,
                current_situation = excluded.current_situation,
                allergies = excluded.allergies,
                dietary_pref = excluded.dietary_pref,
                spice_tolerance = excluded.spice_tolerance,
                medications = excluded.medications,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                body.user_id,
                json.dumps(body.medical_history),
                body.current_situation,
                json.dumps(body.allergies),
                body.dietary_pref,
                body.spice_tolerance,
                body.medications,
            ),
        )
        profile = _profile_for(conn, body.user_id)
    return {"ok": True, "profile": profile}


@router.get("/user/profile")
def get_profile(user_id: int):
    with _db() as conn:
        return {"profile": _profile_for(conn, user_id)}


# --------------------------------------------------------------------------- #
# checkout — same arithmetic as the UI's calculateCartTotals()
# --------------------------------------------------------------------------- #
def _money(x: float) -> float:
    return round(x + 0.0, 2)


def _totals(items: List[CartItemIn]) -> Dict[str, float]:
    subtotal = _money(sum(i.price * i.quantity for i in items))
    discount = _money(subtotal * 0.10)          # campus & student health discount
    taxable = _money(max(0.0, subtotal - discount))
    cgst = _money(taxable * 0.025)
    sgst = _money(taxable * 0.025)
    tax = _money(cgst + sgst)
    return {
        "subtotal": subtotal,
        "discount_amount": discount,
        "taxable_amount": taxable,
        "cgst": cgst,
        "sgst": sgst,
        "total_tax": tax,
        "delivery_fee": 0.00,
        "original_delivery": 40.00,
        "grand_total": _money(taxable + tax),
    }


@router.post("/checkout/calculate")
def checkout_calculate(body: CheckoutIn):
    if not body.items:
        raise HTTPException(status_code=400, detail="Your Sip Stash is empty. Add cans first!")
    totals = _totals(body.items)
    now = datetime.now()
    bill_id = f"GG-INV-{now.strftime('%y%m%d')}-{secrets.randbelow(9000) + 1000}"
    lines = [
        {
            "id": i.id,
            "name": i.name,
            "unit_price": _money(i.price),
            "quantity": i.quantity,
            "line_total": _money(i.price * i.quantity),
        }
        for i in body.items
    ]
    bill = {
        "bill_id": bill_id,
        "timestamp": now.strftime("%d %b %Y, %H:%M"),
        **totals,
        "items": lines,
        "coupon_code": (body.coupon_code or "").strip() or None,
        "loyalty_points": int(totals["grand_total"] * 0.1) if body.user_id else 0,
        "currency": PRODUCT_CURRENCY,
    }
    with _db() as conn:
        conn.execute(
            "INSERT INTO bills (bill_id, user_id, items_json, subtotal, discount, tax, total) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (bill_id, body.user_id, json.dumps(lines), totals["subtotal"],
             totals["discount_amount"], totals["total_tax"], totals["grand_total"]),
        )
    return bill


# --------------------------------------------------------------------------- #
# chat — profile-aware, backed by whichever LLM provider is configured
# --------------------------------------------------------------------------- #
SYSTEM_PROMPT = (
    "You are GutGraph AI, an expert food scientist and gut mixologist. You give short, "
    "specific, practical answers about meals, gut health and which GutGraph botanical drink "
    "pairs with what someone ate. Name the flavour compounds or fibre/sugar numbers when you "
    "know them. Never diagnose, never prescribe medicine, and say plainly that you are not a "
    "doctor when a health condition comes up. Keep it under 120 words and skip preamble."
)


def _memory_block(profile: Dict[str, Any]) -> str:
    parts = []
    if profile["medical_history"]:
        parts.append("conditions: " + ", ".join(profile["medical_history"]))
    if profile["allergies"]:
        parts.append("allergies: " + ", ".join(profile["allergies"]))
    if profile["dietary_pref"]:
        parts.append("diet: " + profile["dietary_pref"])
    if profile["spice_tolerance"]:
        parts.append("spice tolerance: " + profile["spice_tolerance"])
    if profile["medications"]:
        parts.append("medications: " + profile["medications"])
    if profile["current_situation"]:
        parts.append("right now: " + profile["current_situation"])
    return "; ".join(parts)


@router.post("/chat")
async def chat(body: ChatIn):
    message = body.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Say something first.")

    memory = ""
    turns: List[Dict[str, str]] = []
    with _db() as conn:
        if body.user_id:
            profile = _profile_for(conn, body.user_id)
            memory = _memory_block(profile)
            rows = conn.execute(
                "SELECT role, content FROM chat_history WHERE user_id = ? "
                "ORDER BY id DESC LIMIT 8",
                (body.user_id,),
            ).fetchall()
            turns = [{"role": r["role"], "content": r["content"]} for r in reversed(rows)]
            conn.execute(
                "INSERT INTO chat_history (user_id, role, content) VALUES (?, 'user', ?)",
                (body.user_id, message),
            )

    system = SYSTEM_PROMPT
    if memory:
        system += (
            "\n\nProfile memory (saved by this user, reuse it silently instead of asking again): "
            + memory
        )
    messages = [{"role": "system", "content": system}]
    messages += [t for t in turns if t["role"] in ("user", "assistant")]
    messages.append({"role": "user", "content": message})

    try:
        reply = await llm.complete(messages)
    except llm.LLMError as exc:
        raise HTTPException(status_code=503, detail=f"Chat model unavailable: {exc}") from exc

    if memory:
        reply = f"🧬 **[Profile Memory Active]** Factoring in your saved profile ({memory}).\n\n{reply}"

    if body.user_id:
        with _db() as conn:
            conn.execute(
                "INSERT INTO chat_history (user_id, role, content) VALUES (?, 'assistant', ?)",
                (body.user_id, reply),
            )
    return {"reply": reply, "memory_used": bool(memory)}


@router.get("/chat/history")
def chat_history(user_id: int, limit: int = 50):
    with _db() as conn:
        rows = conn.execute(
            "SELECT role, content, timestamp FROM chat_history WHERE user_id = ? "
            "ORDER BY id ASC LIMIT ?",
            (user_id, limit),
        ).fetchall()
    return [{"role": r["role"], "content": r["content"], "timestamp": r["timestamp"]} for r in rows]


init_db()
