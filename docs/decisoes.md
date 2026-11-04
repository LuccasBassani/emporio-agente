# Decisões técnicas da versão de entrega

Este documento descreve a implementação atual. Os registros datados em `docs/` preservam etapas anteriores; a avaliação principal é a [rodada com Gemini e seus retestes](validacao-gemini-2026-11-03.md).

## Aplicação e arquitetura

Python atende à restrição do desafio. Streamlit concentra configuração, chat e exportações na mesma aplicação, reduzindo a instalação e a integração exigidas por uma interface separada. A referência de experiência foi definida pelo candidato; a implementação é independente.

O agente usa `httpx`, sem framework de agentes. O modelo solicita uma das cinco ferramentas permitidas: `buscar_produtos`, `consultar_produto`, `buscar_politicas`, `consultar_pedido` e `listar_meus_pedidos`. O Python valida os argumentos e executa a função. A API do provedor não executa essas funções por conta própria.

Cada turno permite até quatro rodadas de geração, com no máximo quatro ferramentas por rodada. Há uma oportunidade de correção de conteúdo dentro desse limite. Isso é separado de retry HTTP, que não é automático. Somente turnos concluídos entram no histórico; os dois anteriores completos são enviados como contexto. O histórico da sessão e as exportações podem conter mais turnos que esse recorte.

## Dados estruturados e preços

Os seis CSVs foram preservados em `data/`. As consultas usam uma fotografia carregada em memória, adequada ao volume fornecido. Não há SQL, busca vetorial de produtos ou integração com estoque ao vivo.

- Disponibilidade: `status=active` e estoque positivo. Descontinuado e em breve permanecem indisponíveis, mesmo com quantidade cadastrada.
- Preço: `Decimal` e arredondamento `ROUND_HALF_UP` em centavos. Orçamento considera o preço final para o pagamento escolhido, sem frete.
- Desconto: promoção com `is_active=1` prevalece; PIX de 5% só se aplica sem promoção ativa. O mês ou o texto da campanha não ativam uma oferta. Mais de uma promoção ativa por produto interrompe a carga do catálogo para esclarecer a ambiguidade.
- Busca: nome e categoria normalizados, com filtros de orçamento, disponibilidade, material de cordas e classificação elétrica. Nome/ID localiza também modelos indisponíveis. Descrições livres divergentes não entram na identificação textual.

Material de cordas é filtrado apenas nas categorias em que o cadastro o informa. Classificação elétrica usa `specs.electronics` ou indicações explícitas no nome/categoria, com origem declarada. Campo ausente não equivale a falso.

`data/observacoes_dados.json` registra divergências e interpretações separadamente dos originais. As notas acompanham as consultas pertinentes; não substituem o conteúdo do manual nem corrigem silenciosamente o cadastro.

## Pedidos e identificação

A aplicação define o cliente de teste fora dos argumentos enviados pelo modelo. A consulta verifica a associação e dá o mesmo retorno para pedido inexistente e de terceiro. Trocar o cliente na interface limpa a conversa.

As ferramentas de pedidos não retornam nome, telefone, e-mail, endereço, notas ou identificador do cliente. Preservam status, itens, total histórico e rastreamento cadastrado. Não inferem recebimento efetivo, composição de frete ou rastreio ao vivo. Sem identificação ou com pedido não localizado, uma chamada única de pedido recebe orientação determinística do programa.

A seleção na tela é uma simulação, não autenticação real. Mensagens digitadas pelo usuário também integram o contexto do modelo; a minimização descrita acima se aplica aos campos consultados pela ferramenta.

## Recuperação de políticas

O PDF gera 27 trechos com seção, página e ID. O ranking BM25 normaliza acentos e um vocabulário explícito de equivalências. Títulos recebem peso adicional e a busca retorna até quatro trechos por padrão. O manual pequeno favoreceu uma solução local e inspecionável.

Não há embeddings, reranking ou base vetorial. As 14 perguntas de recuperação revisadas encontram as seções esperadas no top 4; isso não cobre todas as reformulações. Score positivo não é garantia de relevância.

No chat, `buscar_politicas` fornece os trechos ao agente. O comando isolado `--ask` usa `PolicyRAG`, sem memória de conversa e com referências sequenciais `[P1]`, `[P2]`. Nesse comando, ausência de trechos encerra a resposta sem chamar o modelo. O chat usa IDs de seção/página, como `[P3.1-p3-1]`.

A validação verifica os IDs reconhecidos e algumas condições de conteúdo. Não compara automaticamente cada afirmação ou valor com a fonte, nem garante resistência a prompt injection. Triagem e estilo continuam parcialmente dependentes da geração.

## Provedores e configuração

Gemini Flash-Lite (`gemini-3.5-flash-lite`) foi selecionado para a demonstração após limites de capacidade nos testes anteriores. A escolha considerou suporte a ferramentas e capacidade gratuita observada, sem benchmark controlado de superioridade. Groq/Qwen continua disponível; Ollama tem contratos HTTP simulados testados, mas não execução validada com modelo instalado.

Groq e Gemini usam chat compatível com o formato OpenAI; o adaptador preserva as assinaturas opacas das chamadas de ferramenta do Gemini. Ollama usa sua API nativa. Não há troca automática de provedor. O intervalo opcional entre chamadas é por cliente HTTP/sessão e não coordena cotas entre usuários.

`.env.example` e a configuração de ambiente sem seleção explícita usam Ollama. O README orienta selecionar Gemini para reproduzir a demonstração. A interface lê o ambiente e permite aplicar outra seleção; o padrão interno de `DemoConfig` é Groq. Essas opções não provocam chamadas ao abrir a tela.

Chaves são lidas do ambiente/`.env`, fora do Git. A configuração JSON exporta preferências e modelos, sem credenciais ou identidade do cliente. O importador aceita o formato legado sem `gemini_model`; campos extras são rejeitados.

## Condução, testes e limites

O candidato definiu referência de interface, persona, escopo, provedores e restrições de custo; orientou cenários e resultados esperados, revisou respostas e priorizou correções e simplificações. Codex apoiou implementação, automação, execução de testes e documentação. Os relatórios identificam a execução assistida e os critérios usados na revisão.

A suíte possui 61 testes locais, com respostas de API simuladas. As avaliações reais registram separadamente versão, modelo, falhas e retestes. As cinco conversas de entrega estão em [examples/](../examples/README.md). A [evolução proposta](evolucao-produto.md) não corresponde a funcionalidades já implementadas.
