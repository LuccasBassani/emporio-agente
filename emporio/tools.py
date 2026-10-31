"""Lista fechada de ferramentas: valida parâmetros e devolve fontes explícitas."""

from dataclasses import dataclass

from emporio.catalog import Catalog
from emporio.policies import PolicyIndex


TOOLS = [
    {"type": "function", "function": {
        "name": "buscar_produtos",
        "description": "Busca catálogo por orçamento final sem frete. Só disponíveis por padrão. Ordena do menor preço. Categorias: 1 guitarras, 2 baixos, 3 baterias, 4 teclados/pianos, 5 violões, 6 sopro madeiras, 7 sopro metais, 8 cordas orquestrais, 9 ukuleles. Para tipos, prefira categoria_id; termo serve para marca/modelo.",
        "parameters": {"type": "object", "properties": {
            "termo": {"type": "string"}, "categoria_id": {"type": "integer", "minimum": 1, "maximum": 9},
            "preco_maximo": {"type": "number", "minimum": 0},
            "pagamento": {"type": "string", "enum": ["padrao", "pix"]},
            "somente_disponiveis": {"type": "boolean"},
            "cordas": {"type": "string", "enum": ["nylon", "aco"]},
            "eletrico": {"type": "boolean"},
            "limite": {"type": "integer", "minimum": 1, "maximum": 5},
        }, "required": [], "additionalProperties": False},
    }},
    {"type": "function", "function": {
        "name": "consultar_produto",
        "description": "Consulta um produto por ID, incluindo preço final e motivo da indisponibilidade. Use para atualizar preços e calcular PIX de um produto já identificado.",
        "parameters": {"type": "object", "properties": {
            "produto_id": {"type": "integer", "minimum": 1},
            "pagamento": {"type": "string", "enum": ["padrao", "pix"]},
        }, "required": ["produto_id"], "additionalProperties": False},
    }},
    {"type": "function", "function": {
        "name": "buscar_politicas",
        "description": "Recupera trechos do PDF para regras de pagamento, promoção, trocas, devoluções, garantia, horários, endereço e entregas. Não retorna estoque nem preço de produto.",
        "parameters": {"type": "object", "properties": {
            "pergunta": {"type": "string"},
        }, "required": ["pergunta"], "additionalProperties": False},
    }},
]


@dataclass(frozen=True)
class ToolResult:
    data: dict
    sources: tuple[dict, ...] = ()

    def for_model(self) -> dict:
        """Mantém a auditoria completa, mas não repete metadados de origem no prompt."""
        def compact_product(product):
            keep = {"encontrado", "produto_id", "nome", "categoria", "estoque", "disponivel",
                    "disponibilidade", "preco_tabela_brl", "preco_final_brl", "pagamento",
                    "desconto_percentual", "tipo_desconto", "promocao", "pix_acumulado",
                    "especificacoes_cadastradas"}
            result = {key: value for key, value in product.items() if key in keep}
            result["fontes"] = [source["id"] for source in product.get("fontes", [])]
            return result

        if "produtos" in self.data:
            return {**self.data, "produtos": [compact_product(p) for p in self.data["produtos"]]}
        if "produto_id" in self.data:
            return compact_product(self.data)
        return self.data


class StoreTools:
    def __init__(self, catalog: Catalog, policies: PolicyIndex):
        self.catalog = catalog
        self.policies = policies

    def execute(self, name: str, arguments: dict) -> ToolResult:
        """O nome vindo do modelo nunca é avaliado como código ou importação."""
        try:
            if name == "buscar_produtos":
                fields = {"termo": "query", "categoria_id": "category_id", "preco_maximo": "max_price",
                          "pagamento": "payment", "somente_disponiveis": "only_available",
                          "cordas": "strings", "eletrico": "electric", "limite": "limit"}
                if set(arguments) - fields.keys():
                    raise ValueError("Parâmetros desconhecidos na busca.")
                limit = arguments.get("limite", 3)
                if type(limit) is not int or not 1 <= limit <= 5:
                    raise ValueError("limite deve estar entre 1 e 5.")
                params = {fields[key]: value for key, value in arguments.items()}
                params["limit"] = limit
                data = self.catalog.search(**params)
                sources = tuple(source for product in data["produtos"] for source in product["fontes"])
                return ToolResult(data, sources)
            if name == "consultar_produto":
                if set(arguments) - {"produto_id", "pagamento"} or "produto_id" not in arguments:
                    raise ValueError("Informe produto_id e, opcionalmente, pagamento.")
                data = self.catalog.quote(arguments["produto_id"], arguments.get("pagamento", "padrao"))
                return ToolResult(data, tuple(data["fontes"]))
            if name == "buscar_politicas":
                if set(arguments) != {"pergunta"}:
                    raise ValueError("Informe somente pergunta para a busca de políticas.")
                question = arguments["pergunta"]
                if not isinstance(question, str) or not 1 <= len(question.strip()) <= 2000:
                    raise ValueError("A pergunta deve ter entre 1 e 2.000 caracteres.")
                sources, chunks = [], []
                for hit in self.policies.search(question):
                    c = hit.chunk
                    source = {"id": f"P{c.id}", "arquivo": c.source, "secao": c.section,
                              "titulo": c.title, "pagina": c.page}
                    sources.append(source)
                    chunks.append({**source, "texto": c.text})
                return ToolResult({"trechos": chunks, "encontrado": bool(chunks)}, tuple(sources))
            return ToolResult({"erro": "Ferramenta não permitida."})
        except (ValueError, TypeError, KeyError) as error:
            # Valores inválidos são devolvidos para permitir correção explícita pelo modelo.
            return ToolResult({"erro": str(error) if isinstance(error, ValueError)
                               else "Tipos ou parâmetros inválidos para a ferramenta."})
