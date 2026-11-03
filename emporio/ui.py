"""Configuração e chat local. Cada sessão mantém seu próprio cliente e histórico."""

import os
import re
from pathlib import Path

from dotenv import load_dotenv
import streamlit as st

from emporio.agent import StoreAgent
from emporio.catalog import Catalog
from emporio.config import Settings
from emporio.llm import LLMClient, ProviderError
from emporio.orders import Orders
from emporio.policies import PolicyIndex
from emporio.profile import DemoConfig, TONES
from emporio.tools import StoreTools


def display_text(text):
    return re.sub(r"(?<!\\)\$", lambda _: r"\$", text)


@st.cache_resource(show_spinner="Lendo catálogo e políticas…")
def load_data():
    catalog = Catalog()
    return catalog, PolicyIndex.from_pdf(), Orders(catalog)


def clear_conversation():
    previous = st.session_state.get("agent")
    if previous:
        previous.client.close()
    st.session_state.agent = None
    st.session_state.failed_question = None
    st.session_state.last_error = None
    st.session_state.conversation_signature = None


def make_agent(config, customer_id, data):
    environment = {**os.environ, "LLM_PROVIDER": config.provider,
                   "GROQ_MODEL": config.groq_model, "OLLAMA_MODEL": config.ollama_model}
    settings = Settings.from_env(environment)
    catalog, policies, orders = data
    return StoreAgent(LLMClient(settings), StoreTools(catalog, policies, orders, customer_id), config)


def render_app():
    st.set_page_config(page_title="Empório da Música · Assistente", page_icon="🎵", layout="wide")
    load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=False)
    if "active_config" not in st.session_state:
        st.session_state.active_config = DemoConfig(
            provider=os.getenv("LLM_PROVIDER", "ollama"),
            groq_model=os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b"),
            ollama_model=os.getenv("OLLAMA_MODEL", "qwen3:8b"),
        )
        st.session_state.form_revision = 0
        clear_conversation()
    config = st.session_state.active_config
    st.title("Empório da Música")
    st.caption("A Lia já vem configurada para atender. Experimente o chat ou personalize o atendimento.")
    try:
        data = load_data()
    except (OSError, ValueError):
        st.error("Não foi possível carregar os arquivos da pasta data. Confira o catálogo e o manual.")
        st.stop()

    settings_column, chat_column = st.columns([1, 2], gap="large")
    with settings_column:
        st.subheader("Configuração do agente")
        revision = st.session_state.form_revision
        with st.form("agent_configuration"):
            name = st.text_input("Nome do assistente", config.name, max_chars=40, key=f"name_{revision}")
            tone = st.selectbox("Tom de voz", TONES, index=TONES.index(config.tone), key=f"tone_{revision}")
            instructions = st.text_area("Instruções adicionais", config.instructions, max_chars=1200,
                                        placeholder="Ex.: prefira respostas curtas e evite emojis.", key=f"instructions_{revision}")
            provider = st.selectbox("Onde executar a IA", ["groq", "ollama"],
                                    index=["groq", "ollama"].index(config.provider),
                                    format_func=lambda p: "Groq · API" if p == "groq" else "Ollama · local",
                                    key=f"provider_{revision}")
            groq_model = st.text_input("Modelo da Groq", config.groq_model, key=f"groq_model_{revision}")
            ollama_model = st.text_input("Modelo do Ollama", config.ollama_model, key=f"ollama_model_{revision}")
            apply = st.form_submit_button("Aplicar e iniciar nova conversa", type="primary")
        if apply:
            try:
                new_config = DemoConfig(provider, groq_model.strip(), ollama_model.strip(),
                                        name.strip(), tone, instructions.strip())
            except ValueError as error:
                st.error(str(error))
            else:
                st.session_state.active_config = new_config
                clear_conversation()
                st.rerun()
        st.caption("As preferências de estilo mantêm as regras de consulta, descontos e acesso a pedidos.")
        st.download_button("Baixar configuração JSON", config.to_json(), "configuracao-agente.json",
                           "application/json", on_click="ignore")
        with st.expander("Importar configuração"):
            uploaded = st.file_uploader("Arquivo JSON exportado", type=["json"], key="config_upload")
            if st.button("Carregar configuração", disabled=uploaded is None):
                try:
                    imported = DemoConfig.from_json(uploaded.getvalue())
                except ValueError as error:
                    st.error(str(error))
                else:
                    st.session_state.active_config = imported
                    st.session_state.form_revision += 1
                    clear_conversation()
                    st.rerun()
        st.caption("A chave da Groq é lida do .env local e não faz parte da configuração exportada.")

    with chat_column:
        st.subheader("Teste de atendimento")
        customer_id = st.selectbox("Cliente de teste", [None, *sorted(data[2].customer_ids)],
                                   format_func=lambda i: "Sem identificação · catálogo e políticas" if i is None else f"Cliente #{i}",
                                   key="customer_id")
        signature = (config.to_json(), customer_id)
        if st.session_state.conversation_signature != signature:
            clear_conversation()
            st.session_state.conversation_signature = signature
        st.caption("Trocar o cliente inicia uma conversa nova. A seleção simula a identificação neste protótipo.")
        if st.button("Nova conversa", key="new_conversation"):
            clear_conversation()
            st.rerun()
        model = config.groq_model if config.provider == "groq" else config.ollama_model
        st.caption(f"{config.name} · {config.provider} · {model}")

        agent = st.session_state.agent
        if not agent or not agent.turns:
            with st.container(border=True):
                st.markdown("**Como posso ajudar?**")
                st.write("Experimente buscar violões até R$ 1.000, perguntar sobre uma devolução ou consultar um pedido.")
        if agent:
            for turn in agent.turns:
                with st.chat_message("user"):
                    st.markdown(display_text(turn.question))
                with st.chat_message("assistant"):
                    st.caption(config.name)
                    # Evita que dois símbolos R$ sejam interpretados como fórmula LaTeX.
                    st.markdown(display_text(turn.text))
                    with st.expander("Ver consultas e fontes"):
                        st.json({"consultas": turn.queries, "fontes_citadas": turn.sources})

        retry = False
        if st.session_state.failed_question:
            with st.chat_message("user"):
                st.markdown(display_text(st.session_state.failed_question))
            st.error(st.session_state.last_error)
            retry = st.button("Tentar novamente", key="retry_question")
        question = st.chat_input("Escreva uma mensagem para o assistente", max_chars=2000)
        if retry:
            question = st.session_state.failed_question
        if question:
            try:
                if agent is None:
                    agent = make_agent(config, customer_id, data)
                    st.session_state.agent = agent
                with st.spinner("Consultando as informações…"):
                    agent.respond(question)
            except (ValueError, ProviderError) as error:
                st.session_state.failed_question = question
                st.session_state.last_error = str(error)
            else:
                st.session_state.failed_question = None
                st.session_state.last_error = None
            st.rerun()

        st.divider()
        include_evidence = st.checkbox("Incluir consultas e fontes na exportação", value=True)
        markdown = agent.to_markdown(include_evidence) if agent else ""
        plain_text = agent.to_text(include_evidence) if agent else ""
        md_column, txt_column = st.columns(2)
        with md_column:
            st.download_button("Baixar conversa Markdown", markdown, "conversa.md", "text/markdown",
                               disabled=not bool(agent and agent.turns), on_click="ignore")
        with txt_column:
            st.download_button("Baixar conversa TXT", plain_text, "conversa.txt", "text/plain",
                               disabled=not bool(agent and agent.turns), on_click="ignore")
