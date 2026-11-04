# Gerar o PDF de entrega

Na raiz do repositório, execute no PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-docs.txt
.\.venv\Scripts\python.exe scripts/exportar_documentacao.py
```

Saída: `output/pdf/emporio-agente-readme-documentacao.pdf`.

O exportador usa as fontes Arial e Consolas do Windows e reúne somente o README e `docs/entrega.md`, com as falas selecionadas dos cinco exemplos. Este guia de geração e os registros de desenvolvimento ficam fora do PDF.
