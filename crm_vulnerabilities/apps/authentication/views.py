import logging
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

logger = logging.getLogger("authentication")


class CustomTokenObtainPairView(TokenObtainPairView):
    """View to obtain JWT tokens, including user role"""

    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            logger.info(
                "JWT token obtained successfully for user: %s",
                request.data.get("username"),
            )
            return response
        except Exception as e:
            logger.error("Error obtaining JWT token: %s", str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    """View for user registration"""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user_repository = UserRepository()
                user_service = UserService(user_repository)
                user = user_service.register_user(serializer.validated_data)
                logger.info("User registered successfully: %s", user.username)
                return Response(
                    {"message": "User registered successfully.", "user_id": user.id},
                    status=status.HTTP_201_CREATED,
                )
            except IntegrityError as e:
                logger.error("IntegrityError during user registration: %s", str(e))
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logger.error("Error during user registration: %s", str(e))
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAndBlacklistRefreshTokenView(APIView):
    """View to logout and blacklist the refresh token"""

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token
            logger.info("Refresh token blacklisted successfully.")
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logger.error("Error blacklisting refresh token: %s", str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
