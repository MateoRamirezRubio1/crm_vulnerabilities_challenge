import logging

logger = logging.getLogger("alerts")


class AlertService:

    def __init__(self, repository) -> None:
        self.repository = repository

    def get_all_alerts(self):
        """Fetches all alerts from the repository."""
        try:
            all_alerts = self.repository.get_all_alerts()
            logger.info("Successfully fetched all alerts.")
            return all_alerts
        except Exception as e:
            logger.error(f"Failed to fetch all alerts: {e}")
            return []
