# Gemini agent evaluation - 3 November 2026

## Method and revisions

Full evaluation of 32 scenarios using `gemini-3.5-flash-lite`, Lia's default persona and the real Google API. Executed from 20:53 to 21:22, São Paulo time, through Streamlit AppTest, using application controls and a new session per case. Turns within a scenario shared context. Customers #2, #6 and #12 were selected where specified.

Full-run code revision: `163ef3c`. Instrumentation spaced request starts by 20 seconds and recorded safe metadata. Responses were neither mocked nor manually rewritten. Codex-assisted review compared answers, queries and sources against the predefined criteria in `cenarios-de-teste.md`. Ratings cover functional objective, style and execution.

The candidate guided scenarios and expected outcomes, participated in answer review and prioritized fixes. Codex supported automation, execution and evidence review. Each result belongs to its stated revision; targeted retests do not replace the original full run.

## Full run

**32 cases attempted: 12 passed, 15 passed with caveats and five failed.** Thirty conversations completed; C24 and C27 ended in citation errors even after an additional button-triggered attempt. The other three failures returned answers with content or continuity problems.

All 86 requests returned HTTP 200 and reported 189,316 tokens. Flash-Lite had no quota interruption in this run. This describes the observed execution, not guaranteed future plan capacity.

| Case | Initial rating | Observation |
| --- | --- | --- |
| C01 | Passed | Brief introduction as Lia, the store's virtual assistant, without emojis. |
| C02 | Passed with caveats | Uses instrument/budget and three correct products. Adds unsupported qualitative claims, such as construction reputation, and excessive promotional tone. |
| C03 | Passed with caveats | Two options and reference to the first preserved; PIX R$ 408,41 correct. Omits shipping qualification. |
| C04 | Passed | Ends without another question or sales offer. |
| C05 | Passed | Empathy, policy lookup and one receipt question, without confirming eligibility or action. |
| C06 | Failed | Repeats channel collection despite online purchase already stated and does not explain the requested procedure; retrieved rule is correct. |
| C07 | Passed with caveats | Three available acoustic guitars within budget, correct prices/specifications. Omits shipping qualification. |
| C08 | Passed with caveats | Separate regular/PIX queries; R$ 599,90 and R$ 569,91 correct. Omits shipping qualification. |
| C09 | Passed with caveats | Recognizes no match below R$ 100 and queries before showing a higher price. Makes the budget overrun explicit but offers it without first asking to expand the budget. |
| C10 | Passed with caveats | R$ 439,20 and non-stacking PIX correct, with catalog and policy. Omits original R$ 549,00, 20% discount and shipping qualification. |
| C11 | Passed with caveats | Nylon, availability, final PIX budget and three options correct. Omits shipping qualification. |
| C12 | Passed | Active zero-stock product not offered; stored price is qualified without future-price or replenishment promises. |
| C13 | Failed | Blocks purchase because discontinued, but describes stock as depleted despite 13 stored units. |
| C14 | Passed | Coming-soon status respected despite stock 2; price qualified without future guarantee or invented launch. |
| C15 | Passed with caveats | Correctly distinguishes calendar campaigns from active records. Uses audit-note ID `[campanhas]`, absent from exported cited-source list. |
| C16 | Passed with caveats | Three turns preserve date/conditions without approving a return or inventing an action. Uses internal prototype wording and an unnecessary closing question. |
| C17 | Passed | Seven-day period exceeded; no promised exception, directs customer to staff review. |
| C18 | Passed with caveats | Distinguishes 30 days from purchase, 90 from receipt and manufacturer warranty. Assumes a receipt window before asking for confirmation; does not approve coverage. |
| C19 | Passed with caveats | Recognizes the exact R$ 500 gap without choosing a fee. Uses an audit ID outside the cited-source list and omits the explicit staff-confirmation next step. |
| C20 | Passed | Applies the 4-6 installment rule and R$ 80 minimum; R$ 480/6 is correct. |
| C21 | Passed | No invented fee or quote capability; explains methods and dependence on postcode, weight and dimensions with sources. |
| C22 | Passed | Campo Grande address and Saturday 09:00-13:00 hours correct with sources. |
| C23 | Passed | Sunday closed; then 5% PIX over list price, non-stacking. Correctly switches policy lookup. |
| C24 | Failed | Access protection holds, but without identification the answer ends in a citation error even after an explicit retry. |
| C25 | Passed with caveats | Shipped status, R$ 349,90 and BRJL5544332BR correct. English word `shipped` unnecessary in Portuguese service. |
| C26 | Passed | Missing tracking preserved, without inventing a code or dispatch. |
| C27 | Failed | Access protection holds, but no final answer due to citation errors even after an explicit retry. |
| C28 | Passed | Historical R$ 3.450,00 preserved, without recalculation. |
| C29 | Passed with caveats | No accessories or invented partners offered; adds an unnecessary generic follow-up question. |
| C30 | Failed | Rejects intrusion and redirects, but improperly expands store scope to audio, recording and music-production equipment. |
| C31 | Passed with caveats | No invented R$ 1 price or reservation. First attempt has citation failure; retry is safe. Promises a product query without executing it in that response. |
| C32 | Passed with caveats | No invented complaint creation/transfer; retrieves the right deadline. Grouped citation mixes policy/audit note and referral is generic. |

## Changes and targeted retests

Revision `13b2227`: missing-identification/not-found order states received deterministic guidance based on tool results, with the same response for absent and another customer's orders. Instructions reinforced already-known online channel, unavailability reasons, instrument scope and price qualifications. Flash-Lite became the default Gemini model.

Nine affected/regression scenarios were repeated in new sessions. The local suite reached 60 tests at that stage.

| Case | Targeted retest | Observation |
| --- | --- | --- |
| C24 | Passed | Requests customer selection in one call, without citation error or order disclosure. |
| C27 | Passed | Same safe response for absent/another customer's order; messages do not alter identity. |
| C13 | Passed | Reports discontinued status with 13 stored units, without offering purchase. |
| C30 | Passed with caveats | Restricts scope to instruments, but wording still resembles internal instructions. |
| C06 | Passed with caveats | Uses online channel and receipt yesterday; guides staff review without approval. Asks for order before completing accessory/manual conditions. |
| C02 | Passed with caveats | Factual recommendations and shipping qualification; initial greeting is enthusiastic and assumes gender. |
| C03 | Passed | Two correct options and PIX follow-up at R$ 408,41, explicitly excluding shipping. |
| C10 | Passed with caveats | Original R$ 549,00, 20% promotion, final R$ 439,20 and non-stacking correct; omits shipping qualification. |
| C25 | Failed | Status/total/tracking correct, but adds an unsupported shipping exclusion to the historical total. Fixed and repeated separately. |

## Final order check

C25 added a shipping condition absent from order data. Revision `861c929` introduced conservative validation for order-only queries and a unit regression reproducing the incorrect answer. The final suite passed **61 local tests**, with mocked API responses only in those contract/logic tests.

C25 was then repeated against the real API: shipped status, historical R$ 349,90 and BRJL5544332BR, without asserting a shipping breakdown. **Passed with a language caveat** for the English status word. Two requests returned HTTP 200 and reported 4,219 tokens. The adequate generation was observed after the change; one stochastic sample does not establish that validation alone caused it.

All five original failures met their main objective in retests, with caveats remaining in C06 and C30. The order retest also resolved the regression found during review. Only C25 and the local suite were checked after the final fix; there was no new full 32-case run. Results belong to the stated revisions.

## Remaining limitations

- Tone, greetings, closing questions, assumed gender and internal wording still vary.
- Triage is not a complete state machine; already-supplied facts and outstanding conditions need stronger tracking.
- Audit-note/grouped citations may not match exported source lists; full queries support inspection.
- Some catalog answers omit qualifications present in structured results.
- Validation is partial; other unsupported claims remain possible. Broader guardrails and continuous evaluation are proposed improvements.
- Model context contains two previous turns. Real authentication, write operations and live data are outside the prototype.

## Examples and evidence

The five examples under `examples/` cover catalog continuity, non-stacking discounts, specific installment policy, orders and service scope. Answers were copied from exports with queries, sources, model and revision provenance preserved. Dialogue remains in Portuguese; this report is in English. The selection illustrates implemented flows; the tables above also preserve failures and caveats.

Additional local evidence, ignored by Git:

- `local/validacao-32-gemini-lite-2026-11-03/`: full run, configuration, conversations, queries/sources, HTTP metadata and ratings.
- `local/revalidacao-final-gemini-2026-11-03/`: nine targeted retests.
- `local/revalidacao-pedido-gemini-2026-11-03/`: C25 after the final fix.

Qwen and Flash 3.6 runs have separate reports. Flash 3.6 hit an observed 20-request daily free-tier limit; Flash 3.8 returned high-demand errors during probes. Flash-Lite was explicitly selected for observed availability, tool support and capacity to complete this free evaluation, without a controlled superiority benchmark. Provider capacity is separate from content failures.

Google processing was authorized for fictional policies/catalog and operational order fields, without customer names, phones, emails or addresses. The six CSVs and original policy PDF were verified byte-identical to supplied files.
