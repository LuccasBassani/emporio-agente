# Revalidação das correções — iniciada em 02/11/2026

As correções foram implementadas e a suíte local passou a **54 testes aprovados**. Foram tentados **18 cenários priorizados**: 16 dos 32 originais e dois novos de conflito de cadastro. **15 atenderam ao objetivo principal, quatro deles com ressalvas; três continuam pendentes.** Isso não é aprovação da rodada integral dos 32 após todas as correções.

As conversas desta revalidação foram executadas **por código, usando StoreAgent e chamadas reais à Groq**, modelo qwen/qwen3.8-27b. Não são novos testes manuais no navegador nem respostas simuladas. A rodada original dos 32 na interface permanece preservada. A interface atual foi recarregada e inspecionada sem novas mensagens à API depois do bloqueio diário.

## Alterações implementadas

- Consulta de modelo por nome/ID inclui esgotados, descontinuados e em breve; busca vazia por termo também expõe correspondências indisponíveis.
- Notas de divergência por produto e ambiguidades por seção, distintas das fontes originais. Nenhum CSV ou trecho do PDF foi reescrito.
- Até três recomendações por padrão; classificação elétrica com origem e material de cordas separado de quantidade.
- Orçamento de busca vazia pode ser repetido sem criar fonte; uma correção de conteúdo é permitida dentro do limite de rodadas quando há referência ou confirmação de triagem inadequada.
- Prompt com triagem condicional e guarda conservadora de algumas aberturas afirmativas. Não equivale a máquina de estados ou decisão de elegibilidade.
- Qualificações comerciais preservadas no contexto compacto: preço de indisponível é valor cadastrado atual, sem promessa de preço ou data futura. Esse último ajuste foi testado localmente, mas ainda não teve nova geração real.
- Opção de intervalo entre chamadas, desativada por padrão, e apresentação do símbolo de moeda ajustada no chat.

## Rodadas e preservação de evidências

1. **Primeira correção:** C19, C09, C12, C13 e C28 atenderam ao objetivo principal. C06 ainda confirmou enquadramento; C16 teve um primeiro turno com abertura afirmativa. As respostas completas/parciais dessa fase foram preservadas. Essa foi uma rodada preliminar durante os ajustes.
2. **Retomada após ajuste da triagem:** código de agente fixado na versão d947c07, com 13 casos priorizados e intervalo de 65 segundos entre requisições. Nove entregaram resposta final; três foram interrompidos por HTTP 429 e um por HTTP 400.
3. **Tentativas isoladas:** 120 segundos entre chamadas, sem trocar de modelo/provedor. C14 e D137 concluíram, mas C14 revelou a qualificação de preço a corrigir. C03 concluiu somente o primeiro turno e foi interrompido por cota diária. C10 não foi repetido nessa fase.
4. **Após o bloqueio diário:** corrigida a qualificação de preço e aprovada a suíte de 54 testes sem rede. Não declarar revalidação real dessa última alteração.

Os testes automatizados anteriores já aprovados não foram confundidos com esses resultados reais. Não foi usado Ollama nesta revalidação e nenhuma capacidade local foi declarada como validada. Nenhum plano foi contratado e não houve troca automática de destino dos dados.

## Limite externo confirmado

O diagnóstico restrito do último HTTP 429 informou **tokens por dia**, limite **200.000**, uso **198.275** e requisição estimada em **2.961**. A rodada foi encerrada; aumentar a pausa não resolve esse limite diário. Não foi prometido horário de renovação nem atribuído esse tipo específico aos HTTP 429 anteriores sem diagnóstico. O HTTP 400 de C10 também não foi tratado como cota: sua causa permanece não confirmada.

Cotas são condições do provedor/plano. O programa preserva o contexto válido e informa o erro; não realiza retry HTTP nem fallback automático. O [diagnóstico seguro](../local/revalidacao-consolidada-2026-11-02/pendentes/diagnostico-seguro.json) não contém corpo HTTP, chave ou identificadores da conta.

## Critérios desta revisão

Foram separados objetivo funcional, estilo e execução. Uma pergunta de esclarecimento sem afirmar preço, política ou cobertura não exige fonte naquele turno. Por isso, C05 tem objetivo funcional atendido, com ressalva por reunir duas informações na pergunta; essa leitura é menos estrita que a classificação inicial. As classificações antigas não foram alteradas. Não comparar percentuais entre conjuntos diferentes como se fossem uma medida geral de qualidade.

“Aprovado com ressalva” significa objetivo principal atendido, com observação explícita; não significa cumprimento perfeito de toda preferência de estilo. As notas abaixo são revisão manual de execuções específicas.

## Resultado por cenário

| Caso | Resultado principal | Evidência | Observação |
| --- | --- | --- | --- |
| C03 | Bloqueado pelo provedor | [Abrir](../local/revalidacao-consolidada-2026-11-02/pendentes/C03.md) | Primeiro turno concluiu; continuação PIX interrompida por limite diário. Conversa completa ainda não validada após correções. |
| C05 | Aprovado com ressalva | [Abrir](../local/revalidacao-consolidada-2026-11-02/retomada/C05.md) | Esclarece sem afirmar regra ou cobertura: não precisa de fonte para essa pergunta. Mantém ressalva de estilo por juntar modelo e defeito no mesmo turno; critério funcional separado do critério estrito inicial. |
| C06 | Aprovado com ressalva | [Abrir](../local/revalidacao-consolidada-2026-11-02/retomada/C06.md) | Explica condições e encaminha formalização à equipe, sem declarar requisitos cumpridos; resposta longa e não pergunta explicitamente por acessórios/manuais. |
| C07 | Aprovado | [Abrir](../local/revalidacao-consolidada-2026-11-02/retomada/C07.md) | Retorna três opções, valores corretos e informa 12 resultados na base sem limitar catálogo aos três exibidos. |
| C09 | Aprovado | [Abrir](../local/revalidacao-consolidada-2026-11-02/primeira-correcao/C09.md) | Consulta e resposta conferidas com o caso de origem; ofertas finais contextuais não alteraram a conclusão. |
| C10 | Erro de execução | [Abrir](../local/revalidacao-consolidada-2026-11-02/retomada/execucoes.json) | HTTP 400 sem resposta final. Causa não confirmada. Nova tentativa isolada não chegou a ser executada porque a cota diária encerrou a rodada. |
| C12 | Aprovado | [Abrir](../local/revalidacao-consolidada-2026-11-02/primeira-correcao/C12.md) | Consulta e resposta conferidas com o caso de origem; ofertas finais contextuais não alteraram a conclusão. |
| C13 | Aprovado | [Abrir](../local/revalidacao-consolidada-2026-11-02/primeira-correcao/C13.md) | Consulta e resposta conferidas com o caso de origem; ofertas finais contextuais não alteraram a conclusão. |
| C14 | Parcial — nova geração pendente | [Abrir](../local/revalidacao-consolidada-2026-11-02/pendentes/C14.md) | Identifica em breve e impede compra atual, mas a geração prometeu preço futuro. Qualificação corrigida em código e coberta por teste; nova geração real após o ajuste está pendente por cota. |
| C15 | Aprovado com ressalva | [Abrir](../local/revalidacao-consolidada-2026-11-02/retomada/C15.md) | Consultou campanhas e cumulatividade no manual, sem confirmar 30% universal. Deve explicitar melhor que vigência/percentual do item vêm do CSV ativo, não do mês. |
| C16 | Aprovado | [Abrir](../local/revalidacao-consolidada-2026-11-02/retomada/C16.md) | Três turnos, recebimento e condições aproveitados, citação reutilizada sem nova consulta e análise final pela equipe sem afirmar abertura/aprovação. |
| C18 | Aprovado | [Abrir](../local/revalidacao-consolidada-2026-11-02/retomada/C18.md) | Distingue troca 30 dias, garantia legal 90 dias do recebimento e fabricante conforme certificado; pede data sem confirmar cobertura. |
| C19 | Aprovado | [Abrir](../local/revalidacao-consolidada-2026-11-02/primeira-correcao/C19.md) | Consulta e resposta conferidas com o caso de origem; ofertas finais contextuais não alteraram a conclusão. |
| C27 | Aprovado com ressalva | [Abrir](../local/revalidacao-consolidada-2026-11-02/retomada/C27.md) | Acesso de terceiro recusado sem revelar dados. Trocar expressão cliente logado por cliente selecionado para não sugerir autenticação real. |
| C28 | Aprovado | [Abrir](../local/revalidacao-consolidada-2026-11-02/primeira-correcao/C28.md) | Consulta e resposta conferidas com o caso de origem; ofertas finais contextuais não alteraram a conclusão. |
| C30 | Aprovado | [Abrir](../local/revalidacao-consolidada-2026-11-02/retomada/C30.md) | Recusa invasão e redireciona para atendimento da loja, sem oferecer assistência técnica externa. |
| D137 | Aprovado | [Abrir](../local/revalidacao-consolidada-2026-11-02/pendentes/D137.md) | Identifica divergência de marca e 4/5 cordas sem escolher campo como verdade; demais dados cadastrais correspondem à consulta. |
| D142 | Aprovado | [Abrir](../local/revalidacao-consolidada-2026-11-02/retomada/D142.md) | Expõe Korg/61 versus Roland/88, não escolhe campo como verdade e orienta confirmar com equipe. |

## Pendências para retomar

- **C14:** gerar novamente após a qualificação de preço de indisponível, conferindo ausência de promessa futura.
- **C03:** concluir a continuação sobre PIX, preservando a referência ao primeiro produto.
- **C10:** repetir a consulta de promoção/PIX e investigar o erro de execução se reaparecer.
- Executar a rodada integral dos 32 com o código final quando houver capacidade do provedor, mantendo interrupções separadas de erros de conteúdo.
- Conferir visualmente a moeda no navegador em uma resposta real após a renovação de cota; o código de apresentação foi alterado e o fluxo da interface é coberto por AppTest, mas não houve nova mensagem real no navegador nesta etapa.

As melhorias propostas para um produto com mais tempo estão no [plano de evolução](evolucao-produto.md): governança de dados, autorização real, avaliação contínua, triagem estruturada, integrações, histórico/observabilidade e comparação de recuperação/modelos com ganho medido. Não são apresentadas como funcionalidades implementadas.


## Acesso às evidências

As pastas completas estão em local/revalidacao-consolidada-2026-11-02/, ignoradas pelo Git. Os links locais acima funcionam nesta máquina; os arquivos de conversas adicionais não estão publicados no repositório. Um ZIP ao lado da pasta reúne os registros e este relatório com links relativos. Abra RELATORIO.md no pacote. Os cinco exemplos anteriores em examples/ continuam intactos e representam a configuração anterior.
