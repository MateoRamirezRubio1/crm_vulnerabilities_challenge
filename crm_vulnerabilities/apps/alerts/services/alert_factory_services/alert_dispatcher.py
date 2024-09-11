from apps.alerts.services.alert_factory_services.alert_factory import AlertFactory


class AlertDispatcher:

    def dispatch(self, alert_severity, recipient, message):
        """Envía la alerta utilizando el servicio adecuado basado en el tipo."""
        alert_service = AlertFactory().get_alert_service(alert_severity)
        alert_service.send_alert(recipient, message)
