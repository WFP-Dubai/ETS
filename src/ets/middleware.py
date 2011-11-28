
from django.contrib.auth.views import login
from django.utils.translation import ugettext

from django.contrib.auth.middleware import AuthenticationMiddleware

class RequiredAuthenticationMiddleware(AuthenticationMiddleware):
    
    def process_request(self, request):
        super(RequiredAuthenticationMiddleware, self).process_request(request)
        
        if not request.user.id:
            return login(request, extra_context={"extra_error": ugettext("The system requires you to be authorized.")})
        elif not request.user.is_active:
            return login(request, extra_context={"extra_error": ugettext("Your account is not active.")})
        else:
            pass
