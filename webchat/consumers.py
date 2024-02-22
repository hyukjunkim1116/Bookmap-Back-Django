from asgiref.sync import async_to_sync
from channels.generic import websocket
from django.contrib.auth import get_user_model
from .models import Message, Notification
from .serializers import NotificationSerializer
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
import json

User = get_user_model()


def get_notification(uid):
    notifications = Notification.objects.filter(reciever=uid).order_by("-created_at")
    serializer = NotificationSerializer(notifications, many=True)
    return serializer.data


# DB model에 관련해서 save가 작동하면, 저장이 완료된 이후에 지정한 동작을 수행
@receiver(post_save, sender=Notification)
def send_update(sender, instance, created, **kwargs):

    serializer = NotificationSerializer(instance)

    if created:

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            str(instance.reciever.id),
            {"type": "notify", "data": serializer.data},
        )


class WebChatConsumer(websocket.JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def connect(self):
        self.user = self.scope["user"]
        self.accept()
        if not self.user.is_authenticated:
            self.close(code=4001)
        self.user = User.objects.get(id=self.user.id)

        async_to_sync(self.channel_layer.group_add)("all_users", self.channel_name)

    def receive_json(self, content):

        sender = self.user
        message = content["message"]
        new_message = Message.objects.create(sender=sender, content=message)
        async_to_sync(self.channel_layer.group_send)(
            "all_users",
            {
                "type": "chat.message",
                "new_message": {
                    "id": new_message.id,
                    "sender": new_message.sender.username,
                    "content": new_message.content,
                    "timestamp": new_message.timestamp.isoformat(),
                    "sender_id": new_message.sender.id,
                    "sender_image": new_message.sender.image,
                },
            },
        )

    def chat_message(self, event):

        self.send_json(event)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("all_users", self.channel_name)
        super().disconnect(close_code)


class NotificationConsumer(websocket.JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def connect(self):
        self.user = self.scope["user"]
        self.accept()
        if not self.user.is_authenticated:
            self.close(code=4001)
        self.user = User.objects.get(id=self.user.id)

        async_to_sync(self.channel_layer.group_add)(
            str(self.user.id), self.channel_name
        )

    def receive_json(self, content):
        pass

    def notify(self, event):

        self.send_json(event)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            str(self.user.id), self.channel_name
        )
        super().disconnect(close_code)
