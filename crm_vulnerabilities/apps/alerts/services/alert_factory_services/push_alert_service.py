from apps.alerts.repositories.alerts_repository import AlertRepository


class PushAlertService:

    def __init__(self) -> None:
        self.alert_repository = AlertRepository()

    def send_alert(self, recipient, message):
        """Simula el envío de una notificación push."""
        print(
            f"Simulación de envío de notificación push a {recipient}. Mensaje: {message}"
        )

        # Guardar la notificación en la base de datos
        self._record_notification(recipient, message)

    def _record_notification(self, recipient, message):
        """Registra la notificación en la base de datos."""
        self.alert_repository.save_alert(
            alert_severity="LOW",
            alert_type="push",
            recipient=recipient,
            message=message,
        )
