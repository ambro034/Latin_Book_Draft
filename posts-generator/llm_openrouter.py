"""Minimal OpenRouter chat client (OpenAI-compatible REST).

Used by the Telegram drafter instead of Azure OpenAI so the CI workflow needs
only one cheap/free secret: OPENROUTER_API_KEY.

Docs: https://openrouter.ai/docs

Env:
  OPENROUTER_API_KEY   (required)
  OPENROUTER_MODEL     (optional; default deepseek/deepseek-chat-v3:free)
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request

_API_URL = "https://openrouter.ai/api/v1/chat/completions"
_DEFAULT_MODEL = "deepseek/deepseek-chat-v3:free"


def default_model() -> str:
    # Treat an unset OR empty/whitespace value (e.g. an undefined CI variable
    # that expands to "") as "use the built-in default".
    return (os.getenv("OPENROUTER_MODEL") or "").strip() or _DEFAULT_MODEL


def chat(
    messages: list[dict],
    *,
    model: str | None = None,
    max_tokens: int = 1024,
    temperature: float = 0.8,
    api_key: str | None = None,
    retries: int = 3,
    timeout: int = 90,
) -> str:
    """Call OpenRouter chat completions and return the assistant text.

    Retries on transient errors (429 / 5xx) with linear backoff — free models
    are rate-limited and occasionally unavailable.
    """
    key = api_key or os.getenv("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY not set")

    payload = json.dumps(
        {
            "model": (model or "").strip() or default_model(),
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
    ).encode("utf-8")

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        # Optional attribution headers recommended by OpenRouter.
        "HTTP-Referer": "https://beops.site",
        "X-Title": "BeOps Telegram Drafter",
    }

    last_err: Exception | None = None
    for attempt in range(1, retries + 1):
        req = urllib.request.Request(_API_URL, data=payload, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            content = (data["choices"][0]["message"].get("content") or "").strip()
            if not content:
                # Free models occasionally return empty content; treat as transient.
                last_err = RuntimeError(f"OpenRouter returned empty content: {data}")
                if attempt < retries:
                    time.sleep(2 * attempt)
                    continue
                raise last_err
            return content
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            last_err = RuntimeError(f"OpenRouter HTTP {e.code}: {body}")
            if e.code in (429, 500, 502, 503, 504) and attempt < retries:
                time.sleep(2 * attempt)
                continue
            raise last_err
        except (urllib.error.URLError, TimeoutError) as e:  # network hiccup
            last_err = e
            if attempt < retries:
                time.sleep(2 * attempt)
                continue
            raise
    raise last_err if last_err else RuntimeError("OpenRouter call failed")
