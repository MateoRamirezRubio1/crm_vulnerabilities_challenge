from django.db import IntegrityError


class UserService:
    """Servicio para manejar la lógica relacionada con los usuarios"""

    def __init__(self, repository):
        self.user_repository = repository

    def register_user(self, validated_data):
        """Registrar un nuevo usuario con datos validados"""
        try:
            user_data = {
                "email": validated_data["email"],
                "username": validated_data["username"],
                "role": validated_data["role"],
            }
            password = validated_data["password"]
            return self.user_repository.save_user(user_data, password)
        except IntegrityError as e:
            raise e
