# Evolução proposta

Este plano parte das limitações observadas nos testes. As propostas não são funcionalidades implementadas nem requisitos para executar o protótipo. A versão resumida está na seção [Melhorias com mais tempo](entrega.md#melhorias-com-mais-tempo).

## 1. Guardrails, triagem e avaliação

Ampliaria a validação de afirmações de preço, estoque, regras e campos ausentes contra os resultados das ferramentas. A triagem teria campos explícitos de canal, recebimento e condições do item, com encaminhamento à equipe quando faltasse informação. As proteções atuais são parciais e não eliminam alucinações ou desvios de instrução.

Para avaliar o ganho, usaria perguntas novas, reformulações, conversas longas e tentativas de desviar as regras. Manteria separados acerto factual, escolha de ferramenta, continuidade, estilo e falha de execução. Os 32 cenários usados no desenvolvimento não seriam o único conjunto de avaliação.

## 2. Contexto de atendimentos anteriores

Começaria por resumos e campos revisáveis por cliente identificado: instrumento de interesse, orçamento, pedido em discussão e informações já fornecidas. O acesso ao histórico teria autorização, retenção definida, origem e validade dos registros.

Informação antiga não comprova preço, estoque, rastreamento ou política atual. Esses fatos continuariam consultados nas fontes. Os testes verificariam continuidade e ausência de mistura entre clientes.

## 3. Recuperação e consultas para bases maiores

Para mais documentação, avaliaria busca híbrida de BM25 e embeddings, reranking e divisão dos documentos em trechos que preservem contexto. Metadados de seção, versão e vigência ajudariam a filtrar fontes. A comparação mediria recuperação relevante, fidelidade, custo e latência.

Para dados operacionais maiores ou atualizados, substituiria os CSVs por banco de dados ou APIs, com consultas parametrizadas, índices, filtros e paginação. Manteria cálculos e autorização no código, dentro de ferramentas delimitadas. Corrigiria conflitos na origem e registraria a versão dos dados usados na resposta.

## 4. Fine-tuning de comportamento

Depois de melhorar dados, prompts e validações, avaliaria adaptação de um modelo compatível com conversas revisadas para tom, triagem e escolha de ferramentas. Treino e avaliação usariam conjuntos separados; a adoção dependeria de ganho medido frente ao modelo base.

Não há ajuste de pesos implementado. Fine-tuning não substituiria as consultas de preço e disponibilidade nem resolveria, por si só, cadastros inconsistentes.

## 5. Requisitos para uso operacional

Acrescentaria autenticação e autorização reais, integrações de estoque/pedidos, atendimento humano e observabilidade de consultas, erros, consumo e latência, com minimização de dados e retenção definida. Operações de escrita exigiriam controle de duplicidade e confirmação apropriada.

Dimensionaria o provedor conforme volume e orçamento. O intervalo atual entre chamadas é por sessão e não controla a capacidade global da conta. Eventual retry futuro distinguiria o tipo de erro e manteria explícito o destino dos dados.
