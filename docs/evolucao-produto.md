# O que melhoraríamos com mais tempo

O protótipo prioriza um atendimento reproduzível com Python, fontes inspecionáveis e consultas de leitura. Esta lista descreve evolução proposta para um produto real; não são funcionalidades existentes nem requisitos adicionais para executar o desafio.

| Prioridade | Melhoria | Por que importa | Como avaliar |
| --- | --- | --- | --- |
| 1 | Governança do catálogo e das políticas | As fontes divergem e não têm histórico operacional completo. Validar cadastros na origem, definir responsáveis, versão e vigência; manter um fluxo de revisão das observações. | Redução de conflitos abertos; rastreabilidade de qual versão fundamentou cada resposta; nenhuma alteração silenciosa de histórico. |
| 1 | Identificação e autorização reais | A escolha de cliente na tela é apenas demonstração. Integrar autenticação e autorização por pedido, com minimização de dados e separação de sessões. | Testes de acesso cruzado, expiração de sessão e ausência de exposição de dados pessoais em logs ou respostas. |
| 1 | Avaliação contínua do atendimento | Os exemplos atuais são pequenos e o comportamento depende do modelo. Ampliar paráfrases, conversas longas, perguntas ambíguas e tentativas de desviar as regras. Separar acerto factual, estilo e falha de execução. | Comparar versões sobre conjunto fixo e perguntas novas; medir escolha de ferramenta, fidelidade à fonte, triagem e conclusão do atendimento. |
| 2 | Triagem estruturada de devolução e garantia | A instrução de uma pergunta por vez não garante coleta completa. Modelar campos pendentes e estados de atendimento, com confirmação humana para decisões e exceções. | Nenhuma elegibilidade confirmada sem dados obrigatórios; aproveitamento de informações já fornecidas; encaminhamento em caso de dúvida. |
| 2 | Integrações operacionais e atendimento humano | Os CSVs são uma fotografia. Conectar estoque, pedidos, frete e suporte por interfaces autenticadas. Separar claramente consulta de qualquer ação de escrita e exigir confirmação quando cabível. | Contratos de integração, dados atualizados, protocolo real quando houver registro e recuperação de erros sem duplicar ações. |
| 2 | Histórico e observabilidade com retenção definida | Hoje o histórico é de sessão. Salvar somente o necessário, com consentimento/regras de retenção, controle de acesso e registros de consultas, erros, latência, consumo e versões de configuração. | Reproduzir incidentes sem registrar credenciais ou dados excessivos; apagar dados conforme a retenção definida. |
| 3 | Comparar recuperação e modelos | BM25 é simples para este manual. Testar busca híbrida/semântica e reranking apenas se houver falhas medidas. Comparar modelos locais e APIs usando o mesmo conjunto de avaliação. | Ganho de relevância e fidelidade que justifique custo, latência e complexidade adicionais; não assumir que embeddings são automaticamente melhores. |

## Provedor e capacidade de execução

Cotas pertencem ao provedor e ao plano escolhido. Para operação contínua, dimensionar volume esperado, modelo, disponibilidade e orçamento; medir chamadas e tokens por atendimento. Um plano com capacidade adequada pode remover o gargalo observado no plano gratuito, mas qualquer novo modelo/provedor precisa passar pela mesma avaliação funcional.

O programa deve informar falhas com clareza e preservar o contexto válido. O intervalo entre chamadas é uma opção de execução, desativada por padrão; não é uma solução geral para toda cota. Eventual retry futuro deve considerar o tipo de erro e a indicação do provedor, sem repetir operações de escrita nem mudar silenciosamente o destino dos dados.

## O que evitaríamos agora

Não adicionaríamos infraestrutura de produção, canais reais ou um banco vetorial apenas para aumentar a quantidade de tecnologias. A próxima etapa seria corrigir os casos reproduzidos e comparar os resultados antes e depois. Cada evolução acima deve responder a uma necessidade observada e ter um critério de aceitação.
