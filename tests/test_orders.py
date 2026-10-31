import unittest

from emporio.catalog import Catalog
from emporio.orders import Orders
from emporio.policies import PolicyIndex
from emporio.tools import StoreTools


class OrderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = Catalog()
        cls.orders = Orders(cls.catalog)

    def test_owner_lookup_returns_only_approved_operational_fields(self):
        result = self.orders.lookup(2, 8)
        self.assertTrue(result["encontrado"])
        self.assertEqual(result["status"], "shipped")
        self.assertEqual(result["total_brl"], "349.90")
        self.assertEqual(result["itens"][0]["produto_id"], 120)
        self.assertEqual(result["rastreamento"], "BRJL5544332BR")
        for forbidden in ["owner", "customer_id", "email", "phone", "city", "order_date", "estimated_delivery", "notes"]:
            self.assertNotIn(forbidden, result)

    def test_unowned_and_missing_orders_have_identical_responses(self):
        self.assertEqual(self.orders.lookup(1, 8), self.orders.lookup(1, 999999))
        self.assertFalse(self.orders.lookup(1, 8)["encontrado"])

    def test_missing_tracking_is_not_filled_and_historical_total_is_preserved(self):
        self.assertIsNone(self.orders.lookup(6, 9)["rastreamento"])
        result = self.orders.lookup(12, 3)
        self.assertEqual(result["total_brl"], "3450.00")
        self.assertEqual(result["itens"][0]["quantidade"], 2)
        self.assertNotEqual(float(result["total_brl"]), 2 * float(self.catalog.quote(130)["preco_tabela_brl"]))

    def test_listing_does_not_include_other_customers(self):
        self.assertEqual({p["pedido_id"] for p in self.orders.list_for_customer(3)["pedidos"]}, {1, 19})
        self.assertEqual(self.orders.list_for_customer(50)["pedidos"], [])
        self.assertTrue(self.orders.list_for_customer(None)["identificacao_necessaria"])
        self.assertTrue(self.orders.lookup(None, 8)["identificacao_necessaria"])

    def test_tool_arguments_cannot_change_customer(self):
        tools = StoreTools(self.catalog, PolicyIndex.from_pdf(), self.orders, 1)
        spoofed = tools.execute("consultar_pedido", {"pedido_id": 8, "customer_id": 2})
        self.assertIn("erro", spoofed.data)
        self.assertFalse(tools.execute("consultar_pedido", {"pedido_id": 8}).data["encontrado"])
        with self.assertRaises(ValueError):
            StoreTools(self.catalog, PolicyIndex.from_pdf(), self.orders, True)


if __name__ == "__main__":
    unittest.main()
