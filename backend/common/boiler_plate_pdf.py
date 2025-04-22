# from tempfile import NamedTemporaryFile
# from django.core.files.storage import default_storage


# from reportlab.lib.pagesizes import A4
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
# from reportlab.lib import colors
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.units import mm, inch
# from reportlab.lib.enums import TA_CENTER


# def boiler_plate():
#     buffer = NamedTemporaryFile(delete=False, suffix='.pdf')

#     # Create PDF document
#     doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=20, rightMargin=20, topMargin= 20, bottomMargin=20)
#     elements = []


#     doc.build(elements)

#     # Save the PDF file
#     buffer.seek(0)
#     pdf_path = default_storage.save(f'{""}_{""}.pdf', buffer)

#     return pdf_path