import logging
from django.db import IntegrityError

logger = logging.getLogger("authentication")


class UserService:
    """Service for handling user-related logic"""

    def __init__(self, repository):
        self.user_repository = repository

    def register_user(self, validated_data):
        """Register a new user with validated data"""
        try:
            user_data = {
                "email": validated_data["email"],
                "username": validated_data["username"],
                "role": validated_data["role"],
            }
            password = validated_data["password"]
            user = self.user_repository.save_user(user_data, password)
            logger.info(f"User {validated_data['username']} registered successfully.")
            return user
        except IntegrityError as e:
            logger.error(f"IntegrityError during user registration: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to register user {validated_data['username']}: {e}")
            raise
