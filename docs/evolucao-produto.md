# Proposed evolution

This plan follows observed limitations. These are proposed features, not requirements for running the prototype or claims of existing functionality. A shorter version appears under [Improvements with more time](entrega.md#improvements-with-more-time).

## 1. Guardrails, triage and evaluation

I would expand validation of prices, stock, policies and missing fields against tool results. Triage would track channel, receipt and item condition explicitly, escalating uncertainty to staff. Current protections are partial and do not eliminate hallucinations or instruction overrides.

Evaluation would add unseen questions, paraphrases, long conversations and adversarial instructions. Factual accuracy, tool selection, continuity, style and execution errors would be assessed separately. The 32 development scenarios would not be the only evaluation set.

## 2. Previous-interaction context

I would start with reviewable summaries/fields per identified customer: instrument preferences, budget, the order under discussion and information already provided. History access would have authorization, retention rules, provenance and validity.

Old conversations do not establish current prices, stock, tracking or policy. Those facts would still come from source queries. Tests would check continuity and isolation between customers.

## 3. Retrieval and queries at larger scale

For more documentation, I would evaluate hybrid BM25/embedding search, reranking and context-preserving chunks. Section, version and effective-date metadata would help filter sources. Comparisons would measure retrieval, faithfulness, cost and latency.

Larger or live operational datasets would use databases/APIs with parameterized queries, indexes, filters and pagination. Pricing and authorization would remain in code behind bounded tools. Conflicts would be corrected upstream and each answer's data version recorded.

## 4. Behavioral fine-tuning

After improving data, prompts and validation, I would evaluate a compatible model trained on reviewed conversations for tone, triage and tool selection. Training and evaluation sets would be separate; adoption would require measured improvement against the base model.

No weight adaptation is implemented. Fine-tuning would not replace price/availability queries or independently resolve inconsistent records.

## 5. Operational requirements

I would add real authentication/authorization, stock/order integrations, human support and observability of queries, errors, usage and latency, with data minimization and retention rules. Write operations would need duplicate prevention and appropriate confirmation.

Provider capacity would follow expected volume and budget. Current pacing is per session and does not control account-wide capacity. Future retries would distinguish error types and keep data destinations explicit.
