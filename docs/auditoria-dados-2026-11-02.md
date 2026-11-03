# Auditoria dos materiais fornecidos — 02/11/2026

Revisão local dos seis CSVs, do manual e do enunciado, realizada com assistência do Codex antes das correções do agente. Não houve chamada à API nem alteração nos dados. Os seis CSVs e o PDF de políticas da pasta data foram comparados byte a byte com os originais recebidos e são idênticos.

Há inconsistências e limites que podem funcionar como armadilhas de avaliação. **Não há evidência para afirmar que foram inseridos intencionalmente.** Diferenciar contradição entre campos, dado ausente e divergência histórica plausível é parte da análise.

## 1. Nomes, descrições e especificações discordam

Fonte: `data/products.csv`, identificando pelo product_id, não pela posição da linha.

| Produto | Evidência no próprio cadastro | Consequência |
| --- | --- | --- |
| 135 | Nome Music Man; descrição Fender Jazz Bass. Descrição cita corpo Alder; specs registra Ash. | Pode gerar recomendação com marca e madeira de outro instrumento. |
| 137 | Nome Yamaha; descrição Ibanez de 5 cordas; specs registra strings=4. | Não confirmar marca/modelo ou número de cordas combinando campos contraditórios. |
| 139 | Nome Yamaha; descrição Pearl Export com Poplar/mogno; specs registra Maple. | Divergência de marca e material. |
| 140 | Nome Pearl; descrição Tama com Birch; specs registra Maple. | Divergência de marca e material. |
| 142 | Nome Korg; descrição Roland com 88 teclas; specs registra 61. | Resposta de marca ou quantidade de teclas pode ficar incorreta. |
| 144 | Nome Roland/sintetizador; descrição Yamaha/arranjador. | Divergência de marca e tipo de instrumento. |
| 102 | Descrição cita tampo sólido sem espécie; specs informa Cedro Sólido. | Informação adicional não é, sozinha, contradição: não classificar todo detalhe ausente como erro. |

A decisão atual usa nome e specs e exclui descrição da busca. Isso reduz mistura de marcas, mas **não prova que todo valor em specs é verdadeiro**. Proposta para a correção: explicitar a divergência quando afetar a pergunta e orientar confirmação com a equipe, preservando os campos originais. Não consultar catálogos externos para substituir silenciosamente os dados fictícios.

## 2. Status e estoque não dizem a mesma coisa

| Produto | Status | Estoque | Tratamento esperado |
| --- | --- | --- | --- |
| 96 — Giannini GF-3D | active | 0 | Existe no catálogo, mas está esgotado. |
| 113 — Shelby SN-7C | discontinued | 0 | Descontinuado; não confundir com esgotamento temporário. |
| 136 — Ibanez Bass 2X | discontinued | 13 | Estoque positivo não autoriza oferecer compra. |
| 130 — Kala KA-ABP-CTG | coming_soon | 2 | Não prometer venda atual ou data de lançamento. |

O código de catálogo já distingue esses casos. A rodada real C12/C14 mostrou que o agente ainda pode usar a busca padrão de disponíveis e concluir apenas que não encontrou o modelo. A ferramenta estar correta não basta se a consulta escolhida oculta o registro relevante.

## 3. Promoções inativas, repetidas e sem vigência por data

Fonte: `data/promotions.csv`. São 25 registros, mas somente quatro ativos:

| Promoção | Produto | Desconto |
| --- | --- | --- |
| 12 | 127 | 10% |
| 14 | 121 | 20% |
| 19 | 90 | 18% |
| 24 | 94 | 8% |

Produtos 93, 96 e 99 têm duas linhas de promoção cada, todas inativas. O produto 96 aparece com 18% e 40%, ambos is_active=0. Não escolher a maior porcentagem nem somar registros. Não há duas promoções ativas para um mesmo produto neste conjunto.

O CSV não contém início/fim de vigência. Nomes como Black Friday e a descrição genérica das campanhas no manual não autorizam ativar descontos pelo mês do calendário. A interpretação documentada usa is_active. Se já houver promoção ativa, não acumular os 5% do PIX, conforme seção 6.2 do manual.

## 4. O total histórico não é uma soma obrigatória dos preços atuais

Fontes: `orders.csv`, `order_items.csv` e `products.csv`.

| Pedido | Total registrado | Quantidades × preço atual | Diferença |
| --- | --- | --- | --- |
| 3 | R$ 3.450,00 | 2 × R$ 1.749,00 = R$ 3.498,00 | R$ 48,00 |
| 20 | R$ 1.400,00 | R$ 799,00 + R$ 689,00 = R$ 1.488,00 | R$ 88,00 |

Os outros 18 pedidos coincidem com a soma dos preços atuais de tabela. Isso **não comprova erro** nos dois totais divergentes: não há preço unitário histórico, frete, desconto aplicado ou composição financeira suficiente para reconciliar os pedidos. Preservar o total registrado e não inventar a origem da diferença.

Também há pedidos pagos em PIX cujo total corresponde ao preço atual sem o desconto geral de 5%, por exemplo o pedido 1. Não recalcular nem afirmar cobrança indevida sem os preços e condições históricos.

## 5. Parcelamento histórico diverge da regra descrita

O manual, seção 3.1, informa mínimo de R$ 80 por parcela de 4x a 6x e R$ 100 de 7x a 12x.

| Pedido | Status | Registro | Parcela aproximada |
| --- | --- | --- | --- |
| 9 | confirmed | R$ 349,90 em 6x | R$ 58,32 |
| 16 | pending | R$ 429,90 em 6x | R$ 71,65 |
| 18 | cancelled | R$ 459,90 em 12x | R$ 38,33 |

São divergências em relação à regra atual do material, não autorização para corrigir o pedido. Não há histórico de versões de políticas ou detalhes do pagamento para explicar cada caso; o pedido cancelado também não prova que o parcelamento chegou a ser aprovado.

O próprio manual merece leitura completa: a tabela da seção 3 menciona mínimo geral de R$ 100, enquanto a seção 3.1 detalha faixas diferentes. A redação sobre até 3x e a exceção abaixo de R$ 50 é pouco clara. A interpretação das regras específicas deve ser documentada; não generalizar o mínimo de R$ 100 para todas as faixas.

## 6. Os pedidos não permitem concluir recebimento ou prazo de devolução

`orders.csv` tem order_date e estimated_delivery, mas não contém data efetiva de recebimento nem canal de compra. Há 12 pedidos sem rastreamento e sem previsão de entrega. Ausência de rastreio não significa erro do arquivo nem autoriza criar um código.

Os pedidos vão de 15/10/2025 a 22/03/2026. Não mudar shipped/confirmed/pending para delivered só porque o tempo passou. A previsão não é prova de entrega. Uma consulta de pedido não fornece todos os dados para confirmar arrependimento; perguntar canal, recebimento e condições quando faltarem.

O produto 130, hoje coming_soon no CSV, aparece no pedido 3 entregue e no pedido 14 pendente. Isso pode representar histórico ou um cadastro inconsistente; sem eventos de mudança de status, não há como escolher uma explicação. Não apagar os pedidos nem reativar a venda do produto por inferência.

## 7. E-mail não identifica um único cliente neste conjunto

Em `customers.csv`, os clientes **11 e 43** têm exatamente o mesmo e-mail. Os customer_id são distintos e não há telefone repetido na verificação normalizada.

Não unir clientes nem conceder acesso aos pedidos só pelo e-mail. O protótipo vincula a consulta ao ID selecionado fora dos argumentos do modelo, o que evita essa associação indevida. A seleção continua sendo simulação de identificação, não autenticação de produção. Não é necessário publicar os contatos para documentar a inconsistência.

## 8. O catálogo fornecido é parcial

O manual menciona mais de 300 instrumentos, mas o CSV contém 65. Há 9 categorias; somente 6 têm produtos nesta amostra: 35 violões, 15 ukuleles, 5 guitarras, 4 baixos, 3 baterias e 3 teclados. As categorias 6, 7 e 8 — sopros de madeiras, metais e cordas orquestrais — não possuem produtos no arquivo.

Não transformar uma busca vazia em “a loja não vende flautas/violinos”. Informar que não há opções na base disponibilizada para os filtros consultados. Ausência de registro não comprova inexistência no catálogo completo.

O product_id 145 aparece antes do 131 no arquivo. É permitido: IDs não são posições de linhas. Relações e consultas devem usar as chaves, como o código atual faz.

## 9. O JSON de specs muda conforme a categoria

- Nos 50 violões/ukuleles, strings indica material (nylon/steel) e há campo electronics.
- Nas 9 guitarras/baixos, strings indica quantidade (6/4) e electronics não existe, embora os nomes indiquem instrumentos elétricos.
- Baterias têm shells/pieces/hardware; teclados têm keys/type/polyphony.
- Peso, dimensões e CEP de entrega do pedido não estão disponíveis para um cotador de frete completo.

Não aplicar o mesmo filtro de cordas a todas as categorias. Não interpretar electronics ausente como instrumento acústico. Um filtro genérico electric=true também pode excluir guitarras reais por não existir esse campo. Não inferir material maciço apenas de uma espécie de madeira ou captação externa a partir de afinador integrado.

## 10. Ambiguidades e informações distintas no manual

Fonte: `data/politicas_da_loja.pdf`.

| Local | Evidência | Cuidado |
| --- | --- | --- |
| 5.1, página 4 | Grátis acima de R$ 500; R$ 35 abaixo de R$ 500. | Exatamente R$ 500 não foi definido. Não inventar a taxa; a rodada C19 fez isso. |
| Capa e 1.2, páginas 1–2; seção 7, página 6 | (67) 3341-4444 versus WhatsApp (67) 3321-4500. | São dois números diferentes, ambos associados a contato/WhatsApp em partes do manual. Não concluir que um é erro de digitação. A escolha de um canal específico precisa citar sua seção e reconhecer a divergência quando relevante. |
| Capa e 1.2 | E-mail com domínio sem acento na capa e com acento na tabela. | São strings diferentes. Domínio com acento não deve ser declarado inválido só por ter acento; não normalizar ou escolher silenciosamente sem confirmação. |
| 4.2 e 8.1–8.2 | Troca em 30 dias da compra; garantia legal em 90 dias do recebimento; fabricante entre 6 meses e 2 anos. | Finalidades e marcos de contagem diferentes. Não negar toda garantia após 30 dias nem inventar cobertura específica de uma marca. |
| 4.4 | Exclusões para personalização, liquidação com aviso de venda final e boquilhas. | Não aplicar inelegibilidade a toda promoção automaticamente; o aviso explícito não está identificado em campos estruturados dos pedidos. Dúvidas devem ser encaminhadas conforme a seção 10. |
| 7.3 e 10 | Registro/encaminhamento de reclamação, retorno em 24 horas úteis e consulta à gerência em dúvida. | São procedimentos da loja. O protótipo só consulta e orienta; não pode afirmar que registrou ou transferiu algo. |

Esta é uma análise de consistência do manual fictício, não uma validação jurídica de suas políticas. Não foram pesquisadas regras externas para substituir o material do desafio.

## 11. O que não apareceu na revisão

- Nenhuma chave primária duplicada nas cinco tabelas com ID próprio; nenhuma referência órfã entre produtos/categorias, pedidos/clientes, itens e promoções.
- Todos os 20 pedidos têm itens. Os JSONs de specs são objetos válidos. Não há preço ou estoque negativo no catálogo.
- Os oito rastreamentos preenchidos correspondem ao padrão descrito no manual. Isso não valida o código numa transportadora real; nenhum foi consultado externamente.
- A busca textual local por padrões comuns de instrução maliciosa não encontrou ocorrência nos textos examinados. Isso não garante ausência de todo conteúdo oculto ou ataque possível nos PDFs.
- Não foram enviados dados à Groq ou outro serviço nesta auditoria. Os originais permanecem intactos.

## Como isso deve orientar as correções

Documentar fonte, ambiguidade e suposição; preservar valores originais; validar identidade e descontos em código; consultar registros indisponíveis ao procurar um modelo específico; distinguir ausência de informação de valor falso; recusar conclusões que as fontes não sustentam. As falhas da rodada real continuam válidas: inconsistência de dados não justifica inventar respostas.

O enunciado permite assumir interpretações razoáveis e documentá-las no README quando houver ambiguidade. As decisões propostas neste documento ainda não equivalem a correções implementadas.
