# Selected real interactions

Five conversations executed on 3 November 2026 with Google Gemini, model `gemini-3.5-flash-lite`, Streamlit AppTest and the real API. Questions and answers remain in the original Brazilian Portuguese, copied from exports without rewriting; each file preserves queries and sources. This English index explains their purpose.

| Conversation | Demonstrated behavior | Context | Execution revision |
| --- | --- | --- | --- |
| [catalogo-e-pix.md](catalogo-e-pix.md) | Catalog query and PIX follow-up | Unidentified customer | `13b2227` |
| [rag-promocao-pix.md](rag-promocao-pix.md) | Promotion and PIX discounts do not stack | Unidentified customer | `13b2227` |
| [rag-parcelamento.md](rag-parcelamento.md) | Specific installment policy | Unidentified customer | `163ef3c` |
| [pedido-rastreamento.md](pedido-rastreamento.md) | Order status, historical total and tracking | Customer #2 | `861c929` |
| [fora-do-escopo.md](fora-do-escopo.md) | Instrument scope and accessory requests | Unidentified customer | `163ef3c` |

The installment example retrieves section 3.1 and applies its minimum-installment condition alongside the manual's general table. The catalog example maintains a reference across two turns and uses a Python-calculated price. The promotion example combines product and policy queries. The order example uses only permitted operational fields. The accessory request uses the fixed service scope without retrieval in that conversation.

The [full evaluation report](../docs/validacao-gemini-2026-11-03.md) includes all 32 scenarios and example caveats. These include an English status word inside the Portuguese order answer and omission of the shipping qualification in the promotional answer. Earlier executions remain in Git history and local evidence files.
