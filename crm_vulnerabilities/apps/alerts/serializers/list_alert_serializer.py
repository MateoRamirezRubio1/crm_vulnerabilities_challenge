from rest_framework import serializers
from apps.alerts.models import Alert


class ListAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = [
            "id",
            "alert_severity",
            "type_alert",
            "recipient",
            "message",
            "sent_at",
        ]
