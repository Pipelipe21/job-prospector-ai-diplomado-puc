from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', size=12)
pdf.cell(200, 10, txt="CV de Carlos: Desarrollador Backend Experto.", ln=1)
pdf.cell(200, 10, txt="Conocimiento avanzado en Flask, Python, AWS y Docker.", ln=1)
pdf.output("dummy_cv.pdf")
print("PDF Dummy creado exitosamente.")
