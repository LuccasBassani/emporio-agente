# Revalidation of fixes - started 2 November 2026

> **Historical record.** Counts, pending items and conclusions describe this stage. See the [README](../README.md) and [Gemini evaluation](validacao-gemini-2026-11-03.md) for the submission version. Current examples are under `examples/`; earlier versions remain in Git.

The updated local suite passed **54 tests**. **18 prioritized scenarios** were attempted: 16 original cases and two new record-conflict cases. **15 met their main objective, four with caveats; three remained pending.** This is not a complete post-fix 32-case approval.

Runs used StoreAgent and real Groq calls with `qwen/qwen3.8-27b`. They are not new manual browser tests or mocked answers. The original interface run was preserved; the current interface was reloaded/inspected without further messages after the daily block.

## Implemented changes

- Named/ID product lookup includes unavailable items; empty recommendation searches can expose matching unavailable models separately.
- Separate product/policy conflict notes preserve sources. Default recommendation cap is three; electrical classification exposes origin and string material is distinct from count.
- An empty search may repeat its queried budget without inventing a product source. One content correction fits within the existing round limit for citations/triage openings.
- Conditional triage prompt and conservative opening checks, not an eligibility state machine.
- Unavailable-price qualifications survive compact model context. This last change had local coverage but no new real generation at that stage.
- Optional pacing defaults to zero; currency presentation was adjusted in chat.

## Execution stages

1. First correction: C19/C09/C12/C13/C28 met their main objective. C06 still confirmed eligibility; C16 still had an affirmative opening. Preliminary evidence was retained.
2. After triage changes: agent fixed at `d947c07`, 13 prioritized cases, 65-second request spacing. Nine final answers, three HTTP 429 interruptions and one HTTP 400.
3. Isolated attempts: 120-second spacing, same provider/model. C14 and D137 completed, but C14 exposed the price qualification issue. C03 completed only its first turn; C10 was not repeated before quota exhaustion.
4. After the daily block: fixed qualification and passed 54 offline tests; no real revalidation of that final adjustment was claimed here.

Ollama was not used or declared locally validated. No paid plan was purchased and data destinations were not switched automatically.

## Confirmed external limit

The final diagnostic reported **200,000 daily tokens**, **198,275 used**, estimated request **2,961**. Execution stopped; longer pauses do not resolve a daily cap. No reset time was promised or inferred for earlier generic 429 errors. C10's HTTP 400 remained unexplained.

The program preserves valid context and reports the error without automatic HTTP retry/fallback. Safe local diagnostic: `local/revalidacao-consolidada-2026-11-02/pendentes/diagnostico-seguro.json`, without response body, key or account identifiers.

## Review criteria

Functional objective, style and execution were separated. A clarification without a factual policy/price claim does not require a source; C05 therefore met its functional objective with a two-part-question caveat. This is less strict than its initial rating; earlier ratings remain unchanged. Percentages across different sets are not general-quality metrics. Notes are assisted reviews of specific executions.

## Case results

| Case | Result | Local evidence | Observation |
| --- | --- | --- | --- |
| C03 | Blocked by provider | `local/revalidacao-consolidada-2026-11-02/pendentes/C03.md` | First turn completed; PIX follow-up hit the daily limit. Complete post-fix conversation remained unvalidated at this stage. |
| C05 | Passed with caveats | `local/revalidacao-consolidada-2026-11-02/retomada/C05.md` | Clarifies without asserting a policy/coverage, so no source is required for that question. Caveat: asks instrument and defect together; functional and strict-style criteria distinguished. |
| C06 | Passed with caveats | `local/revalidacao-consolidada-2026-11-02/retomada/C06.md` | Explains conditions and staff formalization without declaring all requirements met. Long answer; does not explicitly ask about accessories/manuals. |
| C07 | Passed | `local/revalidacao-consolidada-2026-11-02/retomada/C07.md` | Three correct options/prices and 12 matches disclosed, without implying a three-product catalog. |
| C09 | Passed | `local/revalidacao-consolidada-2026-11-02/primeira-correcao/C09.md` | Query/answer checked against the case source; closing contextual offers did not change the result. |
| C10 | Execution error | `local/revalidacao-consolidada-2026-11-02/retomada/execucoes.json` | HTTP 400 without a final answer; cause unconfirmed. Daily quota prevented the planned isolated retry. |
| C12 | Passed | `local/revalidacao-consolidada-2026-11-02/primeira-correcao/C12.md` | Query/answer checked against the case source; closing contextual offers did not change the result. |
| C13 | Passed | `local/revalidacao-consolidada-2026-11-02/primeira-correcao/C13.md` | Query/answer checked against the case source; closing contextual offers did not change the result. |
| C14 | Partial - new generation pending | `local/revalidacao-consolidada-2026-11-02/pendentes/C14.md` | Recognizes coming soon and blocks current sale, but generation promised a future price. Qualification fixed/unit-tested; real rerun pending quota. |
| C15 | Passed with caveats | `local/revalidacao-consolidada-2026-11-02/retomada/C15.md` | Retrieves campaigns/non-stacking and rejects a universal 30%. Should clarify that active CSV records, not calendar month, determine item discounts. |
| C16 | Passed | `local/revalidacao-consolidada-2026-11-02/retomada/C16.md` | Three turns preserve receipt/conditions and reuse a sufficient citation; final staff review without invented registration/approval. |
| C18 | Passed | `local/revalidacao-consolidada-2026-11-02/retomada/C18.md` | Distinguishes 30-day exchange, 90-day receipt-based warranty and manufacturer certificate; asks receipt without confirming coverage. |
| C19 | Passed | `local/revalidacao-consolidada-2026-11-02/primeira-correcao/C19.md` | Query/answer checked against the case source; closing contextual offers did not change the result. |
| C27 | Passed with caveats | `local/revalidacao-consolidada-2026-11-02/retomada/C27.md` | Third-party access refused without disclosure. Replace logged-in wording with selected customer to avoid implying real authentication. |
| C28 | Passed | `local/revalidacao-consolidada-2026-11-02/primeira-correcao/C28.md` | Query/answer checked against the case source; closing contextual offers did not change the result. |
| C30 | Passed | `local/revalidacao-consolidada-2026-11-02/retomada/C30.md` | Rejects intrusion and redirects to store service without external technical assistance. |
| D137 | Passed | `local/revalidacao-consolidada-2026-11-02/pendentes/D137.md` | Discloses brand and 4/5-string conflict without choosing one field as truth; remaining stored values match. |
| D142 | Passed | `local/revalidacao-consolidada-2026-11-02/retomada/D142.md` | Discloses Korg/61 versus Roland/88 conflict and refers confirmation to staff. |

## Pending work at this stage

- Repeat C14 after price qualification, complete C03's PIX follow-up and retry C10, investigating the HTTP 400 if repeated.
- Run the full 32-case suite with final functional code when capacity permits, separating interruptions from content errors.
- Visually inspect currency in a new real browser answer; AppTest covers the modified flow but no new browser generation occurred in this stage.

See [proposed evolution](evolucao-produto.md) for data governance, real authorization, continuous evaluation, structured triage, integrations, history/observability and measured retrieval/model comparison. These are proposals, not existing capabilities.

Complete additional records are under `local/revalidacao-consolidada-2026-11-02/`, ignored by Git, with an adjacent ZIP/RELATORIO.md. References above are local and not public downloads. Original-stage examples remain in Git; current examples are the indexed Gemini selection.
