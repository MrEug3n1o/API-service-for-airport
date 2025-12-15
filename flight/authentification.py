from rest_framework.authentication import SessionAuthentication

class AdminSessionAuthentication(SessionAuthentication):
    def authenticate(self, request):
        user_auth = super().authenticate(request)
        if user_auth is None:
            return None

        user, auth = user_auth
        if not user.is_staff:
            return None

        return (user, auth)
