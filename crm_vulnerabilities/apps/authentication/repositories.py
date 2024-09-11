import logging
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger("authentication")


class UserRepository:
    """Repository for managing user database operations"""

    def save_user(self, user_data, password):
        """Save a new user to the database"""
        try:
            user = User(
                email=user_data["email"],
                username=user_data["username"],
                role=user_data["role"],
            )
            user.set_password(password)  # Encrypt the password
            user.save()
            logger.info(f"User {user_data['username']} saved successfully.")
            return user
        except Exception as e:
            logger.error(f"Failed to save user {user_data['username']}: {e}")
            raise
