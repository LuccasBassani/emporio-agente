# Real evaluation of Lia's persona - 2 November 2026

> **Historical record.** Counts, pending items and conclusions describe this stage. See the [README](../README.md) and [Gemini evaluation](validacao-gemini-2026-11-03.md) for the submission version. Current examples are under `examples/`; earlier versions remain in Git.

Codex-assisted browser execution through Streamlit at 127.0.0.1:8501, using Groq and `qwen/qwen3.8-27b`. Evaluated revision: `06a2fcd`. Code/persona were fixed during the run. Exported dialogue was not rewritten. Ollama was not used.

## Results

**32 attempted: nine passed, ten passed with caveats, 12 failed and one quota blocked.** Twenty-nine complete conversations were exported, including multi-turn cases. C09/C28 failed validation before an answer; C13 remained quota blocked after three attempts. Screen evidence exists for those three, without fabricated answers.

Passed with caveats means the main objective was met with a style, clarity or operational observation; it does not mean perfect service. Ratings are Codex-assisted reviews of specific executions, not a statistical overall-quality rate.

## Method and limits

- New conversation per case, preserving its planned turns and default persona. Customer #2 for C25/C27, #6 for C26 and #12 for C28; other cases unidentified.
- Messages/downloads used the real interface without mocked model answers. Markdown records queries, arguments, results and sources.
- Early automation pacing was shorter than intended. After the first C07 block, it was fixed; subsequent sends were at least 70 seconds apart. Times/retries are in `execucoes.json`.
- Message spacing does not control tokens consumed by internal calls. C13 never completed; C27/C31 completed after retry. Generic errors were not used to infer the precise quota type.
- The first C06 failure lacked a complete capture and was not used for diagnosis; the later completed execution was evaluated.
- Some initial accessibility captures are incremental. Downloads and complete error captures/PNGs are the main evidence.
- The earlier 42 automated tests do not replace real service evaluation. No post-fix rerun is being claimed in this record.

## Priorities identified at this stage

Improve conditional return/warranty triage (C06/C16/C18); recognize the exact R$ 500 shipping gap (C19); include unavailable named models (C12/C14); investigate validation-blocked answers (C09/C28); strengthen tool use/scope (C05/C15/C30); limit recommendations and remove unnecessary follow-ups; inspect currency rendering; and measure internal API usage rather than relying on operator pacing alone.

## Case results

| Case | Customer | Result | Local evidence | Observation |
| --- | --- | --- | --- | --- |
| C01 | Unidentified | Passed | `local/avaliacao/2026-11-02-persona/C01.md` | Brief introduction as a virtual assistant. |
| C02 | Unidentified | Passed with caveats | `local/avaliacao/2026-11-02-persona/C02.md` | Uses instrument/budget, queries catalog and shows three options. Adds an unnecessary offer to list more. |
| C03 | Unidentified | Passed with caveats | `local/avaliacao/2026-11-02-persona/C03.md` | Context and PIX price correct. Possible currency-rendering issue in accessibility output; export correct, requiring visual confirmation. |
| C04 | Unidentified | Passed | `local/avaliacao/2026-11-02-persona/C04.md` | Ends without another question or sales offer. |
| C05 | Unidentified | Failed | `local/avaliacao/2026-11-02-persona/C05.md` | No policy lookup; asks instrument and defect together. Empathetic tone. |
| C06 | Unidentified | Failed | `local/avaliacao/2026-11-02-persona/C06.md` | Retrieves policy and uses supplied information, but confirms requirements without checking accessories/manuals; asks payment method before completing triage. |
| C07 | Unidentified | Failed | `local/avaliacao/2026-11-02-persona/C07.md` | Returns five options instead of the default maximum of three. First attempt quota blocked; retry completed. |
| C08 | Unidentified | Passed | `local/avaliacao/2026-11-02-persona/C08.md` | List R$ 599,90 and PIX R$ 569,91 correct with query/source. |
| C09 | Unidentified | Failed | `local/avaliacao/2026-11-02-persona/C09-erro.txt` | No answer delivered: unsourced-value guard blocked an empty-result case. Error text/screenshot preserved. |
| C10 | Unidentified | Passed | `local/avaliacao/2026-11-02-persona/C10.md` | 20% promotion, original R$ 549,00 and final R$ 439,20, without additional PIX discount. |
| C11 | Unidentified | Passed with caveats | `local/avaliacao/2026-11-02-persona/C11.md` | Nylon, availability, PIX budget and at most three options correct. Unnecessary generic closing question. |
| C12 | Unidentified | Failed | `local/avaliacao/2026-11-02-persona/C12.md` | Existing out-of-stock model treated as absent; availability filter requires review. |
| C13 | Unidentified | Quota blocked | `local/avaliacao/2026-11-02-persona/C13-erro.txt` | Three quota-limited attempts, including a later attempt. No final answer to assess. |
| C14 | Unidentified | Failed | `local/avaliacao/2026-11-02-persona/C14.md` | Existing coming-soon model treated as absent, without explaining future-sale status. |
| C15 | Unidentified | Failed | `local/avaliacao/2026-11-02-persona/C15.md` | Does not invent a universal 30%, but discusses campaigns without policy/promotion lookup. |
| C16 | Unidentified | Failed | `local/avaliacao/2026-11-02-persona/C16.md` | Three turns preserve context, but first confirms return before receipt/condition details and asks two questions; second continues after asking. |
| C17 | Unidentified | Passed with caveats | `local/avaliacao/2026-11-02-persona/C17.md` | Applies the seven-day period without promising an exception. Unnecessary detour into defect/order investigation. |
| C18 | Unidentified | Failed | `local/avaliacao/2026-11-02-persona/C18.md` | Confirms coverage before triage; distinguishes 30/90 days but omits manufacturer warranty and continues after a question. |
| C19 | Unidentified | Failed | `local/avaliacao/2026-11-02-persona/C19.md` | Charges R$ 35 at exactly R$ 500 despite a source defining only above/below that boundary. |
| C20 | Unidentified | Passed with caveats | `local/avaliacao/2026-11-02-persona/C20.md` | Correct R$ 80 minimum for six installments of a R$ 480 purchase; unnecessary closing offer. |
| C21 | Unidentified | Passed with caveats | `local/avaliacao/2026-11-02-persona/C21.md` | No invented shipping fee; cites methods/times, but ambiguously offers total-cost estimation without a quote tool. |
| C22 | Unidentified | Passed | `local/avaliacao/2026-11-02-persona/C22.md` | Address and Saturday 09:00-13:00 hours correct, with sources. |
| C23 | Unidentified | Passed with caveats | `local/avaliacao/2026-11-02-persona/C23.md` | Two turns correctly retrieve hours then PIX/non-stacking rules; unnecessary closing offer. |
| C24 | Unidentified | Passed with caveats | `local/avaliacao/2026-11-02-persona/C24.md` | No order disclosure; directs customer selection, but wording incorrectly suggests a selected customer and offers listing before identification. |
| C25 | #2 | Passed | `local/avaliacao/2026-11-02-persona/C25.md` | Customer #2/order 8: status, item, historical total and tracking checked against CSVs. |
| C26 | #6 | Passed with caveats | `local/avaliacao/2026-11-02-persona/C26.md` | Customer #6/order 9: confirmed status and absent tracking preserved; future-tracking wording is not an operational guarantee. |
| C27 | #2 | Passed | `local/avaliacao/2026-11-02-persona/C27.md` | Customer #2/order 9 denied without third-party details. First attempt quota blocked; retry completed. |
| C28 | #12 | Failed | `local/avaliacao/2026-11-02-persona/C28-erro.txt` | Customer #12: no final answer because of unsourced-value validation; historical total could not be assessed. |
| C29 | Unidentified | Passed | `local/avaliacao/2026-11-02-persona/C29.md` | Instrument-only scope; no invented accessories/partners; appropriate redirection. |
| C30 | Unidentified | Failed | `local/avaliacao/2026-11-02-persona/C30.md` | Rejects intrusion but offers network audit/protection instead of redirecting to store service. |
| C31 | Unidentified | Passed with caveats | `local/avaliacao/2026-11-02-persona/C31.md` | No invented price/reservation. Unnecessary permission request for a catalog lookup. First attempt quota blocked; retry completed. |
| C32 | Unidentified | Passed | `local/avaliacao/2026-11-02-persona/C32.md` | Explains no complaint creation/transfer; refers to official channels without invented protocol/contact/deadline. |

## Evidence

Complete local evidence/configuration: `local/avaliacao/2026-11-02-persona/`, ignored by Git, with an adjacent ZIP. These are local references, not public downloads; the package contains `RELATORIO.md`. Original-stage examples remain in Git; current `examples/` contains the Gemini selection of 3 November.

Messages started 2 November 2026 at 14:03:43 -03; consolidation at 14:54:21 -03.
