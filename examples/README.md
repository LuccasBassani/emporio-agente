# Exemplos executados

Os arquivos desta pasta registram chamadas reais ao modelo, sem editar manualmente as respostas exportadas. Cada arquivo contém pergunta, resposta, provedor/modelo e os trechos recuperados do manual.

| Arquivo | Cenário | Verificação manual |
| --- | --- | --- |
| [rag-promocao-pix.md](rag-promocao-pix.md) | Combinação de promoção com desconto PIX | A resposta segue a regra recuperada e cita o trecho pertinente |
| [rag-devolucao.md](rag-devolucao.md) | Arrependimento em compra online sem data de recebimento | Explica as condições de forma condicional e pergunta quando houve recebimento |

Executados em 31/10/2026 com Groq, modelo `qwen/qwen3.8-27b`, após autorização para enviar os trechos das políticas da loja fictícia.

No primeiro teste de devolução, o modelo começou confirmando a possibilidade de devolução sem perguntar a data de recebimento. A instrução de triagem foi ajustada e o cenário foi executado novamente. O arquivo de devolução contém a nova resposta, que foi revisada. O problema e a correção estão registrados no diário.

São dois testes de um turno, não uma avaliação ampla nem o conjunto final de 3 a 5 conversas do desafio. Ainda serão acrescentados cenários com catálogo, pedidos e continuidade de conversa. Os identificadores de citação permitem conferir a origem; a revisão manual avalia se a afirmação corresponde ao trecho citado.
