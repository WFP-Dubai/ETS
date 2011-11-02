import urllib2
import oauth2 as oauth

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic.simple import direct_to_template
from django.views.decorators.http import require_POST, require_GET
from django.conf import settings
from django.http import HttpResponseRedirect

from ..models import Warehouse

from .forms import ImportDataForm, ExportDataForm
from .models import UpdateLog

SERVER = "127.0.0.1:8000"
API_URL = 'http://%s/ets/api/offline/oauth/' % SERVER
WAREHOUSE = 'ISBX002'
request_token_url = 'http://%s/ets/oauth/request_token' % SERVER
access_token_url = 'http://%s/ets/oauth/access_token' % SERVER
authorize_url = 'http://%s/ets/oauth/authorize' % SERVER
callback_url = 'http://%s/ets/syncro/' % SERVER

def syncro(request):
    """requests data at server and import them localy"""
    if not 'oauth_token' in request.session or not 'oauth_token_secret' in request.session:

        consumer = oauth.Consumer(settings.CONSUMER_KEY,  settings.CONSUMER_SECRET)

        if 'oauth_token' not in request.GET :
            client = oauth.Client(consumer)
            resp, content = client.request(request_token_url)
            request_token = dict(urllib2.urlparse.parse_qsl(content))
            request.session['roauth_token'] = request_token['oauth_token']
            request.session['roauth_token_secret'] = request_token['oauth_token_secret']
            return HttpResponseRedirect(authorize_url+'?oauth_token='+request_token['oauth_token']+'&oauth_callback='+callback_url) 
        elif request.GET['oauth_token']:
            oauth_verifier = request.GET['oauth_token']
            token = oauth.Token(request.session.get('roauth_token', None), request.session.get('roauth_token_secret', None))
            token.set_verifier(oauth_verifier)
            client = oauth.Client(consumer, token)          
            resp, content = client.request(access_token_url)
            access_token = dict(urllib2.urlparse.parse_qsl(content))
            del request.session['roauth_token']
            del request.session['roauth_token_secret']
            request.session['oauth_token'] = access_token['oauth_token']
            request.session['oauth_token_secret'] = access_token['oauth_token_secret']
        
    consumer = oauth.Consumer(settings.CONSUMER_KEY,  settings.CONSUMER_SECRET)
    token = oauth.Token(request.session['oauth_token'], request.session['oauth_token_secret'])
    client = oauth.Client(consumer,token)
    resp, content = client.request("%s%s" % (API_URL, WAREHOUSE))
    UpdateLog.updata_data(content)
    return redirect('synchronization')
    
    

@login_required
def request_update(request):
    """requests data at server and import them localy"""
    last = None
    if UpdateLog.objects.count():
        last = UpdateLog.objects.latest("date")
    UpdateLog.request_data(last)

    return redirect('synchronization')

@require_POST
@login_required
def import_file(request, form_class=ImportDataForm):
    """imports file with data"""    
    form = form_class(request.POST or None, request.FILES or None)
    if form.is_valid():
        file = form.cleaned_data['file']
        UpdateLog.updata_data(file.read())
    return redirect('synchronization')

@require_GET
@login_required
def export_file(request, form_class=ExportDataForm):
    """exports file with data"""

    # auth = '%s:%s' % ('admin', 'admin')
    # auth = 'Basic %s' % base64.encodestring(auth)
    # auth = auth.strip()
    # extra = {
    #     'HTTP_AUTHORIZATION': auth,
    # }
    form = form_class(request.GET or None)
    if form.is_valid():
        warehouse = form.cleaned_data['warehouse']
        #return redirect('api_offline', warehouse_pk=warehouse.pk)
        return redirect('api_offline', warehouse_pk=warehouse.pk)
    return redirect('synchronization')

@login_required
def synchronization(request, template="synchronization.html", export_form=ExportDataForm, import_form=ImportDataForm):
    """
    Page for synchronization
    """
    warehouses = Warehouse.filter_by_user(request.user)
    if not warehouses:
        warehouses = Warehouse.objects.filter(compas__officers=request.user)
    export_form.base_fields['warehouse'].queryset = warehouses
        
    return direct_to_template(request, template, {
        'form_import': import_form,
        'form_export': export_form,
    })

