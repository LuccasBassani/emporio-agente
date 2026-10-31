"""Configuração exportável do agente. Credenciais nunca pertencem a este objeto."""

from dataclasses import asdict, dataclass
import json


TONES = ("Acolhedor e objetivo", "Informal e cordial", "Profissional e direto")


@dataclass(frozen=True)
class DemoConfig:
    provider: str = "groq"
    groq_model: str = "qwen/qwen3.8-27b"
    ollama_model: str = "qwen3:8b"
    name: str = "Lia"
    tone: str = TONES[0]
    instructions: str = ""

    def __post_init__(self):
        if self.provider not in {"groq", "ollama"} or self.tone not in TONES:
            raise ValueError("Provedor ou tom inválido.")
        for key, limit in [("name", 40), ("groq_model", 120), ("ollama_model", 120), ("instructions", 1200)]:
            value = getattr(self, key)
            if not isinstance(value, str) or len(value) > limit or (key != "instructions" and not value.strip()):
                raise ValueError(f"Configuração inválida no campo {key}.")

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, content: bytes | str):
        if len(content) > 20_000:
            raise ValueError("A configuração deve ter até 20 KB.")
        try:
            data = json.loads(content)
            if not isinstance(data, dict) or set(data) != set(cls.__dataclass_fields__):
                raise ValueError()
            return cls(**data)
        except (ValueError, TypeError, UnicodeError):
            raise ValueError("Configuração inválida. Importe um JSON exportado por esta aplicação, sem campos extras.") from None
