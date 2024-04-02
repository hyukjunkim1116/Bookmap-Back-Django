from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from webchat.consumers import WebChatConsumer, NotificationConsumer
from webchat.views import MessageViewSet, NotificationViewSet, NotificationView

router = DefaultRouter()
router.register("api/webchat", MessageViewSet, basename="message")
router.register("api/notification", NotificationViewSet, basename="notification")

urlpatterns = [
    path("admin/", admin.site.urls),
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
