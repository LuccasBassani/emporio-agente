# Project documentation

The submission documentation is in English. The application, supplied business data and original conversation exports remain in Brazilian Portuguese. Original dialogue is retained as evidence rather than presented as an English-language model run.

## Submission version

- [Main README](../README.md): scope, setup, architecture, validation and AI assistance.
- [Technical decisions](decisoes.md): current implementation contracts and limits.
- [Execution guide](guia-do-projeto.md): short demonstration walkthrough.
- [Interaction examples and review](entrega.md): five conversations, fixes and proposed improvements included in the PDF.
- [Five real exports](../examples/README.md): complete queries and sources.
- [Gemini evaluation and retests](validacao-gemini-2026-11-03.md): full evaluation and subsequent revisions.
- [Scenarios and criteria](cenarios-de-teste.md): expected behavior, separate from execution results.
- [Proposed evolution](evolucao-produto.md): guardrails, context, retrieval, queries and fine-tuning.
- [Generate the PDF](gerar-pdf.md): exporter instructions, excluded from the submission PDF.

## Historical records

The [development history](diario.md), [data audit](auditoria-dados-2026-11-02.md) and dated Groq/Qwen and Flash 3.6 reports describe their respective revisions. Counts, pending cases and older examples must be read in that context. Earlier example revisions remain in Git; `examples/` contains the current selection.

Reports preserve observed failures and do not establish general approval of the final version. Additional evidence under `local/` is not published; references identify local records rather than download links. The five published conversations support inspection of the selected flows.
