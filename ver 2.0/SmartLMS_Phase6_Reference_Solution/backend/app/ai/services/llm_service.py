import logging
import time

from flask import current_app
from openai import OpenAI, APIConnectionError, APIError, APITimeoutError, RateLimitError

from app.ai.exceptions import (
    AIConfigurationError,
    AIInvalidResponseError,
    AIProviderError,
    AIRateLimitError,
    AIRequestTimeoutError,
)

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self):
        provider = current_app.config.get("LLM_PROVIDER")
        if provider != "openai":
            raise AIConfigurationError("Unsupported LLM provider.")

        api_key = current_app.config.get("OPENAI_API_KEY")
        self.model = current_app.config.get("LLM_MODEL")
        self.embedding_model = current_app.config.get("EMBEDDING_MODEL")
        timeout = current_app.config.get("AI_REQUEST_TIMEOUT_SECONDS", 30)

        if not api_key:
            raise AIConfigurationError("OPENAI_API_KEY is not configured.")
        if not self.model:
            raise AIConfigurationError("LLM_MODEL is not configured.")
        if not self.embedding_model:
            raise AIConfigurationError("EMBEDDING_MODEL is not configured.")

        self.client = OpenAI(api_key=api_key, timeout=timeout)

    def generate_text(self, *, system_prompt, user_prompt, feature, user_id=None, course_id=None):
        started = time.perf_counter()
        try:
            response = self.client.responses.create(
                model=self.model,
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            text = response.output_text
            if not text or not text.strip():
                raise AIInvalidResponseError("AI provider returned an empty response.")

            latency = time.perf_counter() - started
            usage = getattr(response, "usage", None)
            input_tokens = getattr(usage, "input_tokens", None)
            output_tokens = getattr(usage, "output_tokens", None)

            logger.info(
                "AI_REQUEST feature=%s user_id=%s course_id=%s model=%s input_tokens=%s output_tokens=%s latency=%.3f status=success",
                feature, user_id, course_id, self.model, input_tokens, output_tokens, latency,
            )
            return text

        except RateLimitError as exc:
            self._log_failure(feature, user_id, course_id, started, "rate_limit")
            raise AIRateLimitError("AI provider rate limit reached.") from exc
        except APITimeoutError as exc:
            self._log_failure(feature, user_id, course_id, started, "timeout")
            raise AIRequestTimeoutError("AI provider request timed out.") from exc
        except (APIConnectionError, APIError) as exc:
            self._log_failure(feature, user_id, course_id, started, "provider_error")
            raise AIProviderError("AI provider request failed.") from exc

    def embed_texts(self, texts, *, feature="embedding", user_id=None, course_id=None):
        if not texts:
            return []

        started = time.perf_counter()
        try:
            response = self.client.embeddings.create(model=self.embedding_model, input=texts)
            embeddings = [item.embedding for item in sorted(response.data, key=lambda item: item.index)]
            latency = time.perf_counter() - started
            usage = getattr(response, "usage", None)
            input_tokens = getattr(usage, "prompt_tokens", None)

            logger.info(
                "AI_REQUEST feature=%s user_id=%s course_id=%s model=%s input_tokens=%s latency=%.3f status=success",
                feature, user_id, course_id, self.embedding_model, input_tokens, latency,
            )
            return embeddings

        except RateLimitError as exc:
            raise AIRateLimitError("Embedding provider rate limit reached.") from exc
        except APITimeoutError as exc:
            raise AIRequestTimeoutError("Embedding request timed out.") from exc
        except (APIConnectionError, APIError) as exc:
            raise AIProviderError("Embedding provider request failed.") from exc

    def embed_text(self, text, **kwargs):
        results = self.embed_texts([text], **kwargs)
        if not results:
            raise AIInvalidResponseError("Embedding provider returned no vector.")
        return results[0]

    @staticmethod
    def _log_failure(feature, user_id, course_id, started, status):
        latency = time.perf_counter() - started
        logger.warning(
            "AI_REQUEST feature=%s user_id=%s course_id=%s latency=%.3f status=%s",
            feature, user_id, course_id, latency, status,
        )
