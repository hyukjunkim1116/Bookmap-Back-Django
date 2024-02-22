from rest_framework import serializers

from .models import Message, Notification


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    sender_image = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ["id", "sender_id", "sender", "content", "timestamp", "sender_image"]

    def get_sender_image(self, obj):
        return obj.sender.image

    def get_sender_id(self, obj):
        return obj.sender.id


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
