"""Extração por seção/página e recuperação lexical BM25, sem embeddings."""

from collections import Counter
from dataclasses import dataclass
import math
from pathlib import Path
import re
import unicodedata

from pypdf import PdfReader


DEFAULT_PDF = Path(__file__).resolve().parents[1] / "data" / "politicas_da_loja.pdf"
STOPWORDS = set("a o as os um uma de da do das dos em no na nos nas e ou que com por para "
                "se ao aos como qual quais eu meu minha meus minhas posso pode podem quero "
                "voces voce tem ter ser sao esta estou foi quanto sobre preciso saber loja "
                "emporio musica produto produtos instrumento instrumentos cliente clientes".split())
# Vocabulário pequeno e revisável. Essas equivalências não são busca semântica.
GROUPS = [
    "horario horarios funcionamento abre abrem abrir aberto fecha fecham fechar expediente",
    "devolucao devolucoes devolver devolvi arrependi arrependimento desisti desistir",
    "troca trocas trocar",
    "pagamento pagamentos pagar pagam",
    "parcelamento parcelar parcela parcelas dividir divido vezes",
    "promocao promocoes promocional promocionais oferta ofertas",
    "acumular acumulam acumulativo cumulatividade cumulativas cumulativos juntar somar",
    "frete entrega entregas enviar envio envios",
    "defeito defeitos defeituoso quebrou quebrado",
    "garantia garantias",
    "endereco localizacao localizada fica onde",
    "privacidade dados lgpd pessoais",
]
CANONICAL = {word: group.split()[0] for group in GROUPS for word in group.split()}


def tokens(text: str) -> list[str]:
    text = unicodedata.normalize("NFKD", text.casefold())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return [CANONICAL.get(word, word) for word in re.findall(r"[a-z0-9]+", text)
            if len(word) > 1 and word not in STOPWORDS]


@dataclass(frozen=True)
class PolicyChunk:
    id: str
    section: str
    title: str
    page: int
    text: str
    source: str


@dataclass(frozen=True)
class PolicyHit:
    chunk: PolicyChunk
    score: float


def extract_chunks(path: Path = DEFAULT_PDF, max_chars: int = 1600) -> list[PolicyChunk]:
    chunks = []
    section = title = ""
    # Títulos estão alinhados à esquerda. Passos numerados do fluxo são indentados.
    heading = re.compile(r"^(\d+(?:\.\d+)?)\.?\s+([A-ZÁÀÂÃÉÊÍÓÔÕÚÇ].+)$")
    for page_number, page in enumerate(PdfReader(path).pages, 1):
        lines = []

        def flush():
            if not section or not lines:
                lines.clear()
                return
            # Preserva linhas de tabelas e agrupa blocos sem perder a origem.
            part = []
            size = 0
            for line in lines:
                if part and size + len(line) > max_chars:
                    append_chunk(part)
                    part, size = [], 0
                part.append(line)
                size += len(line) + 1
            if part:
                append_chunk(part)
            lines.clear()

        def append_chunk(part):
            ordinal = 1 + sum(c.section == section and c.page == page_number for c in chunks)
            chunks.append(PolicyChunk(
                f"{section}-p{page_number}-{ordinal}", section, title, page_number,
                "\n".join(part), path.name,
            ))

        for raw in (page.extract_text(extraction_mode="layout") or "").splitlines():
            line = re.sub(r"\s+", " ", raw).strip()
            if (not line or line == "Empório da Música Manual de Políticas e Procedimentos"
                    or re.fullmatch(r"Página \d+", line)):
                continue
            match = heading.match(raw)
            if match:
                flush()
                section, title = match.group(1), match.group(2).strip()
            else:
                lines.append(line)
        flush()  # Uma seção pode continuar na página seguinte.
    if not chunks:
        raise ValueError("Nenhuma seção extraída do manual de políticas.")
    return chunks


class PolicyIndex:
    def __init__(self, chunks: list[PolicyChunk]):
        if not chunks:
            raise ValueError("O índice de políticas está vazio.")
        self.chunks = chunks
        self.documents = [Counter(tokens(c.title + " " + c.title + " " + c.text)) for c in chunks]
        self.lengths = [sum(doc.values()) for doc in self.documents]
        self.average_length = sum(self.lengths) / len(chunks) or 1
        self.frequency = Counter(word for doc in self.documents for word in doc)

    @classmethod
    def from_pdf(cls, path: Path = DEFAULT_PDF):
        return cls(extract_chunks(path))

    def search(self, question: str, top_k: int = 4) -> list[PolicyHit]:
        if not 1 <= top_k <= 8:
            raise ValueError("top_k deve estar entre 1 e 8.")
        terms = set(tokens(question))
        count = len(self.chunks)
        hits = []
        # BM25: frequência do termo, raridade no corpus e ajuste por tamanho.
        k1, b = 1.5, 0.75
        for chunk, document, length in zip(self.chunks, self.documents, self.lengths):
            score = 0.0
            for term in terms:
                tf = document[term]
                if not tf:
                    continue
                df = self.frequency[term]
                idf = math.log(1 + (count - df + 0.5) / (df + 0.5))
                score += idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * length / self.average_length))
            if score > 0:
                hits.append(PolicyHit(chunk, round(score, 6)))
        return sorted(hits, key=lambda hit: (-hit.score, hit.chunk.page, hit.chunk.id))[:top_k]
