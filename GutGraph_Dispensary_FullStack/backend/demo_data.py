"""
Hardcoded demo dataset. In production this would come from RecipeDB + FlavorDB APIs.
"""

from typing import List, Dict

MEALS: List[Dict] = [
    {
        "id": "noodles_coke",
        "name": "Instant noodles + Coke",
        "emoji": "🍜🥤",
        "ingredients": [
            {"name": "wheat noodles", "weight_g": 70, "fibre_g": 1.0, "sugar_g": 0.5},
            {"name": "palm oil", "weight_g": 15, "fibre_g": 0.0, "sugar_g": 0.0},
            {"name": "salt", "weight_g": 2, "fibre_g": 0.0, "sugar_g": 0.0},
            {"name": "MSG", "weight_g": 1, "fibre_g": 0.0, "sugar_g": 0.0},
            {"name": "sugar", "weight_g": 40, "fibre_g": 0.0, "sugar_g": 40.0},  # Coke
            {"name": "caffeine", "weight_g": 0.1, "fibre_g": 0.0, "sugar_g": 0.0},
            {"name": "caramel", "weight_g": 0.5, "fibre_g": 0.0, "sugar_g": 0.3},
        ],
        "expected_score": 2.1,
        "expected_gaps": ["low fibre", "no fermented food", "too much sugar"],
        "drink": {
            "name": "Haldi-Ginger Chaas",
            "emoji": "🥛",
            "ingredients": ["buttermilk", "turmeric", "ginger", "cumin", "black salt"],
            "prep": "Whisk 250ml buttermilk with ¼ tsp turmeric, ½ tsp grated ginger, pinch of roasted cumin, and black salt.",
            "explanation": "Turmeric (130 flavour molecules) and ginger (106 molecules) share 89 compounds — a similarity score of 0.385. This pairing is classic in Ayurvedic drinks because the shared zingiberene family creates a warm, rounded flavour. Buttermilk provides probiotics you missed, while ginger cuts turmeric's earthiness.",
            "shared_molecules": 89,
            "similarity_score": 0.385,
        },
    },
    {
        "id": "rajma_chawal",
        "name": "Rajma chawal + lassi",
        "emoji": "🍛🥛",
        "ingredients": [
            {"name": "kidney beans", "weight_g": 150, "fibre_g": 18.0, "sugar_g": 2.0},
            {"name": "rice", "weight_g": 150, "fibre_g": 1.5, "sugar_g": 0.5},
            {"name": "yogurt", "weight_g": 200, "fibre_g": 0.0, "sugar_g": 8.0},
            {"name": "cumin", "weight_g": 2, "fibre_g": 0.5, "sugar_g": 0.0},
            {"name": "ghee", "weight_g": 15, "fibre_g": 0.0, "sugar_g": 0.0},
            {"name": "onion", "weight_g": 50, "fibre_g": 1.5, "sugar_g": 3.0},
            {"name": "tomato", "weight_g": 80, "fibre_g": 1.2, "sugar_g": 4.0},
            {"name": "garlic", "weight_g": 10, "fibre_g": 0.5, "sugar_g": 0.1},
            {"name": "ginger", "weight_g": 10, "fibre_g": 0.2, "sugar_g": 0.2},
        ],
        "expected_score": 7.2,
        "expected_gaps": ["low spice diversity"],
        "drink": {
            "name": "Jeera-Mint Cooler",
            "emoji": "🌿",
            "ingredients": ["water", "cumin", "mint", "lemon", "black salt", "sugar"],
            "prep": "Boil 1 tsp cumin in 300ml water, cool, add crushed mint, lemon juice, pinch of black salt and ½ tsp sugar.",
            "explanation": "Cumin (apiaceae family) and mint (lamiaceae) share only 12 flavour molecules — this is the 'Indian contrast mode'. Indian cooking deliberately pairs low-similarity ingredients to create layered complexity. The cooling mint balances cumin's warmth, while lemon's citral bridges both families.",
            "shared_molecules": 12,
            "similarity_score": 0.052,
        },
    },
    {
        "id": "burger_fries",
        "name": "Burger + fries + Pepsi",
        "emoji": "🍔🍟🥤",
        "ingredients": [
            {"name": "bun", "weight_g": 80, "fibre_g": 2.0, "sugar_g": 4.0},
            {"name": "patty", "weight_g": 120, "fibre_g": 0.0, "sugar_g": 0.0},
            {"name": "potato", "weight_g": 150, "fibre_g": 3.0, "sugar_g": 1.5},
            {"name": "vegetable oil", "weight_g": 30, "fibre_g": 0.0, "sugar_g": 0.0},
            {"name": "salt", "weight_g": 3, "fibre_g": 0.0, "sugar_g": 0.0},
            {"name": "sugar", "weight_g": 42, "fibre_g": 0.0, "sugar_g": 42.0},  # Pepsi
            {"name": "caffeine", "weight_g": 0.1, "fibre_g": 0.0, "sugar_g": 0.0},
            {"name": "cheese", "weight_g": 20, "fibre_g": 0.0, "sugar_g": 1.0},
        ],
        "expected_score": 1.8,
        "expected_gaps": ["low fibre", "too much sugar", "no fermented food"],
        "drink": {
            "name": "Chaas with Roasted Cumin",
            "emoji": "🥛",
            "ingredients": ["buttermilk", "cumin", "mint", "black salt"],
            "prep": "Whisk 250ml buttermilk with ½ tsp roasted cumin powder, 4-5 mint leaves, and black salt.",
            "explanation": "This is your probiotic rescue. After a high-sugar, zero-fibre meal, your gut bacteria need lactobacilli from buttermilk. Roasted cumin adds the apiaceae spice family you completely missed. The drink's savoury profile directly counters the meal's sweetness bias.",
            "shared_molecules": 45,
            "similarity_score": 0.210,
        },
    },
    {
        "id": "idli_sambar",
        "name": "Idli + sambar + coffee",
        "emoji": "🍽️☕",
        "ingredients": [
            {"name": "idli (fermented rice batter)", "weight_g": 100, "fibre_g": 1.0, "sugar_g": 0.3},
            {"name": "lentils", "weight_g": 80, "fibre_g": 8.0, "sugar_g": 1.5},
            {"name": "tamarind", "weight_g": 20, "fibre_g": 0.5, "sugar_g": 8.0},
            {"name": "mustard", "weight_g": 3, "fibre_g": 0.5, "sugar_g": 0.0},
            {"name": "curry leaves", "weight_g": 5, "fibre_g": 1.0, "sugar_g": 0.2},
            {"name": "coffee", "weight_g": 250, "fibre_g": 0.0, "sugar_g": 0.0},
            {"name": "sambar powder", "weight_g": 10, "fibre_g": 2.0, "sugar_g": 0.5},
        ],
        "expected_score": 6.5,
        "expected_gaps": ["low probiotics"],
        "drink": {
            "name": "Buttermilk with Asafoetida",
            "emoji": "🥛",
            "ingredients": ["buttermilk", "asafoetida", "cumin", "black salt"],
            "prep": "Whisk 250ml buttermilk with a pinch of asafoetida, ¼ tsp roasted cumin, and black salt.",
            "explanation": "Idli is fermented rice, but your coffee has zero probiotics. Buttermilk delivers lactobacilli directly. Asafoetida (hing) is a prebiotic — it feeds beneficial gut bacteria. Its sulphur compounds pair with cumin's terpenes (apiaceae family overlap: 23 molecules, score 0.134) for a deeply savoury, digestively restorative drink.",
            "shared_molecules": 23,
            "similarity_score": 0.134,
        },
    },
    {
        "id": "maggi_chai",
        "name": "Maggi + chai",
        "emoji": "🍜☕",
        "ingredients": [
            {"name": "wheat noodles", "weight_g": 70, "fibre_g": 1.0, "sugar_g": 0.5},
            {"name": "palm oil", "weight_g": 15, "fibre_g": 0.0, "sugar_g": 0.0},
            {"name": "salt", "weight_g": 2, "fibre_g": 0.0, "sugar_g": 0.0},
            {"name": "MSG", "weight_g": 1, "fibre_g": 0.0, "sugar_g": 0.0},
            {"name": "milk", "weight_g": 100, "fibre_g": 0.0, "sugar_g": 5.0},
            {"name": "tea leaves", "weight_g": 3, "fibre_g": 0.0, "sugar_g": 0.0},
            {"name": "sugar", "weight_g": 15, "fibre_g": 0.0, "sugar_g": 15.0},
            {"name": "ginger", "weight_g": 5, "fibre_g": 0.1, "sugar_g": 0.1},
            {"name": "cardamom", "weight_g": 1, "fibre_g": 0.5, "sugar_g": 0.0},
        ],
        "expected_score": 2.5,
        "expected_gaps": ["low fibre", "too much sugar"],
        "drink": {
            "name": "Haldi-Milk with Cardamom",
            "emoji": "🥛",
            "ingredients": ["milk", "turmeric", "cardamom", "black pepper", "honey"],
            "prep": "Warm 250ml milk with ¼ tsp turmeric, 2 crushed cardamom pods, pinch of black pepper, and ½ tsp honey.",
            "explanation": "Your chai already has cardamom (zingiberaceae), so we build on that family. Turmeric (also zingiberaceae) shares 67 molecules with cardamom — score 0.298. Black pepper adds piperine, which increases curcumin bioavailability by 2000%. Honey replaces refined sugar with a lower-glycemic sweetener that feeds beneficial gut bacteria.",
            "shared_molecules": 67,
            "similarity_score": 0.298,
        },
    },
]

# Map for quick lookup
MEAL_BY_ID = {m["id"]: m for m in MEALS}
MEAL_NAMES = [m["name"] for m in MEALS]

# Simple keyword → meal mapping for free-text input
KEYWORD_MAP = {
    "noodle": "noodles_coke",
    "coke": "noodles_coke",
    "coca": "noodles_coke",
    "rajma": "rajma_chawal",
    "burger": "burger_fries",
    "fries": "burger_fries",
    "pepsi": "burger_fries",
    "idli": "idli_sambar",
    "sambar": "idli_sambar",
    "coffee": "idli_sambar",
    "maggi": "maggi_chai",
    "chai": "maggi_chai",
    "tea": "maggi_chai",
}


def find_meal(text: str) -> Dict:
    """Naive keyword match. In production this would use an LLM."""
    text_lower = text.lower()
    for keyword, meal_id in KEYWORD_MAP.items():
        if keyword in text_lower:
            return MEAL_BY_ID[meal_id]
    # Default fallback
    return MEAL_BY_ID["noodles_coke"]
