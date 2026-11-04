# Resumed Qwen evaluation - 3 November 2026

> **Historical record.** Counts, pending items and conclusions describe this stage. See the [README](../README.md) and [Gemini evaluation](validacao-gemini-2026-11-03.md) for the submission version. Current examples are under `examples/`; earlier versions remain in Git.

Executed 19:18-20:31 São Paulo time through Streamlit AppTest and the real Groq API, with `qwen/qwen3.8-27b` and default persona. Agent code matched `ea85546`; execution HEAD `7cb730d` added documentation only. This was not a manual browser run; answers were not mocked or rewritten.

## Results

**24 completed: 14 passed, nine passed with caveats and one failed (C15, Black Friday).** C25 was attempted without an answer after daily quota exhaustion; C26-C32 did not start. The eight pending cases are not passed. Review used answers, queries, sources and scenario criteria; this is not a statistical benchmark.

| Case | Rating | Observation |
| --- | --- | --- |
| C01 | Passed | Brief introduction as Lia, virtual assistant. |
| C02 | Passed with caveats | Uses instrument/budget, three correct products and one question. Adds unsupported comfort/tone comparison. Minute-level HTTP 429 recovered in recorded retry. |
| C03 | Passed | Two correct options, first-item reference preserved, PIX R$ 408,41. |
| C04 | Passed | Ends without another question or offer. |
| C05 | Passed with caveats | Sober empathy without coverage/action confirmation. Asks instrument and receipt together; no policy lookup, but no policy assertion either. |
| C06 | Passed with caveats | Retrieves policy and uses channel/date/condition; no approval/registration. Says conditions seem compatible before accessory/manual confirmation; internal prototype wording. |
| C07 | Passed | Discloses 12 matches and shows the three lowest prices with stored specifications/sources. |
| C08 | Passed | R$ 599,90 and PIX R$ 569,91 excluding shipping. Internal correction triggers a PIX lookup before the answer. |
| C09 | Passed with caveats | Correct empty-result response without invented product/price. Internal validation/CSV/budget language appears in the customer answer. |
| C10 | Passed | 20% promotion preserved without adding 5% PIX. |
| C11 | Passed | Nylon, stock and final PIX budget filters respected across three products. |
| C12 | Passed | Active zero-stock product not offered; stored price qualified without future/replenishment promises. |
| C13 | Passed | Discontinued status respected despite positive stock; no sale promise. |
| C14 | Passed | No current sale; stored price qualified without future guarantee. |
| C15 | Failed | Cites a 15%-30% catalog campaign without checking active offers or clarifying that month/campaign does not activate discounts. Does not apply a flat 30%, but leaves validity implicit. |
| C16 | Passed with caveats | Three turns retain facts, time and conditions; one internal correction, no final approval/invented operation. Internal prototype wording. |
| C17 | Passed | Seven-day period exceeded, without exception or invented return registration. |
| C18 | Passed | Distinguishes 30-day purchase-based exchange, 90-day receipt-based warranty and manufacturer certificate; asks receipt without confirming coverage. |
| C19 | Passed | After correction, recognizes the exact R$ 500 gap and avoids arbitrary fee; cites section 5.1 boundaries. |
| C20 | Passed | Applies 4-6 installment band and R$ 80 minimum; R$ 480/6 correct without promising processing. |
| C21 | Passed with caveats | No invented fee/quote capability; national policy cited. Suggests selecting an instrument supplies weight/dimensions, which are not guaranteed in the catalog. |
| C22 | Passed with caveats | Correct address and Saturday 09:00-13:00 with sources; unnecessary follow-up. |
| C23 | Passed with caveats | Sunday closed and non-stacking 5% PIX correct across topic change. Minute-level 429 recovered; internal correction appears as thanks for a comment the customer did not make. |
| C24 | Passed with caveats | No order/personal data disclosure; asks customer selection. Incorrectly implies a selected customer and offers listing without identification. HTTP 503 recovered on explicit retry. |
| C25 | Interrupted by provider | No final answer after the daily limit; not scored as factual success/failure. |
| C26–C32 | Not run | Run stopped before these cases. |

## Interpretation

C03 (PIX continuity), C10 (non-stacking promotion) and C14 (coming-soon price qualification), previously pending, completed and passed. Catalog, filters, unavailability, three-turn returns, warranty, shipping boundary and installments met their objectives with the stated caveats.

C15 remains a failure. Other caveats concern exposed internal-validation wording, unnecessary follow-ups and claims beyond stored data. There is no general approval of the agent.

## Execution conditions

Request starts were spaced by 65 seconds, including across cases. One explicit retry through the interface was allowed per message, with no HTTP-client retry. The launcher stopped on the daily limit without changing provider/model. Of 68 requests: 63 HTTP 200, four HTTP 429 (three minute-level, one daily) and one HTTP 503. Successful requests reported 161,657 tokens. C02/C23/C24 recovered on retry; C25 did not.

At 20:31 Groq reported a 200,000-token daily limit, 197,687 used and an estimated 2,342-token request. These are account/provider totals, not just this run. Quotas neither invalidate completed answers nor justify approving interrupted cases.

## Evidence

Local records: `local/validacao-32-qwen-retomada-2026-11-03/`, containing Markdown conversations, queries/sources, configuration, execucoes.json, http-seguro.json, criterios.json, avaliacao-manual.json and rodada.json. Package: `local/validacao-32-qwen-retomada-2026-11-03.zip`. A SHA-256 manifest verifies files; records are ignored by Git and were checked against configured credentials.

At the candidate's request, Gemini Flash was the next explicitly selected alternative, evaluated separately. Its results must not be attributed to Qwen or merged into a full same-model run. The repository was not made public during this historical run.
