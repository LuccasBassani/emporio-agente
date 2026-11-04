"""Consultas locais, diagnósticos e agente de atendimento por terminal."""

import argparse
import json
from pathlib import Path

from dotenv import load_dotenv

from emporio.config import Settings
from emporio.llm import LLMClient, ProviderError
from emporio.policies import PolicyIndex
from emporio.rag import PolicyRAG
from emporio.catalog import Catalog
from emporio.tools import StoreTools
from emporio.agent import StoreAgent
from emporio.orders import Orders


def main() -> int:
    parser = argparse.ArgumentParser(description="Agente de atendimento: catálogo, políticas, pedidos e diagnósticos de IA.")
    commands = parser.add_mutually_exclusive_group()
    commands.add_argument("--check", action="store_true", help="Faz uma chamada real ao modelo.")
    commands.add_argument("--test-tools", action="store_true", help="Testa chamada e retorno de uma ferramenta real de diagnóstico.")
    commands.add_argument("--retrieve", metavar="PERGUNTA", help="Busca trechos no PDF sem chamar IA.")
    commands.add_argument("--ask", metavar="PERGUNTA", help="Recupera políticas e gera uma resposta com fontes.")
    commands.add_argument("--catalog", action="store_true", help="Consulta produtos localmente, sem IA.")
    commands.add_argument("--message", metavar="MENSAGEM", help="Envia uma mensagem ao agente com ferramentas.")
    commands.add_argument("--chat", action="store_true", help="Conversa com o agente no terminal; /sair encerra.")
    parser.add_argument("--query", default="", help="Marca/modelo para a consulta local de catálogo.")
    parser.add_argument("--category-id", type=int, help="Categoria da consulta local; 5 é violões.")
    parser.add_argument("--max-price", help="Orçamento máximo em reais para a consulta local.")
    parser.add_argument("--payment", choices=["padrao", "pix"], default="padrao")
    parser.add_argument("--limit", type=int, default=5, help="Limite de resultados na consulta local.")
    parser.add_argument("--customer-id", type=int, help="Cliente fictício para consultas de pedidos nesta sessão.")
    parser.add_argument("--show-sources", action="store_true", help="Exibe o texto completo dos trechos recuperados.")
    parser.add_argument("--export", type=Path, metavar="ARQUIVO.md", help="Exporta a conversa ou resposta de RAG, com consultas e fontes.")
    args = parser.parse_args()
    if args.export and not (args.ask or args.message or args.chat):
        parser.error("--export requer --ask, --message ou --chat")
    if not (args.check or args.test_tools or args.retrieve or args.ask or args.catalog or args.message or args.chat):
        parser.print_help()
        return 0
    load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=False)
    try:
        if args.catalog:
            result = Catalog().search(query=args.query, category_id=args.category_id,
                                      max_price=args.max_price, payment=args.payment, limit=args.limit)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
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
        if args.message or args.chat:
            with LLMClient(settings) as client:
                catalog = Catalog()
                agent = StoreAgent(client, StoreTools(catalog, PolicyIndex.from_pdf(), Orders(catalog), args.customer_id))

                def respond(text):
                    turn = agent.respond(text)
                    print("Agente: " + turn.text)
                    if args.show_sources:
                        print(json.dumps({"consultas": turn.queries, "fontes": turn.sources}, ensure_ascii=False, indent=2))

                if args.message:
                    respond(args.message)
                else:
                    print("Digite /sair para encerrar. Contexto: os dois últimos turnos completos.")
                    while True:
                        try:
                            text = input("Você: ").strip()
                        except (EOFError, KeyboardInterrupt):
                            print("\nConversa encerrada.")
                            break
                        if text.casefold() == "/sair":
                            break
                        if text:
                            try:
                                respond(text)
                            except (ValueError, ProviderError) as error:
                                print(f"Erro: {error}")
                if args.export:
                    args.export.parent.mkdir(parents=True, exist_ok=True)
                    args.export.write_text(agent.to_markdown(), encoding="utf-8")
                    print(f"Conversa exportada: {args.export}")
            return 0
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
