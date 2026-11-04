"""Export the README and selected documentation to the submission PDF."""

import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import textwrap
from urllib.parse import quote

from reportlab.graphics.shapes import Drawing, Line, Polygon, Rect, String
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, LongTable, PageBreak, PageTemplate, Paragraph,
    Preformatted, Spacer, TableStyle,
)


REPO = "https://github.com/LuccasBassani/emporio-agente"
DEFAULT_ROOT = Path(__file__).resolve().parents[1]
SOURCES = ("README.md", "docs/entrega.md")
EXAMPLES = (
    "catalogo-e-pix.md", "rag-promocao-pix.md", "rag-parcelamento.md",
    "pedido-rastreamento.md", "fora-do-escopo.md",
)
INK = colors.HexColor("#24342E")
GREEN = colors.HexColor("#214B3B")
ACCENT = colors.HexColor("#954D3E")
PALE = colors.HexColor("#F1F5F2")
RULE = colors.HexColor("#D7E2DA")


def register_fonts():
    directory = Path("C:/Windows/Fonts")
    for name, filename in (
        ("Doc", "arial.ttf"), ("DocBold", "arialbd.ttf"),
        ("DocItalic", "ariali.ttf"), ("DocBoldItalic", "arialbi.ttf"),
        ("Code", "consola.ttf"),
    ):
        pdfmetrics.registerFont(TTFont(name, str(directory / filename)))
    pdfmetrics.registerFontFamily(
        "Doc", normal="Doc", bold="DocBold", italic="DocItalic",
        boldItalic="DocBoldItalic",
    )


def inline(value, source, root):
    value = value.replace("\u2011", "-").replace("\u2013", "-").replace("\u2014", "-")
    value = html.escape(value)
    value = re.sub(r"`([^`]+)`", r'<font name="Code">\1</font>', value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", value)

    def link(match):
        label, target = match.groups()
        target = html.unescape(target)
        if not target.startswith(("https://", "http://", "mailto:", "#")):
            path, separator, fragment = target.partition("#")
            resolved = (source.parent / path).resolve()
            relative = resolved.relative_to(root.resolve()).as_posix()
            target = REPO + "/blob/main/" + quote(relative, safe="/")
            if separator:
                target += "#" + quote(fragment, safe="-_")
        return f'<link href="{html.escape(target, quote=True)}" color="#285D48">{label}</link>'

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, value)


def architecture(width):
    drawing = Drawing(width, 137)
    scale = width / 490

    def x(value):
        return value * scale

    def box(left, bottom, box_width, label, detail):
        drawing.add(Rect(x(left), bottom, x(box_width), 42, rx=5, ry=5,
                         strokeColor=RULE, fillColor=PALE, strokeWidth=.7))
        drawing.add(String(x(left + box_width / 2), bottom + 25, label,
                           fontName="DocBold", fontSize=9.2,
                           textAnchor="middle", fillColor=GREEN))
        drawing.add(String(x(left + box_width / 2), bottom + 11, detail,
                           fontName="Doc", fontSize=8.2,
                           textAnchor="middle", fillColor=INK))

    def arrow(start_x, start_y, end_x, end_y, both=False):
        drawing.add(Line(x(start_x), start_y, x(end_x), end_y,
                         strokeColor=ACCENT, strokeWidth=.8))
        if start_y == end_y:
            drawing.add(Polygon([x(end_x), end_y, x(end_x - 4), end_y + 2,
                                 x(end_x - 4), end_y - 2],
                                fillColor=ACCENT, strokeColor=ACCENT))
            if both:
                drawing.add(Polygon([x(start_x), start_y, x(start_x + 4), start_y + 2,
                                     x(start_x + 4), start_y - 2],
                                    fillColor=ACCENT, strokeColor=ACCENT))
        else:
            drawing.add(Polygon([x(end_x), end_y, x(end_x - 2), end_y + 4,
                                 x(end_x + 2), end_y + 4],
                                fillColor=ACCENT, strokeColor=ACCENT))

    box(0, 84, 126, "Interface", "Streamlit / terminal")
    box(182, 84, 126, "Python agent", "rules and tools")
    box(364, 84, 126, "Model", "Gemini / Groq / Ollama")
    arrow(128, 105, 180, 105, both=True)
    arrow(310, 105, 362, 105, both=True)
    box(0, 8, 145, "Catalog and prices", "products and promotions / CSV")
    box(172, 8, 145, "Orders", "customer-scoped access / CSV")
    box(344, 8, 145, "Policies", "BM25 retrieval / PDF")
    drawing.add(Line(x(245), 84, x(245), 67, strokeColor=ACCENT, strokeWidth=.8))
    drawing.add(Line(x(72.5), 67, x(416.5), 67, strokeColor=ACCENT, strokeWidth=.8))
    for center in (72.5, 245, 416.5):
        arrow(center, 67, center, 52)
    return drawing


def styles():
    body = ParagraphStyle("Body", fontName="Doc", fontSize=9.7, leading=13.5,
                          textColor=INK, spaceAfter=6)
    return {
        "body": body,
        "small": ParagraphStyle("Small", parent=body, fontSize=8.3, leading=11.3),
        "h1": ParagraphStyle("H1", parent=body, fontName="DocBold", fontSize=21,
                             leading=25, textColor=GREEN, spaceAfter=11, keepWithNext=True),
        "h2": ParagraphStyle("H2", parent=body, fontName="DocBold", fontSize=12.6,
                             leading=16.2, textColor=GREEN, spaceBefore=11,
                             spaceAfter=6, keepWithNext=True),
        "h3": ParagraphStyle("H3", parent=body, fontName="DocBold", fontSize=10.5,
                             leading=14, textColor=GREEN, spaceBefore=8,
                             spaceAfter=5, keepWithNext=True),
        "label": ParagraphStyle("Label", parent=body, fontName="DocBold", fontSize=8.2,
                                leading=11, textColor=ACCENT, spaceBefore=5,
                                spaceAfter=2, keepWithNext=True),
        "bullet": ParagraphStyle("Bullet", parent=body, leftIndent=9, firstLineIndent=-7),
        "code": ParagraphStyle("CodeBlock", fontName="Code", fontSize=8.1,
                               leading=11, backColor=PALE, borderPadding=7,
                               spaceBefore=3, spaceAfter=9),
        "cell": ParagraphStyle("Cell", parent=body, fontSize=9, leading=12.3,
                               spaceAfter=1),
    }


def markdown(source, root, width, sty):
    lines = source.read_text(encoding="utf-8").splitlines()
    story, index = [], 0
    while index < len(lines):
        line = lines[index].strip()
        index += 1
        if not line:
            continue
        if line == "<!-- pagebreak -->":
            story.append(PageBreak())
            continue
        if line.startswith("<!--"):
            raise ValueError(f"Unresolved marker in {source.name}: {line}")
        if line.startswith("```"):
            language, block = line[3:], []
            while index < len(lines) and not lines[index].strip().startswith("```"):
                block.extend(textwrap.wrap(lines[index], width=91, replace_whitespace=False,
                                           drop_whitespace=False) or [""])
                index += 1
            index += 1
            if language == "mermaid":
                story += [architecture(width), Spacer(1, 3)]
            else:
                story.append(Preformatted("\n".join(block), sty["code"]))
            continue
        if line.startswith("|"):
            rows = []
            while True:
                cells = [value.strip() for value in line.strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", value) for value in cells):
                    rows.append(cells)
                if index == len(lines) or not lines[index].strip().startswith("|"):
                    break
                line = lines[index].strip()
                index += 1
            count = len(rows[0])
            table = LongTable(
                [[Paragraph(inline(cell, source, root), sty["cell"]) for cell in row]
                 for row in rows], colWidths=[width / count] * count, repeatRows=1,
                hAlign="LEFT",
            )
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), PALE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LINEBELOW", (0, 0), (-1, 0), .8, GREEN),
                ("LINEBELOW", (0, 1), (-1, -1), .35, RULE),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]))
            story += [table, Spacer(1, 7)]
            continue
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            level = min(len(heading[1]), 3)
            story.append(Paragraph(inline(heading[2], source, root), sty[f"h{level}"]))
            continue
        if line in {"**Customer**", "**Lia**"}:
            story.append(Paragraph(line.strip("*"), sty["label"]))
            continue
        bullet = re.match(r"^([-*]|\d+[.)])\s+(.+)$", line)
        if bullet:
            prefix = bullet[1] if bullet[1][0].isdigit() else "-"
            story.append(Paragraph(prefix + " " + inline(bullet[2], source, root), sty["bullet"]))
            continue
        parts = [line]
        while index < len(lines) and lines[index].strip() and not re.match(
                r"^(?:#|\||```|<!--|[-*]\s|\d+[.)]\s)", lines[index].strip()):
            parts.append(lines[index].strip())
            index += 1
        text = " ".join(parts)
        style = sty["small"] if text.startswith(("Luccas Bassani |", "Full export:")) else sty["body"]
        story.append(Paragraph(inline(text, source, root), style))
    return story


def build(root=DEFAULT_ROOT, target=None):
    root = Path(root).resolve()
    target = Path(target) if target else root / "output/pdf/emporio-agente-readme-documentacao.pdf"
    target.parent.mkdir(parents=True, exist_ok=True)
    register_fonts()
    doc = BaseDocTemplate(
        str(target), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=21 * mm, bottomMargin=20 * mm,
        title="Empório da Música - README and documentation", author="Luccas Bassani",
    )

    def page(canvas, document):
        canvas.saveState()
        canvas.setFillColor(GREEN)
        canvas.setFont("DocBold", 7.6)
        canvas.drawString(18 * mm, A4[1] - 12 * mm, "EMPÓRIO DA MÚSICA")
        canvas.setFont("Doc", 7.6)
        canvas.drawRightString(A4[0] - 18 * mm, A4[1] - 12 * mm, "README and technical documentation")
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(.5)
        canvas.line(18 * mm, 15 * mm, A4[0] - 18 * mm, 15 * mm)
        canvas.setFillColor(INK)
        canvas.setFont("Doc", 7.5)
        canvas.drawString(18 * mm, 10.5 * mm, "Luccas Bassani | AI Engineer - Artefact")
        canvas.drawRightString(A4[0] - 18 * mm, 10.5 * mm, str(document.page))
        canvas.restoreState()

    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates(PageTemplate(id="Main", frames=frame, onPage=page))
    story, sty = [], styles()
    for index, relative in enumerate(SOURCES):
        if index:
            story.append(PageBreak())
        story.extend(markdown(root / relative, root, doc.width, sty))
    doc.build(story)

    used = [*SOURCES, *("examples/" + name for name in EXAMPLES)]
    manifest = {
        "normalization": "UTF-8, LF line endings",
        "files": {
            relative: hashlib.sha256((root / relative).read_text(encoding="utf-8").encode("utf-8")).hexdigest()
            for relative in used
        },
    }
    (target.parent / "fontes-documentacao.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print(target)
    return target


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--output", type=Path)
    options = parser.parse_args()
    build(options.root, options.output)
