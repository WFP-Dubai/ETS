import cStringIO as StringIO
import ho.pisa as pisa
from cgi import escape
import os.path

from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse
from django.template import RequestContext

def render_to_pdf(request, template_name, context, file_name):
    """Renders template with context to HTML, than to PDF"""

    context_dict = {"STATIC_URL": settings.STATIC_URL}
    context_dict.update(context)

    html = render_to_string(template_name, context_dict, RequestContext(request))
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode('utf-8')), 
                            result, debug=True, encoding='utf-8', show_error_as_pdf=True,
                            link_callback=fetch_resources, xhtml=False)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=%s.pdf' % file_name
        return response
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

def fetch_resources(uri, rel):
    """
    Callback to allow pisa/reportlab to retrieve Images,Stylesheets, etc.
    `uri` is the href attribute from the html link element.
    `rel` gives a relative path, but it's not used here.

    """
    if uri.startswith(settings.STATIC_URL):
        path = os.path.abspath(os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, "")))
    elif uri.startswith(settings.MEDIA_URL):
        path = os.path.abspath(os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, "")))
    else:
        path = uri
    return path
