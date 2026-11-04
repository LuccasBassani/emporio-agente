# Exemplos reais selecionados

Cinco conversas executadas em 03/11/2026 com Google Gemini, modelo `gemini-3.5-flash-lite`, pela interface via Streamlit AppTest e API real. As perguntas e respostas foram copiadas das exportações sem edição manual; consultas e fontes estão preservadas em cada arquivo.

| Conversa | Comportamento demonstrado | Contexto | Código da execução |
| --- | --- | --- | --- |
| [catalogo-e-pix.md](catalogo-e-pix.md) | Catálogo e continuidade no PIX | Sem identificação | `13b2227` |
| [rag-promocao-pix.md](rag-promocao-pix.md) | Promoção e PIX não cumulativos | Sem identificação | `13b2227` |
| [rag-parcelamento.md](rag-parcelamento.md) | Parcelamento específico do manual | Sem identificação | `163ef3c` |
| [pedido-rastreamento.md](pedido-rastreamento.md) | Status, total histórico e rastreamento | Cliente #2 | `861c929` |
| [fora-do-escopo.md](fora-do-escopo.md) | Escopo de instrumentos e acessórios | Sem identificação | `163ef3c` |

O parcelamento demonstra recuperação da seção 3.1 e aplicação da condição específica de parcela mínima, diante da tabela geral do manual. O catálogo mostra continuidade entre dois turnos e preço calculado em Python; o exemplo promocional combina consulta de produto e política. O pedido usa apenas campos operacionais autorizados. O exemplo de acessórios usa o escopo fixo do atendimento, sem recuperação naquela conversa.

Resultados dos 32 cenários e as ressalvas dos exemplos estão no [relatório completo](../docs/validacao-gemini-2026-11-03.md). A seleção inclui pequenas ressalvas de apresentação, como termo inglês no pedido e condição sem frete omitida no texto promocional. As execuções anteriores permanecem no histórico Git e nos arquivos locais de evidência.
