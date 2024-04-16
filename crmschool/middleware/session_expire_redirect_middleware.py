from django.contrib import messages
from django.contrib.auth import logout
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import redirect
from datetime import datetime
from crmschool import settings


class SessionExpireRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity_str = request.session.get('last_activity')
            if last_activity_str:
                last_activity = datetime.fromisoformat(last_activity_str)
                if (timezone.now() - last_activity).seconds > settings.SESSION_COOKIE_AGE:
                    # Session has expired, log the user out
                    del request.session['last_activity']
                    return redirect(reverse('login'))  # Redirect to logout URL
                # Update last activity time in session
            request.session['last_activity'] = timezone.now().isoformat()
        response = self.get_response(request)
        return response
