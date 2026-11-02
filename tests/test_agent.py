import json
import unittest

import httpx

from emporio.agent import StoreAgent
from emporio.catalog import Catalog
from emporio.config import Settings
from emporio.llm import LLMClient, ProviderError
from emporio.policies import PolicyIndex
from emporio.tools import StoreTools
from emporio.profile import DemoConfig, DEFAULT_INSTRUCTIONS


def call(name, arguments):
    return {"content": "", "tool_calls": [{"id": "test_call", "type": "function", "function": {
        "name": name, "arguments": json.dumps(arguments),
    }}]}


class AgentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tools = StoreTools(Catalog(), PolicyIndex.from_pdf())

    def client(self, responses, requests=None):
        iterator = iter(responses)

        def handle(request):
            if requests is not None:
                requests.append(json.loads(request.content))
            return httpx.Response(200, json={"choices": [{"message": next(iterator), "finish_reason": "stop"}]})
        settings = Settings.from_env({"LLM_PROVIDER": "groq", "GROQ_API_KEY": "chave-ficticia"})
        return LLMClient(settings, transport=httpx.MockTransport(handle))

    def test_catalog_conversation_keeps_results_and_quotes_pix_without_model_arithmetic(self):
        requests = []
        responses = [
            call("buscar_produtos", {"categoria_id": 5, "preco_maximo": 1000, "limite": 2}),
            {"content": "1. Tagima AC-39: R$ 429,90 [D83]. 2. Rozini RC-104: R$ 459,90 [D85]."},
            call("consultar_produto", {"produto_id": 83, "pagamento": "pix"}),
            {"content": "O primeiro, Tagima AC-39, fica por R$ 408,41 no PIX [D83]."},
        ]
        with self.client(responses, requests) as client:
            agent = StoreAgent(client, self.tools)
            first = agent.respond("Quero dois violões disponíveis até mil reais.")
            second = agent.respond("E o primeiro no PIX?")
            self.assertEqual(first.queries[0]["resultado"]["produtos"][0]["produto_id"], 83)
            self.assertEqual(second.queries[0]["resultado"]["preco_final_brl"], "408.41")
            history = requests[2]["messages"]
            self.assertTrue(any(m.get("content") == first.text for m in history))
            self.assertEqual(second.sources[0]["id"], "D83")
            export = agent.to_markdown()
            self.assertIn("408.41", export)
            self.assertIn("consultar_produto", export)
            self.assertNotIn("chave-ficticia", export)

    def test_policy_tool_uses_real_retriever_and_requires_its_source(self):
        with self.client([
            call("buscar_politicas", {"pergunta": "Acumular promoção e PIX"}),
            {"content": "Não se acumulam [P6.2-p6-1]."},
        ]) as client:
            turn = StoreAgent(client, self.tools).respond("Acumula PIX e promoção?")
            self.assertEqual(turn.sources[0]["pagina"], 6)
            self.assertIn("trechos", turn.queries[0]["resultado"])

    def test_unavailable_item_keeps_reason_and_is_not_converted_to_in_stock(self):
        with self.client([
            call("consultar_produto", {"produto_id": 136}),
            {"content": "O produto está descontinuado [D136]."},
        ]) as client:
            turn = StoreAgent(client, self.tools).respond("Tem o Ibanez Bass 2X?")
            self.assertFalse(turn.queries[0]["resultado"]["disponivel"])

    def test_unknown_tools_and_invalid_parameters_are_not_executed(self):
        for name, arguments in [
            ("executar_codigo", {"codigo": "print('nao executar')"}),
            ("buscar_produtos", {"limite": 100}),
            ("consultar_produto", {"produto_id": True}),
            ("buscar_politicas", {"pergunta": "horários", "arquivo": ".env"}),
        ]:
            with self.subTest(name=name):
                result = self.tools.execute(name, arguments)
                self.assertIn("erro", result.data)
                self.assertFalse(result.sources)

    def test_failed_turn_does_not_pollute_history(self):
        for final in ["Está disponível [D999].", "Está disponível."]:
            with self.subTest(final=final):
                with self.client([call("consultar_produto", {"produto_id": 81}), {"content": final}]) as client:
                    agent = StoreAgent(client, self.tools)
                    with self.assertRaises(ProviderError):
                        agent.respond("Qual o preço do C40?")
                    self.assertEqual(agent.turns, [])
                    self.assertEqual(agent.sources, {})

    def test_values_without_source_and_endless_tool_loops_are_blocked(self):
        with self.client([{"content": "Custa R$ 500."}]) as client:
            with self.assertRaises(ProviderError):
                StoreAgent(client, self.tools).respond("Quanto custa?")
        responses = [call("consultar_produto", {"produto_id": 81})] * 4
        with self.client(responses) as client:
            agent = StoreAgent(client, self.tools)
            with self.assertRaisesRegex(ProviderError, "Limite de rodadas"):
                agent.respond("Quanto custa o C40?")
            self.assertFalse(agent.turns)

    def test_greeting_does_not_require_a_fabricated_source(self):
        requests = []
        with self.client([{"content": "Olá! O que procura hoje?"}], requests) as client:
            turn = StoreAgent(client, self.tools).respond("Oi!")
            self.assertFalse(turn.sources)
            self.assertFalse(turn.queries)
        prompt = requests[0]["messages"][0]["content"]
        self.assertIn(json.dumps(DEFAULT_INSTRUCTIONS, ensure_ascii=False), prompt)

    def test_context_limit_preserves_complete_tool_pairs(self):
        requests, responses = [], []
        for index in range(4):
            responses.extend([call("consultar_produto", {"produto_id": 81}),
                              {"content": f"Resposta do turno {index} [D81]."}])
        with self.client(responses, requests) as client:
            agent = StoreAgent(client, self.tools)
            for index in range(4):
                agent.respond(f"Pergunta {index}")
        fourth_turn = requests[6]["messages"]
        questions = [m["content"] for m in fourth_turn if m["role"] == "user"]
        self.assertEqual(questions, ["Pergunta 1", "Pergunta 2", "Pergunta 3"])
        self.assertEqual(sum(bool(m.get("tool_calls")) for m in fourth_turn), 2)
        self.assertEqual(sum(m["role"] == "tool" for m in fourth_turn), 2)

    def test_profile_reaches_model_while_fixed_rules_remain(self):
        requests = []
        profile = DemoConfig(name="Bia", instructions="Prefira respostas curtas.")
        with self.client([{"content": "Olá, sou a Bia!"}], requests) as client:
            agent = StoreAgent(client, self.tools, profile)
            agent.respond("Oi!")
            self.assertIn('"nome": "Bia"', requests[0]["messages"][0]["content"])
            self.assertIn("Prefira respostas curtas.", requests[0]["messages"][0]["content"])
            self.assertIn("Não calcule descontos mentalmente", requests[0]["messages"][0]["content"])
            self.assertNotIn("Consultas executadas", agent.to_markdown(False))
            self.assertNotIn("Fontes citadas", agent.to_markdown(False))
            self.assertNotIn("Consultas e fontes", agent.to_text(False))


if __name__ == "__main__":
    unittest.main()
