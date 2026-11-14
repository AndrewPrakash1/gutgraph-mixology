"""
Meal Lab API — mirrors the Dispensary SPA's client-side ``analyse()`` logic
so POST /api/analyze-meal returns the same agent cards the UI expects.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List

KW = {
    "dahi": "curd dahi chaas buttermilk lassi yogurt yoghurt kefir paneer shrikhand moru mishti".split(),
    "rough": (
        "dal lentil lentils rajma chana chole salad sabzi bhindi okra roti chapati oats bran "
        "fruit apple banana spinach palak veg vegetable vegetables beans millet ragi thali upma "
        "poha sprouts carrot cucumber guava peas flax chia bajra jowar broccoli"
    ).split(),
    "spike": (
        "cola coke pepsi soda cake jalebi gulab chocolate candy shake sweet donut doughnut "
        "cookie biscuit juice sugar syrup glucose dessert pastry halwa ladoo barfi pastry"
    ).split(),
    "rack": (
        "turmeric haldi pepper jeera cumin ginger adrak garlic lehsun cardamom elaichi cinnamon "
        "dalchini clove laung coriander dhania mustard rai fennel saunf fenugreek methi saffron "
        "kesar chilli chili mirch staranise nutmeg kokum"
    ).split(),
    "kavach": (
        "pomegranate kokum berries tea onion garlic turmeric apple oats flaxseed banana cocoa "
        "citrus grapes plum cabbage"
    ).split(),
    "refined": (
        "noodles maggi ramen fries burger pizza maida naan samosa pakora chips fried roll momo "
        "whitebread bun pasta bhature"
    ).split(),
}

PHRASES = {
    "spike": ["ice cream", "soft drink", "energy drink", "cold drink"],
    "refined": ["white bread", "instant noodles", "french fries"],
    "rack": ["curry leaves", "garam masala", "black pepper"],
    "dahi": ["cultured curd", "sweet lassi", "masala chaas"],
}

PICK = {
    "dahi": "desi-cool",
    "rough": "pink-paradise",
    "spike": "mint-condition",
    "rack": "golden-hour",
    "kavach": "sunkissed",
}


def _clamp(x: float, lo: float, hi: float) -> int:
    return int(max(lo, min(hi, round(x))))


def _tokenize(text: str) -> Dict[str, int]:
    tokens: Dict[str, int] = {}
    for w in re.split(r"[^a-z]+", text.lower()):
        if w:
            tokens[w] = 1
    return tokens


def _count(tokens: Dict[str, int], text: str, key: str) -> int:
    n = 0
    seen: Dict[str, int] = {}
    for w in KW.get(key, []):
        if tokens.get(w) and w not in seen:
            seen[w] = 1
            n += 1
    for p in PHRASES.get(key, []):
        if p in text:
            n += 1
    return n


def analyze_meal_text(meal_text: str) -> Dict[str, Any]:
    text = meal_text.strip()
    low = text.lower()
    tokens = _tokenize(low)

    da = _count(tokens, low, "dahi")
    ro = _count(tokens, low, "rough")
    sp = _count(tokens, low, "spike")
    ra = _count(tokens, low, "rack")
    ka = _count(tokens, low, "kavach")
    rf = _count(tokens, low, "refined")

    dahi_score = _clamp(65 + 14 * (da - 1), 65, 98) if da else 8
    dahi_rule = (
        f"Detected {da} live culture source(s). Lactobacillus active."
        if da
        else "No curd, chaas, or lassi found. Live culture gap detected."
    )

    rough_score = _clamp(16 + 22 * ro - 8 * rf, 6, 98)
    rough_rule = (
        f"Found {ro} high-fibre plant(s) and {rf} refined carb(s). Fibre fermenters "
        f"{'satisfied.' if rough_score >= 60 else 'need fuel.'}"
    )

    spike_score = _clamp(94 - 32 * sp - 9 * rf, 6, 98)
    if sp:
        spike_rule = f"Sugar alarm active! {sp} added sugar item(s) spikes glycemic load."
    elif rf:
        spike_rule = "Glycemic load elevated by refined items, but no direct sugar bomb."
    else:
        spike_rule = "Clean glycemic horizon. Zero added sugar bombs."

    rack_score = _clamp(14 + 20 * ra, 8, 98)
    rack_rule = (
        f"{ra} spice families active! Broad polyphenol parliament assembled."
        if ra >= 3
        else (
            f"{ra} spice family spotted. Diversify spices to broaden polyphenol spectrum."
            if ra > 0
            else "One-note plate. Zero bioactive spices found."
        )
    )

    kavach_score = _clamp(52 + 16 * ka + 8 * ro - 22 * sp - 14 * rf, 6, 98)
    if sp > 0 or rf > 0:
        kavach_rule = (
            "Sugar/refined stress present, but barrier-guarding polyphenols stepped in."
            if ka > 0
            else "Lining vulnerability: sugar-heavy & plant-empty plate weakens Akkermansia shield."
        )
    else:
        kavach_rule = "Epithelial mucosa shielded. Anti-inflammatory balance maintained."

    agents: List[Dict[str, Any]] = [
        {
            "id": "dahi",
            "name": "DAHI",
            "vibe": "Lactobacillus · live cultures",
            "score": dahi_score,
            "rule": dahi_rule,
        },
        {
            "id": "rough",
            "name": "ROUGH",
            "vibe": "Bifidobacterium · fibre fermenter",
            "score": rough_score,
            "rule": rough_rule,
        },
        {
            "id": "spike",
            "name": "SPIKE",
            "vibe": "Sugar alarm · glycemic load story",
            "score": spike_score,
            "rule": spike_rule,
        },
        {
            "id": "rack",
            "name": "RACK",
            "vibe": "Spice parliament · polyphenols",
            "score": rack_score,
            "rule": rack_rule,
        },
        {
            "id": "kavach",
            "name": "KAVACH",
            "vibe": "Lining guard · Akkermansia story",
            "score": kavach_score,
            "rule": kavach_rule,
        },
    ]

    weak = min(agents, key=lambda a: a["score"])
    match_id = "ruby-rush" if weak["score"] >= 70 else PICK.get(weak["id"], "ruby-rush")
    safety_warning = spike_score < 30 or (sp > 0 and rf > 0)

    return {
        "agents": agents,
        "match_id": match_id,
        "safety_warning": safety_warning,
        "meal_text": text,
    }