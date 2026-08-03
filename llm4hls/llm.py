"""Pluggable LLM backend for the reference agent — hardened version.

Changes vs the upstream reference:
- OpenRouterClient retries transient failures (429 / 5xx / timeouts / empty
  completions) with exponential backoff, so a flaky API never kills a 13h run.
- Per-call temperature override: the agent uses low temperature for repair
  and slightly higher for optimization.
- Call audit counters (api_calls / api_failures) so the batch runner can
  prove `real_api_only=True` and report how clean the run was.

Interface is still a single `complete(system, user) -> str` (plus an optional
temperature kwarg), so the two clients remain interchangeable.
"""

from __future__ import annotations

import json
import time
import requests
from typing import Protocol

from . import config

class LLMClient(Protocol):
    def complete(
        self, system: str, user: str, temperature: float | None = None
    ) -> str: ...

class ScriptedClient:
    """Deterministic offline backend: returns the next canned response."""

    def __init__(self, responses: list[str]) -> None:
        self._responses = list(responses)
        self._i = 0
        self.api_calls = 0
        self.api_failures = 0

    def complete(
        self, system: str, user: str, temperature: float | None = None
    ) -> str:
        if not self._responses:
            return ""
        resp = self._responses[min(self._i, len(self._responses) - 1)]
        self._i += 1
        return resp

class OpenRouterClient:
    """Real backend via OpenRouter's OpenAI-compatible chat-completions API,
    with retry + backoff + audit."""

    # Transient HTTP statuses worth retrying.
    RETRY_STATUS = {408, 409, 425, 429, 500, 502, 503, 504}

    def __init__(
        self,
        model: str | None = None,
        api_key: str | None = None,
        temperature: float = 0.2,
        max_tokens: int = 16384,
        token_budget: int = 1000000,  # max total tokens per task (competition requirement)
        max_retries: int = 8,
        base_delay: float = 5.0,
        timeout: int = 300,
    ) -> None:
        self.api_key = api_key or config.OPENROUTER_API_KEY
        if not self.api_key:
            raise RuntimeError(
                "OpenRouter token missing. Set OPENROUTER_API_KEY in the environment "
                "or fill OPENROUTER_API_KEY in llm4hls/config.py."
            )
        self.model = model or config.DEFAULT_LLM_MODEL
        self.base_url = config.OPENROUTER_BASE_URL
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.timeout = timeout
        # audit counters
        self.api_calls = 0
        self.api_failures = 0
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_cached_tokens = 0
        self.token_budget = token_budget

    def _post(self, json_data: dict) -> dict:
        resp = requests.post(
            self.base_url,
            data=json.dumps(json_data, ensure_ascii=True).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json; charset=utf-8",
                "HTTP-Referer": "https://llm4hls.local",
                "X-Title": "LLM4HLS Track A",
            },
            timeout=self.timeout,
        )
        resp.raise_for_status()
        return resp.json()

    def complete(
        self, system: str, user: str, temperature: float | None = None
    ) -> str:
        json_data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": (
                temperature if temperature is not None else self.temperature
            ),
            "max_tokens": self.max_tokens,
        }

        last_err = "unknown"
        for attempt in range(self.max_retries):
            try:
                body = self._post(json_data)
                msg = body["choices"][0]["message"]
                content = msg.get("content") or ""
                if isinstance(content, list):
                    content = "".join(
                        p.get("text", "") for p in content if isinstance(p, dict)
                    )
                if not content.strip():
                    raise ValueError("empty completion content")
                self.api_calls += 1
                usage = body.get("usage", {})
                p_tok = usage.get("prompt_tokens", 0)
                c_tok = usage.get("completion_tokens", 0)
                self.total_prompt_tokens += p_tok
                self.total_completion_tokens += c_tok
                details = usage.get("prompt_tokens_details", {})
                self.total_cached_tokens += details.get("cached_tokens", 0)
                return content
            except requests.exceptions.HTTPError as e:
                code = e.response.status_code if e.response is not None else 0
                detail = str(e)[:400]
                last_err = f"HTTP {code}: {detail}"
                if code not in self.RETRY_STATUS:
                    raise RuntimeError(f"OpenRouter {last_err}") from e
                self.api_failures += 1
            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.RequestException,
                json.JSONDecodeError,
                KeyError,
                IndexError,
                ValueError,
                UnicodeError,
            ) as e:
                import traceback
                traceback.print_exc()
                last_err = f"{type(e).__name__}: {e}"
                self.api_failures += 1

            delay = min(self.base_delay * (2 ** attempt), 120.0)
            print(
                f"  [llm] attempt {attempt + 1}/{self.max_retries} failed "
                f"({last_err}); retrying in {delay:.0f}s",
                flush=True,
            )
            time.sleep(delay)

        raise RuntimeError(
            f"OpenRouter failed after {self.max_retries} attempts: {last_err}"
        )
