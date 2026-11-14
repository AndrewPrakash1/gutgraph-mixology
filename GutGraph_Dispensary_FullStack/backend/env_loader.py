"""Load repo-root ``.env`` into ``os.environ`` (setdefault only)."""

from __future__ import annotations

import os
import pathlib


def load_dotenv() -> None:
    backend = pathlib.Path(__file__).resolve().parent
    repo = backend.parent.parent
    for candidate in (repo / ".env", backend / ".env"):
        if not candidate.is_file():
            continue
        for line in candidate.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(
                    k.strip(), v.strip().strip('"').strip("'")
                )
        return