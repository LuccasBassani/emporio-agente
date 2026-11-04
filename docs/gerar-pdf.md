# Generate the submission PDF

From the repository root, run in PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-docs.txt
.\.venv\Scripts\python.exe scripts/exportar_documentacao.py
```

Output: `output/pdf/emporio-agente-readme-documentacao.pdf`.

The exporter uses Windows Arial and Consolas fonts and includes only the README and `docs/entrega.md`. Explanations are in English; the five conversations remain in their original Portuguese as evidence. This generation guide and historical records are excluded from the PDF.

For the application form, use the filename **Luccas Bassani - AI Engineer.pdf**, following the requested name/career convention.
