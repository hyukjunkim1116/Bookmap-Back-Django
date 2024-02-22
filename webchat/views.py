from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Message, Notification
from .serializers import MessageSerializer, NotificationSerializer
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status


class MessageViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            message = Message.objects.all()
        
            serializer = MessageSerializer(message, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response([])


class NotificationViewSet(viewsets.ViewSet):
    def list(self, request):
       
        try:
            notification = Notification.objects.filter(reciever=request.user).order_by(
                "-created_at"
            )
            serializer = NotificationSerializer(notification, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response([])


class NotificationView(APIView):

    def patch(self, request, not_id):
        notification = get_object_or_404(Notification, id=not_id)
        notification.is_read = True
        notification.save()
        serializer = NotificationSerializer(
            notification, data=request.data, partial=True
        )
        if serializer.is_valid():
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
