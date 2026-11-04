# Retomada da avaliação Qwen — 03/11/2026

> **Registro histórico.** Contagens, pendências e conclusões descrevem as versões e execuções desta etapa. Para a situação atual, consulte o [README](../README.md) e a [avaliação Gemini e seus retestes](validacao-gemini-2026-11-03.md). Os exemplos atuais estão em `examples/`; versões anteriores permanecem no Git.

Execução entre 19h18 e 20h31 (São Paulo), por Streamlit AppTest e API real da Groq, com Qwen/Qwen3.8-27b e persona padrão. Código do agente igual a ea85546; HEAD da execução 7cb730d, que só acrescentou documentação. Não é uma rodada manual no navegador. Nenhuma resposta foi simulada ou editada.

## Resultado

**24 cenários concluídos: 14 aprovados, 9 aprovados com ressalvas e 1 falha (C15, Black Friday).** C25 foi tentado sem resposta final por cota diária; C26 a C32 não começaram. Os oito casos pendentes não estão aprovados. A revisão considera resposta final, consultas, fontes e critérios do roteiro; não é um benchmark estatístico.

| Caso | Avaliação | Observação |
| --- | --- | --- |
| C01 | Aprovado | Apresentação breve como assistente virtual Lia. |
| C02 | Aprovado com ressalva | Instrumento e orçamento preservados, três produtos corretos e uma pergunta. Acrescenta comparação genérica sobre conforto e timbre das cordas, que não consta explicitamente nos resultados cadastrais. Houve um HTTP 429 por minuto, recuperado em tentativa registrada. |
| C03 | Aprovado | Duas opções corretas; referência ao primeiro mantida e PIX R$ 408,41. |
| C04 | Aprovado | Encerra sem nova pergunta nem oferta. |
| C05 | Aprovado com ressalva | Empatia sóbria e sem confirmar cobertura ou ação. Pede instrumento e data de recebimento juntos, contrariando a preferência de um dado principal por turno; ainda não consulta política, mas também não afirma condições. |
| C06 | Aprovado com ressalva | Recupera política e aproveita canal/data/estado informados; não afirma aprovação ou abertura. Diz que condições parecem compatíveis sem confirmar acessórios/manuais e usa expressão técnica este protótipo no atendimento, que pode ser substituída por linguagem natural. |
| C07 | Aprovado | Informa 12 resultados e apresenta três menores preços, com especificações e fontes cadastrais. |
| C08 | Aprovado | R$ 599,90 e R$ 569,91 no PIX, sem frete. Uma revisão interna de validação levou à consulta adicional do PIX antes da resposta final. |
| C09 | Aprovado com ressalva | Busca vazia corretamente comunicada sem produto/preço inventado. Após revisão de validação, resposta fala em resposta correta, CSVs e critério de orçamento; linguagem interna extensa e pouco natural para atendimento. |
| C10 | Aprovado | Promoção de 20% mantida, sem acumular 5% PIX. |
| C11 | Aprovado | Filtro nylon, estoque e preço final PIX respeitados nos três produtos. |
| C12 | Aprovado | Produto ativo sem estoque não oferecido para compra; preço cadastrado sem garantia futura nem reposição inventada. |
| C13 | Aprovado | Status descontinuado respeitado apesar de estoque positivo; sem prometer venda. |
| C14 | Aprovado | Sem venda atual; preço cadastrado sem garantia futura. |
| C15 | Falhou | Cita campanha de 15% a 30% em todo catálogo sem verificar promoções ativas nem esclarecer que o mês/campanha não ativa desconto automaticamente. Não aplica 30% uniforme, mas deixa vigência implícita. |
| C16 | Aprovado com ressalva | Três turnos preservam dados, prazo e condições; uma revisão interna no primeiro turno, sem aprovação final ou operação inventada. Ressalva de linguagem técnica este protótipo na orientação final. |
| C17 | Aprovado | Prazo de sete dias ultrapassado, sem promessa de exceção nem abertura de devolução. |
| C18 | Aprovado | Distingue troca em 30 dias da compra, garantia legal em 90 dias do recebimento e fabricante conforme certificado. Pergunta recebimento, sem confirmar cobertura. |
| C19 | Aprovado | Após uma revisão interna, reconhece lacuna exata de R$ 500 e não escolhe frete arbitrário. Cita limites acima e abaixo com seção 5.1. |
| C20 | Aprovado | Aplica condição específica de 4x a 6x com parcela mínima R$ 80; R$ 480/6 correto, sem prometer processamento. |
| C21 | Aprovado com ressalva | Sem preço inventado nem promessa de cotador; política nacional citada. Sugere que escolher um violão dará peso e dimensões, dados não garantidos no catálogo. |
| C22 | Aprovado com ressalva | Endereço e sábado 09h–13h corretos com fontes. Pergunta automática de continuação desnecessária após resolver a dúvida. |
| C23 | Aprovado com ressalva | Domingo fechado e PIX 5% não cumulativo corretos com fontes; mudança de assunto preservada. Um HTTP 429 por minuto recuperado na tentativa explícita; revisão interna aparece no texto como agradecimento/correção a observação que o cliente não fez. |
| C24 | Aprovado com ressalva | Não revela pedido nem solicita dados pessoais; orienta selecionar cliente na tela. Porém diz cliente atualmente selecionado quando não há identificação e oferece listar pedidos nessa condição. Um HTTP 503 recuperado na tentativa explícita. |
| C25 | Interrompido pelo provedor | Sem resposta final após limite diário; não avaliado como acerto ou erro factual. |
| C26–C32 | Não executados | Interrupção da rodada antes desses casos. |

## Leitura dos resultados

C03 (continuidade e PIX), C10 (promoção sem acumulação) e C14 (preço de item em breve sem garantia futura), pendentes na tentativa anterior, foram concluídos e aprovados nesta retomada. Catálogo e filtros, indisponibilidade, devolução em três turnos, garantia, fronteira de frete e parcelamento produziram respostas compatíveis com seus objetivos, com as ressalvas de linguagem indicadas.

C15 permanece uma falha: a resposta cita a campanha de 15% a 30% em todo catálogo sem verificar promoções ativas e sem esclarecer que calendário não ativa desconto. Não há aprovação geral do agente. As demais ressalvas concentram-se em linguagem interna da validação aparecendo para o cliente, perguntas/ofertas desnecessárias e informações genéricas além do cadastro.

## Condições da execução

Intervalo de 65 segundos entre inícios de requisições, inclusive entre casos. Uma repetição explícita pelo botão da interface foi permitida por mensagem, sem retry no cliente HTTP. O lançador encerra ao identificar cota diária; não muda modelo nem provedor. Foram 68 requisições: 63 HTTP 200, quatro HTTP 429 (três por minuto, um por dia) e um HTTP 503. As chamadas bem-sucedidas reportaram 161.657 tokens. C02, C23 e C24 recuperaram-se na tentativa adicional; C25 permaneceu sem resposta após a recusa diária.

No bloqueio diário das 20h31, a Groq informou limite de 200.000 tokens, uso de 197.687 e solicitação de 2.342. Esses números são da conta/provedor, não apenas desta rodada. A cota externa não é defeito da lógica do agente e não invalida automaticamente respostas já obtidas; também não permite aprovar casos interrompidos.

## Evidências

Arquivos completos em `local/validacao-32-qwen-retomada-2026-11-03/`: conversas Markdown com consultas/fontes, configuração, execucoes.json, http-seguro.json, criterios.json, avaliacao-manual.json e rodada.json. Pacote: `local/validacao-32-qwen-retomada-2026-11-03.zip`. O manifesto SHA-256 permite verificar os arquivos. Conteúdo local ignorado pelo Git e conferido contra as credenciais configuradas.

A pedido do candidato, a alternativa seguinte é Gemini Flash, em avaliação separada. A troca de provedor exige validar o conector e os cenários reais novamente; resultados não devem ser atribuídos ao Qwen nem misturados como uma rodada integral do mesmo modelo. Nenhuma publicação do repositório foi realizada.
