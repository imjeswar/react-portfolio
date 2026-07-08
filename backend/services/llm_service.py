from typing import List, Dict, Any, Generator, Optional
# pyrefly: ignore [missing-import]
from openai import OpenAI
from backend.core.interfaces import LLMProvider
from backend.core.config import settings
import logging
import time

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Provider status constants
# ---------------------------------------------------------------------------
STATUS_READY = "ready"
STATUS_DEGRADED = "degraded"
STATUS_RATE_LIMITED = "rate_limited"


class OpenAILLMProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"

    def _prepare_messages(
        self, prompt: str, system_prompt: str = None, history: List[Dict[str, str]] = None
    ) -> List[Dict[str, str]]:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if history:
            for message in history:
                messages.append({
                    "role": message.get("role", "user"),
                    "content": message.get("content", "")
                })
        messages.append({"role": "user", "content": prompt})
        return messages

    def generate(
        self, prompt: str, system_prompt: str = None, history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        messages = self._prepare_messages(prompt, system_prompt, history)
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.2
            )
            return {
                "answer": response.choices[0].message.content,
                "confidence": 0.9
            }
        except Exception as e:
            logger.warning(f"OpenAI generate failed: {e}. Falling back to RuleBasedLLM.")
            return RuleBasedLLMProvider().generate(prompt, system_prompt, history)

    def generate_stream(
        self, prompt: str, system_prompt: str = None, history: List[Dict[str, str]] = None
    ) -> Generator[str, None, None]:
        messages = self._prepare_messages(prompt, system_prompt, history)
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.2,
                stream=True
            )
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            logger.warning(f"OpenAI generate_stream failed: {e}. Falling back to RuleBasedLLM stream.")
            yield from RuleBasedLLMProvider().generate_stream(prompt, system_prompt, history)


class GeminiLLMProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        self.model = "gemini-1.5-flash"

    def _prepare_messages(
        self, prompt: str, system_prompt: str = None, history: List[Dict[str, str]] = None
    ) -> List[Dict[str, str]]:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if history:
            for message in history:
                messages.append({
                    "role": message.get("role", "user"),
                    "content": message.get("content", "")
                })
        messages.append({"role": "user", "content": prompt})
        return messages

    def generate(
        self, prompt: str, system_prompt: str = None, history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        messages = self._prepare_messages(prompt, system_prompt, history)
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.2
            )
            return {
                "answer": response.choices[0].message.content,
                "confidence": 0.9
            }
        except Exception as e:
            logger.warning(f"Gemini generate failed: {e}. Falling back to RuleBasedLLM.")
            return RuleBasedLLMProvider().generate(prompt, system_prompt, history)

    def generate_stream(
        self, prompt: str, system_prompt: str = None, history: List[Dict[str, str]] = None
    ) -> Generator[str, None, None]:
        messages = self._prepare_messages(prompt, system_prompt, history)
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.2,
                stream=True
            )
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            logger.warning(f"Gemini generate_stream failed: {e}. Falling back to RuleBasedLLM stream.")
            yield from RuleBasedLLMProvider().generate_stream(prompt, system_prompt, history)


class RuleBasedLLMProvider(LLMProvider):
    def generate(
        self, prompt: str, system_prompt: str = None, history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        answer = self._generate_rule_based_response(prompt, system_prompt)
        return {
            "answer": answer,
            "confidence": 0.6
        }

    def generate_stream(
        self, prompt: str, system_prompt: str = None, history: List[Dict[str, str]] = None
    ) -> Generator[str, None, None]:
        answer = self._generate_rule_based_response(prompt, system_prompt)
        for word in answer.split(" "):
            yield word + " "

    def _generate_rule_based_response(self, prompt: str, system_prompt: str = None) -> str:
        full_text_to_search = (system_prompt or "") + "\n" + prompt

        if "Retrieved Context:" in full_text_to_search or "--- Source:" in full_text_to_search:
            import re
            chunks = re.findall(r"--- Source:\s*([^\n]+)\s*---\n(.*?)(?=\n\n---|$)", full_text_to_search, re.DOTALL)
            if chunks:
                summary_lines = []
                for source, text in chunks:
                    source = source.strip()
                    text = text.strip()
                    sentences = text.split(". ")
                    short_text = ". ".join(sentences[:2]).strip()
                    if short_text:
                        if not short_text.endswith("."):
                            short_text += "."
                        summary_lines.append(f"- {short_text} *(Source: {source})*")

                if summary_lines:
                    return "Here is what I found in Jeswar's portfolio:\n\n" + "\n".join(summary_lines)

        return "I'm sorry, I couldn't find any information about that in Jeswar's portfolio. You can reach out to him directly at imjeswar@gmail.com for more details!"


class OpenRouterLLMProvider(LLMProvider):
    """
    OpenRouter LLM provider with startup validation, status-aware error classification,
    active_model tracking, and clean user-facing fallbacks.

    Status values (use the STATUS_* constants above):
      - STATUS_READY        : Primary or fallback model is confirmed reachable
      - STATUS_RATE_LIMITED : API returned 429 — model exists but we're throttled (treated as READY)
      - STATUS_DEGRADED     : Both primary and fallback are unavailable → uses RuleBasedLLMProvider
    """

    def __init__(self, api_key: str, model: str = None, fallback_model: str = None):
        self.api_key = api_key
        self.primary_model = model or settings.OPENROUTER_MODEL
        self.fallback_model = fallback_model or settings.OPENROUTER_FALLBACK_MODEL
        # active_model starts as primary; validate() may switch it to fallback
        self.active_model: str = self.primary_model
        self.status: str = STATUS_READY      # optimistic default before validate()
        self._rule_based = RuleBasedLLMProvider()
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key or "mock_key",
        )

    # ------------------------------------------------------------------
    # Startup Validation
    # ------------------------------------------------------------------

    def validate(self) -> Dict[str, Any]:
        """
        Probe the configured primary model with a tiny completion.
        Returns a dict with keys: status, active_model, reason.

        Error classification:
          401 / AuthenticationError  → DEGRADED  (bad API key, no point retrying)
          404 / model not found      → try fallback
          429 / rate limit           → READY (rate-limited, model exists)
          timeout / connection error → try fallback
          other                      → try fallback
        """
        logger.info(f"[Startup] Validating primary model: {self.primary_model}")
        result = self._probe_model(self.primary_model)

        if result["ok"]:
            self.active_model = self.primary_model
            self.status = STATUS_READY
            return {"status": STATUS_READY, "active_model": self.active_model, "reason": "primary model validated"}

        code = result.get("code")
        reason = result.get("reason", "unknown error")

        # 401 — invalid key, no point trying fallback
        if code == 401:
            logger.error(f"[Startup] OpenRouter auth failed (401). Check OPENROUTER_API_KEY. Entering DEGRADED mode.")
            self.status = STATUS_DEGRADED
            return {"status": STATUS_DEGRADED, "active_model": self.active_model, "reason": f"auth error: {reason}"}

        # 429 — rate-limited but model is reachable
        if code == 429:
            logger.warning(f"[Startup] OpenRouter rate-limited (429) on primary model. Treating as READY.")
            self.active_model = self.primary_model
            self.status = STATUS_RATE_LIMITED
            return {"status": STATUS_RATE_LIMITED, "active_model": self.active_model, "reason": f"rate limited: {reason}"}

        # 404 or timeout / other error → try fallback
        logger.warning(f"[Startup] Primary model '{self.primary_model}' unavailable ({code}): {reason}. Trying fallback model.")
        fallback_result = self._probe_model(self.fallback_model)

        if fallback_result["ok"]:
            self.active_model = self.fallback_model
            self.status = STATUS_READY
            logger.info(f"[Startup] Fallback model '{self.fallback_model}' validated. Using it as active model.")
            return {"status": STATUS_READY, "active_model": self.active_model, "reason": f"using fallback after primary failed ({code})"}

        fallback_code = fallback_result.get("code")
        if fallback_code == 429:
            logger.warning(f"[Startup] Fallback model rate-limited (429). Treating as READY.")
            self.active_model = self.fallback_model
            self.status = STATUS_RATE_LIMITED
            return {"status": STATUS_RATE_LIMITED, "active_model": self.active_model, "reason": "fallback rate limited"}

        # Both failed
        logger.error(
            f"[Startup] Both primary ('{self.primary_model}') and fallback ('{self.fallback_model}') models "
            f"are unavailable. Entering DEGRADED mode — RuleBasedLLMProvider will handle requests."
        )
        self.status = STATUS_DEGRADED
        return {"status": STATUS_DEGRADED, "active_model": self.active_model, "reason": "both models unavailable"}

    def _probe_model(self, model: str) -> Dict[str, Any]:
        """
        Send a minimal 1-token completion to check whether a model is reachable.
        Returns {"ok": bool, "code": int|None, "reason": str}.
        """
        if not self.api_key:
            return {"ok": False, "code": 401, "reason": "no API key configured"}
        try:
            self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "hi"}],
                max_tokens=1,
                temperature=0.0,
                timeout=10.0,
            )
            return {"ok": True, "code": 200, "reason": "success"}
        except Exception as e:
            return self._classify_error(e)

    @staticmethod
    def _classify_error(exc: Exception) -> Dict[str, Any]:
        """Parse OpenAI SDK exception to extract HTTP status code."""
        err_str = str(exc)
        # openai.APIStatusError carries a .status_code attribute
        code = getattr(exc, "status_code", None)
        if code is None:
            # Try to parse from string representation
            import re
            m = re.search(r"\b(400|401|403|404|429|500|502|503)\b", err_str)
            code = int(m.group(1)) if m else None
        ok = False
        return {"ok": ok, "code": code, "reason": err_str[:200]}

    # ------------------------------------------------------------------
    # Recovery: try to reclaim the primary model
    # ------------------------------------------------------------------

    def try_recover_primary(self) -> bool:
        """
        Attempt to switch back to the primary model.
        Called by the background recovery task in main.py.
        Returns True if recovery succeeded.
        """
        if self.active_model == self.primary_model and self.status in (STATUS_READY, STATUS_RATE_LIMITED):
            # Already on primary — nothing to do
            return True

        logger.info(f"[Recovery] Attempting to reclaim primary model: {self.primary_model}")
        result = self._probe_model(self.primary_model)
        if result["ok"] or result.get("code") == 429:
            prev_model = self.active_model
            self.active_model = self.primary_model
            self.status = STATUS_READY if result["ok"] else STATUS_RATE_LIMITED
            logger.info(f"[Recovery] ✅ Switched back to primary model '{self.primary_model}' (was '{prev_model}')")
            return True

        logger.info(f"[Recovery] Primary model still unavailable ({result.get('code')}). Staying on '{self.active_model}'.")
        return False

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _prepare_messages(
        self, prompt: str, system_prompt: str = None, history: List[Dict[str, str]] = None
    ) -> List[Dict[str, str]]:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if history:
            for message in history:
                messages.append({
                    "role": message.get("role", "user"),
                    "content": message.get("content", "")
                })
        messages.append({"role": "user", "content": prompt})
        return messages

    # ------------------------------------------------------------------
    # Generate (non-streaming)
    # ------------------------------------------------------------------

    def generate(
        self, prompt: str, system_prompt: str = None, history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        if self.status == STATUS_DEGRADED:
            return self._rule_based.generate(prompt, system_prompt, history)

        if not self.api_key:
            logger.warning("No OpenRouter API key provided. Falling back to RuleBasedLLM.")
            return self._rule_based.generate(prompt, system_prompt, history)

        messages = self._prepare_messages(prompt, system_prompt, history)
        max_retries = 3
        last_exception = None

        for attempt in range(max_retries):
            try:
                logger.info(f"OpenRouter generate attempt {attempt + 1} with model: {self.active_model}")
                response = self.client.chat.completions.create(
                    model=self.active_model,
                    messages=messages,
                    temperature=0.2,
                    timeout=15.0
                )
                return {
                    "answer": response.choices[0].message.content,
                    "confidence": 0.9
                }
            except Exception as e:
                logger.warning(f"OpenRouter generate attempt {attempt + 1} failed: {e}")
                last_exception = e
                time.sleep(1)

        # Per-request fallback to RuleBased (clean, no error prefix exposed to user)
        logger.error(f"OpenRouter generate failed after {max_retries} attempts: {last_exception}")
        return self._rule_based.generate(prompt, system_prompt, history)

    # ------------------------------------------------------------------
    # Generate (streaming)
    # ------------------------------------------------------------------

    def generate_stream(
        self, prompt: str, system_prompt: str = None, history: List[Dict[str, str]] = None
    ) -> Generator[str, None, None]:
        if self.status == STATUS_DEGRADED:
            yield from self._rule_based.generate_stream(prompt, system_prompt, history)
            return

        if not self.api_key:
            logger.warning("No OpenRouter API key provided. Falling back to RuleBasedLLM stream.")
            yield from self._rule_based.generate_stream(prompt, system_prompt, history)
            return

        messages = self._prepare_messages(prompt, system_prompt, history)
        max_retries = 3
        last_exception = None
        stream = None

        for attempt in range(max_retries):
            try:
                logger.info(f"OpenRouter generate_stream attempt {attempt + 1} with model: {self.active_model}")
                stream = self.client.chat.completions.create(
                    model=self.active_model,
                    messages=messages,
                    temperature=0.2,
                    timeout=15.0,
                    stream=True
                )
                break
            except Exception as e:
                logger.warning(f"OpenRouter generate_stream attempt {attempt + 1} failed: {e}")
                last_exception = e
                time.sleep(1)

        if stream:
            try:
                for chunk in stream:
                    if chunk.choices and chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
                return
            except Exception as e:
                logger.warning(f"Error during streaming: {e}")
                last_exception = e

        # Per-request fallback to RuleBased (clean, no error prefix exposed to user)
        logger.error(f"OpenRouter generate_stream failed: {last_exception}")
        yield from self._rule_based.generate_stream(prompt, system_prompt, history)


def get_llm_provider() -> LLMProvider:
    from backend.services.provider_factory import LLMProviderFactory
    return LLMProviderFactory.get_provider(settings.LLM_PROVIDER)
