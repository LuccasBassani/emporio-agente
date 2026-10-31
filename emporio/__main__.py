"""Teste explícito de conexão. Ainda não é o agente de atendimento."""

import argparse
import json
from pathlib import Path

from dotenv import load_dotenv

from emporio.config import Settings
from emporio.llm import LLMClient, ProviderError


def main() -> int:
    parser = argparse.ArgumentParser(description="Verifica o provedor de IA configurado.")
    parser.add_argument("--check", action="store_true", help="Faz uma chamada real ao modelo.")
    parser.add_argument("--test-tools", action="store_true", help="Testa chamada e retorno de uma ferramenta real de diagnóstico.")
    args = parser.parse_args()
    if not (args.check or args.test_tools):
        parser.print_help()
        return 0
    load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=False)
    try:
        settings = Settings.from_env()
        print(f"Provedor: {settings.provider} | Modelo: {settings.model}")
        messages = [{"role": "user", "content": "Responda em português com uma saudação curta."}]
        tools = None
        if args.test_tools:
            messages = [{"role": "user", "content": "Use a ferramenta obter_nome_loja e informe o nome retornado."}]
            tools = [{"type": "function", "function": {
                "name": "obter_nome_loja", "description": "Retorna o nome da loja para diagnóstico de integração.",
                "parameters": {"type": "object", "properties": {}, "required": [], "additionalProperties": False},
            }}]
        with LLMClient(settings) as client:
            reply = client.complete(messages, tools)
            if args.test_tools:
                if len(reply.tool_calls) != 1:
                    raise ProviderError("Diagnóstico falhou: o modelo não solicitou exatamente uma ferramenta.")
                call = reply.tool_calls[0]
                if call.name != "obter_nome_loja" or call.arguments:
                    raise ProviderError("Diagnóstico falhou: ferramenta ou parâmetros inesperados.")
                messages.extend([reply.as_message(), {
                    "role": "tool", "tool_call_id": call.id, "name": call.name,
                    "content": json.dumps({"nome": "Empório da Música"}, ensure_ascii=False),
                }])
                reply = client.complete(messages)
                if reply.tool_calls or "empório da música" not in reply.content.casefold():
                    raise ProviderError("Diagnóstico falhou: resposta não confirmou o resultado da ferramenta.")
                print("Chamada e retorno de ferramenta: OK")
            print(reply.content)
        return 0
    except (ValueError, ProviderError) as error:
        print(f"Erro: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
