from django.contrib.auth import get_user_model

User = get_user_model()


class UserRepository:
    """Repositorio para gestionar operaciones de base de datos de usuarios"""

    def save_user(self, user_data, password):
        """Guardar un nuevo usuario en la base de datos"""
        user = User(
            email=user_data["email"],
            username=user_data["username"],
            role=user_data["role"],
        )
        user.set_password(password)  # Encriptar la contraseña
        user.save()
        return user
