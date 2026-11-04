# Guia para acompanhar o projeto

Este guia acompanha a construção do agente de atendimento da Empório da Música. Atualizar os itens somente depois de executar e conferir cada etapa.

## Onde estamos

- [x] Ler o enunciado e os arquivos fornecidos.
- [x] Examinar a experiência de configuração e simulação de atendimento de um projeto já desenvolvido.
- [x] Criar documentação inicial e .gitignore.
- [x] Criar repositório privado no GitHub e enviar o primeiro commit.
- [x] Registrar este plano de trabalho.
- [x] Configurar o ambiente Python.
- [x] Implementar conectores Groq/Ollama e testar contratos HTTP simulados.
- [x] Validar conexão e ferramentas com Groq em chamadas reais.
- [ ] Validar o conector Ollama com modelo local.
- [x] Implementar e validar consultas de catálogo, disponibilidade, promoções e PIX.
- [x] Implementar consultas de pedidos por cliente de teste.
- [x] Recuperar as políticas por pergunta e verificar o conjunto inicial de perguntas.
- [x] Validar dois cenários reais de políticas com Groq e registrar evidências.
- [x] Integrar o modelo às ferramentas de catálogo e recuperação de políticas.
- [x] Montar configuração, chat e exportações.
- [x] Executar verificação inicial do conjunto e salvar cinco exemplos reais.
- [x] Tentar os 32 cenários da persona pela interface e salvar resultados/evidências locais em 02/11.
- [x] Implementar correções de consulta, notas de auditoria, validação e instruções de triagem.
- [x] Registrar a revalidação priorizada com respostas, ressalvas e interrupções do provedor separadas.
- [x] Concluir as pendências priorizadas na retomada Qwen de 03/11.
- [x] Executar os 32 com Gemini Flash-Lite, registrar falhas e repetir os casos afetados após ajustes.
- [x] Selecionar cinco conversas reais e preparar a exportação do README/documentação em PDF.
- [ ] Revisar a entrega e tornar o repositório público.

O protótipo tem interface e terminal com catálogo, preços, RAG, pedidos por cliente de teste, configuração e exportações. A Groq passou nos cenários reais registrados, incluindo consulta de pedido pela interface. O navegador foi usado para conferir o envio de mensagem, importação de configuração e downloads. Ollama está preparado, mas ainda sem validação real local. A documentação atual registra a avaliação e as ressalvas da versão de entrega.

## Como acompanhar a versão atual

A Lia já inicia com a persona definida; alterar nome, tom ou instruções é opcional. Para a rodada de avaliação, siga o [roteiro de 32 cenários](cenarios-de-teste.md), com perguntas, resultados esperados e espaço para registrar execuções. Uma nova sessão carrega o padrão atualizado; importar configuração antiga mantém as preferências daquele arquivo.

A [avaliação Gemini de 03/11](validacao-gemini-2026-11-03.md) registra a rodada integral dos 32 e os retestes dirigidos. As [execuções anteriores](revalidacao-correcoes-2026-11-02.md) ficam como histórico. A suíte final tem 61 testes locais passando; a qualidade de conteúdo e as ressalvas do modelo são registradas separadamente.

1. Na pasta do projeto, execute `.\.venv\Scripts\python.exe -m streamlit run app.py` e abra http://127.0.0.1:8501.
2. Ajuste nome, tom, instruções e provedor. Clique em **Aplicar e iniciar nova conversa**.
3. Pergunte por dois violões até R$ 1.000 e depois pergunte pelo preço do primeiro no PIX. Confira as consultas no expansor da resposta.
4. Baixe a conversa antes de mudar o contexto. Selecione **Cliente #2** e consulte o **pedido 8**. Uma consulta a pedido de outro cliente não deve expor seus dados.
5. Teste uma dúvida de política e confira os trechos recuperados do PDF. Os testes já exportados estão em examples/.
6. Baixe a configuração JSON, altere uma preferência e importe o arquivo anterior para reproduzir a configuração. Não é necessário informar chave no JSON.

Trocar cliente ou aplicar/importar configuração limpa a conversa. A sessão não é salva automaticamente; use o download. A API gratuita pode exigir intervalo entre mensagens ou uma nova tentativa depois de renovar a cota.

## Prazo e prioridade

Entrega informada: 03/11/2026 às 23h59. Horário de referência deste planejamento: America/Sao_Paulo; conferir eventual fuso diferente no e-mail.

O planejamento inicial priorizou uma primeira versão completa em 31/10. Em 02/11, a prioridade passou a ser corrigir casos reproduzidos, concluir a revalidação e preparar os exemplos e a publicação final. A tabela abaixo registra o plano inicial; o checklist e o diário registram o andamento efetivo.

| Período | Prioridade | Resultado a conferir |
| --- | --- | --- |
| 31/10, primeiro bloco | Ambiente, dados e consultas | Encontrar instrumentos e calcular preços sem usar IA |
| 31/10, segundo bloco | Políticas e acesso ao modelo | Recuperar trechos relevantes e testar a conexão com a API |
| 31/10, terceiro bloco | Agente e interface mínima | Fazer uma conversa completa e exportá-la |
| 01/11 | Corrigir falhas e ampliar cenários | Validar catálogo, promoções, pedidos, devoluções e escopo |
| 02/11 | Exemplos e documentação | Rodar de 3 a 5 conversas e verificar instalação reproduzível |
| 03/11 | Revisão e entrega com margem | Conferir o repositório público e enviar o link antes do prazo |

## Decisões e propostas

| Tema | Situação | Direção |
| --- | --- | --- |
| Linguagem | Exigência do desafio | Python como linguagem principal |
| Infraestrutura | Combinado | Aplicação independente, inspirada na interação de um projeto já desenvolvido |
| GitHub | Concluído | Repositório privado durante o desenvolvimento; público para entregar |
| Uso de IA | Exigência de transparência | Registrar a assistência efetivamente utilizada |
| API | Decisão confirmada | Groq no plano gratuito ou Ollama local; nenhum gasto pago autorizado |
| Interface | Implementado | Streamlit para configuração, chat e exportações |
| Dados | Implementado | Funções Python sobre os CSVs; cálculos e validações no código |
| Políticas | Implementado e verificado localmente | RAG lexical BM25, com seção/página e 14 perguntas de recuperação |
| Identificação | Implementado para demonstração | Selecionar um cliente fictício e restringir pedidos a esse cliente |
| Publicação da aplicação | Fora da primeira versão | Rodar localmente com instruções reproduzíveis |

Antes de testar o modelo, configurar a chave Groq e confirmar as cotas ou instalar/iniciar Ollama com o modelo escolhido. Os conectores suportam ferramentas, mas o comportamento real de cada modelo ainda precisa ser validado.

## Como o agente vai funcionar

1. A pessoa escreve no chat.
2. O modelo recebe as regras do atendimento e o histórico necessário.
3. Quando precisa de uma informação externa, solicita uma ferramenta com parâmetros.
4. O Python valida esses parâmetros e consulta os CSVs ou os trechos das políticas.
5. O resultado volta para o modelo, que redige a resposta para o cliente.
6. A interface mostra a conversa e permite consultar as fontes e exportar o teste.

O modelo não executa Python sozinho. Nosso programa decide quais funções existem e quais solicitações pode executar. O histórico permite entender continuações como “e esse no PIX?”.

O uso conjunto de ferramentas para dados estruturados e recuperação de políticas será descrito como arquitetura híbrida. Não chamar a busca de semântica se implementarmos apenas busca textual.

## Etapa 1 — Preparar o ambiente

**Vamos fazer:** verificar a versão de Python disponível, criar um ambiente virtual, definir dependências, preparar a estrutura de pastas e um .env.example sem chave real. Trazer os dados fornecidos para a pasta de dados do projeto, preservando os originais.

**Conceitos envolvidos:** ambiente virtual, execução do programa e separação entre código, dados e configurações.

**Concluída quando:** for possível instalar as dependências e executar um comando inicial seguindo as instruções do README. As credenciais devem continuar ignoradas pelo Git.

**Commit sugerido:** `chore: prepara ambiente Python e estrutura inicial`.

## Etapa 2 — Consultar catálogo e preços

**Vamos fazer:** ler produtos, categorias e promoções, normalizar os campos necessários e implementar funções de busca por nome, categoria, orçamento e disponibilidade.

Definir explicitamente se o orçamento filtra o preço de tabela ou o preço final. Calcular valores monetários com precisão decimal e arredondamento em centavos. Produtos com estoque zero, descontinuados e coming_soon precisam de respostas distintas. Promoção inativa não pode alterar preço; desconto promocional e PIX não se acumulam.

**Conceitos envolvidos:** funções de consulta, filtros e testes de regras de negócio.

**Concluída quando:** “violões disponíveis até R$ 1.000” trouxer resultados verificáveis nos arquivos, e testes cobrirem estoque/status, promoção ativa/inativa e não acumulação com PIX.

**Commit sugerido:** `feat: consulta catalogo e calcula precos`.

## Etapa 3 — Consultar pedidos do cliente de teste

**Vamos fazer:** relacionar cliente, pedido e itens. A seleção do cliente acontece fora dos argumentos controlados pelo modelo. Toda consulta deve conferir a associação entre cliente e pedido.

**Conceitos envolvidos:** relacionamentos por ID e controle de acesso aos pedidos.

**Concluída quando:** um pedido do cliente escolhido for exibido corretamente, um pedido de outro cliente for recusado e rastreamento ausente não for inventado. Conservar o total registrado no pedido.

**Limitação a declarar:** a seleção de cliente é uma simulação de contexto autenticado, não autenticação de produção.

**Commit sugerido:** `feat: consulta pedidos por cliente de teste`.

## Etapa 4 — Recuperar as políticas

**Vamos fazer:** extrair o texto do PDF, separar por seções e manter a página de origem. Implementar e avaliar a busca com perguntas conhecidas e reformuladas.

**Conceitos envolvidos:** recuperação de trechos por pergunta e rastreabilidade das fontes.

**Concluída quando:** perguntas sobre horários, pagamento, promoções, devoluções e garantia recuperarem as seções pertinentes. Perguntas sem informação suficiente devem expor a ausência ou ambiguidade.

**Regra de evolução:** registrar falhas de recuperação antes de escolher uma técnica mais complexa. Não prometer ganho de qualidade sem comparação.

**Commit sugerido:** `feat: recupera politicas com referencia de origem`.

## Etapa 5 — Conectar o modelo às ferramentas

**Vamos fazer:** validar o acesso ao provedor gratuito escolhido, definir a persona e as ferramentas, montar o ciclo de chamadas e manter o histórico da conversa.

Tratar limite de uso, indisponibilidade, parâmetros inválidos e limite de chamadas por turno. Não afirmar que houve atendimento humano, reserva ou devolução realizada se o programa não executa essas ações.

**Conceitos envolvidos:** mensagens de sistema/usuário, integração com API e chamadas de ferramentas.

**Concluída quando:** uma conversa real usar uma ferramenta, receber seu resultado e responder com os dados corretos. A chave deve permanecer fora do Git e das exportações.

**Commit sugerido:** `feat: integra modelo ao agente e suas ferramentas`.

## Etapa 6 — Configuração, chat e exportação

**Vamos fazer:** montar a interface com nome/tom/instruções adicionais, cliente de teste, mensagens, nova conversa e exportação. Exportar conversa em Markdown ou texto e configuração em JSON.

As instruções adicionais personalizam o atendimento; não substituem as regras fixas sobre fontes, acesso a pedidos e descontos. Mudanças de cliente devem começar uma nova conversa para evitar mistura de dados.

**Conceitos envolvidos:** estado da sessão, integração da interface com o agente e separação entre configuração e credencial.

**Concluída quando:** a configuração afetar uma nova conversa, o contexto continuar entre mensagens e os arquivos exportados abrirem corretamente sem chave ou dados de outros clientes. Mostrar ferramentas/fontes consultadas, sem exibir raciocínio interno do modelo.

**Commit sugerido:** `feat: adiciona configuracao chat e exportacao`.

## Etapa 7 — Testar e registrar evidências

**Vamos fazer:** executar os testes das regras críticas e conversas completas. Comparar cada resposta com os dados e políticas. Registrar defeitos encontrados e os ajustes realizados.

Conversas propostas para os exemplos de entrega:

1. Buscar violões por orçamento e fazer uma pergunta de continuação.
2. Consultar produto promocional e perguntar sobre pagamento por PIX.
3. Consultar um pedido e lidar com informação ausente.
4. Pedir devolução, informando os dados necessários ao longo da conversa.
5. Pedir acessório ou produto indisponível e receber orientação coerente.

**Concluída quando:** houver entre 3 e 5 exemplos reais exportados e revisados, incluindo situação não trivial. Teste manual e teste automatizado devem ser identificados como tais. Respostas escritas à mão não contam como execução do agente.

**Commits sugeridos:** correções com `fix:` e exemplos/testes com `test:` ou `docs:`, conforme o conteúdo efetivo.

## Etapa 8 — Preparar a entrega

**Vamos fazer:** testar a instalação em ambiente limpo, revisar o README, documentar limitações, conferir os arquivos versionados e a declaração de uso de IA.

**Concluída quando:** outra pessoa conseguir executar o projeto com sua própria chave, os exemplos estiverem no repositório e o histórico mostrar as etapas reais. Tornar o repositório público para a entrega após revisar seu conteúdo.

**Ação do candidato:** responder ao e-mail do processo com o link. O envio não está autorizado neste momento. Não alterar o repositório depois do horário efetivo de entrega.

## Como vamos trabalhar juntos

Em cada etapa: explicar o objetivo, implementar um incremento pequeno, executar a verificação, discutir o resultado e atualizar a documentação. Salvar um commit correspondente à mudança real e enviá-lo ao GitHub.

Não precisa escrever um diário longo. Para cada decisão relevante, responder:

- Qual problema apareceu?
- Qual opção escolhemos e por quê?
- Como conferimos que funciona?
- O que continua limitado ou pendente?

## Pontos para apresentação técnica

- [ ] Explicar por que escolheu a interface e a arquitetura.
- [ ] Mostrar uma consulta de catálogo sem depender do modelo.
- [ ] Explicar como o modelo solicita uma ferramenta e recebe o resultado.
- [ ] Mostrar de onde saiu uma resposta sobre políticas.
- [ ] Explicar como pedidos ficam restritos ao cliente de teste.
- [ ] Demonstrar uma falha encontrada e a correção.
- [ ] Explicar as limitações e onde a IA ajudou.

## Próxima ação

Conferir o PDF e os cinco exemplos selecionados e finalizar a revisão para publicação do repositório. Ollama ainda precisa de validação com modelo local. Manter o repositório privado até a revisão para publicação exigida pelo desafio.
