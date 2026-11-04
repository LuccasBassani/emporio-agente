# Execution and reading guide

Setup and provider selection are documented in the [README](../README.md). The recorded demonstration uses Gemini Flash-Lite. Groq is configurable; Ollama requires a local server/model and its generation has not been validated in this project.

## Demonstrate the service

1. Install dependencies, configure `.env` as described in the README, and start Streamlit.
2. Keep Lia's default persona. Ask for two acoustic guitars under R$ 1,000, then ask for the first one's PIX price. The interface and customer dialogue use Brazilian Portuguese.
3. Expand the queries/sources panel and compare the answer with tool results.
4. Select **test customer #2** and ask about **order 8**. A request for order 9, owned by another customer, must not reveal its data. Customer selection is a test mechanism, not real authentication.
5. Ask about a policy, such as paying R$ 480 in six installments. Inspect the retrieved PDF section.
6. Export the conversation before changing customer, applying configuration or starting another conversation; these actions clear session history.

The interface exports Markdown/TXT conversations and JSON configurations. Environment credentials are not exported configuration fields. [interface.png](interface.png) shows an answer flow.

## Inspect the project

- [Technical decisions](decisoes.md): queries, retrieval, context and providers.
- [Scenarios and acceptance criteria](cenarios-de-teste.md): expected behavior, separate from results.
- [Gemini evaluation](validacao-gemini-2026-11-03.md): 32 scenarios and revision-specific retests.
- [Five real examples](../examples/README.md): published exports with queries and sources.
- [Interaction examples and review](entrega.md): selected original dialogue and proposed improvements included in the PDF.
- [Generate the PDF](gerar-pdf.md): exporter instructions outside the submitted document.

The 61 automated tests mock API responses and do not consume quota. Real evaluation depends on the selected key, model and provider capacity. Execution errors, factual failures and language caveats must be recorded separately.

Dated records and the [development history](diario.md) document progress. Old counts and pending items describe the corresponding stage; the last functional fix was not followed by another complete run of all 32 scenarios. The [documentation index](README.md) separates current material from historical reports.
