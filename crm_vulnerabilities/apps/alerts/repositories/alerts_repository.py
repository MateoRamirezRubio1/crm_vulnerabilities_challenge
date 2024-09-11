from apps.alerts.models import Alert


class AlertRepository:

    def save_alert(self, alert_severity, alert_type, recipient, message):
        notification = Alert(
            alert_severity=alert_severity,
            type_alert=alert_type,
            recipient=recipient,
            message=message,
        )
        notification.save()
