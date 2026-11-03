"""Notas auditáveis separadas das fontes originais, sem respostas por cenário."""

from functools import lru_cache
import json
from pathlib import Path


OBSERVATIONS_FILE = Path(__file__).resolve().parents[1] / "data" / "observacoes_dados.json"


@lru_cache(maxsize=1)
def _load():
    return json.loads(OBSERVATIONS_FILE.read_text(encoding="utf-8"))


def product_observations(product_id: int) -> list[dict]:
    note = _load()["produtos"].get(str(product_id))
    if not note:
        return []
    return [{**note, "arquivo": OBSERVATIONS_FILE.name,
             "orientacao": "Se a divergência afetar a pergunta, informe o conflito e confirme com a equipe; não escolha um dos campos como verdade garantida."}]


def policy_observations(section: str) -> list[dict]:
    return [{**note, "arquivo": OBSERVATIONS_FILE.name}
            for note in _load()["politicas"] if section in note["secoes"]]
