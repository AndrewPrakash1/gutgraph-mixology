"""
FoodoScope (RecipeDB / FlavorDB) client for the campus gateway.

Reads FOODOSCOPE_API_KEY + FOODOSCOPE_BASE_URL from the environment (loaded from
repo-root .env by env_loader at app start). The gateway at
http://cosylab.iiitd.edu.in:6969 is only reachable on the IIIT-D event Wi-Fi, so
every call here fails fast (short timeout) and returns None instead of hanging;
callers fall back to the local keyword/demo data.

Endpoints (per docs/STARTER_GUIDE.md):
    GET /recipe2-api/recipe-bytitle/recipeByTitle?title=...&page=1&limit=N
    GET /flavordb/food/by-alias?food_pair=<ingredient>
    GET /recipe2-api/connections/links?ingredient=...&page=1&limit=N
Auth: `Authorization: Bearer <key>` (Bearer, not Token/Basic).
"""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import time
from typing import Any, Dict, List, Optional

import httpx

DEFAULT_BASE_URL = "http://cosylab.iiitd.edu.in:6969"
_CACHE_DIR = pathlib.Path(__file__).resolve().parent / ".foodoscope_cache"
_TIMEOUT = httpx.Timeout(6.0, connect=4.0)


def _key() -> str:
    return os.environ.get("FOODOSCOPE_API_KEY", "").strip()


def _base() -> str:
    return (os.environ.get("FOODOSCOPE_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")


def enabled() -> bool:
    return bool(_key())


def _cache_path(path: str, params: Dict[str, Any]) -> pathlib.Path:
    digest = hashlib.sha1(json.dumps([path, params], sort_keys=True).encode()).hexdigest()
    return _CACHE_DIR / f"{digest}.json"


def _get(path: str, params: Optional[Dict[str, Any]] = None) -> Optional[Any]:
    """One GET against the gateway; None on any failure (off-campus, auth, 4xx/5xx)."""
    if not enabled():
        return None
    params = params or {}
    cache = _cache_path(path, params)
    if cache.is_file():
        try:
            return json.loads(cache.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            pass
    try:
        res = httpx.get(
            f"{_base()}{path}",
            params=params,
            headers={"Authorization": f"Bearer {_key()}"},
            timeout=_TIMEOUT,
        )
    except httpx.HTTPError:
        return None
    if res.status_code != 200:
        return None
    try:
        data = res.json()
    except ValueError:
        return None
    _CACHE_DIR.mkdir(exist_ok=True)
    try:
        cache.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass
    return data


def reachable() -> bool:
    """One cheap probe; False off-campus or with a bad key."""
    if not enabled():
        return False
    data = _get("/recipe2-api/recipe/recipeofday")
    return isinstance(data, dict) or isinstance(data, list)


def recipe_search(title: str, limit: int = 5) -> Optional[List[Dict[str, Any]]]:
    """RecipeDB by-title search -> [{name, id, ...}] or None."""
    data = _get(
        "/recipe2-api/recipe-bytitle/recipeByTitle",
        {"title": title, "page": 1, "limit": limit},
    )
    if not isinstance(data, (dict, list)):
        return None
    items = data if isinstance(data, list) else (
        data.get("recipes") or data.get("data") or data.get("results") or []
    )
    if not isinstance(items, list):
        return None
    out = []
    for r in items[:limit]:
        if isinstance(r, dict):
            out.append({
                "id": r.get("id") or r.get("recipe_id") or r.get("_id"),
                "name": r.get("name") or r.get("title") or r.get("recipe_name"),
            })
    return [o for o in out if o.get("name")] or None


def _walk_lists(obj: Any) -> List[Dict[str, Any]]:
    """Best-effort: return every list-of-dicts found anywhere in the payload."""
    found: List[Dict[str, Any]] = []
    if isinstance(obj, list):
        for item in obj:
            found += _walk_lists(item)
    elif isinstance(obj, dict):
        for val in obj.values():
            found += _walk_lists(val)
    return found


def pairings(ingredient: str) -> Optional[List[Dict[str, Any]]]:
    """FlavorDB food-pair for an ingredient -> [{name, similarity, shared_molecules}] or None.

    The gateway response shape varies, so this normalises defensively: it walks
    the payload for list-of-dicts and keeps entries that look like a pairing row.
    Anything unrecognised returns None so callers use the demo table.
    """
    data = _get("/flavordb/food/by-alias", {"food_pair": ingredient})
    if data is None:
        return None
    out: List[Dict[str, Any]] = []
    for row in _walk_lists(data):
        name = (
            row.get("food") or row.get("name") or row.get("pair") or row.get("paired_with")
            or row.get("ingredient") or row.get("alias")
        )
        if not name:
            continue
        sim = None
        for k in ("similarity", "jaccard", "score", "similarity_score"):
            if k in row and isinstance(row[k], (int, float)):
                sim = float(row[k])
                break
        shared = row.get("shared_molecules") or row.get("shared") or row.get("common_molecules")
        if isinstance(shared, list):
            shared = len(shared)
        out.append({
            "name": name,
            "similarity": round(sim, 4) if sim is not None else None,
            "shared_molecules": shared if isinstance(shared, (int, float)) else None,
        })
        if len(out) >= 8:
            break
    return out or None
