# Histórico do desenvolvimento

Registro resumido das etapas realizadas. As contagens de testes e pendências abaixo pertencem a cada momento. O [README](../README.md) e a [avaliação Gemini](validacao-gemini-2026-11-03.md) apresentam a versão de entrega. O histórico completo das alterações permanece nos commits.

## Direcionamento e uso de IA

Conduzi a definição da referência de interface, persona, escopo, provedores e custo. Também orientei os testes e seus resultados esperados, revisei respostas, priorizei correções e simplifiquei propostas desproporcionais ao desafio. Usei Codex como apoio à implementação, automação, execução de testes e documentação. Os relatórios identificam a execução assistida e os critérios usados na revisão.

## 31/10/2026 - Escopo, dados e primeira implementação

- Leitura do enunciado, dos seis CSVs e do manual. Levantados 65 produtos, nove categorias, 50 clientes, 20 pedidos e 25 promoções, quatro ativas.
- Definida aplicação independente em Python, usando como referência uma experiência de configuração e simulação de atendimento. Priorizado uso de opções gratuitas e desenvolvimento incremental.
- Criados repositório, configuração de ambiente e conectores Groq/Ollama. A suíte inicial tinha sete testes de configuração e protocolo; Ollama não foi validado com modelo instalado.
- Implementado RAG lexical sobre 27 trechos, com 14 perguntas de recuperação. A suíte chegou a 13 testes. Chamadas reais à Groq verificaram saudação e retorno de ferramenta.
- O primeiro teste real de devolução confirmou possibilidade de devolver sem pedir a data de recebimento. A orientação de triagem foi ajustada e o cenário repetido; a nova resposta pediu a informação ausente.
- Implementados catálogo e descontos com `Decimal`, cinco ferramentas de atendimento, contexto dos dois turnos anteriores e exportação. Uma primeira continuação de catálogo foi bloqueada por cota; outra sessão concluiu a consulta de PIX.
- Acrescentados pedidos restritos ao cliente de teste e interface Streamlit. A suíte chegou a 42 testes. A instalação em um segundo ambiente foi conferida nessa etapa; o navegador foi usado para verificar mensagens, importação e downloads.

## 02/11/2026 - Persona, avaliação e correções

- Consolidada a persona padrão da Lia e um roteiro com 32 cenários e resultados esperados.
- A rodada assistida pelo navegador, com Groq/Qwen, registrou nove aprovados, dez com ressalvas, 12 falhas e um bloqueado por cota. As respostas foram preservadas como evidência da versão testada.
- A auditoria identificou descrições divergentes, status comerciais incompatíveis com uma oferta de compra e ambiguidades do manual. Notas separadas passaram a acompanhar as consultas, preservando os dados originais.
- Corrigidas busca de modelos indisponíveis, tratamento de orçamento sem resultado, instruções de triagem, limites de recomendações e apresentação de moeda. A suíte chegou a 54 testes.
- A revalidação priorizada teve 18 cenários tentados: 15 atenderam ao objetivo principal, quatro com ressalvas; três ficaram pendentes naquela etapa. A interrupção diária e o HTTP 400 sem causa confirmada foram registrados separadamente dos erros de conteúdo.

## 03/11/2026 - Retomada e alternativa de provedor

- A tentativa inicial da rodada completa concluiu C14 e parte de C03 antes de nova interrupção por cota.
- Na retomada Qwen, 24 casos concluíram: 14 aprovados, nove com ressalvas e uma falha de campanha. C25 foi interrompido e C26-C32 não começaram.
- A escolha explícita de Gemini preservou o mesmo agente e as ferramentas. Flash 3.6 teve oito casos concluídos antes do limite diário observado; Flash-Lite permitiu executar os 32 cenários. Essas rodadas não são um benchmark controlado entre modelos.

## 03/11/2026 - Avaliação Gemini e versão de entrega

- A rodada integral com Flash-Lite teve 12 aprovados, 15 com ressalvas e cinco falhas. Execução por Streamlit AppTest e API real, com leitura assistida das respostas, consultas e fontes.
- Nove casos foram repetidos após ajustes. Estados de pedido sem identificação/não localizado receberam orientação determinística, e as instruções foram revistas para status comercial, canal já informado e escopo.
- Uma regressão acrescentou condição de frete ao total histórico de pedido. Foi incluída validação conservadora com teste de regressão; o caso foi repetido na API real, com dados corretos e ressalva de linguagem.
- A suíte chegou a 61 testes. As cinco falhas iniciais tiveram o objetivo principal atendido nos retestes, com ressalvas em dois casos. Não houve nova rodada integral após a última alteração.
- Selecionadas cinco conversas reais com variedade de fluxos. O README e o PDF foram consolidados, com declaração da condução do candidato, uso do Codex e limites da avaliação. Registros históricos ficaram fora do PDF de seis páginas.
