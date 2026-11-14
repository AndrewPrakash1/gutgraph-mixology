# 🌿 GUTGRAPH BOTANICAL DISPENSARY — FULL-STACK SYSTEM

A complete full-stack web application featuring doodle rough-paper aesthetics, Web Audio mechanical sound synthesis, animated tax bill receipt printing, email OTP verification, cryptographic user authentication, personalized medical profile store, and LLM long-term memory for the 5 AI Gut Council Agents.

---

## 📁 Project Structure

```
GutGraph_Dispensary_FullStack/
├── frontend/
│   ├── index.html              # Upgraded responsive SPA (Doodle UI, Bill modal, Auth flow)
│   └── assets/                 # Can photography, photorealistic textures & models
├── backend/
│   ├── server.py               # Production FastAPI backend (REST API & static file serving)
│   ├── gutgraph.db             # Concurrency-hardened SQLite database (WAL Mode)
│   └── tests/
│       └── test_server.py      # Automated security, concurrency & GST calculation test suite
├── start.sh                    # 1-Click launcher script
├── test.sh                     # Automated test runner script
├── requirements.txt            # Python dependencies (FastAPI, Uvicorn, Pydantic)
└── README.md                   # System documentation & API reference
```

---

## 🚀 Quick Start

### 1. Launch the Server
In your terminal, run:
```bash
cd ~/Desktop/GutGraph_Dispensary_FullStack
chmod +x start.sh test.sh
./start.sh
```

### 2. Open in Browser
Visit **[http://localhost:8000](http://localhost:8000)** in any modern web browser.
*(You can also directly double-click `frontend/index.html` — it connects automatically to `http://localhost:8000` via CORS)*.

### 3. Run Automated Tests
To run the automated security and concurrency test suite:
```bash
./test.sh
```

---

## ✨ Key Features & Capabilities

### 1. 🧾 Accurate Bill Generation & Unroll Animation on Checkout
- **Realistic Paper Dispenser**: Clicking **Checkout** in your stash triggers mechanical dot-matrix and thermal paper audio clicks (`sfxBillPrint()`), smoothly extruding a receipt tape from the printer mouth (`billFeedPrint` stepped keyframes).
- **Accurate Indian GST Calculations**:
  - Itemized rows: Flavor Name, 330ml Can spec, Quantity, Unit Rate (`Rs 120.00`), Line Total.
  - **Subtotal**: Exact item sum.
  - **CGST (2.5%)** & **SGST (2.5%)**: 5.0% Indian tax calculation on packaged botanical beverages.
  - **Cold-Chain Eco-Packaging**: Rs 25.00, automatically marked **FREE (WAIVED)** on orders of Rs 360 or more.
  - **Grand Total**: Mathematically verified and rounded to the nearest paisa.
- **Rubber Stamp Seal**: An animated red doodle seal bounces down with sound: `[ APPROVED • PAID • SEALED ]`.
- **Print & Archive**: Features a simulated barcode, invoice serial (`INV #GG-2026-XXXX`), timestamp, patron ID, and a clean **Print Slip** button with dedicated `@media print` rules.

### 2. ⚡ Register & Login System (Top-Right Navbar)
- **Navigation Button**: Small capsule pill `⚡ Sign In / Join` in the top right. Displays `👤 @username` with an active green dot when logged in.
- **Single-Screen Progression**: The modal opens strictly one step at a time, preventing premature exposure to username or password fields:
  1. **Sign In**: Login for existing accounts (by username or email).
  2. **Email Verification**: User inputs email to receive a 6-digit verification code.
  3. **OTP Screen**: 6-digit input with a 30-second countdown resend timer and "Change Email" option.
  4. **Credentials Setup**:
     - **🎲 Whimsical Random Generator**: 1-click button to auto-generate unique gut-themed handles (e.g., `PolyphenolHero341`, `KombuchaNinja42`) and strong passwords (e.g., `Shield$8164c99`) with a copy button.
     - **Live Username Availability**: Debounced endpoint (`/api/auth/check-username`) guaranteeing no two users have the same username (`UNIQUE COLLATE NOCASE`).
  5. **Medical Profile Onboarding**: Interactive doodle chips for medical history, symptoms, and allergies.
  6. **Profile Dashboard**: Inspect saved medical history, verify active LLM memory, edit details, or sign out.

### 3. 🧠 LLM Long-Term Memory & Health Context Injection
- **Guest vs Registered Mode**:
  - **Guests**: See `🟡 GUEST MODE` in the Agents Chat drawer; context is temporary and resets on reload.
  - **Registered Users**: See `🟢 LONG-TERM MEMORY ACTIVE`.
- **Specialized Context-Aware Advice**:
  - The 5 AI Council Agents (**Dahi**, **Rough**, **Spike**, **Rack**, and **Kavach**) review the user's recorded medical profile before every response.
  - *Example*: If **Lactose Sensitivity** is in the user's profile, the agent explicitly warns against dairy ferments (Desi Cool) and advises plant ferments (Sunkissed or Ruby Rush).
  - *Example*: If **Acid Reflux / GERD** is recorded, spice recommendations are moderated toward cooling botanical refreshers (Mint Condition).
- **Persistent History**: All conversation turns are stored in SQLite `chat_memory` and reloaded on return.

### 4. 🛡️ Cyber Security & Concurrency Hardening
- **Multi-User Concurrency**: SQLite runs in **Write-Ahead Logging (WAL)** mode (`PRAGMA journal_mode=WAL;`) with a 10-second busy timeout (`PRAGMA busy_timeout=10000;`). Multiple users can register, log in, or chat simultaneously without collisions or database locks.
- **Password Protection**: Salted PBKDF2-HMAC-SHA256 with 100,000 iterations and 16-byte random salts.
- **SQL Injection Immune**: 100% parameterized queries (`?` binding).
- **Brute Force Protection**: IP rate-limiting on login and OTP verification.
- **Session Tokens**: 256-bit cryptographically random tokens (`secrets.token_hex(32)`).

---

## 📡 REST API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/` | `GET` | Serves the production Single Page Application (`index.html`) |
| `/assets/{file}` | `GET` | Serves product photography, models and textures |
| `/api/auth/random-credentials`| `GET` | Generates a unique doodle username and secure password |
| `/api/auth/check-username` | `GET` | Real-time uniqueness check for usernames |
| `/api/auth/send-otp` | `POST` | Dispatches 6-digit verification code to email |
| `/api/auth/verify-otp` | `POST` | Validates submitted OTP code |
| `/api/auth/register` | `POST` | Registers new user, creates session, hashes password |
| `/api/auth/login` | `POST` | Authenticates user credentials, loads health profile |
| `/api/auth/logout` | `POST` | Revokes current session token |
| `/api/auth/me` | `GET` | Returns authenticated user identity and profile status |
| `/api/profile` | `GET` / `POST` | Reads or updates medical history, situation & allergies |
| `/api/chat` | `POST` | LLM deliberation engine incorporating health profile |
| `/api/chat/history` | `GET` | Retrieves persistent chat turns for logged-in user |
| `/api/checkout` | `POST` | Calculates Indian GST, packaging fees, archives order |

---

## 🎨 Design System
- **Colors**: Cream (`#FFF1D9`), Deep Plum (`#170052`), Yolk Yellow (`#FFE04A`), Hot Pink (`#FF4F9A`), Magenta Accent (`#D4136A`).
- **Typography**: Anton (Display headers), Space Mono (Receipts/data/codes), Caveat Brush (Doodle handwriting), Bricolage Grotesque (Body UI).
- **Borders & Shadows**: `3px solid #170052`, sketchy blob radius (`var(--blob)`), hard drop shadows (`4px 4px 0 #170052`).
