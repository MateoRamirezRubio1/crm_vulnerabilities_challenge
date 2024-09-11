import logging
from apps.alerts.models import Alert

logger = logging.getLogger("alerts")


class AlertRepository:
    def __init__(self) -> None:
        self.model = Alert

    def save_alert(
        self, alert_severity: str, alert_type: str, recipient: str, message: str
    ) -> Alert:
        """
        Saves an alert to the database.

        Args:
            alert_severity (str): The severity of the alert.
            alert_type (str): The type of alert (e.g., email, SMS).
            recipient (str): The recipient of the alert.
            message (str): The message content of the alert.

        Returns:
            Alert: The created Alert object.
        """
        try:
            alert = self.model(
                alert_severity=alert_severity,
                type_alert=alert_type,
                recipient=recipient,
                message=message,
            )
            alert.save()
            logger.info(f"Alert saved successfully: {alert}")
            return alert
        except Exception as e:
            logger.error(f"Error saving alert: {e}")
            raise

    def get_all_alerts(self) -> list[Alert]:
        """
        Retrieves all alerts from the database.

        Returns:
            list[Alert]: A list of all Alert objects.
        """
        try:
            all_alerts = self.model.objects.all()
            logger.info(f"Retrieved {all_alerts.count()} alerts from the database.")
            return all_alerts
        except Exception as e:
            logger.error(f"Error retrieving alerts: {e}")
            raise
