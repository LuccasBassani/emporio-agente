# Exemplos de atendimento e revisão

As cinco conversas abaixo foram executadas em 03/11/2026 com `gemini-3.5-flash-lite`, pela interface via Streamlit AppTest e API real. As falas são reproduzidas das exportações, sem reescrita. Os arquivos vinculados preservam também consultas e fontes.

## 1. Catálogo e continuidade no PIX

O cliente pede duas opções e depois se refere à primeira. O agente consulta os CSVs e usa o preço calculado em Python.

**Cliente**

Quero duas opções de violões disponíveis até R$ 1.000. Mostre nome e preço.

**Lia**

Olá! Temos estas opções de violões disponíveis dentro do seu orçamento:

* Tagima Memphis AC-39 Nylon Natural – R$ 429,90 sem frete [D83].
* Rozini RC-104 Nylon Estudante – R$ 459,90 sem frete [D85].

**Cliente**

E o primeiro no PIX?

**Lia**

O violão Tagima Memphis AC-39 Nylon Natural sai por R$ 408,41 sem frete no pagamento via PIX [D83].

Arquivo completo: [catálogo e PIX](../examples/catalogo-e-pix.md).

## 2. Promoção e desconto não cumulativo

A resposta combina a consulta do produto com a regra de promoção. Mantém a ressalva de apresentação: o texto não explicita a condição sem frete.

**Cliente**

Quanto fica o Ohana CK-20 no PIX? Posso somar os 5% à promoção?

**Lia**

O Ohana CK-20 Concert Natural sai por R$ 439,20 no PIX (preço original de R$ 549,00 com 20% de desconto promocional) [D121].

Não é possível somar o desconto de PIX à promoção, pois as regras da loja determinam que as promoções não são cumulativas e o desconto de PIX não se aplica sobre preços já promocionais [P6.2-p6-1].

Arquivo completo: [promoção e PIX](../examples/rag-promocao-pix.md).

<!-- pagebreak -->

## 3. Aplicação da política de parcelamento

O agente recupera a seção específica do manual e verifica a condição de parcela mínima.

**Cliente**

Uma compra de R$ 480 pode ser dividida em seis vezes sem juros?

**Lia**

Sim, uma compra de R$ 480,00 pode ser dividida em seis vezes sem juros, pois o valor da parcela (R$ 80,00) atinge o mínimo exigido para essa quantidade de parcelas [P3.1-p3-1].

Arquivo completo: [parcelamento](../examples/rag-parcelamento.md).

## 4. Status e rastreamento de pedido

Consulta feita com **Cliente #2** selecionado. Preserva o total histórico e o rastreamento cadastrado. A expressão inglesa "shipped" é uma ressalva de linguagem.

**Cliente**

Qual o status, total e rastreamento do meu pedido 8?

**Lia**

O seu pedido 8 está com o status de enviado (shipped) e o código de rastreamento é BRJL5544332BR [O8]. O valor total histórico é de R$ 349,90 [O8].

Arquivo completo: [pedido e rastreamento](../examples/pedido-rastreamento.md).

## 5. Pergunta fora do escopo

A regra de atendimento restringe a loja a instrumentos. Esta conversa não executou nova consulta.

**Cliente**

Vocês vendem cabos, palhetas ou amplificadores?

**Lia**

Olá! Na Empório da Música, nós somos especializados em instrumentos musicais, como violões, guitarras, baixos, teclados, baterias e outros instrumentos de cordas, sopro e percussão.

Cabos, palhetas e amplificadores são acessórios e não fazem parte do nosso catálogo de instrumentos.

Posso te ajudar a encontrar algum instrumento específico?

Arquivo completo: [fora do escopo](../examples/fora-do-escopo.md).

<!-- pagebreak -->

## Critérios de revisão e ajustes

Orientei os testes a partir do comportamento esperado no atendimento: fatos apoiados nas fontes, preço correto, continuidade de contexto, respeito ao escopo e acesso restrito aos pedidos. Também defini expectativas de tom e coleta das informações necessárias antes de orientar devoluções.

A execução foi apoiada por automação e Codex. A revisão das respostas e a priorização das correções fizeram parte da minha condução do projeto. Três casos ilustram esse processo:

| Problema observado | Ajuste implementado | Verificação registrada |
| --- | --- | --- |
| Pedido sem identificação ou pertencente a outro cliente terminava em erro de referência. | Orientação determinística a partir do resultado da ferramenta, sem revelar o pedido. | C24 e C27 aprovados nos retestes. |
| Produto descontinuado foi descrito como esgotado, apesar de ter quantidade cadastrada. | Instrução distingue status comercial e quantidade em estoque. | C13 informou descontinuado com 13 unidades, sem oferecer compra. |
| A resposta acrescentou "sem frete" ao total histórico de um pedido. | Validação conservadora e teste de regressão para a condição não informada. | C25 repetido com total, status e rastreio corretos, sem afirmar composição de frete. |

Os retestes demonstram o resultado desses casos. A avaliação ainda registrou ressalvas de linguagem e triagem, e o conjunto completo não foi repetido após o último ajuste.

## Melhorias com mais tempo

Começaria pelos controles de resposta e pelo contexto do atendimento. A evolução das consultas acompanharia o crescimento da base, com avaliação de qualidade a cada mudança.

1. **Guardrails e triagem:** validar afirmações de preço, estoque e políticas contra os resultados das ferramentas; estruturar os dados pendentes da triagem e encaminhar dúvidas à equipe. Ampliaria os testes com perguntas novas e tentativas de desviar as regras.
2. **Contexto de atendimentos anteriores:** manter resumos e campos relevantes por cliente identificado, como instrumento de interesse, orçamento e condições já informadas. A recuperação respeitaria autorização e retenção definida; preço, estoque e políticas vigentes seriam consultados novamente nas fontes.
3. **RAG para mais documentação:** avaliar busca híbrida com BM25 e embeddings, seguida de reranking. Refinaria a divisão dos documentos em trechos com contexto, metadados de seção e controle de versão/vigência. Compararia recuperação e fidelidade em um conjunto de perguntas independente.
4. **Consultas para bases maiores:** substituir a leitura dos CSVs por banco de dados ou APIs operacionais, com filtros, índices e paginação. Manteria ferramentas com parâmetros e permissões definidos, preservando os cálculos de preço e as regras de acesso no código.
5. **Fine-tuning de comportamento:** após melhorar dados, prompts e validações, avaliaria um modelo compatível com conversas revisadas para tom, triagem e escolha de ferramentas. Separaria treino e avaliação para medir ganho frente ao modelo base. Preços e disponibilidade continuariam consultados nas fontes.

Autenticação real e integrações de estoque e pedidos seriam necessárias para uso operacional. Essas melhorias são propostas de evolução; a entrega mantém o escopo de protótipo.

Relatórios e exemplos: [avaliação com Gemini](validacao-gemini-2026-11-03.md) e [índice das cinco conversas](../examples/README.md). As decisões de implementação estão resumidas no [README](../README.md).
