# Interaction examples and review

These five conversations were run on 3 November 2026 with `gemini-3.5-flash-lite`, Streamlit AppTest and the real API. Customer-facing dialogue is preserved in its original Portuguese as evidence of the Brazilian store experience. The surrounding submission documentation is in English. Linked exports retain the complete queries and sources.

## 1. Catalog and PIX follow-up

The customer requests two options, then refers to the first one. The agent queries the CSVs and uses the price calculated in Python.

**Customer**

Quero duas opções de violões disponíveis até R$ 1.000. Mostre nome e preço.

**Lia**

Olá! Temos estas opções de violões disponíveis dentro do seu orçamento:

* Tagima Memphis AC-39 Nylon Natural – R$ 429,90 sem frete [D83].
* Rozini RC-104 Nylon Estudante – R$ 459,90 sem frete [D85].

**Customer**

E o primeiro no PIX?

**Lia**

O violão Tagima Memphis AC-39 Nylon Natural sai por R$ 408,41 sem frete no pagamento via PIX [D83].

Full export: [catalog and PIX](../examples/catalogo-e-pix.md).

## 2. Promotion and non-stacking discounts

The answer combines a product lookup with the promotion policy. Presentation caveat: it does not explicitly state that the quoted price excludes shipping.

**Customer**

Quanto fica o Ohana CK-20 no PIX? Posso somar os 5% à promoção?

**Lia**

O Ohana CK-20 Concert Natural sai por R$ 439,20 no PIX (preço original de R$ 549,00 com 20% de desconto promocional) [D121].

Não é possível somar o desconto de PIX à promoção, pois as regras da loja determinam que as promoções não são cumulativas e o desconto de PIX não se aplica sobre preços já promocionais [P6.2-p6-1].

Full export: [promotion and PIX](../examples/rag-promocao-pix.md).

<!-- pagebreak -->

## 3. Applying the installment policy

The agent retrieves the specific policy section and checks the minimum installment amount.

**Customer**

Uma compra de R$ 480 pode ser dividida em seis vezes sem juros?

**Lia**

Sim, uma compra de R$ 480,00 pode ser dividida em seis vezes sem juros, pois o valor da parcela (R$ 80,00) atinge o mínimo exigido para essa quantidade de parcelas [P3.1-p3-1].

Full export: [installments](../examples/rag-parcelamento.md).

## 4. Order status and tracking

Queried with **test customer #2** selected. The answer preserves the historical total and stored tracking code. The English word "shipped" inside the original Portuguese answer is a language caveat.

**Customer**

Qual o status, total e rastreamento do meu pedido 8?

**Lia**

O seu pedido 8 está com o status de enviado (shipped) e o código de rastreamento é BRJL5544332BR [O8]. O valor total histórico é de R$ 349,90 [O8].

Full export: [order and tracking](../examples/pedido-rastreamento.md).

## 5. Out-of-scope request

The fixed service scope restricts the store to musical instruments. This conversation made no new tool call.

**Customer**

Vocês vendem cabos, palhetas ou amplificadores?

**Lia**

Olá! Na Empório da Música, nós somos especializados em instrumentos musicais, como violões, guitarras, baixos, teclados, baterias e outros instrumentos de cordas, sopro e percussão.

Cabos, palhetas e amplificadores são acessórios e não fazem parte do nosso catálogo de instrumentos.

Posso te ajudar a encontrar algum instrumento específico?

Full export: [out of scope](../examples/fora-do-escopo.md).

<!-- pagebreak -->

## Review criteria and fixes

I guided tests around expected service behavior: source-supported facts, correct prices, context continuity, scope boundaries and restricted order access. I also defined expectations for tone and collecting the necessary information before advising on returns.

Automation and Codex supported execution. Reviewing answers and prioritizing fixes were part of my direction of the project. Three examples illustrate the process:

| Observed issue | Implemented change | Recorded verification |
| --- | --- | --- |
| Queries without customer identification or for another customer's order ended in citation errors. | Deterministic guidance based on the tool result, without revealing the order. | C24 and C27 passed targeted retests. |
| A discontinued product was described as out of stock despite a positive stored quantity. | Instructions distinguish commercial status from stock quantity. | C13 reported discontinued status and 13 units without offering a purchase. |
| An answer added "shipping excluded" to a historical order total. | Conservative validation and a regression test for the unsupported qualification. | C25 was repeated with correct status, total and tracking, without asserting a shipping breakdown. |

These retests demonstrate the individual outcomes. Language and triage caveats remain, and the complete real-scenario suite was not rerun after the last fix.

## Improvements with more time

I would start with response controls and interaction context. Query improvements would follow dataset growth, with quality evaluation after each change.

1. **Guardrails and triage:** validate price, stock and policy claims against tool results; structure missing triage fields and escalate uncertainty to staff. Add unseen questions and attempts to override the rules.
2. **Previous-interaction context:** retain summaries and relevant fields per identified customer, such as instrument preferences, budget and information already supplied. Access would follow authorization and retention rules; current prices, stock and policies would still be queried from sources.
3. **RAG for more documentation:** evaluate hybrid BM25/embedding retrieval followed by reranking. Improve context-preserving chunks, section metadata and version/effective-date controls. Compare retrieval and faithfulness on a separate question set.
4. **Queries over larger datasets:** replace CSV loading with databases or operational APIs, using filters, indexes and pagination. Keep tool parameters and permissions explicit, with pricing and access rules in code.
5. **Behavioral fine-tuning:** after improving data, prompts and validation, evaluate a compatible model using reviewed conversations for tone, triage and tool selection. Separate training from evaluation and measure gains against the base model. Prices and availability would remain source-backed queries.

Real authentication and stock/order integrations would be needed for operational use. These are proposed improvements; the submitted application remains a prototype.

Reports and examples: [Gemini evaluation](validacao-gemini-2026-11-03.md) and [five-conversation index](../examples/README.md). Implementation decisions are summarized in the [README](../README.md).
