from apps.alerts.services.alert_factory_services.alert_factory import AlertFactory
import logging

logger = logging.getLogger("alerts")


class AlertDispatcher:

    def dispatch(self, alert_severity, recipient, message):
        """
        Sends an alert using the appropriate service based on the alert severity.
        """
        try:
            alert_service = AlertFactory().get_alert_service(alert_severity)
            alert_service.send_alert(recipient, message)
            logger.info(f"Alert dispatched: {alert_severity}, Recipient: {recipient}")
        except ValueError as e:
            logger.error(f"Failed to dispatch alert: {e}")
