"""
LLM client — DeepSeek or OpenRouter, streamed, failing loudly.

The vote is NEVER decided here (see personas.verdict / loop.run_agent_turn):
the truth layer decides yes/no from gut_engine metrics and the model only
words the reason. Two rules this module exists to enforce:

  1. Provider-agnostic. Whichever of DEEPSEEK_API_KEY / OPENROUTER_API_KEY is
     set wins; LLM_PROVIDER forces one.
  2. Failures are raised, not swallowed. The previous version did
     `except Exception: return None`, so a wrong key, a bad model name or a
     429 degraded every agent to template text with no signal anywhere -- a
     silent failure exactly when you cannot afford one. LLMError now carries
     the status and the response body, and room.py puts it on the wire.

Env (all optional):
  COMMANDCODE_API_KEY   COMMANDCODE_BASE_URL (default https://api.commandcode.ai/provider/v1)
                        COMMANDCODE_MODEL    (default deepseek/deepseek-v4-flash)
  DEEPSEEK_API_KEY      DEEPSEEK_BASE_URL (default https://api.deepseek.com)
                        DEEPSEEK_MODEL    (default deepseek-chat)
  OPENROUTER_API_KEY    OPENROUTER_BASE_URL (default https://openrouter.ai/api/v1)
                        OPENROUTER_MODEL  (default deepseek/deepseek-chat-v3.1)
  LLM_PROVIDER = commandcode | deepseek | openrouter   — force a provider
  LLM_TIMEOUT  = seconds                 — default 30
"""

import json
import os
from typing import AsyncIterator, Dict, List, Optional

import httpx

try:
    from foodoscope_client import _load_dotenv

    _load_dotenv()
except ImportError:
    pass


class LLMError(Exception):
    """A live call failed in a way worth showing on the wire."""

    def __init__(self, message: str, status: Optional[int] = None, body: str = ""):
        super().__init__(message)
        self.status = status
        self.body = body

    def as_dict(self) -> Dict:
        d = {"message": str(self)}
        if self.status is not None:
            d["status"] = self.status
        if self.body:
            d["body"] = self.body
        return d


def _candidates() -> List[Dict]:
    out = []
    cmd_key = os.environ.get("COMMANDCODE_API_KEY") or os.environ.get("CMD_API_KEY")
    if cmd_key:
        base = os.environ.get(
            "COMMANDCODE_BASE_URL", "https://api.commandcode.ai/provider/v1"
        ).rstrip("/")
        out.append({
            "provider": "commandcode",
            "url": f"{base}/chat/completions",
            "key": cmd_key.strip(),
            "model": os.environ.get("COMMANDCODE_MODEL", "deepseek/deepseek-v4-flash"),
            "extra_headers": {},
        })
    if os.environ.get("DEEPSEEK_API_KEY"):
        base = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com").rstrip("/")
        out.append({
            "provider": "deepseek",
            "url": f"{base}/chat/completions",
            "key": os.environ["DEEPSEEK_API_KEY"],
            "model": os.environ.get("DEEPSEEK_MODEL", "deepseek-chat"),
            "extra_headers": {},
        })
    if os.environ.get("OPENROUTER_API_KEY"):
        base = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1").rstrip("/")
        out.append({
            "provider": "openrouter",
            "url": f"{base}/chat/completions",
            "key": os.environ["OPENROUTER_API_KEY"],
            "model": os.environ.get("OPENROUTER_MODEL", "deepseek/deepseek-chat-v3.1"),
            "extra_headers": {
                # OpenRouter attribution headers; ignored by other providers.
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "GutGraph Mixology",
            },
        })
    forced = (os.environ.get("LLM_PROVIDER") or "").strip().lower()
    if forced:
        out = [c for c in out if c["provider"] == forced]
    default_tokens = "200" if any(c["provider"] == "commandcode" for c in out) else "90"
    for c in out:
        c["max_tokens"] = int(os.environ.get("LLM_MAX_TOKENS", default_tokens))
    return out


def provider() -> Optional[Dict]:
    cands = _candidates()
    return cands[0] if cands else None


def provider_name() -> str:
    cfg = provider()
    return cfg["provider"] if cfg else "template"


def llm_enabled() -> bool:
    return provider() is not None


def provider_info() -> Dict:
    """For GET /agents and the UI mode badge."""
    cfg = provider()
    return {
        "mode": "live" if cfg else "mock",
        "provider": cfg["provider"] if cfg else None,
        "model": cfg["model"] if cfg else None,
    }


def build_messages(agent: Dict, meal_name: str, metrics: Dict, vote: str) -> List[Dict]:
    """The truth layer has already decided `vote`; the model only words it."""
    facts = "  ".join(f"{k}={v}" for k, v in metrics.items())
    system = (
        agent["system"]
        + " Reply with that one sentence only: no JSON, no quotation marks, "
          "no preamble, no lists, no emoji."
    )
    user = (
        f"Meal: {meal_name}\n"
        f"Truth-layer metrics: {facts}\n"
        f"Your vote (already decided by the truth layer — do not change or "
        f"argue with it): {vote}\n"
        f"Word this vote in your own voice."
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


async def stream_reason(
    agent: Dict, meal_name: str, metrics: Dict, vote: str
) -> AsyncIterator[str]:
    """
    Yield the reason for an already-decided vote, token by token.

    Raises LLMError on anything that goes wrong (no provider, HTTP error,
    network failure) so the caller can fall back *and* say why.
    """
    cfg = provider()
    if cfg is None:
        raise LLMError("no provider configured (set DEEPSEEK_API_KEY or OPENROUTER_API_KEY)")

    payload = {
        "model": cfg["model"],
        "messages": build_messages(agent, meal_name, metrics, vote),
        "stream": True,
        "temperature": 0.8,
        "max_tokens": cfg["max_tokens"],
    }
    headers = {
        "Authorization": f"Bearer {cfg['key']}",
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
    }
    headers.update(cfg["extra_headers"])
    timeout = httpx.Timeout(float(os.environ.get("LLM_TIMEOUT", "30")), connect=10.0)

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            async with client.stream("POST", cfg["url"], headers=headers, json=payload) as res:
                if res.status_code != 200:
                    body = (await res.aread()).decode("utf-8", errors="replace")[:400]
                    raise LLMError(
                        f"{cfg['provider']} returned HTTP {res.status_code}",
                        status=res.status_code,
                        body=body,
                    )
                async for line in res.aiter_lines():
                    if not line or line.startswith(":"):
                        continue
                    if not line.startswith("data:"):
                        continue
                    data = line[5:].strip()
                    if data == "[DONE]":
                        break
                    try:
                        obj = json.loads(data)
                    except json.JSONDecodeError:
                        continue
                    choices = obj.get("choices") or []
                    if not choices:
                        continue
                    delta_obj = choices[0].get("delta") or {}
                    piece = delta_obj.get("content") or delta_obj.get("reasoning_content")
                    if piece:
                        yield piece
    except httpx.HTTPError as exc:
        raise LLMError(f"{cfg['provider']} unreachable: {type(exc).__name__}: {exc}") from exc


async def smoke_test() -> Dict:
    """
    One cheap live call, for `python -m agent.llm` on demo morning.
    Proves the key, the model name and the network before judges are watching.
    """
    info = provider_info()
    if info["mode"] != "live":
        return {**info, "ok": False, "detail": "no API key set — running in mock mode"}
    probe = {
        "system": "Reply with one short sentence in character. No preamble.",
        "verdict": lambda m: True,
    }
    metrics = {"fibre_per_100": 0.8, "sugar_per_100": 31.7, "note": "smoke test"}
    try:
        reason = "".join([
            d async for d in stream_reason(probe, "smoke test meal", metrics, "no")
        ]).strip()
    except LLMError as exc:
        return {**info, "ok": False, "detail": str(exc), **exc.as_dict()}
    return {**info, "ok": bool(reason), "detail": reason or "provider returned no text"}


if __name__ == "__main__":
    import asyncio

    print(json.dumps(asyncio.run(smoke_test()), indent=2, ensure_ascii=False))
