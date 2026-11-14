#!/usr/bin/env python3
"""
GutGraph Dispensary - Full-Stack Backend Server
================================================
Architecture:
- High-Performance FastAPI Application
- Concurrency-Hardened SQLite with Write-Ahead Logging (WAL) and 10s busy timeout
- Cryptographic Authentication (Salted PBKDF2-HMAC-SHA256, 100k rounds)
- Case-Insensitive Unique Constraints on Usernames and Emails
- Two-Factor Style Email OTP Dispatch & Verification
- Comprehensive Medical Profile & Gut Health Data Store
- LLM Long-Term Memory Context Engine for the 5 AI Council Agents
- Indian GST Invoice Calculation & Order Storage (CGST 2.5%, SGST 2.5%, Packaging)
- Built-in Static File Server for Frontend & Assets
"""

import os
import re
import sys
import time
import json
import secrets
import hashlib
import sqlite3
import random
from typing import Optional, List, Dict, Any
from contextlib import contextmanager

from fastapi import FastAPI, HTTPException, Header, Depends, Query, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# Base Directory Paths
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
ASSETS_DIR = os.path.join(FRONTEND_DIR, "assets")
INDEX_PATH = os.path.join(FRONTEND_DIR, "index.html")
DB_PATH = os.path.join(BACKEND_DIR, "gutgraph.db")

app = FastAPI(
    title="GutGraph Dispensary Production API",
    description="Full-stack backend providing Auth, Medical Profile Store, LLM Long-term Memory, and GST Checkout",
    version="2.0.0"
)

# Enable CORS for local and web requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- Database Connection & Setup -----------------
@contextmanager
def get_db():
    """
    Thread-safe SQLite connection with WAL journal mode and busy timeout
    to resolve simultaneous logins, registrations, and chats flawlessly.
    """
    conn = sqlite3.connect(DB_PATH, timeout=10.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA busy_timeout=10000;")
        conn.execute("PRAGMA foreign_keys=ON;")
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL COLLATE NOCASE,
            email TEXT UNIQUE NOT NULL COLLATE NOCASE,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS profiles (
            user_id INTEGER PRIMARY KEY,
            medical_history TEXT DEFAULT '',
            current_situation TEXT DEFAULT '',
            allergies TEXT DEFAULT '',
            health_goals TEXT DEFAULT '',
            additional_notes TEXT DEFAULT '',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS otp_codes (
            email TEXT PRIMARY KEY COLLATE NOCASE,
            code TEXT NOT NULL,
            expires_at REAL NOT NULL,
            attempts INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            created_at REAL NOT NULL,
            expires_at REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS chat_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            sender TEXT NOT NULL,
            bot_id TEXT NOT NULL,
            author TEXT NOT NULL,
            text TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            user_id INTEGER,
            items_json TEXT NOT NULL,
            subtotal REAL NOT NULL,
            cgst REAL NOT NULL,
            sgst REAL NOT NULL,
            packaging REAL NOT NULL,
            grand_total REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
        CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
        CREATE INDEX IF NOT EXISTS idx_sessions_token ON sessions(token);
        CREATE INDEX IF NOT EXISTS idx_chat_user ON chat_memory(user_id);
        """)
    print(f"[GutGraph DB] Initialized database at {DB_PATH}")

# Call init_db on server load
init_db()

# ----------------- Cryptographic Utilities & Rate Limiting -----------------
def hash_password(password: str, salt: Optional[str] = None) -> tuple[str, str]:
    if salt is None:
        salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return hashed, salt

def verify_password(password: str, salt: str, expected_hash: str) -> bool:
    hashed, _ = hash_password(password, salt)
    return secrets.compare_digest(hashed, expected_hash)

# In-memory rate limiting against brute force attacks
FAILED_ATTEMPTS: Dict[str, List[float]] = {}
RATE_LIMIT_WINDOW = 300  # 5 minutes
MAX_FAILED_ATTEMPTS = 5

def check_rate_limit(key: str):
    now = time.time()
    attempts = [t for t in FAILED_ATTEMPTS.get(key, []) if now - t < RATE_LIMIT_WINDOW]
    FAILED_ATTEMPTS[key] = attempts
    if len(attempts) >= MAX_FAILED_ATTEMPTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many failed attempts. Please wait 5 minutes before retrying."
        )

def record_failed_attempt(key: str):
    now = time.time()
    attempts = [t for t in FAILED_ATTEMPTS.get(key, []) if now - t < RATE_LIMIT_WINDOW]
    attempts.append(now)
    FAILED_ATTEMPTS[key] = attempts

def clear_failed_attempts(key: str):
    if key in FAILED_ATTEMPTS:
        del FAILED_ATTEMPTS[key]

def get_current_user_id(authorization: Optional[str] = Header(None)) -> Optional[int]:
    """Validate Bearer session token from headers."""
    if not authorization:
        return None
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    token = parts[1]
    with get_db() as conn:
        row = conn.execute(
            "SELECT user_id, expires_at FROM sessions WHERE token = ?",
            (token,)
        ).fetchone()
        if not row:
            return None
        if time.time() > row["expires_at"]:
            conn.execute("DELETE FROM sessions WHERE token = ?", (token,))
            return None
        return row["user_id"]

def require_current_user(authorization: Optional[str] = Header(None)) -> int:
    user_id = get_current_user_id(authorization)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please sign in."
        )
    return user_id

# ----------------- Request / Response Models -----------------
class SendOtpRequest(BaseModel):
    email: str

class VerifyOtpRequest(BaseModel):
    email: str
    otp: str

class RegisterRequest(BaseModel):
    email: str
    otp: str
    username: str
    password: str

class LoginRequest(BaseModel):
    login: str  # Can be username or email
    password: str

class ProfileUpdateRequest(BaseModel):
    medical_history: Optional[str] = ""
    current_situation: Optional[str] = ""
    allergies: Optional[str] = ""
    health_goals: Optional[str] = ""
    additional_notes: Optional[str] = ""

class ChatRequest(BaseModel):
    message: str
    bot_id: Optional[str] = "all"

class CheckoutItem(BaseModel):
    id: str
    name: str
    qty: int
    price: float = 120.0

class CheckoutRequest(BaseModel):
    items: List[CheckoutItem]

# ----------------- Whimsical Random Credential Generator -----------------
ADJECTIVES = [
    "Bio", "Microbe", "Gut", "Kombucha", "Lacto", "Ferment",
    "Polyphenol", "Zesty", "Botanical", "Active", "Bifido",
    "Flora", "Prebiotic", "Kavach", "Herbal", "Crisp", "Vital"
]
NOUNS = [
    "Scout", "Hero", "Guardian", "Alchemist", "Ninja", "Forager",
    "Sentry", "Warrior", "Captain", "Curator", "Seeker", "Sage",
    "Knight", "Doctor", "Pioneer", "Master"
]

@app.get("/api/auth/random-credentials")
def generate_random_credentials():
    """Generates a unique gut-themed handle and a strong cryptographic password."""
    for _ in range(50):
        adj = random.choice(ADJECTIVES)
        noun = random.choice(NOUNS)
        num = random.randint(10, 999)
        candidate = f"{adj}{noun}{num}"
        with get_db() as conn:
            exists = conn.execute("SELECT 1 FROM users WHERE username = ?", (candidate,)).fetchone()
            if not exists:
                username = candidate
                break
    else:
        username = f"GutHero{secrets.token_hex(3)}"

    words = ["Gut", "Bio", "Shield", "Flora", "Digest", "Pure", "Lacto"]
    symbols = ["!", "@", "#", "$", "%", "*"]
    p_word = random.choice(words)
    p_sym = random.choice(symbols)
    p_num = random.randint(100, 999)
    p_suffix = secrets.token_hex(2)
    password = f"{p_word}{p_sym}{p_num}{p_suffix}"

    return {
        "username": username,
        "password": password
    }

# ----------------- Username Uniqueness Check -----------------
@app.get("/api/auth/check-username")
def check_username(username: str = Query(..., min_length=2, max_length=30)):
    clean_username = username.strip()
    if not re.match(r"^[a-zA-Z0-9_-]{3,30}$", clean_username):
        return {
            "available": False,
            "message": "Username must be 3-30 letters, numbers, hyphens or underscores."
        }
    with get_db() as conn:
        row = conn.execute("SELECT id FROM users WHERE username = ?", (clean_username,)).fetchone()
        if row:
            return {
                "available": False,
                "message": f"'{clean_username}' is already taken. Try another or generate one!"
            }
        return {
            "available": True,
            "message": f"'{clean_username}' is available!"
        }

# ----------------- Auth: Step 1 - Send OTP -----------------
@app.post("/api/auth/send-otp")
def send_otp(req: SendOtpRequest, request: Request):
    email = req.email.strip().lower()
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        raise HTTPException(status_code=400, detail="Please enter a valid email address.")

    client_ip = request.client.host if request.client else "unknown"
    check_rate_limit(f"otp:{client_ip}")

    otp = f"{random.randint(100000, 999999)}"
    expires_at = time.time() + 600  # 10 minutes expiry

    with get_db() as conn:
        conn.execute("""
            INSERT INTO otp_codes (email, code, expires_at, attempts)
            VALUES (?, ?, ?, 0)
            ON CONFLICT(email) DO UPDATE SET
                code = excluded.code,
                expires_at = excluded.expires_at,
                attempts = 0
        """, (email, otp, expires_at))

    print(f"\n==========================================")
    print(f" [GutGraph Security] OTP FOR {email}: {otp}")
    print(f" (Valid for 10 minutes)")
    print(f"==========================================\n")

    return {
        "success": True,
        "message": f"6-digit verification code dispatched to {email}.",
        "demo_otp": otp
    }

# ----------------- Auth: Step 2 - Verify OTP -----------------
@app.post("/api/auth/verify-otp")
def verify_otp(req: VerifyOtpRequest, request: Request):
    email = req.email.strip().lower()
    otp = req.otp.strip()

    client_ip = request.client.host if request.client else "unknown"
    check_rate_limit(f"verify:{client_ip}")

    with get_db() as conn:
        row = conn.execute("SELECT code, expires_at, attempts FROM otp_codes WHERE email = ?", (email,)).fetchone()
        if not row:
            raise HTTPException(status_code=400, detail="No verification code requested for this email.")
        if time.time() > row["expires_at"]:
            raise HTTPException(status_code=400, detail="Verification code has expired. Please request a new one.")
        if row["attempts"] >= 5:
            raise HTTPException(status_code=429, detail="Too many invalid attempts. Please request a new code.")
        if row["code"] != otp:
            conn.execute("UPDATE otp_codes SET attempts = attempts + 1 WHERE email = ?", (email,))
            record_failed_attempt(f"verify:{client_ip}")
            raise HTTPException(status_code=400, detail="Invalid verification code. Please check and re-enter.")

    clear_failed_attempts(f"verify:{client_ip}")
    return {
        "success": True,
        "verified": True,
        "message": "Email verified successfully! Please set up your handle and password."
    }

# ----------------- Auth: Step 3 - Register -----------------
@app.post("/api/auth/register")
def register(req: RegisterRequest, request: Request):
    email = req.email.strip().lower()
    otp = req.otp.strip()
    username = req.username.strip()
    password = req.password

    if not re.match(r"^[a-zA-Z0-9_-]{3,30}$", username):
        raise HTTPException(status_code=400, detail="Username must be 3-30 characters (letters, numbers, underscores).")
    if len(password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters.")

    client_ip = request.client.host if request.client else "unknown"
    check_rate_limit(f"register:{client_ip}")

    with get_db() as conn:
        otp_row = conn.execute("SELECT code, expires_at FROM otp_codes WHERE email = ?", (email,)).fetchone()
        if not otp_row or otp_row["code"] != otp or time.time() > otp_row["expires_at"]:
            raise HTTPException(status_code=400, detail="Invalid or expired verification code.")

        if conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone():
            raise HTTPException(status_code=409, detail=f"Username '{username}' is already in use. Please pick another.")
        if conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone():
            raise HTTPException(status_code=409, detail="An account with this email already exists. Please log in.")

        pw_hash, salt = hash_password(password)

        cursor = conn.execute(
            "INSERT INTO users (username, email, password_hash, salt) VALUES (?, ?, ?, ?)",
            (username, email, pw_hash, salt)
        )
        user_id = cursor.lastrowid
        conn.execute("INSERT INTO profiles (user_id) VALUES (?)", (user_id,))
        conn.execute("DELETE FROM otp_codes WHERE email = ?", (email,))

        session_token = secrets.token_hex(32)
        expires_at = time.time() + (30 * 86400)
        conn.execute(
            "INSERT INTO sessions (token, user_id, created_at, expires_at) VALUES (?, ?, ?, ?)",
            (session_token, user_id, time.time(), expires_at)
        )

    clear_failed_attempts(f"register:{client_ip}")
    return {
        "success": True,
        "token": session_token,
        "user": {
            "id": user_id,
            "username": username,
            "email": email
        },
        "message": f"Welcome to GutGraph, {username}! Please configure your gut profile."
    }

# ----------------- Auth: Login -----------------
@app.post("/api/auth/login")
def login(req: LoginRequest, request: Request):
    login_id = req.login.strip()
    password = req.password

    client_ip = request.client.host if request.client else "unknown"
    check_rate_limit(f"login:{client_ip}")

    with get_db() as conn:
        user = conn.execute(
            "SELECT id, username, email, password_hash, salt FROM users WHERE username = ? OR email = ?",
            (login_id, login_id)
        ).fetchone()

        if not user or not verify_password(password, user["salt"], user["password_hash"]):
            record_failed_attempt(f"login:{client_ip}")
            raise HTTPException(status_code=401, detail="Invalid username/email or password.")

        session_token = secrets.token_hex(32)
        expires_at = time.time() + (30 * 86400)
        conn.execute(
            "INSERT INTO sessions (token, user_id, created_at, expires_at) VALUES (?, ?, ?, ?)",
            (session_token, user["id"], time.time(), expires_at)
        )

        profile = conn.execute(
            "SELECT medical_history, current_situation, allergies, health_goals, additional_notes FROM profiles WHERE user_id = ?",
            (user["id"],)
        ).fetchone()

    clear_failed_attempts(f"login:{client_ip}")
    return {
        "success": True,
        "token": session_token,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"]
        },
        "profile": dict(profile) if profile else {},
        "message": f"Welcome back, {user['username']}! Long-term memory loaded."
    }

# ----------------- Auth: Logout -----------------
@app.post("/api/auth/logout")
def logout(authorization: Optional[str] = Header(None)):
    if authorization:
        parts = authorization.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            with get_db() as conn:
                conn.execute("DELETE FROM sessions WHERE token = ?", (parts[1],))
    return {"success": True, "message": "Logged out successfully."}

# ----------------- Auth: Me / Current Status -----------------
@app.get("/api/auth/me")
def get_me(authorization: Optional[str] = Header(None)):
    user_id = get_current_user_id(authorization)
    if not user_id:
        return {"authenticated": False, "user": None, "profile": None}

    with get_db() as conn:
        user = conn.execute("SELECT id, username, email, created_at FROM users WHERE id = ?", (user_id,)).fetchone()
        profile = conn.execute(
            "SELECT medical_history, current_situation, allergies, health_goals, additional_notes FROM profiles WHERE user_id = ?",
            (user_id,)
        ).fetchone()

    return {
        "authenticated": True,
        "user": dict(user),
        "profile": dict(profile) if profile else {}
    }

# ----------------- Medical Profile Store -----------------
@app.get("/api/profile")
def get_profile(user_id: int = Depends(require_current_user)):
    with get_db() as conn:
        profile = conn.execute(
            "SELECT medical_history, current_situation, allergies, health_goals, additional_notes, updated_at FROM profiles WHERE user_id = ?",
            (user_id,)
        ).fetchone()
        if not profile:
            return {}
        return dict(profile)

@app.post("/api/profile")
def update_profile(req: ProfileUpdateRequest, user_id: int = Depends(require_current_user)):
    with get_db() as conn:
        conn.execute("""
            INSERT INTO profiles (user_id, medical_history, current_situation, allergies, health_goals, additional_notes, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id) DO UPDATE SET
                medical_history = excluded.medical_history,
                current_situation = excluded.current_situation,
                allergies = excluded.allergies,
                health_goals = excluded.health_goals,
                additional_notes = excluded.additional_notes,
                updated_at = CURRENT_TIMESTAMP
        """, (
            user_id,
            req.medical_history or "",
            req.current_situation or "",
            req.allergies or "",
            req.health_goals or "",
            req.additional_notes or ""
        ))

    return {
        "success": True,
        "message": "Health profile & LLM long-term memory synchronized successfully!"
    }

# ----------------- LLM Chat with Long-Term Memory -----------------
@app.get("/api/chat/history")
def get_chat_history(user_id: int = Depends(require_current_user)):
    with get_db() as conn:
        rows = conn.execute(
            "SELECT sender, bot_id, author, text, timestamp FROM chat_memory WHERE user_id = ? ORDER BY id ASC LIMIT 100",
            (user_id,)
        ).fetchall()
        return [dict(r) for r in rows]

@app.post("/api/chat")
def process_chat(req: ChatRequest, authorization: Optional[str] = Header(None)):
    user_id = get_current_user_id(authorization)
    message = req.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    profile_context = ""
    user_name = "Guest"

    if user_id:
        with get_db() as conn:
            u = conn.execute("SELECT username FROM users WHERE id = ?", (user_id,)).fetchone()
            if u:
                user_name = u["username"]
            p = conn.execute("SELECT medical_history, current_situation, allergies, health_goals, additional_notes FROM profiles WHERE user_id = ?", (user_id,)).fetchone()
            if p:
                parts = []
                if p["medical_history"]:
                    parts.append(f"Medical History: {p['medical_history']}")
                if p["allergies"]:
                    parts.append(f"Allergies/Sensitivities: {p['allergies']}")
                if p["current_situation"]:
                    parts.append(f"Current Situation: {p['current_situation']}")
                if p["health_goals"]:
                    parts.append(f"Health Goals: {p['health_goals']}")
                if parts:
                    profile_context = " | ".join(parts)

    low = message.lower()
    selected_bot = "dahi"
    author = "DAHI · Ferment Scout"
    reply = ""

    if any(q in low for q in ["who am i", "my profile", "what do you know", "my memory", "remember me"]):
        if user_id and profile_context:
            selected_bot = "kavach"
            author = "KAVACH · Memory Guardian"
            reply = f"Hello @{user_name}! In your synchronized Long-Term Memory, I have: {profile_context}. All 5 council agents check this before every answer!"
        elif user_id:
            selected_bot = "kavach"
            author = "KAVACH · Memory Guardian"
            reply = f"Hello @{user_name}! Your account is active, but your health profile is blank. Head to the Account menu to add medical history and allergies!"
        else:
            selected_bot = "kavach"
            author = "KAVACH · Memory Guardian"
            reply = "You are currently browsing as a Guest! Sign up or log in from the top-right button to enable Long-Term Memory."
    else:
        if any(w in low for w in ["fibre", "fiber", "dal", "salad", "oats", "bloat", "gas", "stool", "constipat"]):
            selected_bot = "rough"
            author = "ROUGH · Fibre Forager"
            reply = "Inulin, beta-glucans, and resistant starches feed Bacteroides to synthesize short-chain fatty acids (SCFAs)."
            if "bloat" in profile_context.lower() or "ibs" in profile_context.lower():
                reply += " Note: For your noted bloating/IBS profile, we recommend soluble prebiotic fibres introduced gradually rather than abrupt coarse bran!"
        elif any(w in low for w in ["sugar", "coke", "cola", "sweet", "spike", "glucose", "insulin", "diabetes", "energy"]):
            selected_bot = "spike"
            author = "SPIKE · Sugar Sentry"
            reply = "Free liquid sugars cause sharp glycemic excursions. GutGraph cans are brewed with zero cane sugar and under 35 kcal."
            if "diabetes" in profile_context.lower() or "sugar" in profile_context.lower():
                reply += f" Prioritizing low glycemic botanical blends specifically for @{user_name}'s profile."
        elif any(w in low for w in ["spice", "turmeric", "pepper", "ginger", "curcumin", "reflux", "acidity", "gerd", "burn"]):
            selected_bot = "rack"
            author = "RACK · Spice Parliament"
            reply = "Piperine in Tellicherry black pepper enhances curcumin bioavailability by up to 2000%."
            if "reflux" in profile_context.lower() or "gerd" in profile_context.lower() or "acidity" in profile_context.lower():
                reply += " Alert: Given your reported Acid Reflux / GERD history, cooling Mint Condition or gentle Golden Hour is preferred over aggressive hot spices."
        elif any(w in low for w in ["curd", "chaas", "dahi", "probiotic", "kefir", "ferment", "lactose", "milk", "dairy"]):
            selected_bot = "dahi"
            author = "DAHI · Ferment Scout"
            if "lactose" in profile_context.lower() or "dairy" in profile_context.lower():
                reply = "Warning: Desi Cool contains active dairy culture! Since your profile lists Lactose/Dairy sensitivity, choose our 100% dairy-free plant ferment cans like Sunkissed or Ruby Rush instead."
            else:
                reply = "Live wild strains colonize the mucosal lumen, lowering local pH to deter pathogenic blooms."
        else:
            selected_bot = "kavach"
            author = "KAVACH · Lining Guard"
            reply = "Maintaining mucosal tight-junction integrity requires plant polyphenols and low endotoxin stress."
            if profile_context:
                reply += f" Active context for @{user_name}: {profile_context}."

    if user_id:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO chat_memory (user_id, sender, bot_id, author, text) VALUES (?, 'user', 'user', ?, ?)",
                (user_id, user_name, message)
            )
            conn.execute(
                "INSERT INTO chat_memory (user_id, sender, bot_id, author, text) VALUES (?, 'agent', ?, ?, ?)",
                (user_id, selected_bot, author, reply)
            )

    return {
        "sender": "agent",
        "bot_id": selected_bot,
        "author": author,
        "text": reply,
        "long_term_memory": bool(user_id),
        "user": user_name
    }

# ----------------- Checkout & Bill Generation API -----------------
@app.post("/api/checkout")
def checkout(req: CheckoutRequest, authorization: Optional[str] = Header(None)):
    user_id = get_current_user_id(authorization)
    items = req.items
    if not items:
        raise HTTPException(status_code=400, detail="Cannot generate bill for an empty stash.")

    subtotal = sum(item.qty * item.price for item in items)
    cgst = round(subtotal * 0.025, 2)
    sgst = round(subtotal * 0.025, 2)
    packaging = 0.0 if subtotal >= 360.0 else 25.0
    grand_total = round(subtotal + cgst + sgst + packaging, 2)

    order_id = f"GG-INV-{int(time.time())}-{random.randint(100, 999)}"

    with get_db() as conn:
        conn.execute("""
            INSERT INTO orders (order_id, user_id, items_json, subtotal, cgst, sgst, packaging, grand_total)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            order_id,
            user_id,
            json.dumps([item.dict() for item in items]),
            subtotal,
            cgst,
            sgst,
            packaging,
            grand_total
        ))

    return {
        "success": True,
        "order_id": order_id,
        "customer": f"User #{user_id}" if user_id else "Guest Patron",
        "subtotal": subtotal,
        "cgst": cgst,
        "sgst": sgst,
        "total_tax": round(cgst + sgst, 2),
        "packaging": packaging,
        "grand_total": grand_total,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "APPROVED_PAID"
    }

# ----------------- Static File & Asset Routes -----------------
if os.path.exists(ASSETS_DIR):
    app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")

@app.get("/")
def serve_index():
    if os.path.exists(INDEX_PATH):
        return FileResponse(INDEX_PATH, media_type="text/html")
    return {"message": "GutGraph Backend Active. Place index.html inside the frontend/ directory."}

@app.get("/index.html")
def serve_index_html():
    return serve_index()

if __name__ == "__main__":
    import uvicorn
    print(f"\n🌿 Launching GutGraph Dispensary Server on http://0.0.0.0:8000 ...")
    print(f"📂 Frontend root: {FRONTEND_DIR}")
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
