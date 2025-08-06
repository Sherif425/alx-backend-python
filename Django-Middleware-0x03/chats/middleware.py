# Django-Middleware-0x03/apps/core/middleware/middleware.py

import logging
from datetime import datetime
from django.http import HttpResponseForbidden
from collections import defaultdict
from django.http import HttpResponse


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
    
    
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_log = defaultdict(list)  # {ip: [timestamps]}

    def __call__(self, request):
        if request.method == 'POST':
            ip = self.get_client_ip(request)
            current_time = time.time()

            # Keep only timestamps within the last 60 seconds
            self.request_log[ip] = [t for t in self.request_log[ip] if current_time - t < 60]

            if len(self.request_log[ip]) >= 5:
                return HttpResponseTooManyRequests("You have exceeded the message limit. Try again later.")

            self.request_log[ip].append(current_time)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip