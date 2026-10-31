"""Teste explícito de conexão. Ainda não é o agente de atendimento."""

import argparse
import json
from pathlib import Path

from dotenv import load_dotenv

from emporio.config import Settings
from emporio.llm import LLMClient, ProviderError
from emporio.policies import PolicyIndex
from emporio.rag import PolicyRAG


def main() -> int:
    parser = argparse.ArgumentParser(description="Diagnóstico de IA e RAG das políticas da loja.")
    commands = parser.add_mutually_exclusive_group()
    commands.add_argument("--check", action="store_true", help="Faz uma chamada real ao modelo.")
    commands.add_argument("--test-tools", action="store_true", help="Testa chamada e retorno de uma ferramenta real de diagnóstico.")
    commands.add_argument("--retrieve", metavar="PERGUNTA", help="Busca trechos no PDF sem chamar IA.")
    commands.add_argument("--ask", metavar="PERGUNTA", help="Recupera políticas e gera uma resposta com fontes.")
    parser.add_argument("--show-sources", action="store_true", help="Exibe o texto completo dos trechos recuperados.")
    parser.add_argument("--export", type=Path, metavar="ARQUIVO.md", help="Exporta pergunta, resposta e trechos do teste de RAG.")
    args = parser.parse_args()
    if args.export and not args.ask:
        parser.error("--export requer --ask")
    if not (args.check or args.test_tools or args.retrieve or args.ask):
        parser.print_help()
        return 0
    load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=False)
    try:
        if args.retrieve:
            hits = PolicyIndex.from_pdf().search(args.retrieve)
            for index, hit in enumerate(hits, 1):
                print(f"[P{index}] {hit.chunk.section} {hit.chunk.title} | página {hit.chunk.page} | score {hit.score}")
                if args.show_sources:
                    print(hit.chunk.text + "\n")
            if not hits:
                print("Nenhum trecho encontrado.")
            return 0
        settings = Settings.from_env()
        print(f"Provedor: {settings.provider} | Modelo: {settings.model}")
        if args.ask:
            with LLMClient(settings) as client:
                answer = PolicyRAG(PolicyIndex.from_pdf(), client).answer(args.ask)
            print(answer.text)
            for index, hit in enumerate(answer.sources, 1):
                print(f"[P{index}] {hit.chunk.source} | seção {hit.chunk.section} | página {hit.chunk.page}")
                if args.show_sources:
                    print(hit.chunk.text + "\n")
            if args.export:
                args.export.parent.mkdir(parents=True, exist_ok=True)
                args.export.write_text(answer.to_markdown(settings.provider, settings.model), encoding="utf-8")
                print(f"Teste exportado: {args.export}")
            return 0
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
