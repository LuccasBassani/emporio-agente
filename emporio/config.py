"""Configuração explícita do provedor, sem carregar credenciais na importação."""

from dataclasses import dataclass, field
from collections.abc import Mapping
from urllib.parse import urlsplit
import math
import os


@dataclass(frozen=True)
class Settings:
    provider: str
    model: str
    base_url: str
    api_key: str = field(default="", repr=False)
    timeout: float = 120.0
    min_interval: float = 0.0

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> "Settings":
        values = os.environ if env is None else env
        provider = values.get("LLM_PROVIDER", "ollama").strip().lower()
        try:
            timeout = float(values.get("LLM_TIMEOUT_SECONDS", "120"))
        except ValueError:
            raise ValueError("LLM_TIMEOUT_SECONDS deve ser um número positivo.") from None
        if not math.isfinite(timeout) or timeout <= 0:
            raise ValueError("LLM_TIMEOUT_SECONDS deve ser um número positivo.")
        try:
            interval = float(values.get("LLM_MIN_INTERVAL_SECONDS", "0"))
        except ValueError:
            raise ValueError("LLM_MIN_INTERVAL_SECONDS deve estar entre 0 e 300.") from None
        if not math.isfinite(interval) or not 0 <= interval <= 300:
            raise ValueError("LLM_MIN_INTERVAL_SECONDS deve estar entre 0 e 300.")
        if provider == "groq":
            key = values.get("GROQ_API_KEY", "").strip()
            if not key:
                raise ValueError("Preencha GROQ_API_KEY no .env para usar a Groq.")
            model = values.get("GROQ_MODEL", "qwen/qwen3.8-27b").strip()
            url = "https://api.groq.com/openai/v1"
        elif provider == "ollama":
            key = ""  # A chave Groq nunca é enviada ao servidor Ollama.
            model = values.get("OLLAMA_MODEL", "qwen3:8b").strip()
            url = values.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434").strip().rstrip("/")
            try:
                parsed = urlsplit(url)
                parsed.port  # Valida também portas não numéricas ou fora da faixa.
            except ValueError:
                raise ValueError("OLLAMA_BASE_URL contém um endereço ou porta inválidos.") from None
            if (parsed.scheme not in {"http", "https"} or not parsed.hostname
                    or parsed.username or parsed.password or parsed.query or parsed.fragment
                    or parsed.path not in {"", "/"}):
                raise ValueError("OLLAMA_BASE_URL deve ser a origem do servidor, sem credenciais ou caminho.")
        else:
            raise ValueError("LLM_PROVIDER deve ser groq ou ollama.")
        if not model:
            raise ValueError("Informe o nome do modelo do provedor selecionado.")
        return cls(provider, model, url, key, timeout, interval)
