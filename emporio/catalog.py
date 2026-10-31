"""Consultas determinísticas aos CSVs. Dinheiro é calculado com Decimal."""

from dataclasses import dataclass
import csv
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import json
from pathlib import Path
import re
import unicodedata


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
CENT = Decimal("0.01")
PIX_DISCOUNT = Decimal("5")  # Manual, seção 3. Não cumulativo: seção 6.2.


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.casefold())
    return re.sub(r"[^a-z0-9]+", " ", "".join(c for c in text if not unicodedata.combining(c))).strip()


def amount(value) -> Decimal:
    if isinstance(value, bool):
        raise ValueError("O valor monetário deve ser numérico e não negativo.")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError("O valor monetário deve ser numérico e não negativo.") from None
    if not result.is_finite() or not 0 <= result <= Decimal("1000000000"):
        raise ValueError("O valor monetário deve estar entre zero e um bilhão.")
    return result


def money(value: Decimal) -> str:
    return str(value.quantize(CENT, rounding=ROUND_HALF_UP))


def positive_id(value, name="ID") -> int:
    if type(value) is not int or value < 1:
        raise ValueError(f"{name} deve ser um inteiro positivo.")
    return value


@dataclass(frozen=True)
class Product:
    id: int
    name: str
    category_id: int
    price: Decimal
    stock: int
    status: str
    specs: dict

    @property
    def available(self) -> bool:
        return self.status == "active" and self.stock > 0


@dataclass(frozen=True)
class Promotion:
    id: int
    product_id: int
    percent: Decimal
    description: str


class Catalog:
    def __init__(self, directory: Path = DATA_DIR):
        def rows(filename):
            with (directory / filename).open(encoding="utf-8-sig", newline="") as stream:
                return list(csv.DictReader(stream))

        self.categories = {}
        for row in rows("categories.csv"):
            category_id = positive_id(int(row["category_id"]))
            if category_id in self.categories:
                raise ValueError("Categoria duplicada no catálogo.")
            self.categories[category_id] = row["name"]
        self.products = {}
        for row in rows("products.csv"):
            product = Product(
                positive_id(int(row["product_id"])), row["name"], int(row["category_id"]),
                amount(row["price_brl"]), int(row["stock_quantity"]), row["status"], json.loads(row["specs"]),
            )
            if (product.id in self.products or product.stock < 0
                    or product.category_id not in self.categories
                    or product.status not in {"active", "discontinued", "coming_soon"}
                    or not isinstance(product.specs, dict)):
                raise ValueError(f"Cadastro inválido ou duplicado no produto {product.id}.")
            self.products[product.id] = product
        self.promotions = {}
        for row in rows("promotions.csv"):
            if row["is_active"] not in {"0", "1"}:
                raise ValueError("Status de promoção inválido.")
            product_id = int(row["product_id"])
            percent = amount(row["discount_percent"])
            if product_id not in self.products or percent > 100:
                raise ValueError("Promoção referencia produto ausente ou percentual inválido.")
            if row["is_active"] == "1":
                if product_id in self.promotions:
                    raise ValueError("Mais de uma promoção ativa para o mesmo produto; confirme a regra antes de cotar.")
                self.promotions[product_id] = Promotion(
                    positive_id(int(row["promotion_id"])), product_id, percent, row["description"],
                )

    def quote(self, product_id: int, payment: str = "padrao") -> dict:
        positive_id(product_id, "product_id")
        if payment not in {"padrao", "pix"}:
            raise ValueError("pagamento deve ser padrao ou pix.")
        product = self.products.get(product_id)
        if product is None:
            return {"encontrado": False, "produto_id": product_id, "fontes": []}
        promotion = self.promotions.get(product_id)
        percent = promotion.percent if promotion else PIX_DISCOUNT if payment == "pix" else Decimal("0")
        final = product.price * (1 - percent / 100)
        availability = (
            "descontinuado" if product.status == "discontinued" else
            "em_breve_sem_venda_atual" if product.status == "coming_soon" else
            "disponivel" if product.available else "sem_estoque"
        )
        return {
            "encontrado": True, "produto_id": product.id, "nome": product.name,
            "categoria": self.categories[product.category_id], "categoria_id": product.category_id,
            "estoque": product.stock, "status_cadastrado": product.status,
            "disponivel": product.available, "disponibilidade": availability,
            "preco_tabela_brl": money(product.price), "preco_final_brl": money(final),
            "pagamento": payment, "desconto_percentual": str(percent),
            "tipo_desconto": "promocao" if promotion else "pix" if payment == "pix" else "nenhum",
            "promocao": ({"id": promotion.id, "descricao": promotion.description} if promotion else None),
            "pix_acumulado": False,
            "especificacoes_cadastradas": product.specs,
            "fontes": [{
                "id": f"D{product.id}", "arquivo": "products.csv", "produto_id": product.id,
                "promocao_id": promotion.id if promotion else None,
                "arquivo_promocoes": "promotions.csv",
                "regras_preco": "politicas_da_loja.pdf, seções 3 e 6.2",
            }],
            "observacao": "Preço sem frete. Indisponibilidade impede oferta de compra mesmo com preço cadastrado.",
        }

    def search(self, *, query: str = "", category_id: int | None = None,
               max_price=None, payment: str = "padrao", only_available: bool = True,
               strings: str | None = None, electric: bool | None = None, limit: int = 5) -> dict:
        if not isinstance(query, str) or len(query) > 200:
            raise ValueError("termo deve ser texto de até 200 caracteres.")
        if category_id is not None:
            positive_id(category_id, "categoria_id")
            if category_id not in self.categories:
                raise ValueError("Categoria não encontrada.")
        if type(only_available) is not bool or (electric is not None and type(electric) is not bool):
            raise ValueError("Filtros de disponibilidade e elétrico devem ser booleanos.")
        if type(limit) is not int or not 1 <= limit <= 10:
            raise ValueError("limite deve estar entre 1 e 10.")
        if strings not in {None, "nylon", "aco"} or payment not in {"padrao", "pix"}:
            raise ValueError("Filtro de cordas ou pagamento inválido.")
        budget = amount(max_price) if max_price is not None else None
        aliases = {"violao": "violoes", "ukulele": "ukuleles", "guitarra": "guitarras",
                   "baixo": "baixos", "bateria": "baterias", "teclado": "teclados", "piano": "pianos"}
        terms = [aliases.get(term, term) for term in normalize(query).split()]
        matches = []
        for product in self.products.values():
            if category_id is not None and product.category_id != category_id:
                continue
            if only_available and not product.available:
                continue
            if strings is not None and product.specs.get("strings") != {"aco": "steel", "nylon": "nylon"}[strings]:
                continue
            if electric is not None and product.specs.get("electronics") != ("yes" if electric else "no"):
                continue
            searchable = normalize(product.name + " " + self.categories[product.category_id])
            if not all(term in searchable for term in terms):
                continue
            quote = self.quote(product.id, payment)
            if budget is not None and Decimal(quote["preco_final_brl"]) > budget:
                continue
            matches.append(quote)
        matches.sort(key=lambda q: (Decimal(q["preco_final_brl"]), q["produto_id"]))
        return {
            "total_encontrado": len(matches), "retornados": len(matches[:limit]),
            "ha_mais_resultados": len(matches) > limit, "produtos": matches[:limit],
            "criterio_orcamento": "Preço final para o pagamento escolhido, com promoção ativa quando houver, sem frete.",
            "fonte": "CSVs fornecidos; não representa estoque em tempo real.",
        }
