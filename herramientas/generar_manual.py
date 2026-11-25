"""Exporta docs/manual_usuario.md a PDF."""
from pathlib import Path

import markdown
from xhtml2pdf import pisa

DOCS = Path(__file__).resolve().parent.parent / "docs"

ESTILO = """
@page { size: letter; margin: 1.7cm 1.9cm; }
body { font-family: Helvetica; font-size: 9.6pt; line-height: 1.35; color: #141a2e; }
h1 { font-size: 15pt; margin: 0 0 6pt; }
h2 { font-size: 11.5pt; margin: 9pt 0 3pt; }
h3 { font-size: 10pt; margin: 6pt 0 2pt; }
p { margin: 0 0 4pt; }
table { width: 100%; border: 0.5pt solid #b9c6d1; margin: 2pt 0 6pt; }
th { background-color: #dbe5ec; text-align: left; }
th, td { padding: 2.5pt 4pt; border-bottom: 0.5pt solid #d5dde4; }
pre { background-color: #eef3f7; padding: 5pt; font-size: 8.6pt; }
code { font-family: Courier; }
"""

# Helvetica integrada no incluye el signo menos tipográfico
REEMPLAZOS = {"−": "-"}


def generar():
    texto = (DOCS / "manual_usuario.md").read_text(encoding="utf-8")
    for original, sustituto in REEMPLAZOS.items():
        texto = texto.replace(original, sustituto)
    cuerpo = markdown.markdown(texto, extensions=["tables"])
    html = f"<html><head><meta charset='utf-8'><style>{ESTILO}</style></head><body>{cuerpo}</body></html>"
    with open(DOCS / "manual_usuario.pdf", "wb") as salida:
        if pisa.CreatePDF(html, dest=salida, encoding="utf-8").err:
            raise SystemExit("No se pudo generar el PDF")


if __name__ == "__main__":
    generar()
