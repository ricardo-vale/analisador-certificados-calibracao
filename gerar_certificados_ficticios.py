# Gera 4 certificados de calibração FICTÍCIOS (padrões de pressão) + gabarito.
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import csv

LAB = "Laboratório Delta de Metrologia (fictício)"
LAB_END = "Rua das Medições, 100 – Distrito Industrial – Cidade Exemplo/UF"
CLIENTE = "Laboratório de Calibração Ômega (fictício)"
CLI_END = "Av. dos Padrões, 2000 – Centro – Cidade Modelo/UF"
W, H = A4

# cada certificado: dados + quais itens do checklist omitir
CERTS = [
    dict(num="DLT-P-2026/0101", arq="CERT-001_ref_0-10MPa", tipo="ref",
         item="Manômetro digital – padrão de referência", fab="Fabricante X", mod="PX-500",
         serie="X50-1234", tag="PAD-REF-01", faixa_txt="(0 a 10) MPa", fe=10.0, un="MPa",
         res="0,001 MPa", pts=[0, 2, 4, 6, 8, 10],
         cres=[0, 2.002, 4.001, 6.003, 8.002, 10.003], dec=[0, 2.003, 4.003, 6.004, 8.004, 10.004],
         U=[None, 0.0015, 0.0015, 0.0015, 0.0015, 0.0015], omit=[]),
    dict(num="DLT-P-2026/0102", arq="CERT-002_trab_0-20MPa", tipo="trab",
         item="Manômetro digital – padrão de trabalho", fab="Fabricante Y", mod="DY-20",
         serie="Y20-5678", tag="PAD-TRB-03", faixa_txt="(0 a 20) MPa", fe=20.0, un="MPa",
         res="0,01 MPa", pts=[0, 4, 8, 12, 16, 20],
         cres=[0, 4.01, 8.02, 12.02, 16.03, 20.03], dec=[0, 4.02, 8.03, 12.04, 16.04, 20.04],
         U=[None, 0.012, 0.012, 0.015, 0.018, 0.025], omit=[]),
    dict(num="DLT-P-2026/0103", arq="CERT-003_analog_0-1600kPa", tipo="analog",
         item="Manômetro analógico – padrão", fab="Fabricante Z", mod="AZ-160",
         serie="Z16-9012", tag="PAD-ANL-02", faixa_txt="(0 a 1600) kPa", fe=1600.0, un="kPa",
         res="divisão de escala 10 kPa; classe declarada 0,5 %", div=10.0, classe=0.5,
         pts=[0, 400, 800, 1200, 1600],
         cres=[0, 402, 801, 1203, 1602], dec=[0, 404, 805, 1206, 1604],
         U=[None, 2.5, 2.5, 2.5, 2.5], omit=["k", "l_k"]),
    dict(num="DLT-P-2026/0104", arq="CERT-004_ref_0-2000kPa", tipo="ref",
         item="Manômetro digital – padrão de referência", fab="Fabricante X", mod="PX-200",
         serie="X20-3456", tag="PAD-REF-02", faixa_txt="(0 a 2000) kPa", fe=2000.0, un="kPa",
         res="0,1 kPa", pts=[0, 500, 1000, 1500, 2000],
         cres=[0, 500.3, 1000.4, 1500.6, 2000.5], dec=[0, 500.5, 1000.6, 1501.1, 2000.8],
         U=[None, 0.3, 0.3, 0.3, 0.3], omit=["f", "m", "o"]),
]

def br(x, nd):
    return f"{x:.{nd}f}".replace(".", ",")

def nd_of(c):
    return {"MPa": 3 if c["fe"] <= 10 else 2, "kPa": 1 if c["fe"] <= 2000 and c["tipo"] != "analog" else 0}[c["un"]]

def gerar(c):
    p = canvas.Canvas(f"/home/claude/certs/{c['arq']}.pdf", pagesize=A4)
    total = 2
    def marca(pag):
        p.saveState()
        p.setFont("Helvetica-Bold", 38); p.setFillGray(0.88)
        p.translate(W/2, H/2); p.rotate(40)
        p.drawCentredString(0, 0, "FICTÍCIO – USO DIDÁTICO"); p.restoreState()
        p.setFont("Helvetica-Bold", 11)
        p.drawString(20*mm, H-20*mm, LAB)
        p.setFont("Helvetica", 8)
        p.drawString(20*mm, H-25*mm, LAB_END + " – Acreditação nº CAL-0000 (fictícia)")
        p.drawRightString(W-20*mm, H-20*mm, f"Certificado nº {c['num']}")
        if "o" not in c["omit"]:
            p.drawRightString(W-20*mm, H-25*mm, f"Página {pag}/{total}")
        p.line(20*mm, H-28*mm, W-20*mm, H-28*mm)

    # ---------- página 1 ----------
    marca(1)
    y = H-40*mm
    p.setFont("Helvetica-Bold", 14); p.drawCentredString(W/2, y, "CERTIFICADO DE CALIBRAÇÃO"); y -= 12*mm
    def linha(rot, txt, b=False):
        nonlocal y
        p.setFont("Helvetica-Bold", 9); p.drawString(20*mm, y, rot)
        p.setFont("Helvetica-Bold" if b else "Helvetica", 9); p.drawString(62*mm, y, txt); y -= 5.5*mm
    linha("Cliente:", CLIENTE); linha("Endereço:", CLI_END); y -= 3*mm
    linha("Item:", c["item"]); linha("Fabricante / Modelo:", f"{c['fab']} / {c['mod']}")
    linha("Nº de série / Tag:", f"{c['serie']} / {c['tag']}")
    linha("Faixa nominal:", c["faixa_txt"]); linha("Resolução:", c["res"]); y -= 3*mm
    linha("Procedimento:", "PT-PRE-01, revisão 3 – calibração por comparação")
    linha("Local da calibração:", "Instalações permanentes do laboratório")
    linha("Data da calibração:", "05/11/2026"); linha("Data de emissão:", "06/11/2026"); y -= 3*mm
    if "f" not in c["omit"]:
        linha("Padrão utilizado:", "Transmissor de pressão PDL-TP-01 – Cert. nº LAB-R-2026/551 – validade 03/2027")
    if "m" in c["omit"]:
        linha("Rastreabilidade:", "Padrões rastreáveis.")
    else:
        linha("Rastreabilidade:", "Padrão rastreável ao SI via RBC (Cert. nº LAB-R-2026/551, laboratório acreditado).")
    if "k" not in c["omit"]:
        linha("Condições ambientais:", "Temperatura (20,0 ± 1,0) °C; umidade relativa (50 ± 10) %")
    y -= 3*mm
    p.setFont("Helvetica", 8.5)
    if "l_k" in c["omit"]:
        txt = ["A incerteza expandida U está declarada na tabela de resultados."]
    else:
        txt = ["A incerteza expandida U é a incerteza padrão combinada multiplicada pelo fator de abrangência k,",
               "para uma probabilidade de abrangência de aproximadamente 95 %."]
    for t in txt: p.drawString(20*mm, y, t); y -= 4.5*mm
    p.drawString(20*mm, y, "Os resultados referem-se somente ao item calibrado. Indicação do padrão: média de 3 séries."); y -= 4.5*mm
    p.showPage()

    # ---------- página 2 ----------
    marca(2)
    y = H-40*mm
    p.setFont("Helvetica-Bold", 11); p.drawString(20*mm, y, "RESULTADOS"); y -= 8*mm
    un = c["un"]; nd = nd_of(c)
    cols = [f"Instrumento ({un})", f"Padrão cresc. ({un})", f"Padrão decresc. ({un})", f"U ({un})"]
    if "l_k" not in c["omit"]: cols.append("k")
    xs = [20, 55, 92, 132, 160]
    p.setFont("Helvetica-Bold", 8.5)
    for x, t in zip(xs, cols): p.drawString(x*mm, y, t)
    y -= 2*mm; p.line(20*mm, y, W-20*mm, y); y -= 5*mm
    p.setFont("Helvetica", 9)
    ndU = 4 if (un == "MPa" and c["fe"] <= 10) else 3
    for i, pt in enumerate(c["pts"]):
        vals = [br(pt, nd), br(c["cres"][i], nd), br(c["dec"][i], nd),
                "-" if c["U"][i] is None else br(c["U"][i], ndU if un == "MPa" else 1)]
        if "l_k" not in c["omit"]: vals.append("-" if c["U"][i] is None else "2,00")
        for x, t in zip(xs, vals): p.drawString(x*mm, y, t)
        y -= 5.5*mm
    y -= 15*mm
    p.setFont("Helvetica", 9)
    p.drawString(20*mm, y, "Ana Exemplo da Silva (fictícia)"); y -= 4.5*mm
    p.drawString(20*mm, y, "Signatária Autorizada"); y -= 10*mm
    p.setFont("Helvetica-Oblique", 8)
    p.drawString(20*mm, y, "Fim do certificado.")
    p.showPage(); p.save()

def gabarito(c):
    fe = c["fe"]; errs = []
    for i, pt in enumerate(c["pts"]):
        if pt == 0: continue
        errs.append(max(abs(pt - c["cres"][i]), abs(pt - c["dec"][i])))
    emax = max(errs); umax = max(u for u in c["U"] if u is not None)
    if c["tipo"] == "ref":   lim_e, lim_u = 0.0005*fe, 0.0002*fe
    elif c["tipo"] == "trab": lim_e, lim_u = 0.0025*fe, 0.001*fe
    else:                    lim_e, lim_u = c["classe"]/100*fe, c["div"]/2
    met = "APROVADO" if (emax <= lim_e + 1e-9 and umax <= lim_u + 1e-9) else "REPROVADO"
    nomes = {"f": "f) padrão não identificado", "m": "m) rastreabilidade sem evidência",
             "o": "o) sem numeração de página", "k": "k) sem condições ambientais",
             "l_k": "l) sem fator k e nível de confiança"}
    doc = "; ".join(nomes[o] for o in c["omit"]) or "nenhuma"
    return dict(certificado=c["num"], arquivo=c["arq"] + ".pdf", tipo=c["tipo"], unidade=c["un"],
                erro_max=round(emax, 4), lim_erro=round(lim_e, 4), U_max=umax, lim_U=round(lim_u, 4),
                resultado_metrologico=met, pendencias_documentais=doc,
                parecer=("APROVADO" if met == "APROVADO" and not c["omit"] else
                         "REPROVADO" if met == "REPROVADO" else "PENDENTE – solicitar correção"))

rows = []
for c in CERTS:
    gerar(c); rows.append(gabarito(c))
with open("/home/claude/certs/gabarito.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys(), delimiter=";"); w.writeheader(); w.writerows(rows)
for r in rows: print(r)
