from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.alerts.services.api_alerts_services.alert_service import AlertService
from apps.alerts.repositories.alerts_repository import AlertRepository
from apps.alerts.serializers.list_alert_serializer import ListAlertSerializer


class AlertListView(APIView):

    def get(self, request):
        repository = AlertRepository()
        service = AlertService(repository)
        all_alerts = service.get_all_alerts()
        serializer = ListAlertSerializer(all_alerts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
