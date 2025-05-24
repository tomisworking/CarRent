from django.conf import settings


class SeparateAdminSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Dla ścieżek admina używaj innych ustawień sesji
        if request.path.startswith('/admin/'):
            request.session_cookie_name = settings.SESSION_COOKIE_NAME_ADMIN
            request.session_cookie_path = settings.SESSION_COOKIE_PATH_ADMIN
        else:
            request.session_cookie_name = settings.SESSION_COOKIE_NAME
            request.session_cookie_path = settings.SESSION_COOKIE_PATH

        response = self.get_response(request)
        return response