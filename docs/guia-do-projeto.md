# Guia de execução e leitura

As instruções de instalação e seleção do provedor estão no [README](../README.md). A demonstração documentada usa Gemini Flash-Lite. Groq é alternativa configurável; Ollama depende de servidor e modelo local e ainda não teve sua geração validada neste projeto.

## Demonstrar o atendimento

1. Instale as dependências, configure o `.env` conforme o README e inicie Streamlit.
2. Mantenha a persona padrão da Lia. Pergunte por duas opções de violões até R$ 1.000 e depois pelo preço do primeiro no PIX.
3. Abra **Ver consultas e fontes** e confronte o texto com os resultados das ferramentas.
4. Selecione **Cliente #2** e consulte o **pedido 8**. Uma consulta ao pedido 9, de outro cliente, não deve revelar seus dados. O cliente é uma seleção de teste, sem autenticação real.
5. Teste uma política, por exemplo parcelamento de R$ 480 em seis vezes. Confira a seção recuperada do PDF.
6. Exporte a conversa antes de trocar cliente, aplicar configuração ou iniciar outra conversa, pois essas ações limpam o histórico da sessão.

A interface permite baixar conversas em Markdown/TXT e configurações em JSON. Credenciais do ambiente não são campos da configuração exportada. A imagem [interface.png](interface.png) mostra o fluxo de uma resposta.

## Conferir o projeto

- [Decisões técnicas](decisoes.md): comportamento atual de consultas, recuperação, contexto e provedores.
- [Cenários e critérios de aceitação](cenarios-de-teste.md): resultados esperados, separados das execuções.
- [Avaliação Gemini](validacao-gemini-2026-11-03.md): 32 cenários e retestes nas versões indicadas.
- [Cinco exemplos reais](../examples/README.md): seleção publicada com consultas e fontes.
- [Exemplos de atendimento e revisão](entrega.md): falas selecionadas e melhorias propostas, incorporadas ao PDF.
- [Gerar o PDF](gerar-pdf.md): instruções do exportador, fora do documento entregue.

Os 61 testes automatizados usam respostas de API simuladas e não consomem cota. Uma avaliação real depende de chave, modelo e capacidade do provedor. Erro de execução, falha factual e ressalva de linguagem devem ser registrados separadamente.

Os registros datados e o [diário](diario.md) documentam a evolução. Pendências ou contagens antigas descrevem a etapa correspondente; a última correção não foi seguida por outra rodada integral dos 32 cenários. O [índice da documentação](README.md) identifica o material atual e o histórico.
