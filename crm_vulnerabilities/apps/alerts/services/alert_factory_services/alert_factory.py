from apps.alerts.services.alert_factory_services.email_alert_service import (
    EmailAlertService,
)
from apps.alerts.services.alert_factory_services.sms_alert_service import (
    SMSAlertService,
)
from apps.alerts.services.alert_factory_services.push_alert_service import (
    PushAlertService,
)
from apps.alerts.services.alert_factory_services.slack_alert_service import (
    SlackAlertService,
)
import logging

logger = logging.getLogger("alerts")


class AlertFactory:
    def get_alert_service(self, alert_severity: str):
        """
        Returns the appropriate alert service based on the severity level.
        """
        services = {
            "HIGH": EmailAlertService,
            "MEDIUM": SMSAlertService,
            "LOW": PushAlertService,
            "CRITICAL": SlackAlertService,
        }

        if alert_severity not in services:
            logger.error(f"Unsupported alert severity: {alert_severity}")
            raise ValueError(f"Alert severity '{alert_severity}' is not supported.")

        logger.info(
            f"Using {services[alert_severity].__name__} for alert severity: {alert_severity}"
        )
        return services[alert_severity]()
