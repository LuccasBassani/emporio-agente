# Technical decisions for the submission version

This document describes the current implementation. Dated records under `docs/` preserve earlier stages; the main evaluation is the [Gemini run and targeted retests](validacao-gemini-2026-11-03.md).

## Application and architecture

Python meets the challenge's language requirement. Streamlit keeps configuration, chat and exports in one application, reducing setup and integration work compared with a separate frontend. The candidate selected the experience reference; the implementation is independent.

The agent uses `httpx` without an agent framework. The model requests one of five allowed tools: `buscar_produtos`, `consultar_produto`, `buscar_politicas`, `consultar_pedido` and `listar_meus_pedidos`. Python validates arguments and runs the function; the provider API does not execute these functions itself.

Each turn allows up to four generation rounds and four tool calls per round. One content-correction opportunity fits within that limit. HTTP retries are separate and are not automatic. Only completed turns enter history; the previous two complete turns form model context. Session history and exports can contain more turns than this context window.

## Structured data and pricing

The six supplied CSVs remain unchanged in `data/`. Queries use an in-memory snapshot suited to the supplied volume. There is no SQL, vector product retrieval or live inventory integration.

- Availability: `status=active` and positive stock. Discontinued and coming-soon products remain unavailable despite positive quantities.
- Prices: `Decimal`, rounded to cents with `ROUND_HALF_UP`. Budget filtering uses the final price for the selected payment method, excluding shipping.
- Discounts: a promotion with `is_active=1` takes precedence; the 5% PIX discount applies only without an active promotion. Neither month nor campaign text activates an offer. Multiple active promotions for one product stop catalog loading until the ambiguity is resolved.
- Search: normalized name/category plus budget, availability, string material and electrical classification filters. Name/ID lookups include unavailable models. Conflicting free-text descriptions are excluded from product identification.

String material is filtered only in categories with that information. Electrical classification uses `specs.electronics` or explicit name/category evidence, with its origin exposed. Missing values are not treated as false.

`data/observacoes_dados.json` records conflicts and interpretations separately. Relevant notes accompany queries; they do not replace the manual or silently repair source records.

## Orders and identification

The application selects the test customer outside model-controlled arguments. Queries verify ownership and return the same outcome for nonexistent and another customer's orders. Changing the customer clears the conversation.

Order tools omit customer names, phone numbers, emails, addresses, notes and customer IDs. They preserve status, items, historical total and stored tracking. They do not infer actual receipt, shipping breakdown or live carrier location. A single order-tool call without identification or without an authorized match receives deterministic guidance from the program.

The selector is a demonstration, not real authentication. User-entered messages also reach the model; the minimization above concerns fields returned by the tools.

## Policy retrieval

The PDF produces 27 passages with section, page and ID. BM25 normalizes accents and explicit vocabulary equivalents. Titles receive extra weight; retrieval returns up to four passages by default. The small manual favored a local, inspectable approach.

There are no embeddings, reranking or vector database. The expected sections appear in the top four for the 14 reviewed retrieval questions; this does not cover every paraphrase. A positive score is not a relevance guarantee.

In chat, `buscar_politicas` supplies passages to the agent. The standalone `--ask` command uses `PolicyRAG`, without conversation memory and with sequential references such as `[P1]`. If retrieval returns no passages, that command responds without calling the model. Chat instead uses section/page IDs such as `[P3.1-p3-1]`.

Validation checks recognized IDs and selected content conditions. It does not compare every statement or amount with its source, or guarantee resistance to prompt injection. Triage and style remain partly generation-dependent.

## Providers and configuration

Gemini Flash-Lite (`gemini-3.5-flash-lite`) was selected after capacity limits in earlier runs. The choice used observed free-tier capacity and tool support, without a controlled superiority benchmark. Groq/Qwen remains supported; Ollama has mocked HTTP contract tests but no validated run with an installed local model.

Groq and Gemini use OpenAI-compatible chat; the adapter preserves Gemini's opaque tool-call signatures. Ollama uses its native API. Provider selection never changes automatically. Optional pacing is per HTTP client/session and does not coordinate quotas across users.

`.env.example` and environment configuration without an explicit selection default to Ollama. The README selects Gemini to reproduce the demonstration. The interface reads the environment and supports explicit changes; the internal `DemoConfig` default is Groq. Opening the interface does not call a model.

Keys are read from the environment/`.env`, outside Git. Exported JSON contains preferences and model names, without credentials or customer identity. The importer accepts legacy files without `gemini_model` and rejects unknown fields.

## Project direction, tests and limits

The candidate defined the interface reference, persona, scope, providers and cost constraints; guided scenarios and expected outcomes; reviewed answers; and prioritized fixes and simplifications. Codex supported implementation, automation, execution and documentation. Reports identify assisted execution and review criteria.

The suite has 61 local tests with mocked API responses. Real evaluations distinguish revisions, models, failures and retests. The five submission conversations are indexed in [examples/](../examples/README.md). [Proposed improvements](evolucao-produto.md) are not implemented features.
