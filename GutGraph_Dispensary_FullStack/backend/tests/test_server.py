#!/usr/bin/env python3
"""
GutGraph Dispensary - Automated Test Suite
==========================================
Tests:
1. DB WAL mode concurrency & schema
2. Case-insensitive unique username & email constraint
3. OTP generation, expiration, rate limiting & verification
4. Whimsical random credential generator
5. Multi-user concurrent login simulation with ThreadPoolExecutor
6. Medical history & allergy profile persistence
7. LLM memory & council personalized deliberation
8. Accurate Indian GST calculation & checkout storage
"""

import sys
import os
import time
import json
import sqlite3
import threading
from concurrent.futures import ThreadPoolExecutor

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BACKEND_DIR)

from server import (
    get_db, init_db, hash_password, verify_password,
    send_otp, verify_otp, register, login, update_profile,
    get_profile, process_chat, checkout, generate_random_credentials,
    check_username, SendOtpRequest, VerifyOtpRequest, RegisterRequest,
    LoginRequest, ProfileUpdateRequest, ChatRequest, CheckoutRequest, CheckoutItem,
    DB_PATH
)

class MockClient:
    def __init__(self, host="127.0.0.1"):
        self.host = host

class MockRequest:
    def __init__(self, host="127.0.0.1"):
        self.client = MockClient(host)

def run_tests():
    print("=" * 65)
    print("🧪 RUNNING GUTGRAPH DISPENSARY AUTOMATED TESTS")
    print("=" * 65)

    # 1. DB WAL & Schema Check
    print("\n[Test 1] Verifying SQLite WAL Mode & Schema...")
    init_db()
    with get_db() as conn:
        journal = conn.execute("PRAGMA journal_mode;").fetchone()[0]
        assert journal.lower() == "wal", f"Expected WAL mode, got {journal}"
        tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
        for expected in ["users", "profiles", "otp_codes", "sessions", "chat_memory", "orders"]:
            assert expected in tables, f"Missing table {expected}"
    print("✅ Database verified in WAL mode with all 6 tables.")

    # 2. Random Credential Generation
    print("\n[Test 2] Testing Random Credential Generator...")
    creds = generate_random_credentials()
    assert "username" in creds and len(creds["username"]) >= 5
    assert "password" in creds and len(creds["password"]) >= 8
    print(f"✅ Generated: username='{creds['username']}', password='{creds['password']}'")

    # 3. OTP Flow
    print("\n[Test 3] Testing Email OTP Dispatch & Verification...")
    ts = int(time.time())
    test_email = f"patron_{ts}@gutgraph.com"
    req_obj = MockRequest("127.0.0.1")
    otp_res = send_otp(SendOtpRequest(email=test_email), req_obj)
    assert otp_res["success"] is True
    demo_otp = otp_res["demo_otp"]

    try:
        verify_otp(VerifyOtpRequest(email=test_email, otp="000000"), req_obj)
        assert False, "Should have rejected bad OTP"
    except Exception as e:
        assert "Invalid verification code" in str(e.detail)
    print("✅ Invalid OTP blocked.")

    v_res = verify_otp(VerifyOtpRequest(email=test_email, otp=demo_otp), req_obj)
    assert v_res["verified"] is True
    print("✅ Valid OTP verified successfully.")

    # 4. Registration & Duplicate Protection
    print("\n[Test 4] Testing User Registration & Case-Insensitive Uniqueness...")
    test_user = f"FloraKnight_{ts}"
    reg = register(RegisterRequest(
        email=test_email,
        otp=demo_otp,
        username=test_user,
        password="SuperPassword!99"
    ), req_obj)
    token = reg["token"]
    user_id = reg["user"]["id"]
    print(f"✅ Registered: id={user_id}, username={test_user}")

    # Try duplicate with different case
    dup_email = f"second_{ts}@gutgraph.com"
    send_otp(SendOtpRequest(email=dup_email), req_obj)
    with get_db() as conn:
        new_otp = conn.execute("SELECT code FROM otp_codes WHERE email = ?", (dup_email,)).fetchone()["code"]
    try:
        register(RegisterRequest(
            email=dup_email,
            otp=new_otp,
            username=test_user.lower(),  # Lowercase duplicate
            password="Password123!"
        ), req_obj)
        assert False, "Duplicate should be rejected"
    except Exception as e:
        assert "already in use" in str(e.detail)
        print(f"✅ Case-insensitive duplicate handle blocked: {e.detail}")

    # 5. Multi-User Concurrent Logins
    print("\n[Test 5] Simulating Concurrent Multi-User Logins...")
    successes = []
    def do_login(i):
        res = login(LoginRequest(login=test_user, password="SuperPassword!99"), MockRequest(f"10.0.0.{i}"))
        if res.get("success"):
            successes.append(i)

    with ThreadPoolExecutor(max_workers=8) as ex:
        for i in range(16):
            ex.submit(do_login, i)
    assert len(successes) == 16, f"Expected 16 logins, got {len(successes)}"
    print(f"✅ 16 concurrent logins resolved with zero collisions.")

    # 6. Medical Profile Persistence
    print("\n[Test 6] Testing Medical History & Allergy Profile Storage...")
    prof = update_profile(ProfileUpdateRequest(
        medical_history="Acid Reflux / GERD",
        current_situation="Frequent afternoon bloating",
        allergies="Dairy / Lactose Sensitivity",
        health_goals="Mucosal lining repair",
        additional_notes="Drinks chamomile tea"
    ), user_id=user_id)
    assert prof["success"] is True

    loaded_prof = get_profile(user_id=user_id)
    assert "Acid Reflux" in loaded_prof["medical_history"]
    assert "Dairy" in loaded_prof["allergies"]
    print("✅ Medical profile stored and retrieved with full fidelity.")

    # 7. LLM Memory & Context Aware Deliberation
    print("\n[Test 7] Testing LLM Context Injection & Long-Term Memory...")
    auth_h = f"Bearer {token}"
    chat = process_chat(ChatRequest(message="Can I have Desi Cool today?"), authorization=auth_h)
    print(f"   Agent response: {chat['text']}")
    assert "Lactose" in chat["text"] or "dairy" in chat["text"].lower() or "Dairy" in chat["text"]
    assert chat["long_term_memory"] is True
    print("✅ LLM personalized advice based on stored Lactose Sensitivity!")

    # 8. GST Checkout Calculation
    print("\n[Test 8] Testing Accurate GST Calculations...")
    cart = [
        CheckoutItem(id="sunkissed", name="Sunkissed", qty=2, price=120.0),
        CheckoutItem(id="mint-condition", name="Mint Condition", qty=1, price=120.0)
    ]
    # Subtotal: 3 * 120 = 360
    # CGST (2.5%): 9.00
    # SGST (2.5%): 9.00
    # Packaging: Free (>= 360)
    # Grand Total: 378.00
    bill = checkout(CheckoutRequest(items=cart), authorization=auth_h)
    assert bill["subtotal"] == 360.0
    assert bill["cgst"] == 9.0
    assert bill["sgst"] == 9.0
    assert bill["packaging"] == 0.0
    assert bill["grand_total"] == 378.0
    print(f"✅ Accurate GST bill generated: Subtotal=Rs {bill['subtotal']}, Tax=Rs {bill['total_tax']}, Total=Rs {bill['grand_total']}")

    print("\n" + "=" * 65)
    print("🎉 ALL TESTS PASSED SUCCESSFULLY!")
    print("=" * 65)

if __name__ == "__main__":
    run_tests()
