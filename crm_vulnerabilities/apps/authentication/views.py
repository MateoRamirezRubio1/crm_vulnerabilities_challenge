from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.authentication.serializers import (
    CustomTokenObtainPairSerializer,
    RegisterSerializer,
)
from apps.authentication.services import UserService
from django.db import IntegrityError
from apps.authentication.repositories import UserRepository


class CustomTokenObtainPairView(TokenObtainPairView):
    """Vista para generar el token JWT, incluyendo el rol del usuario"""

    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except IntegrityError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    """Vista para registrar nuevos usuarios"""

    permission_classes = [AllowAny]

    def post(self, request):
        # Uso del serializer para validar los datos de entrada
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user_repository = UserRepository()
            user_service = UserService(user_repository)
            user = user_service.register_user(serializer.validated_data)
            return Response(
                {"message": "Usuario registrado con éxito.", "user_id": user.id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAndBlacklistRefreshTokenView(APIView):
    """Vista para hacer logout y revocar el token de refresco"""

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Revocar el token de refresco agregándolo a la lista negra
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except IntegrityError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
