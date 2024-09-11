from apps.alerts.repositories.alerts_repository import AlertRepository
import logging

logger = logging.getLogger("alerts")


class EmailAlertService:
    def __init__(self) -> None:
        self.alert_repository = AlertRepository()

    def send_alert(self, recipient: str, message: str):
        """
        Sends an alert via email and records it in the database.
        """
        try:
            self._send_email(recipient, message)
            self._record_notification(recipient, message)
            logger.info(f"Email sent to {recipient} with message: {message}")
        except Exception as e:
            logger.error(f"Failed to send email to {recipient}: {e}")

    def _send_email(self, recipient: str, message: str):
        """
        Sends an email. This is a placeholder for actual email sending logic.
        """
        # Example email sending logic (to be replaced with real implementation)
        print(f"Sending email to {recipient} with message: {message}")

    def _record_notification(self, recipient: str, message: str):
        """
        Records the email notification in the database.
        """
        try:
            self.alert_repository.save_alert(
                alert_severity="HIGH",
                alert_type="email",
                recipient=recipient,
                message=message,
            )
            logger.info(f"Notification recorded in database for recipient: {recipient}")
        except Exception as e:
            logger.error(f"Failed to record notification in database: {e}")
