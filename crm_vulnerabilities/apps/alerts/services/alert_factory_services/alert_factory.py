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


class AlertFactory:
    def get_alert_service(self, alert_severity):
        if alert_severity == "HIGH":
            return EmailAlertService()
        elif alert_severity == "MEDIUM":
            return SMSAlertService()
        elif alert_severity == "LOW":
            return PushAlertService()
        elif alert_severity == "CRITICAL":
            return SlackAlertService()
        else:
            raise ValueError(f"Severidad de alerta '{alert_severity}' no soportada.")
