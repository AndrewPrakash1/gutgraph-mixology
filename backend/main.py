"""
GutGraph × Mixology — FastAPI Backend
"""

import json
import re
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Any, List, Dict

from gut_engine import compute_gut_score
from demo_data import MEALS, MEAL_BY_ID, find_meal, MEAL_NAMES
from agent import llm as agent_llm
from agent.personas import roster
from agent.pipeline import run_pipeline
from foodoscope_client import FoodoscopeError, _load_dotenv, get_foodoscope

_load_dotenv()  # repo-root .env → DEEPSEEK_*, FOODOSCOPE_*, etc.
from foodoscope_service import (
    connection_links,
    flavor_pairings,
    normalize_pairings,
    recipe_by_title,
)

ALLOWED_FOODOSCOPE = re.compile(r"^(recipe2-api|flavordb|cocktaildb)/")

SITE_DIR = Path(__file__).resolve().parents[1] / "GutGraph-Website"

app = FastAPI(title="GutGraph Mixology", version="0.1.0")

# CORS so frontend can call from file:// or localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    meal_text: str


class MealOut(BaseModel):
    id: str
    name: str
    emoji: str
    ingredients: List[Dict]


class AnalyzeResponse(BaseModel):
    meal: MealOut
    gut_score: float
    gaps: List[str]
    drink: Dict
    disclaimer: str = "This is a concept mockup. Gut scores are simulated, not medical advice."


class ChatRequest(BaseModel):
    message: str


class PairRequest(BaseModel):
    ingredient: str


class PairResponse(BaseModel):
    ingredient: str
    pairs: List[Dict]


@app.get("/")
def root():
    """Flagship GutGraph site (not the temporary frontend/ demo)."""
    return FileResponse(SITE_DIR / "index.html")


@app.get("/meals")
def list_meals():
    """Return all available demo meals."""
    return [
        {"id": m["id"], "name": m["name"], "emoji": m["emoji"]}
        for m in MEALS
    ]


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_meal(req: AnalyzeRequest):
    """
    Analyze a meal text and return gut score + recommended drink.
    In production this would call RecipeDB to resolve ingredients,
    then FlavorDB for real pairing scores.
    """
    meal = find_meal(req.meal_text)
    score, gaps, metrics = compute_gut_score(meal["ingredients"])

    return AnalyzeResponse(
        meal=MealOut(
            id=meal["id"],
            name=meal["name"],
            emoji=meal["emoji"],
            ingredients=meal["ingredients"],
        ),
        gut_score=score,
        gaps=gaps,
        drink=meal["drink"],
    )


@app.get("/analyze/{meal_id}")
def analyze_meal_by_id(meal_id: str):
    """Direct lookup by meal ID (for the dropdown)."""
    meal = MEAL_BY_ID.get(meal_id)
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    score, gaps, metrics = compute_gut_score(meal["ingredients"])
    return {
        "meal": {
            "id": meal["id"],
            "name": meal["name"],
            "emoji": meal["emoji"],
            "ingredients": meal["ingredients"],
        },
        "gut_score": score,
        "gaps": gaps,
        "drink": meal["drink"],
        "disclaimer": "This is a concept mockup. Gut scores are simulated, not medical advice.",
    }


@app.get("/foodoscope/status")
def foodoscope_status():
    fs = get_foodoscope()
    return {
        "configured": fs is not None,
        "base_url": fs.base_url if fs else None,
        "cache": str(fs.cache) if fs and fs.cache else None,
    }


@app.get("/recipe/search")
def search_recipe(title: str, limit: int = 5):
    """RecipeDB by title (cached). Falls back to message when no campus key."""
    hits = recipe_by_title(title, limit=limit)
    if hits is None:
        raise HTTPException(
            status_code=503,
            detail="FoodoScope unavailable. Set FOODOSCOPE_API_KEY in repo-root .env on campus network.",
        )
    return {"title": title, "results": hits}


@app.api_route("/api/{full_path:path}", methods=["GET", "POST"])
async def foodoscope_proxy(request: Request, full_path: str):
    """
    Browser-safe proxy to the FoodoScope gateway (STARTER_GUIDE §3).
    Frontend calls http://localhost:8000/api/recipe2-api/... — key stays server-side.
    """
    if not ALLOWED_FOODOSCOPE.match(full_path):
        raise HTTPException(
            status_code=404,
            detail="Use /api/recipe2-api/..., /api/flavordb/..., or /api/cocktaildb/...",
        )
    fs = get_foodoscope()
    if not fs:
        raise HTTPException(status_code=503, detail="FOODOSCOPE_API_KEY not configured")
    path = "/" + full_path
    params = dict(request.query_params)
    try:
        if request.method == "POST":
            raw = await request.body()
            body: Any = json.loads(raw.decode()) if raw else None
            data = fs.post(path, body=body, **params)
        else:
            data = fs.get(path, **params)
    except FoodoscopeError as e:
        return JSONResponse(status_code=e.status, content={"error": e.message})
    return data


@app.get("/pair/{ingredient}")
def pair_ingredient(ingredient: str):
    """
    Return pairing suggestions for an ingredient.
    Live: FlavorDB ``/flavordb/food/by-alias`` when key is set; else demo table.
    """
    # Hardcoded demo pairs for offline / pre-campus
    PAIRS = {
        "turmeric": [
            {"name": "ginger", "similarity": 0.385, "shared_molecules": 89},
            {"name": "black pepper", "similarity": 0.210, "shared_molecules": 45},
            {"name": "cardamom", "similarity": 0.298, "shared_molecules": 67},
        ],
        "ginger": [
            {"name": "turmeric", "similarity": 0.385, "shared_molecules": 89},
            {"name": "lemon", "similarity": 0.156, "shared_molecules": 34},
            {"name": "mint", "similarity": 0.089, "shared_molecules": 18},
        ],
        "cumin": [
            {"name": "coriander", "similarity": 0.245, "shared_molecules": 52},
            {"name": "mint", "similarity": 0.052, "shared_molecules": 12},
            {"name": "asafoetida", "similarity": 0.134, "shared_molecules": 23},
        ],
        "mint": [
            {"name": "cumin", "similarity": 0.052, "shared_molecules": 12},
            {"name": "lemon", "similarity": 0.178, "shared_molecules": 38},
            {"name": "ginger", "similarity": 0.089, "shared_molecules": 18},
        ],
        "cardamom": [
            {"name": "turmeric", "similarity": 0.298, "shared_molecules": 67},
            {"name": "saffron", "similarity": 0.112, "shared_molecules": 25},
            {"name": "cinnamon", "similarity": 0.087, "shared_molecules": 19},
        ],
    }
    key = ingredient.lower().strip()
    live = normalize_pairings(flavor_pairings(key))
    if live:
        return {"ingredient": ingredient, "pairs": live, "source": "flavordb"}
    links = connection_links(key)
    from_links = normalize_pairings(links)
    if from_links:
        return {"ingredient": ingredient, "pairs": from_links, "source": "recipe2_connections"}
    return {
        "ingredient": ingredient,
        "pairs": PAIRS.get(key, []),
        "source": "demo",
    }


@app.get("/agents")
def list_agents():
    """Roster for the chat sidebar. `mode` tells the UI whether agent
    reasons are LLM-worded (deepseek/openrouter) or template-worded (mock)."""
    info = agent_llm.provider_info()
    return {
        "mode": info["mode"],
        "provider": info["provider"],
        "model": info["model"],
        "agents": roster(),
    }


@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    """
    Grokbot-style agent transcript over SSE (POST, so EventSource won't work —
    read it with fetch + ReadableStream on the frontend).

    Event sequence: agent_start/token* (Mixologist) -> meal -> tool
    -> per-agent (agent_start, token*, vote) -> tally -> tool -> result -> done.
    """
    async def event_source():
        async for ev in run_pipeline(req.message):
            yield f"data: {json.dumps(ev, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        event_source(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/health")
def health():
    return {"status": "ok", "meals_loaded": len(MEALS)}


app.mount(
    "/",
    StaticFiles(directory=str(SITE_DIR), html=True),
    name="gutgraph-site",
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
