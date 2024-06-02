import time
from django.conf import settings
from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin
from rest_framework.authtoken.models import Token


class AutoLogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return

        current_time = time.time()
        last_activity = request.session.get('last_activity', current_time)

        if current_time - last_activity > settings.AUTO_LOGOUT_DELAY:
            Token.objects.filter(user=request.user).delete()
            logout(request)
        else:
            request.session['last_activity'] = current_time

