from apps.vulnerabilities.services.vulnerability_service import VulnerabilityService
from apps.vulnerabilities.repositories.vulnerability_repository import (
    VulnerabilityRepository,
)
from apps.vulnerabilities.clients.nvd_client import NVDClient
from apps.vulnerabilities.aggregators.vulnerability_aggregator import (
    VulnerabilityAggregator,
)


def get_vulnerability_service():
    """Crea e inyecta las dependencias para VulnerabilityService"""
    repository = VulnerabilityRepository()
    nvd_client = NVDClient()
    aggregator = VulnerabilityAggregator()

    return VulnerabilityService(repository, nvd_client, aggregator)
