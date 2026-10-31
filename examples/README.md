# Exemplos executados

Os arquivos desta pasta registram chamadas reais ao modelo, sem editar manualmente as respostas exportadas. Cada arquivo contém pergunta, resposta, provedor/modelo e os trechos recuperados do manual.

| Arquivo | Cenário | Verificação manual |
| --- | --- | --- |
| [rag-promocao-pix.md](rag-promocao-pix.md) | Combinação de promoção com desconto PIX | A resposta segue a regra recuperada e cita o trecho pertinente |
| [rag-devolucao.md](rag-devolucao.md) | Arrependimento em compra online sem data de recebimento | Explica as condições de forma condicional e pergunta quando houve recebimento |
| [catalogo-e-pix.md](catalogo-e-pix.md) | Duas opções de violões por orçamento e continuação sobre PIX | Consulta os CSVs, mantém a referência ao primeiro produto e usa o preço calculado em Python |
| [pedido-rastreamento.md](pedido-rastreamento.md) | Status, item e rastreamento do pedido 8 | Executado pela interface via AppTest com cliente de teste #2; dados conferidos contra os CSVs |
| [fora-do-escopo.md](fora-do-escopo.md) | Pedido de cabos e palhetas | Executado no navegador; explica o escopo fixo do atendimento sem inventar parceiros |

Executados em 31/10/2026 com Groq, modelo `qwen/qwen3.8-27b`, após autorização para enviar os trechos das políticas da loja fictícia.

No primeiro teste de devolução, o modelo começou confirmando a possibilidade de devolução sem perguntar a data de recebimento. A instrução de triagem foi ajustada e o cenário foi executado novamente. O arquivo de devolução contém a nova resposta, que foi revisada. O problema e a correção estão registrados no diário.

O teste de catálogo foi executado depois, em dois turnos. Uma primeira tentativa atingiu a cota gratuita na continuação. A evidência salva é a nova sessão concluída com intervalo entre as mensagens, sem editar as respostas.

São cinco exemplos: quatro testes de um turno e uma conversa de dois turnos. O teste de pedido foi autorizado com envio somente dos campos operacionais dos pedidos fictícios, sem nomes ou contatos. O exemplo fora do escopo usa a regra fixa de atendimento no prompt e não executou recuperação; isso está explícito no arquivo exportado. Os identificadores de citação permitem conferir a origem; a revisão manual avalia se a afirmação corresponde ao trecho citado. Ainda é necessário revisar essa seleção antes da entrega final.
