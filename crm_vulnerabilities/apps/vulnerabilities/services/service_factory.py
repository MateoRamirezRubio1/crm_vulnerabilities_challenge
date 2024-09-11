from apps.vulnerabilities.services.vulnerability_service import VulnerabilityService
from apps.vulnerabilities.repositories.vulnerability_repository import (
    VulnerabilityRepository,
)
from apps.vulnerabilities.clients.nvd_client import NVDClient
from apps.vulnerabilities.aggregators.vulnerability_aggregator import (
    VulnerabilityAggregator,
)
from apps.alerts.observers.alert_subject import AlertSubject


def get_vulnerability_service(subject=None):
    """Crea e inyecta las dependencias para VulnerabilityService"""
    repository = VulnerabilityRepository()
    nvd_client = NVDClient()
    aggregator = VulnerabilityAggregator()
    if subject is None:
        subject = AlertSubject()

    return VulnerabilityService(repository, nvd_client, aggregator, subject)
