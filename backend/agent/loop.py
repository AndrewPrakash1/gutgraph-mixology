"""
Agent turn loop — the grokbot-clone loop.py pattern, shrunk for a hackathon.

One turn = decide the vote (truth layer) -> word it (model, streamed) ->
validate -> vote. The vote itself NEVER comes from the model:
personas.verdict() computes it from truth-layer metrics. The model only
phrases the reason.

Yields partial events so the caller can put words on the wire as they arrive:

    {"kind": "token", "delta": str}                 — live words from the model
    {"kind": "vote",  "vote": AgentVote,
     "source": "deepseek" | "openrouter" | "template",
     "error": dict | None}                          — the final validated vote

`error` is populated when a live call failed. It is reported, never swallowed:
the run still completes on template text, but the caller knows why, so a 401
on demo morning is visible instead of silent.
"""

from typing import AsyncIterator, Dict

from pydantic import BaseModel, field_validator

from . import llm


class AgentVote(BaseModel):
    agent: str
    vote: str
    reason: str

    @field_validator("vote")
    @classmethod
    def vote_must_be_binary(cls, v: str) -> str:
        if v not in ("yes", "no"):
            raise ValueError("vote must be 'yes' or 'no'")
        return v


def render_mock_line(agent: Dict, vote: str, metrics: Dict) -> str:
    template = agent["no_line"] if vote == "no" else agent["yes_line"]
    return template.format(**metrics)


def _tidy(text: str) -> str:
    """Models like to wrap a one-liner in quotes or a code fence. Unwrap it."""
    out = text.strip()
    if out.startswith("```"):
        out = out.strip("`").strip()
        if out.lower().startswith("text"):
            out = out[4:].strip()
    if len(out) >= 2 and out[0] == out[-1] and out[0] in "\"'":
        out = out[1:-1].strip()
    return out


async def run_agent_turn(agent: Dict, meal_name: str, metrics: Dict) -> AsyncIterator[Dict]:
    """
    1. Truth layer: verdict() decides the vote from real metrics.
    2. If a provider is configured, the model words the reason, streamed.
    3. Otherwise (or on failure), the persona template words it.
    """
    concerned = agent["verdict"](metrics)
    vote = "no" if concerned else "yes"

    chunks = []
    source = "template"
    error = None

    if llm.llm_enabled():
        try:
            async for delta in llm.stream_reason(agent, meal_name, metrics, vote):
                chunks.append(delta)
                yield {"kind": "token", "delta": delta}
            source = llm.provider_name()
        except llm.LLMError as exc:
            error = exc.as_dict()
        except Exception as exc:  # noqa: BLE001 — one bad turn must not kill the run
            error = {"message": f"{type(exc).__name__}: {exc}"}

    reason = _tidy("".join(chunks))
    if not reason:
        # Live mode with no usable text (failed, or the model sent nothing).
        source = "template"
        reason = render_mock_line(agent, vote, metrics)

    yield {
        "kind": "vote",
        "vote": AgentVote(agent=agent["handle"], vote=vote, reason=reason),
        "source": source,
        "error": error,
    }
