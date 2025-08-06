# Django-Middleware-0x03/apps/core/middleware/middleware.py

import logging
from datetime import datetime
from django.http import HttpResponseForbidden


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Configure logging
        logging.basicConfig(
            filename='user_requests.log',
            level=logging.INFO,
            format='%(message)s'
        )

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)

        response = self.get_response(request)
        return response




class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Allow access only between 18 (6 PM) and 21 (9 PM)
        if not (18 <= current_hour < 21):
            return HttpResponseForbidden("Access to chat is only allowed between 6PM and 9PM.")
        return self.get_response(request)