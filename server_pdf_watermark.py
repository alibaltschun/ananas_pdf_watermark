from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader
from flask import Flask, request, send_file, current_app as app

app = Flask(__name__)


@app.route('/pdf')
def show_static_pdf():
    input_file = PdfFileReader(open('./pdf_target.pdf', "rb"))

    text = request.args.get('text', 'empty')
    
    c = canvas.Canvas('watermark.pdf')
    
    if text:
         c.setFontSize(12)
         c.setFont('Helvetica-Bold', 12)
         c.drawString(15, 15,text)
    c.save()
    watermark = PdfFileReader(open("watermark.pdf", "rb"))
    
    output_file = PdfFileWriter()
    
    page_count = input_file.getNumPages()
    for page_number in range(page_count):
        input_page = input_file.getPage(page_number)
        if page_number < 3:
            input_page.mergePage(watermark.getPage(0))
        output_file.addPage(input_page)
    
    output_pdf = './output_pdf.pdf'
    with open(output_pdf, "wb") as outputStream:
        output_file.write(outputStream)
    
    file = open(output_pdf, "rb")
    return send_file(file, attachment_filename='I Hate Diet - Online PDF Program - V2.pdf',as_attachment=True, mimetype='application/pdf')


app.run(host='localhost', port=5000)