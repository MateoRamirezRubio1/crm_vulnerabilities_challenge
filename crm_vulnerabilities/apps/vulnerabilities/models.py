from django.db import models


class Vulnerability(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    description = models.TextField()
    severity = models.CharField(
        max_length=50,
        choices=[
            ("LOW", "Low"),
            ("MEDIUM", "Medium"),
            ("HIGH", "High"),
            ("CRITICAL", "Critical"),
        ],
    )
    is_fixed = models.BooleanField(
        default=True
    )  # Default to False, assuming not fixed initially
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Vulnerability {self.id} - Severity: {self.severity}"
