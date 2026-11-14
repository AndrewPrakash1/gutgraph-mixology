"""
GutGraph Mixology — Gut Scoring Engine
Rule-based gut health scoring (not ML). Each rule checks one dietary factor.
"""

from typing import List, Dict, Tuple

# Thresholds
FIBRE_PER_100G_MIN = 2.0      # grams
SUGAR_PER_100G_MAX = 10.0     # grams
SPICE_DIVERSITY_MIN = 3       # unique spice families
FERMENTED_TAGS = {"yogurt", "curd", "buttermilk", "chaas", "lassi", "kefir",
                  "kimchi", "sauerkraut", "pickle", "fermented", "dosa", "idli",
                  "kanji", "dhokla", "tempeh", "miso"}
PROBIOTIC_TAGS = {"yogurt", "curd", "buttermilk", "chaas", "lassi", "kefir"}
SPICE_FAMILIES = {
    "turmeric": "zingiberaceae", "ginger": "zingiberaceae", "galangal": "zingiberaceae",
    "cumin": "apiaceae", "coriander": "apiaceae", "fennel": "apiaceae", "caraway": "apiaceae",
    "black pepper": "piperaceae", "long pepper": "piperaceae",
    "cinnamon": "lauraceae", "clove": "myrtaceae", "nutmeg": "myristicaceae",
    "cardamom": "zingiberaceae", "star anise": "schisandraceae",
    "mustard": "brassicaceae", "fenugreek": "fabaceae", "asafoetida": "apiaceae",
    "saffron": "iridaceae", "bay leaf": "lauraceae",
    "chilli": "solanaceae", "paprika": "solanaceae",
    "garlic": "amaryllidaceae", "onion": "amaryllidaceae",
    "mint": "lamiaceae", "basil": "lamiaceae", "oregano": "lamiaceae",
    "tamarind": "fabaceae", "amchur": "anacardiaceae",
}


def compute_gut_score(ingredients: List[Dict]) -> Tuple[float, List[str], Dict]:
    """
    Returns: (score 0-10, gap_labels, detailed_metrics)
    """
    metrics = {
        "fibre_g": 0.0,
        "sugar_g": 0.0,
        "total_weight_g": 0.0,
        "fermented_count": 0,
        "probiotic_count": 0,
        "spice_families": set(),
    }

    normalized = [i["name"].lower().strip() for i in ingredients]

    for ing in ingredients:
        name = ing["name"].lower().strip()
        weight = ing.get("weight_g", 100)
        metrics["total_weight_g"] += weight
        metrics["fibre_g"] += ing.get("fibre_g", 0)
        metrics["sugar_g"] += ing.get("sugar_g", 0)

        # Check fermented
        if any(tag in name for tag in FERMENTED_TAGS):
            metrics["fermented_count"] += 1

        # Check probiotic
        if any(tag in name for tag in PROBIOTIC_TAGS):
            metrics["probiotic_count"] += 1

        # Check spice family
        for spice, family in SPICE_FAMILIES.items():
            if spice in name:
                metrics["spice_families"].add(family)

    # Per-100g normalizations
    if metrics["total_weight_g"] > 0:
        fibre_per_100 = (metrics["fibre_g"] / metrics["total_weight_g"]) * 100
        sugar_per_100 = (metrics["sugar_g"] / metrics["total_weight_g"]) * 100
    else:
        fibre_per_100 = 0
        sugar_per_100 = 0

    gaps = []
    score = 10.0

    # Rule 1: Fibre
    if fibre_per_100 < FIBRE_PER_100G_MIN:
        gaps.append("low fibre")
        score -= 2.0

    # Rule 2: Fermented food
    if metrics["fermented_count"] == 0:
        gaps.append("no fermented food")
        score -= 2.0

    # Rule 3: Sugar
    if sugar_per_100 > SUGAR_PER_100G_MAX:
        gaps.append("too much sugar")
        score -= 2.5

    # Rule 4: Probiotics
    if metrics["probiotic_count"] == 0:
        gaps.append("low probiotics")
        score -= 1.5

    # Rule 5: Spice diversity
    if len(metrics["spice_families"]) < SPICE_DIVERSITY_MIN:
        gaps.append("low spice diversity")
        score -= 1.5

    score = max(0.0, min(10.0, score))
    return round(score, 1), gaps, metrics
