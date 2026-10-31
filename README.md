# Agente de atendimento — Empório da Música

Protótipo do desafio técnico de AI Engineer da Artefact.

## Situação atual

Planejamento iniciado em 31/10/2026. Ainda não existe agente executável.
Entrega informada pelo candidato: terça-feira, 03/11/2026; horário a confirmar no e-mail.

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

DeepSeek é o provedor inicialmente considerado, sujeito à disponibilidade de chave e saldo.
A API oficial publica cobrança por tokens; não se pressupõe acesso gratuito.
A chave deve ficar em variável de ambiente local, fora do histórico e das exportações.

## Entrega planejada

- Código com instruções reproduzíveis de instalação e execução.
- Justificativas, suposições e limitações conhecidas.
- Entre 3 e 5 conversas reais de teste exportadas, incluindo aplicação de regras.
- Histórico de commits representando etapas reais do desenvolvimento.
- Declaração de uso de IA.

## Uso de IA até o momento

Codex foi usado para ler o enunciado, examinar os dados, consultar documentação oficial, analisar a referência de interface e propor este planejamento. Estes documentos iniciais foram redigidos com assistência de IA. As decisões propostas ainda precisam ser discutidas e validadas durante a implementação.

## Documentação

- [Decisões e questões em aberto](docs/decisoes.md)
- [Diário do desenvolvimento](docs/diario.md)

## Referências técnicas consultadas

- https://docs.streamlit.io/develop/api-reference/chat
- https://docs.streamlit.io/develop/api-reference/widgets/st.download_button
- https://api-docs.deepseek.com/quick_start/pricing/
- https://api-docs.deepseek.com/guides/tool_calls/
