"""RecipeDB / FlavorDB helpers with demo fallbacks."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from foodoscope_client import FoodoscopeError, get_foodoscope


def recipe_by_title(title: str, limit: int = 5) -> Optional[List[Dict[str, Any]]]:
    fs = get_foodoscope()
    if not fs:
        return None
    try:
        data = fs.get(
            "/recipe2-api/recipe-bytitle/recipeByTitle",
            title=title,
            page=1,
            limit=limit,
        )
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            return data.get("recipes") or data.get("data") or data.get("results") or [data]
        return None
    except FoodoscopeError:
        return None


def flavor_pairings(ingredient: str) -> Optional[Any]:
    fs = get_foodoscope()
    if not fs:
        return None
    alias = ingredient.strip().lower()
    return fs.get("/flavordb/food/by-alias", food_pair=alias)


def connection_links(ingredient: str, limit: int = 5) -> Optional[Any]:
    fs = get_foodoscope()
    if not fs:
        return None
    return fs.get(
        "/recipe2-api/connections/links",
        ingredient=ingredient,
        page=1,
        limit=limit,
    )


def normalize_pairings(raw: Any, top_n: int = 5) -> List[Dict[str, Any]]:
    """Best-effort parse of FlavorDB pairing payloads into UI shape."""
    if not raw:
        return []
    items: List[Any]
    if isinstance(raw, list):
        items = raw
    elif isinstance(raw, dict):
        items = raw.get("pairs") or raw.get("pairings") or raw.get("data") or raw.get("results") or []
        if not items and raw:
            items = [raw]
    else:
        return []

    out: List[Dict[str, Any]] = []
    for row in items[:top_n]:
        if isinstance(row, str):
            out.append({"name": row, "similarity": None, "shared_molecules": None})
            continue
        if not isinstance(row, dict):
            continue
        name = (
            row.get("food_pair")
            or row.get("entity_alias_readable")
            or row.get("name")
            or row.get("ingredient")
        )
        if not name:
            continue
        out.append({
            "name": str(name),
            "similarity": row.get("similarity") or row.get("score"),
            "shared_molecules": row.get("shared_molecules") or row.get("shared"),
        })
    return out