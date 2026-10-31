# Decisões e questões em aberto

As opções abaixo são propostas iniciais, não resultados de implementação ou testes.

## 1. Python e Streamlit

Motivo: atender à exigência de Python e concentrar interface e agente na mesma linguagem, reduzindo a complexidade de instalação e integração dentro do prazo de entrega.
Streamlit oferece elementos de chat e download de arquivos.
Alternativa considerada: interface React com API Python. Adicionaria duas aplicações e mais configuração sem necessidade para o protótipo.
Limitação: menor liberdade de interface que uma aplicação web personalizada.

## 2. Consultas estruturadas para dados operacionais

Ler os CSVs e expor funções Python com parâmetros definidos. O modelo solicita a consulta; o código valida e executa.
Preços, estoque, status e descontos não devem depender de similaridade de texto.
Começar com leitura direta dos arquivos; avaliar SQLite apenas se as consultas justificarem a camada adicional.

## 3. Recuperação de políticas

Extrair o PDF preservando página e seção. Recuperar trechos por pergunta antes da geração da resposta.
Começar avaliando busca textual com normalização e sinônimos sobre esse manual pequeno.
Se houver falhas de recuperação nos cenários, comparar outra estratégia e registrar a evidência.
Ainda não foi escolhido nem avaliado um algoritmo de ranking. Não afirmar que existe busca semântica ou embeddings sem implementá-los.

## 4. API do modelo

DeepSeek foi sugerido pelo candidato. A documentação oficial consultada em 31/10/2026 informa cobrança por tokens e suporte a ferramentas.
Não foi verificado saldo, crédito promocional ou acesso a qualquer conta de provedor.
Manter modelo, endereço da API e chave configuráveis. Não incluir chave nas exportações.

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

1. Encontrar violões disponíveis dentro de um orçamento e manter o contexto no turno seguinte.
2. Aplicar promoção ativa e explicar por que não acumula com PIX.
3. Explicar uma devolução pedindo as informações ausentes.
4. Consultar pedido do cliente de teste, sem inventar rastreamento ausente.
5. Responder a pergunta fora do escopo e oferecer alternativa para produto indisponível.

Além das conversas, testar funções críticas de preço, filtros e acesso a pedidos. Conferir manualmente as fontes recuperadas para as perguntas sobre políticas.

## Pendências

- Confirmar o horário exato de entrega no e-mail.
- Configurar uma chave pessoal de provedor e verificar as condições de uso/custo.
- Validar com o candidato o escopo e a estratégia de recuperação.
- Implementar e testar antes de declarar qualquer funcionalidade como concluída.
