from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class AuthCheckView(APIView):
    """
    A simple view to verify JWT authentication and user permissions.
    Ensures users can access their own data (e.g., messages and conversations).
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": f"Authenticated as {request.user.username}"})