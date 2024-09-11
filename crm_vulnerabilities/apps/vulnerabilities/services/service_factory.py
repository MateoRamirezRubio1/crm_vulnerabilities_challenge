from apps.vulnerabilities.services.vulnerability_service import VulnerabilityService
from apps.vulnerabilities.repositories.vulnerability_repository import (
    VulnerabilityRepository,
)
from apps.vulnerabilities.clients.nvd_client import NVDClient
from apps.vulnerabilities.aggregators.vulnerability_aggregator import (
    VulnerabilityAggregator,
)
from apps.alerts.observers.alert_subject import AlertSubject
import logging

# Configure logger for this module
logger = logging.getLogger("vulnerabilities")


def get_vulnerability_service(subject=None):
    """
    Creates and injects dependencies for the VulnerabilityService.

    Args:
        subject (AlertSubject, optional): The alert subject for notifications. If not provided, a default instance will be created.

    Returns:
        VulnerabilityService: An instance of VulnerabilityService with all dependencies injected.

    Raises:
        Exception: If there is an issue creating instances of the required components.
    """
    try:
        repository = VulnerabilityRepository()
        nvd_client = NVDClient()
        aggregator = VulnerabilityAggregator()

        if subject is None:
            subject = AlertSubject()

        return VulnerabilityService(repository, nvd_client, aggregator, subject)
    except Exception as e:
        logger.error(
            f"Error creating VulnerabilityService instance: {e}", exc_info=True
        )
        raise
