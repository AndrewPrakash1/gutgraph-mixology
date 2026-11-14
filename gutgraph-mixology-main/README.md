# 🍹 GutGraph × Mixology

Prototype for Foodoscope Fork It 2026, IIIT Delhi — Team Byte and Bite.

---

## What this is

A working demo of the concept: you log a meal, your "gut agents" score it, and you get a drink prescription based on real flavour chemistry.

**This is a mockup.** The gut scores are rule-based heuristics, not medical diagnostics. The FlavorDB pairing scores are hardcoded for the 5 demo meals. In production these would be real API calls.

---

## Quick Start

### 1. Start the backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs at `http://localhost:8000`

Test it: `curl http://localhost:8000/health`

### 2. Open the frontend

Just open `frontend/index.html` in a browser. No build step.

Or serve it:
```bash
cd frontend
python3 -m http.server 3000
```

Then visit `http://localhost:3000`

---

## API Endpoints

| Endpoint | Method | What |
|---|---|---|
| `/` | GET | Health check |
| `/meals` | GET | List all 5 demo meals |
| `/analyze` | POST | `{meal_text: "noodles and coke"}` → gut score + drink |
| `/analyze/{meal_id}` | GET | Direct lookup by meal ID |
| `/pair/{ingredient}` | GET | Pairing suggestions (demo data) |
| `/health` | GET | Status + meals loaded count |

---

## Project Structure

```
gutgraph-mixology/
├── backend/
│   ├── main.py           # FastAPI app
│   ├── gut_engine.py     # 5-rule gut scoring
│   ├── demo_data.py      # 5 meals + drinks + hardcoded pairs
│   └── requirements.txt
├── frontend/
│   └── index.html        # Single-file mobile UI
└── README.md
```

---

## The 5-Rule Gut Engine

1. **Fibre check** — fibre per 100g below 2g → "low fibre"
2. **Fermented food** — no fermented ingredient → "no fermented food"
3. **Sugar check** — sugar per 100g above 10g → "too much sugar"
4. **Probiotics** — no probiotic ingredient → "low probiotics"
5. **Spice diversity** — fewer than 3 spice families → "low spice diversity"

Each gap deducts from a base score of 10.0.

---

## Demo Meals

| Meal | Score | Gaps | Drink |
|---|---|---|---|
| Instant noodles + Coke | 2.1 | low fibre, no fermented, too much sugar | Haldi-Ginger Chaas |
| Rajma chawal + lassi | 7.2 | low spice diversity | Jeera-Mint Cooler |
| Burger + fries + Pepsi | 1.8 | low fibre, too much sugar, no fermented | Chaas with Roasted Cumin |
| Idli + sambar + coffee | 6.5 | low probiotics | Buttermilk with Asafoetida |
| Maggi + chai | 2.5 | low fibre, too much sugar | Haldi-Milk with Cardamom |

---

## What to do at the hackathon

### Replace mocks with real APIs (Lakshay)

When you get the real API keys from organizers:

1. In `main.py`, replace `find_meal()` with a call to RecipeDB:
   ```python
   # GET https://api.foodoscope.com/recipe2-api/recipe/recipesinfo?name={meal}
   ```

2. Replace the hardcoded pairing scores with FlavorDB:
   ```python
   # GET https://flavordb-api.foodoscope.com/food/by-alias?alias={ingredient}
   ```

3. Add the CocktailDB non-alcoholic filter:
   ```python
   # GET https://www.thecocktaildb.com/api/json/v1/1/filter.php?a=Non_Alcoholic
   ```

### Add the LLM ingredient extractor (Andrew)

Replace the keyword matcher in `find_meal()` with an OpenAI/Anthropic call:

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{
        "role": "user",
        "content": f"Extract ingredients from: '{meal_text}'. Return JSON list."
    }]
)
```

### Polish the UI (Shubhi)

- Add the pairing network graph (D3.js)
- Add loading skeletons
- Add the "next meal re-scored" feedback loop UI

---

## Team

- **Lakshay** — Backend (FastAPI, API integration)
- **Shubhi** — Frontend (React/HTML, UI/UX)
- **Andrew** — ML/Rules (gut scoring, pitch, demo data)

---

## License

Hackathon prototype. Not for production use.
