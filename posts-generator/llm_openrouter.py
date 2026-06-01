"""Minimal OpenRouter chat client (OpenAI-compatible REST).

Used by the Telegram drafter instead of Azure OpenAI so the CI workflow needs
only one cheap/free secret: OPENROUTER_API_KEY.

Docs: https://openrouter.ai/docs

Env:
  OPENROUTER_API_KEY   (required)
  OPENROUTER_MODEL     (optional; default meta-llama/llama-3.3-70b-instruct:free)
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request

_API_URL = "https://openrouter.ai/api/v1/chat/completions"
_DEFAULT_MODEL = "meta-llama/llama-3.3-70b-instruct:free"

# Free models are individually rate-limited / occasionally retired upstream.
# When no explicit model is requested we try these in order so a transient
# 429 or a retired slug on one model falls through to the next.
_FALLBACK_MODELS = [
    "meta-llama/llama-3.3-70b-instruct:free",
    "qwen/qwen3-next-80b-a3b-instruct:free",
    "openai/gpt-oss-120b:free",
    "z-ai/glm-4.5-air:free",
    "google/gemma-4-31b-it:free",
]


def default_model() -> str:
    # Treat an unset OR empty/whitespace value (e.g. an undefined CI variable
    # that expands to "") as "use the built-in default".
    return (os.getenv("OPENROUTER_MODEL") or "").strip() or _DEFAULT_MODEL


def _candidate_models(model: str | None) -> list[str]:
    """Models to try, in order. An explicit model (arg or env) is used alone;
    otherwise fall back across the built-in free-model list."""
    explicit = (model or "").strip() or (os.getenv("OPENROUTER_MODEL") or "").strip()
    if explicit:
        return [explicit]
    # de-dupe while preserving order
    seen: set[str] = set()
    out: list[str] = []
    for m in _FALLBACK_MODELS:
        if m not in seen:
            seen.add(m)
            out.append(m)
    return out


def chat(
    messages: list[dict],
    *,
    model: str | None = None,
    max_tokens: int = 1024,
    temperature: float = 0.8,
    api_key: str | None = None,
    retries: int = 4,
    timeout: int = 90,
) -> str:
    """Call OpenRouter chat completions and return the assistant text.

    Tries each candidate model in turn; for each, retries on transient errors
    (429 / 5xx / empty content) honoring any Retry-After header. A 404 (retired
    model) or exhausted retries falls through to the next candidate model.
    """
    key = api_key or os.getenv("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY not set")

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        # Optional attribution headers recommended by OpenRouter.
        "HTTP-Referer": "https://beops.site",
        "X-Title": "BeOps Telegram Drafter",
    }

    last_err: Exception | None = None
    for mdl in _candidate_models(model):
        payload = json.dumps(
            {
                "model": mdl,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
            }
        ).encode("utf-8")

        for attempt in range(1, retries + 1):
            req = urllib.request.Request(_API_URL, data=payload, headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                content = (data["choices"][0]["message"].get("content") or "").strip()
                if not content:
                    # Free models occasionally return empty content; transient.
                    last_err = RuntimeError(f"OpenRouter returned empty content: {data}")
                    if attempt < retries:
                        time.sleep(2 * attempt)
                        continue
                    break  # try next model
                return content
            except urllib.error.HTTPError as e:
                body = e.read().decode("utf-8", "replace")
                last_err = RuntimeError(f"OpenRouter HTTP {e.code} ({mdl}): {body}")
                if e.code == 404:
                    break  # retired/unavailable model -> next candidate
                if e.code in (429, 500, 502, 503, 504) and attempt < retries:
                    time.sleep(_retry_after(e.headers, attempt))
                    continue
                break  # non-retryable or retries exhausted -> next candidate
            except (urllib.error.URLError, TimeoutError) as e:  # network hiccup
                last_err = e
                if attempt < retries:
                    time.sleep(2 * attempt)
                    continue
                break
    raise last_err if last_err else RuntimeError("OpenRouter call failed")


def _retry_after(hdrs, attempt: int) -> float:
    """Honor a Retry-After header (seconds), capped; else linear backoff."""
    try:
        ra = float(hdrs.get("Retry-After", "")) if hdrs else 0.0
    except (TypeError, ValueError):
        ra = 0.0
    return min(max(ra, 2.0 * attempt), 20.0)
