# importing the necessary libraries
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa  
# from weasyprint import HTML
# import pdfkit

# defining the function to convert an HTML file to a PDF file
@staticmethod
def html_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
   
    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="output.pdf"'

    font_path = '/static/fonts/arialuni.ttf'
    # Generate PDF using xhtml2pdf
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response
    # pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result, string=html)
    # if not pdf.err:
    #     return HttpResponse(result.getvalue(), content_type='application/pdf')
    # return None
    
    # Function to handle file links
def FileLink(uri, font_path):
    if uri.startswith(font_path):
        return uri

    if uri.startswith("/"):
        return uri

    return f'{font_path}#{uri}'