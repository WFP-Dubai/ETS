
from django.contrib.auth.views import login
from django.utils.translation import ugettext

from django.contrib.auth.middleware import AuthenticationMiddleware

from piston.authentication import HttpBasicAuthentication

class RequiredAuthenticationMiddleware(object):
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        
        #DIRTY HACK. CHANGE IT LATER.
        print "hasattr(view_func, 'authentication') --> %s " % hasattr(view_func, 'authentication')
        print "isinstance(view_func.authentication, HttpBasicAuthentication) --> %s" % isinstance(view_func.authentication, HttpBasicAuthentication)
        print "view_func.authentication --> %s " % view_func.authentication
        print "view_func.authentication --> %s " % type(view_func.authentication)
        if hasattr(view_func, 'authentication') and  isinstance(view_func.authentication, HttpBasicAuthentication):
            return
        
        if not request.user.is_authenticated():
            return login(request, extra_context={"extra_error": ugettext("The system requires you to be authenticated.")})
        elif not request.user.is_active:
            return login(request, extra_context={"extra_error": ugettext("Your account is not active.")})
        