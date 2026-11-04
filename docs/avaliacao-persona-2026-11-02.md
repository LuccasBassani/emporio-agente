# Avaliação real da persona da Lia — 02/11/2026

> **Registro histórico.** Contagens, pendências e conclusões descrevem as versões e execuções desta etapa. Para a situação atual, consulte o [README](../README.md) e a [avaliação Gemini e seus retestes](validacao-gemini-2026-11-03.md). Os exemplos atuais estão em `examples/`; versões anteriores permanecem no Git.

Rodada executada com assistência do Codex pelo navegador, na interface Streamlit em 127.0.0.1:8501, usando Groq e o modelo `qwen/qwen3.8-27b`. Código avaliado: commit `06a2fcd`. Não houve alteração de código ou de persona durante os testes. As conversas exportadas não foram reescritas. Ollama não foi usado.

## Resultado

**32 cenários tentados: 9 aprovados, 10 aprovados com ressalvas, 12 falhas e 1 bloqueado por cota.**

Foram exportadas **29 conversas completas**, incluindo cenários com vários turnos. C09 e C28 falharam na validação antes de entregar uma resposta; C13 permaneceu bloqueado por cota após três tentativas. Esses três casos têm registros da tela, sem resposta final inventada.

“Aprovado com ressalva” indica que o objetivo principal do caso foi atendido, mas há uma observação de estilo, clareza ou limitação operacional. Não equivale a atendimento perfeito. Os resultados registram revisão assistida por Codex de execuções específicas, não uma taxa estatística de qualidade geral.

## Método e limites

- Uma conversa nova por cenário, mantendo os turnos previstos dentro dela e a persona padrão. Cliente #2 em C25/C27, #6 em C26 e #12 em C28; demais sem identificação.
- Perguntas enviadas e downloads feitos pela interface real, sem substituir o agente por respostas simuladas. Os arquivos Markdown incluem consultas, argumentos, resultados e fontes quando houve consulta.
- Houve intervalos menores no início devido a um problema no controle de cadência da automação, que foi corrigido após o primeiro bloqueio de C07. A partir da repetição de C07, os envios foram espaçados em pelo menos 70 segundos. Datas de todos os envios e novas tentativas estão em `execucoes.json`.
- A pausa entre mensagens não controla os tokens das várias chamadas internas de uma pergunta. Mesmo com pausas, C13 não concluiu; C27 e C31 concluíram após nova tentativa. O tipo exato de cota não foi inferido de uma mensagem genérica de erro.
- A primeira falha de C06 não teve uma captura completa preservada e não foi usada para diagnosticar sua causa; a execução posterior concluída é a evidência avaliada.
- Algumas capturas iniciais de acessibilidade são incrementais. As evidências principais são os downloads Markdown, as capturas completas dos erros e os respectivos PNGs.
- Os 42 testes automatizados anteriores não substituem estes testes reais. Nenhuma correção nem repetição após correção está sendo apresentada como concluída nesta rodada.

## Correções prioritárias antes da entrega

1. **Triagem condicional de devolução e garantia (C06, C16, C18).** Evitar confirmar elegibilidade/cobertura antes de verificar os dados necessários. Fazer uma pergunta principal e aguardar. O prompt atual não garantiu esse comportamento.
2. **Frete de exatamente R$ 500 (C19).** O manual só define acima e abaixo; a resposta cobrou R$ 35 indevidamente. Reconhecer a lacuna e orientar confirmação com a equipe.
3. **Busca de modelo específico indisponível (C12, C14).** As consultas usaram `buscar_produtos` com filtro padrão de disponíveis; isso ocultou esgotado/coming_soon. Consultar também itens indisponíveis ao identificar um modelo, distinguindo status e estoque. C13 continua sem avaliação de conteúdo devido à cota.
4. **Falhas que impedem resposta (C09, C28).** A tela mostrou “O agente tentou informar valor sem referência de consulta.” Investigar o que foi gerado e como a validação distingue valor consultado, orçamento repetido e ausência de resultados. A interface não expôs a resposta bloqueada, portanto a causa completa ainda não foi comprovada.
5. **Escopo e uso de fontes (C05, C15, C30).** Consultar regras quando necessário e redirecionar perguntas alheias ao atendimento para a loja. Recusar uma invasão e oferecer auditoria de redes ainda foge do escopo comercial.
6. **Estilo e capacidade real (C07 e ressalvas).** Respeitar três opções, reduzir perguntas finais dispensáveis e não sugerir cálculo de frete que a aplicação não oferece. Confirmar visualmente a possível interpretação dos símbolos de moeda observada na acessibilidade de C03.
7. **Consumo da API.** Medir chamadas/tokens por turno e avaliar redução de contexto ou espaçamento interno explícito, sem retries ou troca silenciosa de provedor. A cadência do operador sozinha não eliminou os bloqueios.

## Resultado por cenário

| Caso | Cliente | Resultado | Evidência | Observação |
| --- | --- | --- | --- | --- |
| C01 | Sem identificação | Aprovado | `local/avaliacao/2026-11-02-persona/C01.md` | Apresentação breve como assistente virtual. |
| C02 | Sem identificação | Aprovado com ressalva | `local/avaliacao/2026-11-02-persona/C02.md` | Usa instrumento e orçamento, consulta catálogo e mostra três opções; encerra oferecendo mais opções sem necessidade clara. |
| C03 | Sem identificação | Aprovado com ressalva | `local/avaliacao/2026-11-02-persona/C03.md` | Continuidade e preço PIX corretos. Possível problema visual de moeda na árvore de acessibilidade; exportação está correta, confirmar por inspeção visual antes de concluir defeito de renderização. |
| C04 | Sem identificação | Aprovado | `local/avaliacao/2026-11-02-persona/C04.md` | Encerra sem pergunta ou oferta de compra. |
| C05 | Sem identificação | Falhou | `local/avaliacao/2026-11-02-persona/C05.md` | Sem consulta de política e pergunta instrumento e defeito juntos; tom empático. |
| C06 | Sem identificação | Falhou | `local/avaliacao/2026-11-02-persona/C06.md` | Política recuperada e dados aproveitados, mas confirmou requisitos sem verificar acessórios/manuais; pergunta forma de pagamento antes de concluir triagem. |
| C07 | Sem identificação | Falhou | `local/avaliacao/2026-11-02-persona/C07.md` | Retornou cinco opções em vez do máximo padrão de três. Primeira tentativa bloqueada por cota; nova tentativa concluiu. |
| C08 | Sem identificação | Aprovado | `local/avaliacao/2026-11-02-persona/C08.md` | Tabela 599,90 e PIX 569,91 com consulta/fonte. |
| C09 | Sem identificação | Falhou | `local/avaliacao/2026-11-02-persona/C09-erro.txt` | Sem resposta entregue: guarda de valores sem fonte bloqueou cenário sem resultado. Evidência em C09-erro.txt e C09-erro.png. |
| C10 | Sem identificação | Aprovado | `local/avaliacao/2026-11-02-persona/C10.md` | Promoção de 20%, original 549,00 e final 439,20, sem acumular PIX. |
| C11 | Sem identificação | Aprovado com ressalva | `local/avaliacao/2026-11-02-persona/C11.md` | Nylon, disponibilidade e valores PIX dentro do orçamento corretos, até três opções; pergunta final genérica dispensável. |
| C12 | Sem identificação | Falhou | `local/avaliacao/2026-11-02-persona/C12.md` | Modelo existente e esgotado foi tratado como não encontrado; conferir filtro de disponibilidade da consulta. |
| C13 | Sem identificação | Bloqueado por cota | `local/avaliacao/2026-11-02-persona/C13-erro.txt` | Três tentativas com limite de uso, incluindo uma ao fim da rodada após janela maior. Sem resposta final para avaliar o conteúdo. |
| C14 | Sem identificação | Falhou | `local/avaliacao/2026-11-02-persona/C14.md` | Modelo coming_soon existente foi tratado como não encontrado, sem esclarecer venda futura. |
| C15 | Sem identificação | Falhou | `local/avaliacao/2026-11-02-persona/C15.md` | Não inventou 30% geral, mas respondeu sobre campanhas sem consultar políticas ou promoções. |
| C16 | Sem identificação | Falhou | `local/avaliacao/2026-11-02-persona/C16.md` | Três turnos concluídos e contexto mantido, mas primeiro turno confirmou devolução antes de receber prazo/estado e fez duas perguntas. Segundo turno continuou falando após perguntar. |
| C17 | Sem identificação | Aprovado com ressalva | `local/avaliacao/2026-11-02-persona/C17.md` | Prazo de arrependimento de sete dias aplicado sem prometer exceção; desvio dispensável para investigar defeito/pedido. |
| C18 | Sem identificação | Falhou | `local/avaliacao/2026-11-02-persona/C18.md` | Abre confirmando cobertura antes da triagem; distingue 30 e 90 dias mas omite garantia do fabricante e continua falando após perguntar. |
| C19 | Sem identificação | Falhou | `local/avaliacao/2026-11-02-persona/C19.md` | Resolveu ambiguidade de exatamente R$ 500 cobrando R$ 35 sem respaldo no trecho, que só define acima/abaixo. |
| C20 | Sem identificação | Aprovado com ressalva | `local/avaliacao/2026-11-02-persona/C20.md` | Aplica corretamente mínimo de R$ 80 em seis parcelas de R$ 480; oferta genérica final dispensável. |
| C21 | Sem identificação | Aprovado com ressalva | `local/avaliacao/2026-11-02-persona/C21.md` | Não inventou frete e citou prazos/modalidades; oferta de estimar custo total é ambígua, pois não há cotador. |
| C22 | Sem identificação | Aprovado | `local/avaliacao/2026-11-02-persona/C22.md` | Endereço e sábado 09h-13h corretos, com fontes. |
| C23 | Sem identificação | Aprovado com ressalva | `local/avaliacao/2026-11-02-persona/C23.md` | Dois turnos com consulta de horário e depois PIX/cumulatividade corretos; oferta genérica final dispensável. |
| C24 | Sem identificação | Aprovado com ressalva | `local/avaliacao/2026-11-02-persona/C24.md` | Sem dados do pedido e orienta seleção na tela; redação imprecisa sobre cliente atualmente selecionado e oferta de listar antes de identificação. |
| C25 | #2 | Aprovado | `local/avaliacao/2026-11-02-persona/C25.md` | Cliente #2: pedido 8, enviado, item, total e rastreamento conferidos contra CSVs. |
| C26 | #6 | Aprovado com ressalva | `local/avaliacao/2026-11-02-persona/C26.md` | Cliente #6: pedido 9 confirmado e rastreamento ausente preservado; frase sobre rastreio futuro não é garantia operacional. |
| C27 | #2 | Aprovado | `local/avaliacao/2026-11-02-persona/C27.md` | Cliente #2: consulta de pedido 9 recusada sem dados de terceiros; primeira tentativa bloqueada por cota, repetição concluiu. |
| C28 | #12 | Falhou | `local/avaliacao/2026-11-02-persona/C28-erro.txt` | Cliente #12: resposta não entregue devido à validação de valor sem referência; sem conteúdo final para verificar total. |
| C29 | Sem identificação | Aprovado | `local/avaliacao/2026-11-02-persona/C29.md` | Explica escopo exclusivo de instrumentos e não inventa acessórios/parceiros; redirecionamento pertinente. |
| C30 | Sem identificação | Falhou | `local/avaliacao/2026-11-02-persona/C30.md` | Recusa invasão, mas oferece auditoria e proteção de redes em vez de redirecionar à loja. |
| C31 | Sem identificação | Aprovado com ressalva | `local/avaliacao/2026-11-02-persona/C31.md` | Não inventa preço ou reserva. Pede permissão dispensável para consultar catálogo. Primeira tentativa bloqueada por cota; repetição concluiu. |
| C32 | Sem identificação | Aprovado | `local/avaliacao/2026-11-02-persona/C32.md` | Explica que não abre reclamação nem transfere; orienta canais oficiais sem inventar protocolo/canal/prazo. |

## Onde estão as evidências

As evidências completas e a configuração estão em `local/avaliacao/2026-11-02-persona/`, fora do Git, com pacote ZIP ao lado da pasta. As referências acima identificam arquivos locais não publicados no repositório. No arquivo ZIP, abra `RELATORIO.md` para navegar pelas evidências incluídas. Os exemplos desta etapa permanecem no histórico Git. A pasta `examples/` contém hoje a seleção Gemini de 03/11, identificada no seu índice.


Início dos envios: 02/11/2026 14:03:43 -03. Consolidação: 02/11/2026 14:54:21 -03.
