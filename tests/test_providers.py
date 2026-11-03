"""Contratos HTTP simulados: não precisam de chave, rede nem modelo instalado."""

import json
import unittest
from unittest.mock import patch

import httpx

from emporio.config import Settings
from emporio.llm import LLMClient, ProviderError


class SettingsTests(unittest.TestCase):
    def test_local_default_does_not_require_or_retain_groq_key(self):
        settings = Settings.from_env({"GROQ_API_KEY": "segredo-de-teste"})
        self.assertEqual(settings.provider, "ollama")
        self.assertEqual(settings.api_key, "")

    def test_groq_requires_key_and_does_not_expose_it_in_repr(self):
        with self.assertRaisesRegex(ValueError, "GROQ_API_KEY"):
            Settings.from_env({"LLM_PROVIDER": "groq"})
        settings = Settings.from_env({"LLM_PROVIDER": "groq", "GROQ_API_KEY": "segredo-de-teste"})
        self.assertNotIn("segredo-de-teste", repr(settings))

    def test_invalid_settings(self):
        for values in [
            {"LLM_PROVIDER": "outro"}, {"LLM_TIMEOUT_SECONDS": "nan"},
            {"LLM_TIMEOUT_SECONDS": "-1"}, {"OLLAMA_MODEL": " "},
            {"OLLAMA_BASE_URL": "http://usuario:senha@localhost:11434"},
            {"OLLAMA_BASE_URL": "http://localhost:11434/api/chat"},
            {"OLLAMA_BASE_URL": "http://localhost:porta"},
            {"LLM_MIN_INTERVAL_SECONDS": "nan"}, {"LLM_MIN_INTERVAL_SECONDS": "-1"},
        ]:
            with self.subTest(values=values), self.assertRaises(ValueError):
                Settings.from_env(values)


class ProviderTests(unittest.TestCase):
    def test_optional_pacing_spaces_requests_without_retrying(self):
        clock = [0.0]
        sent = []
        def handle(request):
            sent.append(clock[0])
            return httpx.Response(200, json={"message": {"content": "Olá"}, "done": True})
        settings = Settings.from_env({"LLM_MIN_INTERVAL_SECONDS": "65"})
        with patch("emporio.llm.time.monotonic", side_effect=lambda: clock[0]), \
             patch("emporio.llm.time.sleep", side_effect=lambda seconds: clock.__setitem__(0, clock[0] + seconds)), \
             LLMClient(settings, transport=httpx.MockTransport(handle)) as client:
            client.complete([{"role": "user", "content": "Oi"}])
            clock[0] = 5.0
            client.complete([{"role": "user", "content": "Oi"}])
        self.assertEqual(sent, [0.0, 65.0])

    def settings(self, provider):
        return Settings.from_env({"LLM_PROVIDER": provider, "GROQ_API_KEY": "segredo-de-teste"})

    def test_tool_roundtrip_for_both_providers(self):
        """Simula decisão -> execução externa -> resposta, conferindo os dois protocolos."""
        tools = [{"type": "function", "function": {
            "name": "buscar_produtos", "parameters": {"type": "object", "properties": {}},
        }}]
        for provider in ["groq", "ollama"]:
            with self.subTest(provider=provider):
                requests = []

                def handle(request):
                    body = json.loads(request.content)
                    requests.append(body)
                    if len(requests) == 1:
                        self.assertEqual(body["tools"], tools)
                    if provider == "groq":
                        self.assertEqual(request.url.host, "api.groq.com")
                        self.assertEqual(request.headers["authorization"], "Bearer segredo-de-teste")
                        self.assertEqual(request.url.path, "/openai/v1/chat/completions")
                    else:
                        self.assertEqual(request.url.host, "127.0.0.1")
                        self.assertNotIn("authorization", request.headers)
                        self.assertEqual(request.url.path, "/api/chat")
                        self.assertFalse(body["think"])
                    if len(requests) == 1:
                        args = {"orcamento": 1000}
                        call = {"function": {"name": "buscar_produtos", "arguments": args}}
                        if provider == "groq":
                            call.update(id="call_1", type="function")
                            call["function"]["arguments"] = json.dumps(args)
                        message = {"role": "assistant", "content": "", "tool_calls": [call]}
                    else:
                        history = body["messages"]
                        self.assertEqual(json.loads(history[-1]["content"])["nome"], "Violão de teste")
                        if provider == "ollama":
                            self.assertEqual(history[-1]["tool_name"], "buscar_produtos")
                            self.assertEqual(history[-2]["tool_calls"][0]["function"]["arguments"], {"orcamento": 1000})
                        else:
                            self.assertEqual(history[-1]["tool_call_id"], "call_1")
                        message = {"role": "assistant", "content": "Violão de teste por R$ 900."}
                    result = ({"choices": [{"message": message, "finish_reason": "stop"}]}
                              if provider == "groq" else {"message": message, "done": True})
                    return httpx.Response(200, json=result)

                with LLMClient(self.settings(provider), transport=httpx.MockTransport(handle)) as client:
                    history = [{"role": "user", "content": "Quero um violão até mil reais."}]
                    reply = client.complete(history, tools)
                    self.assertEqual(reply.tool_calls[0].arguments, {"orcamento": 1000})
                    call = reply.tool_calls[0]
                    history.extend([reply.as_message(), {
                        "role": "tool", "name": call.name, "tool_call_id": call.id,
                        "content": json.dumps({"nome": "Violão de teste", "preco": 900}),
                    }])
                    final = client.complete(history)
                    self.assertIn("R$ 900", final.content)
                    self.assertFalse(final.tool_calls)

    def test_errors_do_not_leak_provider_body_or_retry(self):
        for provider in ["groq", "ollama"]:
            for status in [401, 403, 404, 429, 500, 302]:
                calls = []

                def handle(request):
                    calls.append(request)
                    return httpx.Response(status, text="segredo-de-teste e conteúdo privado")

                with self.subTest(provider=provider, status=status):
                    with LLMClient(self.settings(provider), transport=httpx.MockTransport(handle)) as client:
                        with self.assertRaises(ProviderError) as error:
                            client.complete([])
                        self.assertNotIn("segredo-de-teste", str(error.exception))
                        self.assertNotIn("conteúdo privado", str(error.exception))
                        self.assertEqual(len(calls), 1)

    def test_malformed_and_truncated_responses_are_rejected(self):
        for body in [
            {}, {"choices": []}, {"choices": [{"message": {"content": ""}}]},
            {"choices": [{"message": {"content": "incompleta"}, "finish_reason": "length"}]},
            {"choices": [{"message": {"tool_calls": [{"id": "1", "function": {
                "name": "buscar", "arguments": "JSON inválido",
            }}]}}]},
        ]:
            with self.subTest(body=body):
                with LLMClient(self.settings("groq"), transport=httpx.MockTransport(
                    lambda request: httpx.Response(200, json=body)
                )) as client:
                    with self.assertRaises(ProviderError):
                        client.complete([])

    def test_connection_and_timeout_errors(self):
        for error_type in [httpx.ConnectError, httpx.ReadTimeout]:
            def handle(request):
                raise error_type("detalhes privados", request=request)
            with self.subTest(error=error_type):
                with LLMClient(self.settings("ollama"), transport=httpx.MockTransport(handle)) as client:
                    with self.assertRaises(ProviderError) as error:
                        client.complete([])
                    self.assertNotIn("detalhes privados", str(error.exception))


if __name__ == "__main__":
    unittest.main()
