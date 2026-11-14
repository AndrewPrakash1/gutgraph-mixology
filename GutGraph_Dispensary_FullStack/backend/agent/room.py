"""
GutParliament — the "room" from the Notion plan.

Every agent receives the SAME MealContext + truth-layer metrics, then speaks
in a SERIAL QUEUE (grokbot-clone pattern: one agent at a time so turns never
collide, and the transcript reads like a group chat).

This module is an async generator of SSE-ready event dicts; main.py serialises
them. Events:
  agent_start {agent fields}                  — an agent takes the floor
  token       {agent, delta}                  — streamed word of its reason
  error       {agent, provider, status, body} — a live call failed (demo-safe:
                                                the turn falls back to template)
  vote        {agent, vote, reason, source}   — final validated vote
  tally       {votes, yes, total}             — the room's verdict

Live vs mock tokens: with a provider configured the words arrive straight from
the model as it generates them (no fake typing pause). With no key — or when a
live call fails — the persona template is typed out word by word so the demo
still reads like a conversation.
"""

import asyncio
from typing import AsyncIterator, Dict, List

from .loop import AgentVote, render_mock_line, run_agent_turn

# pacing for the demo — small enough that a full 8-agent run stays snappy
WORD_DELAY_S = 0.014
THINK_DELAY_S = 0.35


def normalize_metrics(raw: Dict) -> Dict:
    """Round/convert gut_engine metrics into the template/LLM-friendly shape."""
    total = raw["total_weight_g"] or 1
    families = sorted(raw["spice_families"])
    return {
        "fibre_g": round(raw["fibre_g"], 1),
        "sugar_g": round(raw["sugar_g"], 1),
        "total_weight_g": round(total, 0),
        "fibre_per_100": round(raw["fibre_g"] / total * 100, 2),
        "sugar_per_100": round(raw["sugar_g"] / total * 100, 2),
        "fermented_count": raw["fermented_count"],
        "probiotic_count": raw["probiotic_count"],
        "n_families": len(families),
        "families_csv": ", ".join(families) if families else "none",
    }


class GutParliament:
    def __init__(self, agents: List[Dict]):
        self.agents = agents

    async def convene(self, meal_name: str, metrics: Dict) -> AsyncIterator[Dict]:
        votes = []
        for agent in self.agents:
            handle = agent["handle"]
            yield {"event": "agent_start", "agent": {
                "handle": handle, "name": agent["name"],
                "emoji": agent["emoji"], "role": agent["role"], "color": agent["color"],
            }}
            await asyncio.sleep(THINK_DELAY_S)  # "thinking" beat for the UI

            streamed = False
            final = None
            async for partial in run_agent_turn(agent, meal_name, metrics):
                if partial["kind"] == "token":
                    streamed = True
                    yield {"event": "token", "agent": handle, "delta": partial["delta"]}
                else:
                    final = partial

            if final is None:
                # The turn yielded nothing at all. Never let that end the run.
                concerned = agent["verdict"](metrics)
                vote = "no" if concerned else "yes"
                final = {
                    "vote": AgentVote(agent=handle, vote=vote,
                                      reason=render_mock_line(agent, vote, metrics)),
                    "source": "template",
                    "error": {"message": "agent turn produced no vote; used the persona template"},
                }

            result = final["vote"]

            if final["error"]:
                # Report it. The run continues on the template, but a bad key or
                # an empty balance is now visible in the transcript and the logs.
                yield {"event": "error", "agent": handle, **final["error"]}

            if not streamed:
                # Mock mode, or a live call that produced nothing: type it out.
                for word in result.reason.split(" "):
                    yield {"event": "token", "agent": handle, "delta": word + " "}
                    await asyncio.sleep(WORD_DELAY_S)

            votes.append({**result.model_dump(), "source": final["source"]})
            yield {"event": "vote", "agent": handle, "vote": result.vote,
                   "reason": result.reason, "source": final["source"]}

        yield {"event": "tally", "votes": votes,
               "yes": sum(1 for v in votes if v["vote"] == "yes"),
               "total": len(votes)}
        yield {"event": "sources", "sources": sorted({v["source"] for v in votes})}
