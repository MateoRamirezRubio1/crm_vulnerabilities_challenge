from apps.alerts.repositories.alerts_repository import AlertRepository
import logging

logger = logging.getLogger("alerts")


class PushAlertService:
    def __init__(self) -> None:
        self.alert_repository = AlertRepository()

    def send_alert(self, recipient: str, message: str):
        """Simulates sending a push notification."""
        try:
            print(
                f"Simulating sending push notification to {recipient}. Message: {message}"
            )
            self._record_notification(recipient, message)
            logger.info(f"Push notification sent to {recipient}.")
        except Exception as e:
            logger.error(f"Failed to send push notification to {recipient}: {e}")

    def _record_notification(self, recipient: str, message: str):
        """Records the notification in the database."""
        try:
            self.alert_repository.save_alert(
                alert_severity="LOW",
                alert_type="push",
                recipient=recipient,
                message=message,
            )
            logger.info(
                f"Push notification recorded in database for recipient: {recipient}"
            )
        except Exception as e:
            logger.error(f"Failed to record push notification in database: {e}")
