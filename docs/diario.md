# Diário do desenvolvimento

Registrar apenas ações realmente realizadas. Separar observação, decisão e resultado de teste.

## 31/10/2026 — Entendimento e levantamento inicial

### Realizado

- Leitura do enunciado, do manual de políticas e dos seis CSVs com assistência do Codex.
- Identificação de 65 produtos, 9 categorias, 50 clientes, 20 pedidos, 22 registros de itens e 25 promoções, sendo 4 ativas.
- Verificação de que os itens referenciam produtos existentes e os pedidos referenciam clientes existentes.
- Identificação de limitações e divergências dos dados, registradas em decisoes.md.
- Análise da experiência de configuração de agente e simulação de atendimento de um projeto já desenvolvido, como inspiração para a interface.
- Consulta à documentação oficial de preços e ferramentas da DeepSeek e aos elementos de chat e download do Streamlit.
- Criação destes documentos iniciais em uma pasta independente.
- Registrado o prazo de entrega em 03/11/2026.
- Candidato solicitou iniciar o repositorio no GitHub como privado, com commits por etapas reais. A publicacao final devera atender a exigencia de repositorio publico do desafio.
- Preparado .gitignore para evitar versionar credenciais, ambiente Python e exportacoes locais. Exemplos de entrega deverao ser revisados e incluidos explicitamente.
- Criado o repositório privado LuccasBassani/emporio-agente, vinculado à pasta local. Primeiro envio com a documentação inicial e .gitignore.
- Configurada autoria local com o perfil pessoal e endereço noreply do GitHub, sem alterar a configuração global do computador.
- Criado guia com etapas, critérios de conclusão, conceitos técnicos e preparação da entrega.
- Candidato confirmou entrega em 03/11 às 23h59, preferência por créditos gratuitos e intenção de adiantar a maior parte em 31/10.

### Propostas ainda não implementadas

- Aplicação Streamlit com configuração, chat, consultas e exportação.
- Dados operacionais consultados por funções Python e políticas recuperadas por trechos.
- Provedor de modelo configurável, inicialmente considerando DeepSeek.

### Resultados de testes

Ainda não há testes do agente nem chamadas à API. A verificação dos arquivos não demonstra qualidade de atendimento.

## 31/10/2026 — Ambiente e conectores de modelo

### Realizado

- Confirmado suporte a Groq e Ollama, com seleção explícita de provedor e modelo.
- Criado ambiente virtual com Python 3.14.4; instalados httpx e python-dotenv e registradas versões em requirements.lock.txt.
- Copiados os seis CSVs e o manual para data/, preservando o conteúdo dos arquivos fornecidos. Os nomes dos CSVs foram reduzidos ao nome da tabela e o PDF foi nomeado politicas_da_loja.pdf.
- Implementadas validação da configuração, camada comum de resposta e adaptação dos protocolos de ferramentas da Groq e Ollama.
- Adicionados diagnósticos por terminal para saudação e chamada/retorno de uma ferramenta de teste.
- Preparado .env local sem chave e confirmado que ele e o ambiente virtual são ignorados pelo Git.
- Implementação e documentação realizadas com assistência do Codex.

### Verificação

- Sete testes automatizados passaram, com subcasos para os dois provedores, retorno de ferramenta, isolamento de credencial, parâmetros inválidos, erros HTTP, timeout e resposta inválida/interrompida.
- pip check não identificou incompatibilidades e o comando de ajuda executou corretamente.
- Não foi encontrado serviço respondendo na porta local padrão do Ollama durante o levantamento inicial.

### Limitações

Não houve geração real: não foi configurada chave Groq e não foi encontrado Ollama em execução. Testes simulados validam o protocolo implementado, não disponibilidade de modelo, desempenho, qualidade em português ou qualidade do futuro atendimento. O agente de negócio e a interface continuam pendentes.

## 31/10/2026 — Diagnóstico real Groq e RAG de políticas

### Realizado

- Configuração local selecionada como Groq, preservando a chave fora do Git.
- Diagnósticos reais de saudação em português e chamada/retorno da ferramenta de teste concluídos com sucesso no modelo qwen/qwen3.8-27b.
- Extraído o manual em 27 trechos com seção, página e ID. Implementada recuperação lexical BM25 com equivalências explícitas de vocabulário.
- Implementado o fluxo de recuperação e geração, validação de IDs de citação e exportação de pergunta/resposta/trechos por terminal.
- Adicionado conjunto de 14 perguntas revisadas e testes de recuperação, continuação de seções entre páginas e geração simulada.

### Verificação e limitações

- Treze testes automatizados passaram, incluindo os conectores e o RAG. Todas as 14 perguntas de recuperação encontraram as seções esperadas no top 4.
- O teste de envio de políticas à Groq foi bloqueado antes da execução pela revisão automática porque o manual está marcado como interno. Solicitada autorização específica; nenhuma resposta real de políticas foi gerada até este registro.
- A verificação lexical e de IDs não demonstra fidelidade de todas as afirmações do modelo. A geração real, perguntas adicionais e comportamento com histórico ainda precisam ser avaliados.
- Código, testes e documentação desta etapa desenvolvidos com assistência do Codex.

## 31/10/2026 — Validação real do RAG

### Realizado

- Recebida autorização explícita para enviar os trechos pertinentes das políticas da loja fictícia à Groq e salvar os resultados dos dois cenários no repositório privado.
- Executado o cenário promoção + PIX; a resposta correspondeu à regra recuperada e citou a seção pertinente.
- Executado o cenário de devolução online sem data de recebimento. A resposta inicial explicou o manual, mas começou com uma confirmação e não perguntou a data, contrariando o comportamento esperado.
- Ajustada a instrução de triagem: em pedido de devolução específico com dados ausentes, apresentar condições sem confirmar elegibilidade e perguntar explicitamente quando o produto foi recebido.
- Repetido o cenário de devolução; a nova resposta explicou as condições e perguntou a data de recebimento. Resposta revisada em relação aos trechos enviados.
- Salvas as duas respostas finais reais em examples/, com pergunta, provedor/modelo e trechos recuperados. As respostas exportadas não foram editadas manualmente.

### Limitações

As evidências cobrem dois cenários de um turno, não todas as reformulações nem o conjunto completo do desafio. O ajuste depende de cumprimento da instrução pelo modelo. Não houve envio de dados de clientes. Ollama, continuidade de conversa, catálogo e pedidos continuam pendentes.

## 31/10/2026 — Catálogo, preços e agente com ferramentas

### Realizado

- Implementadas consultas diretas aos CSVs de produtos, categorias e promoções, com filtros de orçamento final, nome/categoria, cordas, captação e disponibilidade.
- Implementados cálculos Decimal, PIX não cumulativo e rejeição de múltiplas promoções ativas ambíguas. Produtos ativos esgotados, descontinuados e coming_soon preservam motivos distintos.
- Implementado agente com ferramentas permitidas, recuperação de políticas, histórico dos dois últimos turnos completos e exportação de mensagens, consultas e fontes.
- Adicionados comandos de consulta local, mensagem única e chat interativo no terminal.
- Desenvolvidos código, testes e documentação com assistência do Codex.

### Verificação inicial

- Vinte e oito testes automatizados passaram, incluindo orçamento e arredondamento, promoções, status/estoque, chamada/retorno de ferramentas, fontes, histórico após erro e limites de execução.
- Consulta local à categoria de violões até R$ 1.000 encontrou 12 produtos disponíveis; os resultados foram comparados aos CSVs.
- Primeira busca real pela Groq apresentou corretamente as duas opções mais baratas. A pergunta de continuação atingiu a cota gratuita; não foi apresentada como um teste completo aprovado.
- Removidos metadados repetidos dos resultados enviados ao modelo, preservando os dados completos nas evidências. Iniciada nova sessão para verificar o fluxo com intervalo entre turnos.
- Nova sessão concluída e revisada: duas opções retornadas pelo catálogo e pergunta "o primeiro no PIX" corretamente relacionada ao produto 83. A ferramenta calculou R$ 408,41, valor que foi apresentado pelo modelo. Evidência real salva em examples/catalogo-e-pix.md, sem edição das respostas.
- Acrescentado teste para o limite de contexto, verificando que mantém dois turnos completos e não separa chamadas dos resultados de ferramentas. A suíte final desta etapa contém 29 testes.

### Limitações

As verificações de referência e o teste de valores sem fonte não comprovam automaticamente a fidelidade de todas as afirmações. A geração segue dependendo da escolha correta de ferramentas e da interpretação pelo modelo. Não há consulta de pedidos, persistência de sessão nem interface gráfica nesta etapa.

## Como registrar as próximas etapas

Para cada etapa, anotar: problema, solução escolhida e motivo, alternativa considerada, teste executado, resultado e limitação restante.
Atualizar a seção de uso de IA do README conforme a assistência efetivamente utilizada.
Gerar commits por mudanças reais e manter os exemplos como conversas executadas, sem apresentá-los como testes antes de rodá-los.
