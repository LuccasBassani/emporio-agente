# Decisões e questões em aberto

Este documento registra escolhas implementadas, motivos e limitações. Pendências estão indicadas explicitamente.

## 1. Python e Streamlit

Motivo: atender à exigência de Python e concentrar interface e agente na mesma linguagem, reduzindo a complexidade de instalação e integração dentro do prazo de entrega.
Streamlit oferece elementos de chat e download de arquivos.
Alternativa considerada: interface React com API Python. Adicionaria duas aplicações e mais configuração sem necessidade para o protótipo.
Limitação: menor liberdade de interface que uma aplicação web personalizada.

Implementada tela com configuração e chat lado a lado, importação/exportação JSON e download de conversa em Markdown/TXT, com evidências opcionais. Aplicar ou importar configuração e trocar de cliente iniciam conversa nova. Dados de catálogo/políticas são compartilhados em cache de leitura, enquanto cliente HTTP, contexto de cliente e histórico ficam na sessão do usuário.

A chave não é um campo de configuração exportável. JSON importado aceita somente os campos conhecidos; campos extras, credenciais e identidade são rejeitados. A escolha de cliente fica fora do JSON de estilo/modelo.

Requisitos fixados: Python 3.12 ou superior, devido ao NumPy instalado como dependência do Streamlit. Ambiente testado: Python 3.14.4 no Windows.

## 2. Consultas estruturadas para dados operacionais

Implementada leitura direta dos CSVs por funções Python com parâmetros definidos. O modelo solicita a consulta; o código valida e executa. Preços, estoque, status e descontos não dependem de similaridade textual. SQLite não foi necessário para o tamanho e as consultas atuais.

Orçamento: filtrar pelo preço final arredondado para o pagamento escolhido, sem frete. Decimal com ROUND_HALF_UP evita aritmética binária de ponto flutuante. Promoção ativa prevalece; não aplicar PIX adicional. Sem promoção, PIX aplica 5% sobre a tabela. Múltiplas promoções ativas para um produto são consideradas ambíguas, sem selecionar uma arbitrariamente.

Disponibilidade: status active e estoque positivo. Preservar motivos distintos para esgotado, descontinuado e coming_soon. Estoque positivo não reativa um produto. Os dados são uma fotografia carregada no início da sessão.

Busca: normalizar acentos e consultar nome/categoria, sem usar descrições livres divergentes para identificar marcas ou modelos. Filtros de cordas e captação usam specs; valores ausentes não são inferidos. Ordenar pelo preço final e informar quando existem mais resultados do que os exibidos.

Agente: lista fechada de cinco ferramentas, limite de quatro rodadas por turno e histórico dos dois últimos turnos completos. Chamadas e respostas de ferramenta permanecem juntas; turnos com falha não entram no histórico. A exportação registra consultas completas, enquanto o contexto enviado ao modelo omite metadados repetidos para economizar tokens.

Pedidos: identidade vinculada pela aplicação e ausente do schema das ferramentas. Pedido de terceiro e pedido inexistente geram resposta equivalente. A seleção local simula identificação, sem pretender autenticação real. As ferramentas enviam somente número/status/itens/total/rastreamento e referências; não enviam nome, contato, notas ou data estimada de entrega. Preservar o total histórico e a ausência de rastreamento/data real de recebimento.

Limitação observada: uma conversa rápida na Groq atingiu a cota gratuita durante uma pergunta de continuação. Não fazer fallback ou retry automático; orientar nova tentativa após renovar a cota.

## 3. Recuperação de políticas

Implementado RAG lexical: extrair o PDF com pypdf em modo layout, separar por título de seção e página, limitar o tamanho dos trechos e preservar as continuações entre páginas. O manual atual gerou 27 trechos.

Ranking escolhido: BM25 com normalização de acentos e equivalências explícitas de vocabulário. Os títulos recebem peso adicional; até quatro trechos são fornecidos ao modelo por pergunta. Motivo: o manual é pequeno e a estratégia é local, inspecionável e não exige outro serviço de IA.

Verificação inicial: as seções esperadas foram recuperadas entre os quatro primeiros resultados nas 14 perguntas revisadas. Isso é cobertura desse conjunto, não garantia de relevância geral. Não há embeddings nem busca semântica. Se surgirem falhas em reformulações ou perguntas com vários assuntos, registrar o caso e comparar alternativas.

O modelo precisa citar IDs dos trechos fornecidos. IDs inexistentes e ausência de citações são rejeitados. Essa validação não verifica automaticamente se o conteúdo da resposta é fiel à fonte; é necessário revisar os exemplos gerados.

Validação real inicial: executados e revisados dois cenários na Groq, com autorização para envio dos trechos do manual. O cenário de devolução mostrou uma confirmação antecipada sem data de recebimento. A instrução foi reforçada para explicar condições sem confirmar elegibilidade e perguntar explicitamente a data ausente; a repetição passou nessa revisão. Essa correção de prompt não garante acerto em todas as perguntas e deve continuar sendo avaliada com variações.

Dados sem correspondência não provocam geração. Não há memória de conversa nessa primeira versão do RAG por terminal. O envio do conteúdo do manual a um provedor externo depende de autorização.

## 4. Provedores do modelo: Groq e Ollama

Decisão confirmada em 31/10/2026: suportar Groq e Ollama, com escolha explícita por configuração. A alternativa inicial DeepSeek foi substituída por esta combinação para permitir uso do plano gratuito da Groq ou execução local.

Modelos iniciais configuráveis: `qwen/qwen3.8-27b` na Groq e `qwen3:8b` no Ollama. Groq validada em chamadas reais de saudação e chamada/retorno de ferramenta. Ollama ainda não validado com modelo local. Nenhuma contratação ou gasto pago foi autorizado; conferir cotas antes de novas chamadas.

Implementação: HTTP com httpx, sem framework de agentes nesta etapa. Groq usa o endpoint de chat compatível com o formato OpenAI; Ollama usa sua API nativa, permitindo desabilitar thinking e configurar contexto local. As diferenças de argumentos e respostas de ferramentas são normalizadas no conector.

Motivo: separar o atendimento do provedor e tornar explícita a requisição enviada, sem exigir dois SDKs. Alternativa: usar um único SDK de compatibilidade para ambos. A API nativa do Ollama facilita controlar suas opções específicas; a camada comum mantém o restante do código independente.

Não há fallback automático, retries automáticos ou execução de ferramentas dentro do conector. O programa chamador deve validar a ferramenta solicitada e executar apenas as funções permitidas. A chave Groq não é retida na configuração Ollama nem enviada ao servidor local. Corpos de erros HTTP não são mostrados ao usuário.

Um intermediário adicional de modelos não é necessário nesta versão. A integração direta reduz dependências de instalação e configuração para reproduzir o projeto.

## 5. Inspiração e implementação independente

Usar como inspiração o padrão de configuração e simulação de atendimento de um projeto já desenvolvido. Implementar o desafio em Python com dados e configurações próprios, sem dependência da infraestrutura do projeto de referência.

## 6. Dados e limitações que precisam de tratamento

- Status ativo não garante estoque; há item ativo esgotado.
- Há itens descontinuados e um item coming_soon, inclusive com estoque positivo.
- Algumas descrições divergem dos nomes e das especificações. Não completar essas divergências por suposição.
- Os pedidos não fornecem data efetiva de recebimento nem canal de compra; solicitar esses dados para analisar arrependimento.
- Totais históricos de pedidos podem diferir do catálogo atual; conservar o total registrado.
- O manual traz contatos diferentes e regras gerais/específicas de parcelamento. Registrar como interpretar e quando encaminhar a dúvida.
- A regra de frete não explicita a condição para exatamente R$ 500.
- CSVs representam uma fotografia dos dados, não uma integração com estoque ou rastreamento ao vivo.
- Definir uma identificação de cliente simulada e limitar pedidos ao cliente selecionado. Isso não equivale a autenticação de produção.
- Instruções editáveis de estilo não devem permitir desativar as regras de consulta, privacidade e fidelidade às fontes.

## 7. Critérios propostos para testar o agente

Em 02/11/2026, a configuração inicial passou a incluir a persona completa definida para Lia: acolhedora, objetiva e consultiva; linguagem natural, sem emojis por padrão; até três opções; uma pergunta principal necessária por turno e encerramento sem insistência. O padrão é compartilhado entre terminal e interface por `DemoConfig`, mantendo personalização opcional e prioridade das regras fixas. As sessões e configurações anteriormente salvas não são sobrescritas.

O roteiro `cenarios-de-teste.md` amplia a avaliação proposta para 32 casos, incluindo tom, continuidade, políticas ambíguas, disponibilidade, descontos, pedidos e tentativas de indução. Ter um resultado esperado não equivale a já ter executado a conversa com o modelo.

1. Encontrar violões disponíveis dentro de um orçamento e manter o contexto no turno seguinte.
2. Aplicar promoção ativa e explicar por que não acumula com PIX.
3. Explicar uma devolução pedindo as informações ausentes.
4. Consultar pedido do cliente de teste, sem inventar rastreamento ausente.
5. Responder a pergunta fora do escopo e oferecer alternativa para produto indisponível.

Além das conversas, testar funções críticas de preço, filtros e acesso a pedidos. Conferir manualmente as fontes recuperadas para as perguntas sobre políticas.

## Correções após a auditoria e a rodada real de 02/11

- Mantida a arquitetura Python com cinco ferramentas. `consultar_produto` aceita exatamente ID ou termo e localiza indisponíveis. A busca de recomendação mantém o filtro e, quando fica vazia por termo, também retorna modelos correspondentes indisponíveis em campo separado.
- Criado `data/observacoes_dados.json` com evidências de divergência e notas por seção do manual. As notas têm origem própria, são distintas do texto recuperado e não substituem os dados fornecidos. Não há mapeamento de perguntas dos testes para respostas prontas.
- Material de cordas é tratado somente em violões/ukuleles. Tipo elétrico usa o campo existente ou indicação explícita no nome/descrição da categoria, com origem declarada; ausência permanece desconhecida. Não inferir captação ou material a partir de campo contraditório.
- O programa aplica até três resultados de recomendação por padrão; quantidade explícita de uma a cinco pode ampliar/reduzir o limite. A exportação mostra argumentos solicitados e efetivamente aplicados quando diferentes.
- A validação permite repetir orçamento de busca vazia, mas não libera qualquer valor recebido do usuário. Referência inválida/ausente ou valor não fundamentado recebem uma oportunidade de correção de conteúdo, dentro das quatro rodadas; turnos só entram no histórico quando concluem. Isso é distinto de retry HTTP, que continua desativado.
- Reorganizado o prompt com consulta, triagem, limites e fontes. Reforçadas respostas condicionais, aproveitamento do contexto, uma pergunta principal seguida de espera e escopo comercial. Essas instruções ainda dependem de cumprimento pelo modelo; não há alegação de máquina de estados ou aprovação automática de devoluções.
- Adicionado intervalo opcional entre requisições na mesma sessão, padrão 0. Cotas pertencem ao provedor/plano e ficam separadas das limitações do protótipo. A opção não coordena sessões concorrentes nem garante evitar todo tipo de cota.
- Escapados símbolos de moeda apenas na apresentação do chat para evitar interpretação LaTeX; o texto exportado permanece original.
- Suíte ampliada de 42 para 53 testes, com regressões úteis para os casos observados. Após nova falha real de triagem, incluída guarda conservadora para algumas aberturas de confirmação em casos pessoais, com correção de conteúdo dentro do limite existente. Não é classificador completo nem validação de elegibilidade. Revalidação real em andamento, separada da primeira rodada no navegador; evidências antigas preservadas.
- Evolução proposta para um produto real documentada em `evolucao-produto.md`, com prioridades e critérios, sem tratar propostas como capacidades implementadas.

## Pendências atualizadas

- Prazo informado pelo candidato: 03/11/2026 às 23h59. Conferir eventual fuso específico no e-mail. Priorizar uma primeira versão completa em 31/10.
- Groq configurada e testada; validar Ollama com modelo instalado e respeitar as cotas disponíveis.
- Revisar as cinco conversas e ampliar testes com variações, ambiguidades e tentativa de induzir respostas sem fontes.
- Revisão final da entrega e mudança do repositório para público permanecem pendentes; não publicar a aplicação nem enviar e-mail automaticamente.
