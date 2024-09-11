from apps.alerts.repositories.alerts_repository import AlertRepository


class EmailAlertService:
    def __init__(self) -> None:
        self.alert_repository = AlertRepository()

    def send_alert(self, recipient, message):
        """Envía una alerta por correo electrónico."""

        # Lógica para enviar un correo electrónico
        self._send_email(recipient, message)

        # Guardar la notificación en la base de datos
        self._record_notification(recipient, message)

    def _send_email(self, recipient, message):
        # Lógica ficticia de envío de email.
        print(f"Enviando email a {recipient} con mensaje: {message}")

    def _record_notification(self, recipient, message):
        """Registra la notificación en la base de datos."""
        self.alert_repository.save_alert(
            alert_severity="HIGH",
            alert_type="email",
            recipient=recipient,
            message=message,
        )
