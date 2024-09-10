from django.db import models


class Vulnerability(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    description = models.TextField()
    severity = models.CharField(max_length=50)
    is_fixed = models.BooleanField(default=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Vulnerability {self.id} - Severity: {self.severity}"
