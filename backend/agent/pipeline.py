"""
Mixologist orchestrator — the only agent that talks to the user
(per the Notion plan). Pipeline:

  parse meal -> truth layer (gut_engine) -> convene parliament
  -> aggregate -> pairing tool -> drink card

Emits SSE-ready event dicts. Everything here is mock-safe: with no
DeepSeek key the agent lines come from persona templates, and the
numbers ALWAYS come from gut_engine, never from a model.
"""

import asyncio
from typing import AsyncIterator, Dict

from demo_data import KEYWORD_MAP, MEAL_BY_ID, MEALS
from gut_engine import compute_gut_score

from .personas import AGENTS, MIXOLOGIST
from .room import GutParliament, normalize_metrics

STATUS_DELAY_S = 0.4


def _mixologist_event() -> Dict:
    return {"event": "agent_start", "agent": {
        "handle": MIXOLOGIST["handle"], "name": MIXOLOGIST["name"],
        "emoji": MIXOLOGIST["emoji"], "role": MIXOLOGIST["role"],
        "color": MIXOLOGIST["color"],
    }}


async def _speak(text: str, agent: str = MIXOLOGIST["handle"]) -> AsyncIterator[Dict]:
    for word in text.split(" "):
        yield {"event": "token", "agent": agent, "delta": word + " "}
        await asyncio.sleep(0.014)


def _match_meal(message: str):
    """Keyword match, but honest: returns None when nothing matches
    (find_meal silently falls back to noodles — fine for the old UI,
    wrong for a chat agent)."""
    text = message.lower()
    for keyword, meal_id in KEYWORD_MAP.items():
        if keyword in text:
            return MEAL_BY_ID[meal_id]
    return None


async def run_pipeline(message: str) -> AsyncIterator[Dict]:
    m = MIXOLOGIST

    yield _mixologist_event()
    async for ev in _speak("On it. Let me parse that meal and pull the facts."):
        yield ev
    await asyncio.sleep(STATUS_DELAY_S)

    meal = _match_meal(message)
    if meal is None:
        names = ", ".join(x["name"] for x in MEALS)
        async for ev in _speak(
            "I don't recognise that meal yet — my recipe knowledge is still mocked. "
            f"For the demo I know: {names}. Try one of those."
        ):
            yield ev
        yield {"event": "unknown_meal"}
        yield {"event": "done"}
        return

    yield {"event": "meal", "meal": {
        "id": meal["id"], "name": meal["name"], "emoji": meal["emoji"],
        "ingredients": [i["name"] for i in meal["ingredients"]],
    }}

    # --- truth layer: Python computes, agents interpret ---------------------
    score, gaps, raw_metrics = compute_gut_score(meal["ingredients"])
    metrics = normalize_metrics(raw_metrics)
    yield {"event": "tool", "tool": "gut_engine.compute_score",
           "output": {"gut_score": score, "gaps": gaps, **metrics}}
    await asyncio.sleep(STATUS_DELAY_S)

    async for ev in _speak(
        f"Facts are in — gut score {score}/10. Convening the gut parliament, 8 microbes on the floor…"
    ):
        yield ev
    await asyncio.sleep(STATUS_DELAY_S)

    # --- parliament ----------------------------------------------------------
    room = GutParliament(AGENTS)
    tally = None
    async for ev in room.convene(meal["name"], metrics):
        if ev["event"] == "tally":
            tally = ev
        yield ev

    # --- aggregate + prescribe ----------------------------------------------
    yield _mixologist_event()
    yes = tally["yes"] if tally else 0
    verdict_line = (
        f"Parliament has spoken: {yes} of 8 approve. "
        + ("Your microbes are broadly happy — minor tune-ups only."
           if yes >= 6 else
           "Your microbes are revolting. Prescribing a rescue drink.")
        if tally else "Parliament adjourned."
    )
    async for ev in _speak(verdict_line):
        yield ev
    await asyncio.sleep(STATUS_DELAY_S)

    drink = meal["drink"]
    yield {"event": "tool", "tool": "pairing_engine.flavordb_lookup",
           "output": {"drink": drink["name"],
                      "shared_molecules": drink["shared_molecules"],
                      "similarity_score": drink["similarity_score"]}}
    await asyncio.sleep(STATUS_DELAY_S)

    async for ev in _speak(
        f"Prescription: {drink['name']} — {drink['prep']} {drink['explanation']}"
    ):
        yield ev

    yield {"event": "result", "result": {
        "gut_score": score,
        "gaps": gaps,
        "drink": drink,
        "tally": {"yes": yes, "total": tally["total"] if tally else 0},
    }}
    yield {"event": "done"}
