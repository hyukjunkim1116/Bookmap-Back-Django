from django.urls import path
from . import views


urlpatterns = [
    path(
        "pay/",
        views.PaymentsView.as_view(),
        name="payments",
    ),
]
