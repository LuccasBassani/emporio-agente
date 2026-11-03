import unittest

from emporio.catalog import Catalog
from emporio.policies import PolicyIndex
from emporio.tools import StoreTools


class ObservationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = PolicyIndex.from_pdf()
        cls.tools = StoreTools(Catalog(), cls.index)

    def test_shipping_gap_note_does_not_change_original_chunk(self):
        result = self.tools.execute("buscar_politicas", {"pergunta": "frete Campo Grande R$ 500"})
        chunk = next(c for c in result.data["trechos"] if c["secao"] == "5.1")
        original = next(c for c in self.index.chunks if c.id == chunk["id"][1:])
        self.assertEqual(chunk["texto"], original.text)
        notes = result.data["notas_da_auditoria_nao_sao_texto_do_manual"]
        gap = next(n for n in notes if n["id"] == "frete-limite")
        self.assertIn("exatamente R$ 500", gap["observacao"])
        self.assertEqual(gap["arquivo"], "observacoes_dados.json")

    def test_unavailable_fallback_preserves_filter_and_exposes_existing_model(self):
        result = self.tools.execute("buscar_produtos", {"termo": "Giannini GF-3D"})
        self.assertEqual(result.data["total_encontrado"], 0)
        product = result.data["modelos_indisponiveis"][0]
        self.assertEqual(product["produto_id"], 96)
        self.assertEqual(product["disponibilidade"], "sem_estoque")
        self.assertIn("D96", [s["id"] for s in result.sources])
        self.assertFalse(result.for_model()["modelos_indisponiveis"][0]["disponivel"])

    def test_lookup_parameters_and_conflict_survive_model_compaction(self):
        invalid = self.tools.execute("consultar_produto", {"produto_id": 81, "termo": "Yamaha"})
        self.assertIn("erro", invalid.data)
        result = self.tools.execute("consultar_produto", {"termo": "Korg Synth 1"})
        self.assertEqual(result.data["produto_id"], 142)
        self.assertTrue(result.for_model()["divergencias_cadastrais"])

    def test_unavailable_price_qualification_reaches_model_without_changing_price(self):
        result = self.tools.execute("consultar_produto", {"termo": "Kala KA-ABP-CTG"})
        model = result.for_model()
        self.assertFalse(model["disponivel"])
        self.assertEqual(model["preco_final_brl"], "1749.00")
        self.assertIn("cadastrado atual", model["observacao"])
        self.assertIn("não garante preço futuro", model["observacao"])


if __name__ == "__main__":
    unittest.main()
