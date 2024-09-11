from django.db import models

from django.db import models


class Alert(models.Model):
    SEVERITY_CHOICES = [
        ("HIGH", "High"),
        ("LOW", "Low"),
        ("CRITICAL", "Critical"),
        ("MEDIUM", "Medium"),
    ]

    TYPE_CHOICES = [
        ("email", "Email"),
        ("slack", "Slack"),
        ("push", "Push Notification"),
        ("sms", "SMS"),
    ]

    id = models.AutoField(primary_key=True)
    alert_severity = models.CharField(
        max_length=10, choices=SEVERITY_CHOICES, default="LOW"
    )
    type_alert = models.CharField(max_length=10, choices=TYPE_CHOICES, default="email")
    recipient = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification to {self.recipient} with severity {self.alert_severity} on {self.sent_at}"
