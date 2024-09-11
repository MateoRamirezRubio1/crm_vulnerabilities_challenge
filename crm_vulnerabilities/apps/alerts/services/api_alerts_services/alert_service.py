class AlertService:

    def __init__(self, repository) -> None:
        self.repository = repository

    def get_all_alerts(self):
        """Obtiene todas las alertas desde el repositorio"""
        all_alerts = self.repository.get_all_alerts()

        return all_alerts
