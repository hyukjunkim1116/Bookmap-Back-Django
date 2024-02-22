from rest_framework import status, generics
from .serializers import PaymentsSerializer
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Payment


class PaymentsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PaymentsSerializer

    def get_queryset(self):
        queryset = Payment.objects.filter(buyer=self.request.user).order_by(
            "-updated_at"
        )
        return queryset

    def post(self, request):
        serializer = PaymentsSerializer(data=request.data)
        if serializer.is_valid():
            # buyer=request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
