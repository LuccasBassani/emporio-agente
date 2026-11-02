import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch

import httpx
from streamlit.testing.v1 import AppTest

from emporio.llm import LLMClient
from emporio.profile import DEFAULT_INSTRUCTIONS


APP = Path(__file__).resolve().parents[1] / "app.py"


class InterfaceTests(unittest.TestCase):
    def setUp(self):
        self.environment = patch.dict(os.environ, {"LLM_PROVIDER": "groq", "GROQ_API_KEY": "chave-ficticia"})
        self.environment.start()

    def tearDown(self):
        self.environment.stop()

    def app(self):
        app = AppTest.from_file(str(APP), default_timeout=20).run()
        self.assertFalse(app.exception)
        return app

    def test_initial_load_does_not_call_api_and_downloads_have_no_credentials(self):
        with patch("emporio.ui.LLMClient", side_effect=AssertionError("Não chamar IA ao abrir a página")):
            app = self.app()
        self.assertEqual(app.title[0].value, "Empório da Música")
        self.assertEqual(len(app.chat_input), 1)
        self.assertIsNone(app.session_state["agent"])
        self.assertEqual(app.text_area(key="instructions_0").value, DEFAULT_INSTRUCTIONS)
        self.assertEqual(app.session_state["active_config"].instructions, DEFAULT_INSTRUCTIONS)
        self.assertNotIn("chave-ficticia", app.session_state["active_config"].to_json())

    def test_chat_and_changing_customer_clear_history(self):
        def factory(settings):
            return LLMClient(settings, transport=httpx.MockTransport(lambda request:
                httpx.Response(200, json={"choices": [{"message": {"content": "Olá! Como posso ajudar?"}, "finish_reason": "stop"}]})))
        with patch("emporio.ui.LLMClient", side_effect=factory):
            app = self.app()
            app.chat_input[0].set_value("Oi!").run()
            self.assertFalse(app.exception)
            self.assertEqual(len(app.chat_message), 2)
            agent = app.session_state["agent"]
            self.assertEqual(len(agent.turns), 1)
            self.assertNotIn("chave-ficticia", agent.to_markdown())
            self.assertIn("Cliente: Oi!", agent.to_text())
            app.selectbox(key="customer_id").set_value(2).run()
            self.assertFalse(app.exception)
            self.assertIsNone(app.session_state["agent"])
            self.assertEqual(len(app.chat_message), 0)

    def test_apply_profile_changes_configuration_and_new_conversation_resets(self):
        app = self.app()
        app.text_input(key="name_0").set_value("Bia")
        app.text_area(key="instructions_0").set_value("Prefira respostas curtas.")
        submit = next(button for button in app.button if button.label == "Aplicar e iniciar nova conversa")
        submit.click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state["active_config"].name, "Bia")
        self.assertEqual(app.session_state["active_config"].instructions, "Prefira respostas curtas.")
        app.button(key="new_conversation").click().run()
        self.assertFalse(app.exception)
        self.assertIsNone(app.session_state["agent"])

    def test_rate_limit_can_be_retried_without_polluting_history(self):
        responses = [httpx.Response(429), httpx.Response(200, json={"choices": [{
            "message": {"content": "Olá!"}, "finish_reason": "stop",
        }]})]

        def factory(settings):
            return LLMClient(settings, transport=httpx.MockTransport(lambda request: responses.pop(0)))

        with patch("emporio.ui.LLMClient", side_effect=factory):
            app = self.app()
            app.chat_input[0].set_value("Oi!").run()
            self.assertFalse(app.exception)
            self.assertTrue(app.error)
            self.assertEqual(app.session_state["agent"].turns, [])
            app.button(key="retry_question").click().run()
            self.assertFalse(app.exception)
            self.assertFalse(app.error)
            self.assertEqual(len(app.session_state["agent"].turns), 1)


if __name__ == "__main__":
    unittest.main()
