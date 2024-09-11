from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Modelo de usuario personalizado con roles"""

    ROLES = (
        ("admin", "Admin"),
        ("advanced", "Advanced User"),
        ("basic", "Basic User"),
    )
    role = models.CharField(max_length=20, choices=ROLES, default="basic")

    def __str__(self):
        return str(self.username)
