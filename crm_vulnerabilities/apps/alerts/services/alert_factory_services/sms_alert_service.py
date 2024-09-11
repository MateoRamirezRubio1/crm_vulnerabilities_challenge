from apps.alerts.repositories.alerts_repository import AlertRepository


class SMSAlertService:

    def __init__(self) -> None:
        self.alert_repository = AlertRepository()

    def send_alert(self, recipient, message):
        """Simula el envío de una alerta por SMS."""
        print(f"Simulación de envío de SMS a {recipient}. Mensaje: {message}")

    def _record_notification(self, recipient, message):
        """Registra la notificación en la base de datos."""
        self.alert_repository.save_alert(
            alert_severity="MEDIUM",
            alert_type="sms",
            recipient=recipient,
            message=message,
        )
