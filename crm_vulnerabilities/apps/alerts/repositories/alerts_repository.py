from apps.alerts.models import Alert


class AlertRepository:
    def __init__(self) -> None:
        self.model = Alert

    def save_alert(self, alert_severity, alert_type, recipient, message):
        alert = self.model(
            alert_severity=alert_severity,
            type_alert=alert_type,
            recipient=recipient,
            message=message,
        )
        alert.save()

    def get_all_alerts(self):
        """Obtiene todas las alertas de la base de datos"""
        all_alerts = self.model.objects.all()

        return all_alerts
