from django.apps import AppConfig


class AlertsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.alerts"

    def ready(self):
        from apps.vulnerabilities.observers.vulnerability_observer import (
            VulnerabilityObserver,
        )
        from apps.alerts.observers.alert_subject import AlertSubject
        from apps.alerts.services.alert_factory_services.alert_factory import (
            AlertFactory,
        )

        alert_subject = AlertSubject()

        alert_factory = AlertFactory()
        vulneravility_observer = VulnerabilityObserver(alert_factory)
        alert_subject.attach(vulneravility_observer)
