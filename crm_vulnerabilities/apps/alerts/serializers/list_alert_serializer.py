from rest_framework import serializers
from apps.alerts.models import Alert


class ListAlertSerializer(serializers.ModelSerializer):
    """
    Serializer for listing alerts.
    """

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

    def validate(self, data):
        """
        Perform custom validation on the data.
        """
        if not data.get("message"):
            raise serializers.ValidationError("Message field cannot be empty.")
        return data
