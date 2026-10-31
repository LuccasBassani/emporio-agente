"""Pedidos restritos ao cliente de teste definido pela aplicação, não pelo modelo."""

import csv
from pathlib import Path

from emporio.catalog import Catalog, DATA_DIR, amount, money, positive_id


class Orders:
    def __init__(self, catalog: Catalog, directory: Path = DATA_DIR):
        def rows(filename):
            with (directory / filename).open(encoding="utf-8-sig", newline="") as stream:
                return list(csv.DictReader(stream))

        # Não guarda nomes, contatos, e-mails ou cidades para as ferramentas.
        self.customer_ids = {int(row["customer_id"]) for row in rows("customers.csv")}
        self.orders = {}
        for row in rows("orders.csv"):
            order_id, customer_id = int(row["order_id"]), int(row["customer_id"])
            if order_id in self.orders or customer_id not in self.customer_ids:
                raise ValueError("Pedido duplicado ou cliente inexistente na base.")
            if row["status"] not in {"pending", "confirmed", "shipped", "delivered", "cancelled"}:
                raise ValueError("Status de pedido desconhecido.")
            self.orders[order_id] = {
                "owner": customer_id, "pedido_id": order_id, "status": row["status"],
                "total_brl": money(amount(row["total_brl"])),
                "rastreamento": row["tracking_code"] or None, "itens": [],
            }
        for row in rows("order_items.csv"):
            order_id, product_id, quantity = int(row["order_id"]), int(row["product_id"]), int(row["quantity"])
            if order_id not in self.orders or product_id not in catalog.products or quantity < 1:
                raise ValueError("Item de pedido com vínculo ou quantidade inválidos.")
            self.orders[order_id]["itens"].append({
                "produto_id": product_id, "nome": catalog.products[product_id].name, "quantidade": quantity,
            })

    def validate_customer(self, customer_id: int | None):
        if customer_id is not None:
            positive_id(customer_id, "cliente de teste")
            if customer_id not in self.customer_ids:
                raise ValueError("Cliente de teste não encontrado.")

    def lookup(self, customer_id: int | None, order_id: int) -> dict:
        self.validate_customer(customer_id)
        positive_id(order_id, "pedido_id")
        if customer_id is None:
            return {"encontrado": False, "identificacao_necessaria": True, "fontes": []}
        order = self.orders.get(order_id)
        # Não diferencia pedido ausente de pedido pertencente a outro cliente.
        if order is None or order["owner"] != customer_id:
            return {"encontrado": False, "mensagem": "Pedido não localizado para o cliente selecionado.", "fontes": []}
        return {
            "encontrado": True, **{key: value for key, value in order.items() if key != "owner"},
            "observacao": "Dados cadastrados, sem rastreamento ao vivo. Total histórico preservado; data real de recebimento não informada.",
            "fontes": [{"id": f"O{order_id}", "arquivo": "orders.csv", "pedido_id": order_id,
                        "itens_origem": "order_items.csv", "nomes_origem": "products.csv"}],
        }

    def list_for_customer(self, customer_id: int | None) -> dict:
        self.validate_customer(customer_id)
        if customer_id is None:
            return {"identificacao_necessaria": True, "pedidos": [], "fontes": []}
        summaries, sources = [], []
        for order_id, order in sorted(self.orders.items()):
            if order["owner"] == customer_id:
                summaries.append({key: order[key] for key in ["pedido_id", "status", "total_brl"]})
                sources.append({"id": f"O{order_id}", "arquivo": "orders.csv", "pedido_id": order_id})
        return {"pedidos": summaries, "fontes": sources, "identificacao_necessaria": False}
