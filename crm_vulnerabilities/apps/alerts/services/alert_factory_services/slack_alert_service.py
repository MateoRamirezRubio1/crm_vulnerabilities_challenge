from apps.alerts.repositories.alerts_repository import AlertRepository
import logging

logger = logging.getLogger("alerts")


class SlackAlertService:
    def __init__(self) -> None:
        self.alert_repository = AlertRepository()

    def send_alert(self, recipient: str, message: str):
        """Simulates sending an alert to a Slack channel."""
        try:
            print(
                f"Simulating sending alert to Slack for {recipient}. Message: {message}"
            )
            self._record_notification(recipient, message)
            logger.info(f"Slack alert sent to {recipient}.")
        except Exception as e:
            logger.error(f"Failed to send Slack alert to {recipient}: {e}")

    def _record_notification(self, recipient: str, message: str):
        """Records the notification in the database."""
        try:
            self.alert_repository.save_alert(
                alert_severity="CRITICAL",
                alert_type="slack",
                recipient=recipient,
                message=message,
            )
            logger.info(f"Slack alert recorded in database for recipient: {recipient}")
        except Exception as e:
            logger.error(f"Failed to record Slack alert in database: {e}")
