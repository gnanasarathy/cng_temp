from fpdf import FPDF

text = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus lacinia odio vitae vestibulum vestibulum. Cras venenatis euismod malesuada. Nullam ac magna et felis lacinia varius. Praesent ac mauris non purus semper egestas. Maecenas lacinia, 
* lorem ut dignissim porta 
* neque metus viverra risus
* non volutpat tortor nisi non orci.
"""

class CreatePDF():
    def __init__(self, font, size) -> None:
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.set_font(font, size = size)
    
    def add_heading(self, text, align_center = True):
        if align_center:
            self.pdf.cell(200, 10, txt = text, ln = True,  align = 'C')
        else:
            self.pdf.cell(200, 10, txt = text, ln = True)
    
    def add_text(self, text, align_center = False):
        if align_center:
            self.pdf.multi_cell(0, 10, text, align = 'C')
        else:
            self.pdf.multi_cell(0, 10, text)

    def save_pdf(self, file_name):
        self.pdf.output(file_name)

c = CreatePDF("Arial", 12)
c.add_heading("PDF created using Python")
c.add_text(text)
c.save_pdf("output.pdf")

