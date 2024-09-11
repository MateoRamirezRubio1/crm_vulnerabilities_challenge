from django.urls import path
from apps.alerts.views.alert_views import AlertListView

urlpatterns = [
    path("", AlertListView.as_view(), name="alert-list"),
]
