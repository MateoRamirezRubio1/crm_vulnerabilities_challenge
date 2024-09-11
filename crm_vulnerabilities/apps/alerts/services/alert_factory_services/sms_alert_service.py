from apps.alerts.repositories.alerts_repository import AlertRepository
import logging

logger = logging.getLogger("alerts")


class SMSAlertService:
    def __init__(self) -> None:
        self.alert_repository = AlertRepository()

    def send_alert(self, recipient: str, message: str):
        """Simulates sending an SMS alert."""
        try:
            print(f"Simulating sending SMS to {recipient}. Message: {message}")
            self._record_notification(recipient, message)
            logger.info(f"SMS alert sent to {recipient}.")
        except Exception as e:
            logger.error(f"Failed to send SMS alert to {recipient}: {e}")

    def _record_notification(self, recipient: str, message: str):
        """Records the notification in the database."""
        try:
            self.alert_repository.save_alert(
                alert_severity="MEDIUM",
                alert_type="sms",
                recipient=recipient,
                message=message,
            )
            logger.info(f"SMS alert recorded in database for recipient: {recipient}")
        except Exception as e:
            logger.error(f"Failed to record SMS alert in database: {e}")
