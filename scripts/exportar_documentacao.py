"""Gera um PDF do README e docs Markdown. Dependência opcional: reportlab."""
from pathlib import Path
from datetime import date
import hashlib
import html
import json
import re
import textwrap
from urllib.parse import quote

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
                               Spacer, PageBreak, LongTable, TableStyle, Preformatted)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf"
REPO = "https://github.com/LuccasBassani/emporio-agente"


def build():
    fonts = Path("C:/Windows/Fonts")
    for name, filename in [("Doc", "arial.ttf"), ("DocBold", "arialbd.ttf"),
                           ("DocItalic", "ariali.ttf"), ("DocBoldItalic", "arialbi.ttf"),
                           ("Code", "consola.ttf")]:
        pdfmetrics.registerFont(TTFont(name, str(fonts / filename)))
    pdfmetrics.registerFontFamily("Doc", normal="Doc", bold="DocBold",
                                  italic="DocItalic", boldItalic="DocBoldItalic")
    blue = colors.HexColor("#183E58")
    styles = getSampleStyleSheet()
    base = ParagraphStyle("BaseDoc", fontName="Doc", fontSize=9.3, leading=13.5,
                          spaceAfter=7, textColor=colors.HexColor("#253642"))
    tiny = ParagraphStyle("SmallDoc", parent=base, fontSize=7.4, leading=10.1, spaceAfter=2)
    heading = {i: ParagraphStyle(f"HeadingDoc{i}", parent=base, fontName="DocBold",
                 fontSize={1:21, 2:14, 3:11, 4:10}[min(i,4)],
                 leading={1:26, 2:19, 3:15, 4:14}[min(i,4)],
                 textColor=blue, spaceBefore=12, spaceAfter=8, keepWithNext=True)
               for i in range(1,5)}
    code = ParagraphStyle("CodeDoc", fontName="Code", fontSize=7.1, leading=9.4,
                          backColor=colors.HexColor("#F0F4F7"), borderPadding=7,
                          spaceBefore=5, spaceAfter=10)

    def inline(value, source):
        value = value.replace("\u2011", "-").replace("—", "-").replace("–", "-")
        value = value.replace("✅", "[x]").replace("☑", "[x]").replace("☐", "[ ]")
        value = html.escape(value)
        value = re.sub(r"`([^`]+)`", r'<font name="Code">\1</font>', value)
        value = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", value)
        def link(match):
            label, target = match.groups()
            target = html.unescape(target)
            if not target.startswith(("https://", "http://", "mailto:", "#")):
                target = REPO + "/blob/main/" + quote(str((source.parent / target).relative_to(ROOT)).replace("\\", "/"), safe="/#:")
            return f'<link href="{html.escape(target, quote=True)}" color="#17618A">{label}</link>'
        value = re.sub(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", link, value)
        return value

    class Doc(BaseDocTemplate):
        def afterFlowable(self, flowable):
            if hasattr(flowable, "toc_level"):
                key = flowable.bookmark
                self.canv.bookmarkPage(key)
                self.notify("TOCEntry", (flowable.toc_level, flowable.getPlainText(), self.page, key))

    def page(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#D8E2EA"))
        canvas.line(20*mm, 18*mm, 190*mm, 18*mm)
        canvas.setFillColor(blue)
        canvas.setFont("Doc", 7.4)
        canvas.drawString(20*mm, 12*mm, "Empório da Música | README e documentação")
        canvas.drawRightString(190*mm, 12*mm, str(doc.page))
        canvas.restoreState()

    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / "emporio-agente-readme-documentacao.pdf"
    doc = Doc(str(target), pagesize=A4, leftMargin=20*mm, rightMargin=20*mm,
              topMargin=20*mm, bottomMargin=24*mm,
              title="Empório da Música - README e documentação", author="Luccas Bassani")
    doc.addPageTemplates(PageTemplate(id="Main", frames=Frame(doc.leftMargin, doc.bottomMargin,
                         doc.width, doc.height, leftPadding=0, rightPadding=0,
                         topPadding=0, bottomPadding=0), onPage=page))
    story = [Spacer(1, 30*mm), Paragraph("Empório da Música", heading[1]),
             Paragraph("Agente de atendimento", heading[2]),
             Paragraph("README e documentação técnica", base),
             Spacer(1, 9*mm), Paragraph("Luccas Bassani | Desafio técnico de AI Engineer", base),
             Paragraph("Arquitetura, execução, decisões, auditoria dos dados, validação e evolução do produto.", base),
             Paragraph(f'<link href="{REPO}">{REPO}</link>', base),
             Spacer(1, 9*mm), Paragraph("Documento gerado dos arquivos Markdown versionados. O README apresenta o estado atual; registros datados preservam as evidências e decisões de cada etapa.", base),
             Paragraph(f"Gerado em {date.today().strftime('%d/%m/%Y')}.", base), PageBreak(),
             Paragraph("Sumário", heading[1])]
    toc = TableOfContents()
    toc.levelStyles = [ParagraphStyle("TOC0", parent=base, fontName="DocBold", fontSize=10,
                                      leading=15, spaceBefore=9),
                       ParagraphStyle("TOC1", parent=base, fontSize=8.3, leading=12, leftIndent=12)]
    story += [toc, PageBreak()]
    preferred = ["README.md", "docs/decisoes.md", "docs/evolucao-produto.md",
                 "docs/auditoria-dados-2026-11-02.md", "docs/cenarios-de-teste.md",
                 "docs/validacao-gemini-2026-11-03.md", "docs/validacao-qwen-retomada-2026-11-03.md",
                 "docs/guia-do-projeto.md", "docs/diario.md"]
    sources = [ROOT / p for p in preferred if (ROOT/p).exists()]
    sources += [p for p in sorted((ROOT/"docs").glob("*.md")) if p not in sources]
    serial = 0
    for chapter, source in enumerate(sources):
        if chapter:
            story.append(PageBreak())
        lines = source.read_text(encoding="utf-8").splitlines()
        story.append(Paragraph("Fonte: " + html.escape(str(source.relative_to(ROOT)).replace("\\", "/")), tiny))
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            if line.startswith("```"):
                lang, block = line[3:], []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    for wrapped in textwrap.wrap(lines[i], width=104, replace_whitespace=False,
                                                  drop_whitespace=False, break_long_words=True) or [""]:
                        block.append(wrapped.replace("\u2011", "-").replace("—", "-").replace("–", "-"))
                    i += 1
                if lang == "mermaid":
                    story.append(Paragraph("Diagrama de arquitetura - fonte Mermaid", tiny))
                # Blocos divididos em linhas permitem quebra de página sem cortes.
                for start in range(0, len(block), 32):
                    story.append(Preformatted("\n".join(block[start:start+32]), code))
                i += 1
                continue
            if line.startswith("|"):
                rows = []
                while i < len(lines) and lines[i].strip().startswith("|"):
                    cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                    if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                        rows.append(cells)
                    i += 1
                count = max(map(len, rows))
                if count == 3 and rows[0][0].casefold() in {"id", "caso"}:
                    widths = [.08,.39,.53]
                elif count == 4:
                    widths = [.10,.19,.32,.39]
                else:
                    widths = [1/count]*count
                data = [[Paragraph(inline(cell, source), tiny) for cell in row+[""]*(count-len(row))] for row in rows]
                table = LongTable(data, colWidths=[doc.width*w for w in widths], repeatRows=1, hAlign="LEFT")
                table.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#E4EDF4")),
                     ("VALIGN",(0,0),(-1,-1),"TOP"), ("BOX",(0,0),(-1,-1),.4,colors.HexColor("#CAD7E1")),
                     ("INNERGRID",(0,0),(-1,-1),.25,colors.HexColor("#DCE4EA")),
                     ("LEFTPADDING",(0,0),(-1,-1),5), ("RIGHTPADDING",(0,0),(-1,-1),5),
                     ("TOPPADDING",(0,0),(-1,-1),5), ("BOTTOMPADDING",(0,0),(-1,-1),5)]))
                story += [table, Spacer(1,9)]
                continue
            match = re.match(r"^(#{1,6})\s+(.+)$", line)
            if match:
                level = len(match[1])
                paragraph = Paragraph(inline(match[2],source), heading[min(level,4)])
                if level <= 2:
                    paragraph.toc_level = level-1
                    paragraph.bookmark = f"section-{serial}"
                    serial += 1
                story.append(paragraph)
                i += 1
                continue
            if line in {"---", "***"}:
                i += 1
                continue
            bullet = re.match(r"^(?:[-*]|\d+[.)])\s+(.+)$", line)
            if bullet:
                paragraph = ParagraphStyle("ListDoc", parent=base, leftIndent=11, firstLineIndent=-8)
                story.append(Paragraph("- " + inline(bullet[1],source), paragraph))
                i += 1
                continue
            parts = [line]
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r"^(?:#|\||```|[-*]\s|\d+[.)]\s)", lines[i].strip()):
                parts.append(lines[i].strip())
                i += 1
            # Imagens do Markdown são referidas pela legenda; nenhuma captura privada é incorporada.
            text = " ".join(parts)
            text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"Figura disponível no repositório: \1.", text)
            story.append(Paragraph(inline(text,source),base))
    doc.multiBuild(story)
    manifest = {str(p.relative_to(ROOT)).replace("\\", "/"):
                hashlib.sha256(p.read_text(encoding="utf-8").encode("utf-8")).hexdigest() for p in sources}
    (OUT/"fontes-documentacao.json").write_text(json.dumps(
        {"normalizacao": "UTF-8, finais de linha LF", "arquivos": manifest}, indent=2), encoding="utf-8")
    print(target)


if __name__ == "__main__":
    build()
