# 🍹 GutGraph × Mixology (Botanical Dispensary)

Fork-IT 2026 — Team Byte and Bite. The project is a single full-stack app:

**`GutGraph_Dispensary_FullStack/`** — doodle SPA (`frontend/`) + production API (`backend/server.py`).

---

## Quick start

```bash
chmod +x start.sh
./start.sh
```

Open **[http://localhost:8000](http://localhost:8000)**.

API keys (optional LLM upgrades): copy `.env.example` → `.env` at the repo root when you add integrations later.

Automated tests:

```bash
cd GutGraph_Dispensary_FullStack && ./test.sh
```

---

## Layout

```
gutgraph-mixology/
├── GutGraph_Dispensary_FullStack/
│   ├── frontend/          # UI — edit here
│   ├── backend/server.py  # API — edit here
│   ├── start.sh
│   └── test.sh
├── start.sh               # launcher from repo root
├── .env                   # secrets (not committed)
└── README.md
```

Full feature list and API reference: `GutGraph_Dispensary_FullStack/README.md`.

---

## Note

Gut scores and pairing copy are **educational mockups**, not medical advice.