"""FoodoScope API gateway client (Fork-IT 2026 starter pattern).

Reads ``FOODOSCOPE_API_KEY`` / ``FOODOSCOPE_BASE_URL`` from repo-root ``.env``.
Disk cache in ``.foodoscope_cache/`` at repo root (per STARTER_GUIDE §6).
"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import time
from typing import Any

import requests

DEFAULT_BASE_URL = "http://cosylab.iiitd.edu.in:6969"
_REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


def _load_dotenv(path: str = ".env") -> None:
    for candidate in (_REPO_ROOT / path, pathlib.Path(path)):
        if candidate.is_file():
            for line in candidate.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            return


class FoodoscopeError(RuntimeError):
    def __init__(self, status: int, message: str, url: str):
        super().__init__(f"[{status}] {message} ({url})")
        self.status, self.message, self.url = status, message, url


class Foodoscope:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        cache_dir: str | pathlib.Path | None = None,
        timeout: float = 30,
    ):
        _load_dotenv()
        self.api_key = (api_key or os.getenv("FOODOSCOPE_API_KEY", "")).strip()
        if not self.api_key:
            raise FoodoscopeError(503, "FOODOSCOPE_API_KEY is not set", "")
        self.base_url = (base_url or os.getenv("FOODOSCOPE_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout
        cache_path = cache_dir if cache_dir is not None else _REPO_ROOT / ".foodoscope_cache"
        self.cache = pathlib.Path(cache_path) if cache_path else None
        if self.cache:
            self.cache.mkdir(exist_ok=True)
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Bearer {self.api_key}"
        self._pause_until = 0.0

    def get(self, path: str, **params: Any) -> Any:
        return self._request("GET", path, params=params)

    def post(self, path: str, body: Any = None, **params: Any) -> Any:
        return self._request("POST", path, params=params, body=body)

    def _cache_file(self, method: str, url: str, params: dict, body: Any) -> pathlib.Path | None:
        if not self.cache:
            return None
        key = json.dumps([method, url, sorted(params.items()), body], sort_keys=True, default=str)
        return self.cache / (hashlib.sha1(key.encode()).hexdigest() + ".json")

    def _request(self, method: str, path: str, params: dict, body: Any = None) -> Any:
        url = self.base_url + (path if path.startswith("/") else "/" + path)
        cf = self._cache_file(method, url, params, body)
        if cf and cf.exists():
            return json.loads(cf.read_text(encoding="utf-8"))

        wait = self._pause_until - time.time()
        if wait > 0:
            time.sleep(wait)

        resp = self.session.request(method, url, params=params or None, json=body, timeout=self.timeout)

        remaining = resp.headers.get("X-RateLimit-Remaining")
        if remaining is not None and remaining.lstrip("-").isdigit() and int(remaining) <= 0:
            self._pause_until = time.time() + 61

        if resp.status_code == 429:
            raise FoodoscopeError(
                429,
                "Rate limit exceeded (60/min). Cache and slow down.",
                url,
            )
        try:
            data = resp.json()
        except ValueError:
            data = resp.text
        if not resp.ok:
            if isinstance(data, dict):
                msg = data.get("error") or data.get("message")
            else:
                msg = str(data)[:200]
            raise FoodoscopeError(resp.status_code, msg or resp.reason, url)

        if cf:
            cf.write_text(json.dumps(data), encoding="utf-8")
        return data


_client: Foodoscope | None | bool = False


def get_foodoscope() -> Foodoscope | None:
    """Singleton; None when no key (demo offline)."""
    global _client
    if _client is False:
        try:
            _client = Foodoscope()
        except FoodoscopeError:
            _client = None
    return _client if isinstance(_client, Foodoscope) else None