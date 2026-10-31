# Teste de RAG sobre políticas

Provedor: groq. Modelo: qwen/qwen3.8-27b.

## Pergunta
Se o produto já está em promoção, posso ter mais 5% pagando no PIX?

## Resposta
Não, você não pode acumular o desconto de PIX sobre um preço que já está em promoção. As promoções não são cumulativas, e o desconto de 5% para pagamento via PIX não se aplica a preços já promocionais [P1].

## Trechos recuperados

### [P1] 6.2 Regras de Promoções
Fonte: politicas_da_loja.pdf, página 6. ID: 6.2-p6-1. Score lexical: 7.727894.

Cumulatividade: promoções não são cumulativas. O desconto de PIX (5%) não se aplica sobre
preços já promocionais.
Estoque: promoções estão sujeitas à disponibilidade de estoque. Produtos esgotados durante a
promoção não geram direito a rain check (reserva de preço).
Comunicação: preços promocionais devem sempre ser apresentados junto ao preço original e o
percentual de desconto, para total transparência ao cliente.

### [P2] 7.3 Situações Especiais
Fonte: politicas_da_loja.pdf, página 7. ID: 7.3-p7-1. Score lexical: 4.476019.

Produto fora de estoque: informar que o produto está temporariamente indisponível e sugerir
alternativas semelhantes que estejam disponíveis. Nunca confirmar disponibilidade sem verificar o
estoque atual.
Produto descontinuado: informar que o produto não faz mais parte do catálogo e oferecer modelos
equivalentes ou sucessores.
Promoção expirada: caso o cliente pergunte sobre uma promoção, verificar se ela encontra-se ativa
no sistema. Se a promoção estiver vencida, informar com transparência e apresentar o preço atual.
Nunca prometer um desconto que não está mais vigente.
Reclamação: ouvir o cliente com empatia, registrar a reclamação e encaminhar para o responsável.
Prazo de retorno: 24 horas úteis.

### [P3] 7.2 Fluxo de Atendimento Padrão
Fonte: politicas_da_loja.pdf, página 7. ID: 7.2-p7-1. Score lexical: 3.971587.

3. Consulta: buscar no sistema as informações relevantes (produto, estoque, promoção,
pedido).
4. Resposta: apresentar as opções de forma clara e objetiva, com preços e condições.
5. Fechamento: confirmar se o cliente precisa de mais alguma coisa e encerrar com
cordialidade.

### [P4] 6.1 Tipos de Promoção
Fonte: politicas_da_loja.pdf, página 6. ID: 6.1-p6-1. Score lexical: 2.71987.

A Empório da Música realiza promoções periódicas ao longo do ano. As principais campanhas
incluem:
• Aniversário da Loja (Agosto): descontos de 10% a 25% em itens selecionados.
• Black Friday (Novembro): descontos de 15% a 30% em todo o catálogo.
• Volta às Aulas (Fevereiro): descontos especiais em instrumentos para estudantes.
• Queima de Estoque: promoções pontuais para renovação de catálogo.
• Semana do Músico: promoções na semana do Dia do Músico (22 de novembro).
