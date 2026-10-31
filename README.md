# Agente de atendimento — Empório da Música

Protótipo do desafio técnico de AI Engineer da Artefact.

## Situação atual

Desenvolvimento iniciado em 31/10/2026. Ambiente Python, dados e conectores Groq/Ollama implementados, com diagnóstico por terminal. O agente de atendimento, as consultas de negócio e a interface ainda estão pendentes.
Entrega informada pelo candidato: terça-feira, 03/11/2026 às 23h59. Planejamento em America/Sao_Paulo, sujeito ao fuso indicado no e-mail.

## Escopo proposto para a primeira versão

- Aplicação local em Python com interface Streamlit.
- Configuração de nome, tom e instruções adicionais do agente.
- Chat com histórico da sessão e botão para começar outra conversa.
- Consulta de catálogo, disponibilidade, preços, promoções e pedidos nos CSVs.
- Busca de trechos relevantes no PDF de políticas, com indicação da seção/página.
- Exportação da conversa em Markdown ou texto e da configuração em JSON.
- Visualização opcional das consultas e fontes usadas, sem expor raciocínio interno do modelo.

O agente é inspirado na experiência de configuração e simulação de atendimento de um projeto já desenvolvido. A implementação será independente, em Python, sem copiar código ou depender da infraestrutura do projeto de referência.

## Arquitetura proposta

Interface Streamlit -> agente Python -> ferramentas de consulta -> CSVs e políticas.
O agente usa uma API de modelo para escolher ferramentas e redigir respostas.
Filtros, cálculos de preço e validação dos parâmetros ficam no código Python.

Groq e Ollama são os provedores escolhidos. A seleção é explícita em `LLM_PROVIDER`, sem troca automática entre processamento local e externo.
Groq depende de chave e das cotas disponíveis na conta. Ollama depende do servidor local e do modelo baixado.
A chave fica em variável de ambiente ou `.env` local, fora do Git. Os modelos são configuráveis; a qualidade com modelos reais ainda não foi avaliada.

## Preparar e executar

Requer Python 3.11 ou superior. Ambiente verificado nesta etapa: Python 3.14.4 no Windows.
No PowerShell, a partir da pasta do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.lock.txt
Copy-Item .env.example .env
```

Copie o exemplo apenas na primeira configuração; preserve o `.env` se ele já contiver sua chave. Não é necessário ativar o ambiente virtual para usar os comandos abaixo.
`requirements.txt` declara as dependências diretas; `requirements.lock.txt` registra as versões instaladas nesta etapa, incluindo dependências transitivas.

### Usar Groq

Edite somente o `.env` local:

```dotenv
LLM_PROVIDER=groq
GROQ_API_KEY=sua_chave_pessoal
GROQ_MODEL=qwen/qwen3.8-27b
```

Crie sua chave na [conta Groq](https://console.groq.com/keys) e confira as cotas do plano gratuito antes dos testes. A disponibilidade do modelo também depende da conta. Não coloque a chave em mensagens, commits ou capturas de tela.

### Usar Ollama local

Instale o [Ollama](https://ollama.com/download/windows), deixe o servidor em execução e baixe o modelo:

```powershell
ollama pull qwen3:8b
```

Configure o `.env`:

```dotenv
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=qwen3:8b
```

Essa opção não exige chave Groq. A configuração acima usa o modelo no computador; não seleciona um modelo cloud. O download e o consumo de memória são requisitos adicionais para quem executar localmente.

### Verificar o provedor

```powershell
.\.venv\Scripts\python.exe -m emporio --check
.\.venv\Scripts\python.exe -m emporio --test-tools
```

`--check` faz uma chamada real de saudação. `--test-tools` verifica se o modelo solicita uma ferramenta de diagnóstico e usa seu resultado na resposta. Esse comando não testa catálogo ou políticas. Cada execução na Groq consome a cota da API.

Variáveis já definidas no processo têm prioridade sobre o `.env`. Rodar sem opções mostra a ajuda e não chama nenhum modelo.

### Testes sem modelo

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Os testes usam respostas HTTP simuladas para verificar os dois protocolos, retorno de ferramentas, configurações e falhas. Não precisam de internet, chave ou modelo instalado e não demonstram a qualidade do atendimento real.

## Organização atual

- `emporio/config.py`: leitura e validação das configurações.
- `emporio/llm.py`: requisições Groq/Ollama e normalização de texto e ferramentas.
- `emporio/__main__.py`: comandos de diagnóstico.
- `data/`: cópias dos seis CSVs e do manual fornecido, sem alterar os originais.
- `tests/`: testes de integração simulada dos conectores.
- `docs/`: decisões, guia e diário.

## Entrega planejada

- Código com instruções reproduzíveis de instalação e execução.
- Justificativas, suposições e limitações conhecidas.
- Entre 3 e 5 conversas reais de teste exportadas, incluindo aplicação de regras.
- Histórico de commits representando etapas reais do desenvolvimento.
- Declaração de uso de IA.

## Uso de IA até o momento

Codex foi usado para ler o enunciado, examinar os dados, consultar documentação oficial, analisar a referência de interface, preparar a documentação e implementar a camada inicial de configuração, conectores e testes. As escolhas de suporte a Groq e Ollama foram confirmadas durante o desenvolvimento. Os testes executados e as limitações estão registrados no diário.

## Documentação

- [Guia para acompanhar as etapas](docs/guia-do-projeto.md)
- [Decisões e questões em aberto](docs/decisoes.md)
- [Diário do desenvolvimento](docs/diario.md)

## Referências técnicas consultadas

- https://docs.streamlit.io/develop/api-reference/chat
- https://docs.streamlit.io/develop/api-reference/widgets/st.download_button
- https://console.groq.com/docs/openai
- https://console.groq.com/docs/tool-use/overview
- https://console.groq.com/docs/rate-limits
- https://docs.ollama.com/api/chat
- https://docs.ollama.com/capabilities/tool-calling
