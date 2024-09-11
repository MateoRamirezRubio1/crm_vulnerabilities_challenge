from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.alerts.services.api_alerts_services.alert_service import AlertService
from apps.alerts.repositories.alerts_repository import AlertRepository
from apps.alerts.serializers.list_alert_serializer import ListAlertSerializer
import logging

logger = logging.getLogger("alerts")


class AlertListView(APIView):
    """
    View to list all alerts.
    """

    def get(self, request):
        try:
            repository = AlertRepository()
            service = AlertService(repository)
            all_alerts = service.get_all_alerts()
            serializer = ListAlertSerializer(all_alerts, many=True)
            logger.info("Successfully retrieved all alerts.")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving alerts: {e}")
            return Response(
                {"detail": "Error retrieving alerts."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
