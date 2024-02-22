from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.urls import re_path
from rest_framework.routers import DefaultRouter
from webchat.consumers import WebChatConsumer, NotificationConsumer
from webchat.views import MessageViewSet, NotificationViewSet, NotificationView


def health_check(request):
    return HttpResponse(status=200)


router = DefaultRouter()
router.register("api/webchat", MessageViewSet, basename="message")
router.register("api/notification", NotificationViewSet, basename="notification")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health-check/", health_check, name="health_check"),
    path("api/users/", include("users.urls")),
    path("api/posts/", include("posts.urls")),
    path("api/reports/", include("reports.urls")),
    path("api/payments/", include("payments.urls")),
    path("api/notification/<int:not_id>", NotificationView.as_view()),
] + router.urls

websocket_urlpatterns = [
    path("webchat", WebChatConsumer.as_asgi()),
    path("notification", NotificationConsumer.as_asgi()),
]
