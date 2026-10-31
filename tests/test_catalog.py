import csv
from decimal import Decimal
from pathlib import Path
import shutil
import tempfile
import unittest

from emporio.catalog import Catalog, DATA_DIR, money


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = Catalog()

    def test_budget_and_availability_match_raw_source(self):
        with (DATA_DIR / "products.csv").open(encoding="utf-8-sig", newline="") as stream:
            expected = {int(r["product_id"]) for r in csv.DictReader(stream)
                        if r["category_id"] == "5" and r["status"] == "active"
                        and int(r["stock_quantity"]) > 0 and Decimal(r["price_brl"]) <= 1000}
        first = self.catalog.search(category_id=5, max_price=1000, limit=10)
        self.assertEqual(first["total_encontrado"], len(expected))
        self.assertTrue(first["ha_mais_resultados"])
        self.assertTrue({p["produto_id"] for p in first["produtos"]} <= expected)
        self.assertEqual(len(first["produtos"]), 10)
        self.assertEqual(first["produtos"][0]["produto_id"], 83)

    def test_pix_rounds_to_cents_and_never_combines_with_promotion(self):
        self.assertEqual(self.catalog.quote(81, "pix")["preco_final_brl"], "569.91")
        normal = self.catalog.quote(121)
        pix = self.catalog.quote(121, "pix")
        self.assertEqual(normal["preco_tabela_brl"], "549.00")
        self.assertEqual(normal["preco_final_brl"], "439.20")
        self.assertEqual(pix["preco_final_brl"], "439.20")
        self.assertEqual(pix["promocao"]["id"], 14)
        self.assertFalse(pix["pix_acumulado"])
        self.assertEqual(money(Decimal("1.005")), "1.01")

    def test_inactive_promotions_do_not_change_price(self):
        self.assertEqual(self.catalog.quote(93)["preco_final_brl"], "11499.00")
        self.assertIsNone(self.catalog.quote(93)["promocao"])

    def test_stock_and_status_are_checked_together(self):
        for product_id, status in [(96, "sem_estoque"), (113, "descontinuado"),
                                   (130, "em_breve_sem_venda_atual"), (136, "descontinuado")]:
            with self.subTest(product_id=product_id):
                quote = self.catalog.quote(product_id)
                self.assertFalse(quote["disponivel"])
                self.assertEqual(quote["disponibilidade"], status)
        self.assertEqual(self.catalog.quote(136)["estoque"], 13)
        self.assertEqual(self.catalog.search(query="Ibanez Bass 2X")["total_encontrado"], 0)

    def test_budget_uses_selected_payment_and_exact_boundary(self):
        self.assertEqual(self.catalog.search(query="Yamaha C40", max_price="569.90", payment="pix")["total_encontrado"], 0)
        self.assertEqual(self.catalog.search(query="Yamaha C40", max_price="569.91", payment="pix")["total_encontrado"], 1)
        self.assertEqual(self.catalog.search(query="Ohana CK-20", max_price="440")["total_encontrado"], 1)

    def test_search_handles_accents_specs_and_missing_product(self):
        result = self.catalog.search(query="violão", category_id=5, strings="aco", electric=True)
        self.assertGreater(result["total_encontrado"], 0)
        for quote in result["produtos"]:
            self.assertEqual(quote["especificacoes_cadastradas"]["strings"], "steel")
            self.assertEqual(quote["especificacoes_cadastradas"]["electronics"], "yes")
        self.assertFalse(self.catalog.quote(999999)["encontrado"])
        self.assertEqual(self.catalog.search(category_id=6)["total_encontrado"], 0)

    def test_invalid_parameters_fail_explicitly(self):
        for args in [{"max_price": -1}, {"max_price": "NaN"}, {"max_price": True},
                     {"category_id": True}, {"category_id": 99}, {"limit": 0},
                     {"only_available": "true"}, {"strings": "metal"}, {"payment": "boleto"}]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                self.catalog.search(**args)

    def test_two_active_promotions_fail_instead_of_choosing_arbitrarily(self):
        with tempfile.TemporaryDirectory() as folder:
            directory = Path(folder)
            for filename in ["products.csv", "categories.csv", "promotions.csv"]:
                shutil.copyfile(DATA_DIR / filename, directory / filename)
            target = directory / "promotions.csv"
            with target.open(encoding="utf-8-sig", newline="") as stream:
                rows = list(csv.reader(stream))
            with target.open("w", encoding="utf-8", newline="") as stream:
                csv.writer(stream).writerows(rows + [[26, 121, 10, "Outra promoção", 1]])
            with self.assertRaisesRegex(ValueError, "Mais de uma promoção ativa"):
                Catalog(directory)


if __name__ == "__main__":
    unittest.main()
