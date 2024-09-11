from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom serializer to include user role in JWT tokens"""

    def validate(self, attrs):
        data = super().validate(attrs)
        data["role"] = self.user.role  # Add user's role to the token payload
        return data


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for registering new users"""

    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=User.ROLES)

    class Meta:
        model = User
        fields = ["username", "password", "email", "role"]
