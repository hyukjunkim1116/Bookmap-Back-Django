from django.urls import path
from . import views


urlpatterns = [
    # api/reports/<int:post_id>
    path(
        "<int:post_id>",
        views.ReportView.as_view(),
        name="post_root",
    ),
]
