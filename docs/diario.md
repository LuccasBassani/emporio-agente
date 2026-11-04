# Development history

A concise record of completed stages. Test counts and pending items belong to their stated stage. The [README](../README.md) and [Gemini evaluation](validacao-gemini-2026-11-03.md) describe the submission version. Full changes remain in Git history.

## Direction and AI assistance

I directed the interface reference, persona, scope, providers and cost constraints. I also guided tests and expected outcomes, reviewed answers, prioritized fixes and simplified approaches that were disproportionate to the challenge. Codex supported implementation, automation, execution and documentation. Reports identify assisted execution and review criteria.

## 31 October 2026 - Scope, data and first implementation

- Read the challenge, six CSVs and manual. Identified 65 products, nine categories, 50 customers, 20 orders and 25 promotions, four active.
- Defined an independent Python application inspired by an agent-configuration/service-simulation experience. Prioritized free options and incremental development.
- Created the repository, environment configuration and Groq/Ollama connectors. The initial suite had seven configuration/protocol tests; Ollama was not validated with an installed model.
- Implemented lexical RAG over 27 passages and 14 retrieval questions. The suite reached 13 tests. Real Groq requests checked greeting and tool round-trip behavior.
- The first real return-policy answer confirmed a return before asking when the item was received. Triage instructions were adjusted and the scenario repeated; the new answer asked for the missing information.
- Implemented catalog/pricing with `Decimal`, five service tools, two-turn context and exports. A catalog follow-up initially hit quota; another session completed the PIX query.
- Added customer-scoped orders and Streamlit. The suite reached 42 tests. A second environment installation was checked at that stage; browser checks covered messages, imports and downloads.

## 2 November 2026 - Persona, evaluation and fixes

- Consolidated Lia's default persona and 32 scenarios with expected outcomes.
- The assisted browser run with Groq/Qwen recorded nine passes, ten passes with caveats, 12 failures and one quota block. Answers were retained as evidence of that revision.
- The audit identified conflicting descriptions, commercial statuses incompatible with immediate purchase, and policy ambiguities. Separate notes were added to queries while preserving original data.
- Fixed unavailable-model lookup, empty-budget handling, triage instructions, recommendation limits and currency rendering. The suite reached 54 tests.
- Targeted revalidation attempted 18 scenarios: 15 met their main objective, four with caveats; three remained pending at that stage. Daily quota interruption and an unexplained HTTP 400 were recorded separately from content failures.

## 3 November 2026 - Resumption and alternative provider

- The first complete-run attempt finished C14 and part of C03 before another quota interruption.
- Qwen resumption completed 24 cases: 14 passes, nine passes with caveats and one campaign failure. C25 was interrupted; C26-C32 did not start.
- Explicit Gemini selection retained the agent/tools. Flash 3.6 completed eight cases before the observed daily limit; Flash-Lite enabled the full 32-scenario run. These runs are not a controlled model benchmark.

## 3 November 2026 - Gemini evaluation and submission version

- The full Flash-Lite run had 12 passes, 15 passes with caveats and five failures. Execution used Streamlit AppTest and the real API, with assisted review of answers, queries and sources.
- Nine cases were repeated after changes. Missing identification/not-found order states received deterministic guidance; instructions clarified commercial status, previously supplied channel and service scope.
- A regression added an unsupported shipping qualification to a historical order total. Conservative validation and a regression test were added; the real-API rerun returned correct data with a language caveat.
- The suite reached 61 tests. The five original failures met their main objective in retests, with caveats in two. There was no full rerun after the last functional change.
- Selected five real conversations. Consolidated the README/PDF with the candidate's direction, Codex assistance and evaluation limits; historical records were excluded from the six-page PDF.
- Prepared English submission documentation as required by the application email. Original Portuguese dialogue and supplied data were preserved; this language revision did not add new real-model evaluations.
