import json
import unittest

from emporio.profile import DemoConfig


class ProfileTests(unittest.TestCase):
    def test_roundtrip_preserves_editable_configuration(self):
        profile = DemoConfig(provider="ollama", name="Bia", instructions="Prefira respostas breves.")
        self.assertEqual(DemoConfig.from_json(profile.to_json()), profile)

    def test_import_rejects_credential_and_unknown_fields(self):
        for key in ["api_key", "GROQ_API_KEY", "customer_id", "base_url"]:
            data = json.loads(DemoConfig().to_json())
            data[key] = "valor não permitido"
            with self.subTest(key=key), self.assertRaises(ValueError):
                DemoConfig.from_json(json.dumps(data))

    def test_invalid_or_oversized_inputs_are_rejected(self):
        for content in ["[1,2]", "{}", "não é JSON", " " * 20_001]:
            with self.subTest(content=content[:20]), self.assertRaises(ValueError):
                DemoConfig.from_json(content)
        with self.assertRaises(ValueError):
            DemoConfig(name="")
        with self.assertRaises(ValueError):
            DemoConfig(instructions="x" * 1201)


if __name__ == "__main__":
    unittest.main()
