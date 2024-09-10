from django.urls import path
from apps.vulnerabilities.views.vulnerability_views import (
    VulnerabilityListView,
    UnfixedVulnerabilitiesView,
    VulnerabilityFixedView,
    VulnerabilitySummaryView,
)

urlpatterns = [
    path("", VulnerabilityListView.as_view(), name="vulnerability-list"),
    path(
        "unfixed/",
        UnfixedVulnerabilitiesView.as_view(),
        name="unfixed-vulnerability-list",
    ),
    path(
        "fixed/",
        VulnerabilityFixedView.as_view(),
        name="vulnerability-fixed",
    ),
    path(
        "summary/",
        VulnerabilitySummaryView.as_view(),
        name="vulnerability-summary",
    ),
]
