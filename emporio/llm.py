"""Conectores Groq, Gemini e Ollama com uma resposta comum para o agente."""

from dataclasses import dataclass
import json
import time
from typing import Any

import httpx

from emporio.config import Settings


class ProviderError(RuntimeError):
    """Erro seguro para apresentar, sem copiar corpo HTTP ou credenciais."""


@dataclass(frozen=True)
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]
    extra_content: dict[str, Any] | None = None


@dataclass(frozen=True)
class Reply:
    content: str
    tool_calls: tuple[ToolCall, ...] = ()

    def as_message(self) -> dict:
        message = {"role": "assistant", "content": self.content}
        if self.tool_calls:
            message["tool_calls"] = [
                {"id": call.id, "type": "function", "function": {
                    "name": call.name,
                    "arguments": json.dumps(call.arguments, ensure_ascii=False),
                }, **({"extra_content": call.extra_content} if call.extra_content else {})}
                for call in self.tool_calls
            ]
        return message


class LLMClient:
    def __init__(self, settings: Settings, *, transport=None):
        self.settings = settings
        self._last_request_at = None
        # Sem retries ou fallback automáticos: cada chamada fica explícita.
        self.http = httpx.Client(
            timeout=settings.timeout, transport=transport, trust_env=False,
            follow_redirects=False,
        )

    def close(self):
        self.http.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def complete(self, messages: list[dict], tools: list[dict] | None = None) -> Reply:
        cfg = self.settings
        payload = {"model": cfg.model, "messages": messages, "stream": False}
        headers = {}
        if tools:
            payload["tools"] = tools
        if cfg.provider in {"groq", "gemini"}:
            endpoint = cfg.base_url + "/chat/completions"
            headers["Authorization"] = f"Bearer {cfg.api_key}"
            payload.update(temperature=0.2, max_tokens=1024)
            if cfg.provider == "gemini":
                payload["reasoning_effort"] = "low"
        else:
            endpoint = cfg.base_url + "/api/chat"
            payload["messages"] = [self._ollama_message(m) for m in messages]
            payload.update(think=False, options={
                "temperature": 0.2, "num_ctx": 8192, "num_predict": 1024,
            })
        try:
            if self._last_request_at is not None and cfg.min_interval:
                remaining = cfg.min_interval - (time.monotonic() - self._last_request_at)
                if remaining > 0:
                    time.sleep(remaining)
            self._last_request_at = time.monotonic()
            response = self.http.post(endpoint, json=payload, headers=headers)
        except httpx.TimeoutException:
            raise ProviderError("Tempo limite excedido. Tente novamente ou revise o modelo selecionado.") from None
        except httpx.RequestError:
            raise ProviderError(
                "Não foi possível conectar ao provedor. Verifique a rede ou se o Ollama está em execução."
            ) from None
        if response.status_code != 200:
            reason = {
                401: "Chave da API ausente ou inválida.",
                403: "Acesso ao modelo ou provedor não autorizado.",
                404: "Modelo ou endpoint não encontrado. Confira o nome e, no Ollama, o download do modelo.",
                429: "Limite de uso do provedor atingido. Aguarde a renovação da cota antes de tentar novamente.",
            }.get(response.status_code, f"O provedor retornou erro HTTP {response.status_code}.")
            raise ProviderError(reason)
        try:
            data = response.json()
            if cfg.provider in {"groq", "gemini"}:
                choice = data["choices"][0]
                if choice.get("finish_reason") in {"length", "content_filter"}:
                    raise ProviderError("A resposta do modelo foi interrompida; não será usada como resposta completa.")
                message = choice["message"]
            else:
                if not data.get("done") or data.get("done_reason") == "length":
                    raise ProviderError("A resposta do modelo foi interrompida; não será usada como resposta completa.")
                message = data["message"]
            content = message.get("content") or ""
            if not isinstance(content, str):
                raise ValueError()
            calls = []
            for index, call in enumerate(message.get("tool_calls") or []):
                function = call["function"]
                arguments = function["arguments"]
                if isinstance(arguments, str):
                    arguments = json.loads(arguments)
                if not isinstance(arguments, dict) or not isinstance(function["name"], str):
                    raise ValueError()
                call_id = call.get("id") or f"ollama_{index}"
                if cfg.provider in {"groq", "gemini"} and not call.get("id"):
                    raise ValueError()
                extra = call.get("extra_content") if cfg.provider == "gemini" else None
                if extra is not None and not isinstance(extra, dict):
                    raise ValueError()
                # Assinatura opaca retornada pelo Gemini: devolver intacta na chamada seguinte.
                calls.append(ToolCall(call_id, function["name"], arguments, extra))
            if not content.strip() and not calls:
                raise ValueError()
            return Reply(content, tuple(calls))
        except (ValueError, KeyError, TypeError, IndexError, AttributeError):
            raise ProviderError("Resposta inválida do provedor; nenhuma ferramenta foi executada.") from None

    @staticmethod
    def _ollama_message(message: dict) -> dict:
        """Ollama recebe argumentos como objeto; Groq e Gemini usam string JSON."""
        result = {k: v for k, v in message.items() if k not in {"tool_call_id", "name"}}
        if message.get("role") == "tool":
            result["tool_name"] = message["name"]
        if message.get("tool_calls"):
            result["tool_calls"] = [
                {"type": "function", "function": {
                    "name": call["function"]["name"],
                    "arguments": json.loads(call["function"]["arguments"]),
                }} for call in message["tool_calls"]
            ]
        return result
