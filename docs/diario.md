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

## Como registrar as próximas etapas

Para cada etapa, anotar: problema, solução escolhida e motivo, alternativa considerada, teste executado, resultado e limitação restante.
Atualizar a seção de uso de IA do README conforme a assistência efetivamente utilizada.
Gerar commits por mudanças reais e manter os exemplos como conversas executadas, sem apresentá-los como testes antes de rodá-los.
