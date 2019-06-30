from django.conf import settings
from django.contrib.auth.models import AnonymousUser


class GetUserMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.session.modified = True
        request.session['logged_in'] = False
        if not isinstance(request.user, AnonymousUser):
            request.session['logged_in'] = True
        return self.get_response(request)

    def process_exception(self, request, exception):
        pass