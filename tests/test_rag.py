import json
from pathlib import Path
import unittest

import httpx

from emporio.config import Settings
from emporio.llm import LLMClient, ProviderError
from emporio.policies import PolicyIndex
from emporio.rag import PolicyRAG


class RetrievalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = PolicyIndex.from_pdf()

    def test_retrieves_expected_sections_for_reviewed_questions(self):
        cases = json.loads(Path(__file__).with_name("policy_questions.json").read_text(encoding="utf-8"))
        for case in cases:
            with self.subTest(question=case["question"]):
                sections = {hit.chunk.section for hit in self.index.search(case["question"])}
                self.assertTrue(set(case["sections"]) <= sections, (case, sections))

    def test_continuations_keep_section_and_actual_page(self):
        continuation = next(c for c in self.index.chunks if c.section == "5.2" and c.page == 5)
        self.assertIn("SEDEX", continuation.text)
        privacy = next(c for c in self.index.chunks if c.section == "9" and c.page == 8)
        self.assertIn("consentimento", privacy.text)
        # Passos 3, 4 e 5 do fluxo não viram títulos de seções.
        self.assertTrue(any(c.section == "7.2" and c.page == 7 for c in self.index.chunks))
        self.assertFalse(any(c.section in {"3", "4", "5"} and c.page == 7 for c in self.index.chunks))

    def test_unknown_question_and_empty_query_do_not_return_random_context(self):
        self.assertEqual(self.index.search("Vocês consertam saxofones?"), [])
        self.assertEqual(self.index.search(""), [])


class GenerationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = PolicyIndex.from_pdf()

    def test_generation_receives_selected_chunks_and_exports_provenance(self):
        def handle(request):
            payload = json.loads(request.content)
            context = payload["messages"][1]["content"]
            self.assertIn("PIX", context)
            self.assertIn("6.2 Regras de Promoções", context)
            self.assertNotIn("9. Privacidade", context)
            self.assertIn("PERGUNTA DO CLIENTE", context)
            return httpx.Response(200, json={"message": {
                "content": "O desconto PIX não se acumula com promoções. [P1]",
            }, "done": True})

        with LLMClient(Settings.from_env({}), transport=httpx.MockTransport(handle)) as client:
            answer = PolicyRAG(self.index, client).answer("Posso acumular promoção com PIX?")
        self.assertEqual(answer.cited_ids, ("P1",))
        self.assertEqual(answer.sources[0].chunk.section, "6.2")
        exported = answer.to_markdown()
        self.assertIn("politicas_da_loja.pdf", exported)
        self.assertIn("página 6", exported)
        self.assertIn("6.2-p6-1", exported)

    def test_no_hits_does_not_call_model(self):
        def fail(request):
            self.fail("Sem trecho relevante, o modelo não deve ser chamado.")
        with LLMClient(Settings.from_env({}), transport=httpx.MockTransport(fail)) as client:
            answer = PolicyRAG(self.index, client).answer("Vocês consertam saxofones?")
        self.assertFalse(answer.sources)
        self.assertIn("Não encontrei", answer.text)

    def test_missing_and_fabricated_source_ids_are_rejected(self):
        for text in ["Pode sim.", "Pode sim. [P999]"]:
            with self.subTest(text=text):
                with LLMClient(Settings.from_env({}), transport=httpx.MockTransport(
                    lambda request: httpx.Response(200, json={"message": {"content": text}, "done": True})
                )) as client:
                    with self.assertRaises(ProviderError):
                        PolicyRAG(self.index, client).answer("Posso acumular promoção com PIX?")


if __name__ == "__main__":
    unittest.main()
