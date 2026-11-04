# Supplied-data audit - 2 November 2026

> **Historical record.** Findings, pending work and implementation references describe this stage. See the [README](../README.md) and [Gemini evaluation](validacao-gemini-2026-11-03.md) for the submission version. Current examples are under `examples/`; earlier versions remain in Git.

Local review of six CSVs, the policy manual and challenge, assisted by Codex before agent fixes. No API requests or source edits were made. The six CSVs and policy PDF were compared byte-for-byte with supplied originals and matched.

Some inconsistencies could expose weaknesses during evaluation. **There is no evidence that they were inserted deliberately.** Contradictory fields, missing information and plausible historical differences need separate treatment.

## 1. Conflicting names, descriptions and specifications

Source: `data/products.csv`, identified by `product_id`, not row position.

| Product | Evidence in the record | Consequence |
| --- | --- | --- |
| 135 | Music Man name; Fender Jazz Bass description. Description says Alder body; specs say Ash. | A recommendation could combine another instrument's brand/material. |
| 137 | Yamaha name; Ibanez five-string description; `strings=4` in specs. | Do not confirm brand/model or string count by combining conflicting fields. |
| 139 | Yamaha name; Pearl Export description with Poplar/mahogany; Maple specs. | Conflicting brand/material. |
| 140 | Pearl name; Tama/Birch description; Maple specs. | Conflicting brand/material. |
| 142 | Korg name; Roland/88-key description; 61 in specs. | Brand or key-count answer could be wrong. |
| 144 | Roland/synthesizer name; Yamaha/arranger description. | Conflicting brand/instrument type. |
| 102 | Description says solid top without species; specs say solid cedar. | Extra detail alone is not a contradiction. |

Using names/specs and excluding descriptions from search reduces mixing but does not prove every specification correct. Disclose a relevant conflict and refer it to staff, preserving the original fields. Do not silently replace fictional records using external catalogs.

## 2. Status is distinct from stock

| Product | Status | Stock | Expected treatment |
| --- | --- | --- | --- |
| 96 - Giannini GF-3D | active | 0 | Exists but is out of stock. |
| 113 - Shelby SN-7C | discontinued | 0 | Discontinued, not merely temporarily out of stock. |
| 136 - Ibanez Bass 2X | discontinued | 13 | Positive quantity does not authorize a purchase offer. |
| 130 - Kala KA-ABP-CTG | coming_soon | 2 | No current sale or invented launch date. |

Catalog code distinguishes these states. Earlier real cases C12/C14 showed the model could still use available-only search and conclude the model was absent. A correct tool is insufficient when the selected query hides the relevant record.

## 3. Inactive/repeated promotions without validity dates

`data/promotions.csv` has 25 rows and four active promotions:

| Promotion | Product | Discount |
| --- | --- | --- |
| 12 | 127 | 10% |
| 14 | 121 | 20% |
| 19 | 90 | 18% |
| 24 | 94 | 8% |

Products 93, 96 and 99 each have two inactive promotion rows. Product 96 has 18% and 40%, both `is_active=0`. Do not choose the largest rate or add rows. This dataset has no product with two active promotions.

There are no start/end dates. Names such as Black Friday and general manual campaigns do not activate discounts by calendar month. The documented interpretation uses `is_active`; section 6.2 prevents stacking an active promotion with 5% PIX.

## 4. Historical totals are not necessarily current-price sums

Sources: `orders.csv`, `order_items.csv`, `products.csv`.

| Order | Recorded total | Quantity times current price | Difference |
| --- | --- | --- | --- |
| 3 | R$ 3.450,00 | 2 x R$ 1.749,00 = R$ 3.498,00 | R$ 48,00 |
| 20 | R$ 1.400,00 | R$ 799,00 + R$ 689,00 = R$ 1.488,00 | R$ 88,00 |

The other 18 orders match current list-price sums. This does not prove the two differences are errors: historical unit prices, shipping and applied discounts are unavailable. Preserve recorded totals without inventing an explanation. Some PIX orders, such as order 1, also match current prices without the general discount; that does not establish an overcharge.

## 5. Historical installments differ from the described rule

Section 3.1 states minimum installments of R$ 80 for 4-6 payments and R$ 100 for 7-12.

| Order | Status | Record | Approximate installment |
| --- | --- | --- | --- |
| 9 | confirmed | R$ 349,90 in 6 installments | R$ 58,32 |
| 16 | pending | R$ 429,90 in 6 installments | R$ 71,65 |
| 18 | cancelled | R$ 459,90 in 12 installments | R$ 38,33 |

These differ from the current manual, but do not authorize rewriting orders. Historical policies/payment details are missing; a cancelled order does not prove approval. Section 3's general R$ 100 table differs from section 3.1's specific bands. The up-to-three-installment wording and below-R$ 50 exception are ambiguous. Document the adopted specific-rule interpretation.

## 6. Orders do not establish actual receipt or return eligibility

`orders.csv` includes `order_date` and `estimated_delivery`, not actual receipt date or purchase channel. Twelve orders lack tracking and estimated delivery. Missing tracking does not authorize inventing a code.

Order dates range from 15 October 2025 to 22 March 2026. Elapsed time does not turn shipped/confirmed/pending into delivered; an estimate is not delivery evidence. Ask for missing channel, receipt and condition details.

Product 130 is currently `coming_soon` but appears in delivered order 3 and pending order 14. This may be historical or inconsistent; without status events, neither explanation is proven. Do not delete orders or reactivate the product by inference.

## 7. Email is not a unique customer identifier

Customers **11 and 43** share the same email but have different IDs. No normalized phone duplicate was found. Do not merge customers or authorize orders by email alone. Application-bound IDs avoid that association, but the selector remains simulated identification. Publishing the contacts is unnecessary to document this finding.

## 8. The supplied catalog is partial

The manual mentions over 300 instruments; the CSV has 65. Of nine categories, six have sampled products: 35 acoustic guitars, 15 ukuleles, five electric guitars, four basses, three drum kits and three keyboards. Categories 6, 7 and 8 (woodwinds, brass and orchestral strings) have no products in this file.

A missing match does not establish that the store never sells flutes/violins. Explain the supplied dataset/filter limitation. Product 145 preceding 131 is valid: keys are not row positions.

## 9. Specifications vary by category

- For 50 acoustic guitars/ukuleles, `strings` means material (nylon/steel), and `electronics` exists.
- For nine electric guitars/basses, `strings` means count (6/4); `electronics` is absent despite electric instrument names.
- Drums have `shells/pieces/hardware`; keyboards have `keys/type/polyphony`.
- Weight, dimensions and order delivery postcode are unavailable for a full shipping quote.

Do not apply one string filter universally, infer acoustic status from missing `electronics`, or filter out actual electric guitars solely because that field is absent. Wood species does not establish solid construction; an integrated tuner does not prove external pickup capability.

## 10. Policy ambiguities

| Location | Evidence | Interpretation limit |
| --- | --- | --- |
| 5.1, page 4 | Free above R$ 500; R$ 35 below. | Exactly R$ 500 is undefined. Earlier C19 invented a fee. |
| Cover/1.2, pages 1-2; section 7, page 6 | (67) 3341-4444 versus WhatsApp (67) 3321-4500. | Do not assume a typo; cite the chosen section and disclose relevant conflict. |
| Cover and 1.2 | Email domain appears with and without an accent. | Different strings; do not silently normalize or declare an accented domain invalid. |
| 4.2 and 8.1-8.2 | Exchange within 30 days of purchase; legal warranty 90 days from receipt; manufacturer 6 months-2 years. | Different purposes/start dates; do not deny all warranty after 30 days or invent brand-specific coverage. |
| 4.4 | Customized/final-sale items and mouthpieces have exclusions. | Promotions do not automatically establish final-sale ineligibility; structured order data lacks the required notice. Refer uncertainty under section 10. |
| 7.3 and 10 | Complaint registration/referral, 24 business-hour response and management review. | Store procedures are not implemented actions; the prototype must not claim registration or transfer. |

This is a consistency review of the fictional manual, not legal validation. External law was not used to replace challenge material.

## 11. Checks without detected issues

- No duplicate primary keys in the five tables with their own IDs; no orphan product/category, order/customer, item or promotion references.
- All 20 orders have items; specification JSON values are objects; no negative price or stock was found.
- Eight populated tracking codes match the manual's described pattern. None was checked with a real carrier.
- Local text searches found no common malicious-instruction patterns in the inspected text; this does not exclude all hidden PDF content or attacks.
- No data was sent to external providers during this audit; originals stayed intact.

## Implications for fixes

Record sources, ambiguity and assumptions; preserve original values; validate identity/discounts in code; include unavailable records in model-specific lookup; distinguish missing information from false; reject unsupported conclusions. Data conflicts do not excuse invented answers. The challenge permits documented reasonable assumptions. Proposed fixes in this historical audit are not evidence that they were already implemented at that point.
