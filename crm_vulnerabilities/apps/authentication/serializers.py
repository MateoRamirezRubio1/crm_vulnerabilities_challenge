from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializador personalizado para obtener tokens JWT, incluye rol de usuario"""

    def validate(self, attrs):
        data = super().validate(attrs)
        data["role"] = (
            self.user.role
        )  # Incluir el rol del usuario en el payload del token
        return data


class RegisterSerializer(serializers.ModelSerializer):
    """Serializador para registrar nuevos usuarios"""

    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=User.ROLES)

    class Meta:
        model = User
        fields = ["username", "password", "email", "role"]
