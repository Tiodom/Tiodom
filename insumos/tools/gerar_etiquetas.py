"""Gera o PDF de etiquetas QR dos insumos (A4, 3x5 por folha).

Uso: python3 gerar_etiquetas.py backup/insumos.json etiquetas/etiquetas-qr.pdf
O QR traz "INS:<id>"; o app abre o insumo direto quando o HF bipa.
"""
import json, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF

APP = "https://claude.ai/artifact/ThvGpgJm43bdjrFrZTXEGG"
COLS, ROWS = 3, 5
MARGEM = 10 * mm


def qr_draw(c, valor, x, y, lado):
    w = qr.QrCodeWidget(valor, barLevel="M")
    b = w.getBounds()
    d = Drawing(lado, lado, transform=[lado / (b[2] - b[0]), 0, 0, lado / (b[3] - b[1]), 0, 0])
    d.add(w)
    renderPDF.draw(d, c, x, y)


def quebra(c, texto, largura, fonte, tam):
    linhas, atual = [], ""
    for p in texto.split():
        t = (atual + " " + p).strip()
        if c.stringWidth(t, fonte, tam) <= largura:
            atual = t
        else:
            linhas.append(atual)
            atual = p
    return linhas + [atual]


def main(entrada, saida):
    itens = json.load(open(entrada, encoding="utf8"))
    etiquetas = [("abrir o app de insumos", APP, "link do app")]
    etiquetas += sorted(((v["nome"], "INS:" + k, k) for k, v in itens.items() if v.get("ativo", True)),
                        key=lambda e: e[0])
    W, H = A4
    cw, ch = (W - 2 * MARGEM) / COLS, (H - 2 * MARGEM) / ROWS
    c = canvas.Canvas(saida, pagesize=A4)
    c.setTitle("Etiquetas QR - Insumos T2")
    for n, (nome, valor, cod) in enumerate(etiquetas):
        if n and n % (COLS * ROWS) == 0:
            c.showPage()
        col, lin = n % COLS, (n // COLS) % ROWS
        x, y = MARGEM + col * cw, H - MARGEM - (lin + 1) * ch
        c.setDash(2, 3); c.setStrokeGray(0.6); c.rect(x, y, cw, ch); c.setDash()
        lado = min(cw, ch) - 22 * mm
        qr_draw(c, valor, x + (cw - lado) / 2, y + ch - lado - 4 * mm, lado)
        c.setFillGray(0)
        ty = y + ch - lado - 9 * mm
        for l in quebra(c, nome.upper(), cw - 6 * mm, "Helvetica-Bold", 10)[:2]:
            c.setFont("Helvetica-Bold", 10); c.drawCentredString(x + cw / 2, ty, l); ty -= 11
        c.setFont("Helvetica", 7); c.setFillGray(0.35)
        c.drawCentredString(x + cw / 2, y + 3 * mm, cod)
    c.save()
    print(len(etiquetas), "etiquetas ->", saida)


if __name__ == "__main__":
    main(*sys.argv[1:3])
