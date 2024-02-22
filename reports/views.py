from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from .serializers import ReportSerializer
from posts.models import Post


class ReportView(APIView):
    def post(self, request, post_id):

        post = get_object_or_404(Post, id=post_id)
        serializer = ReportSerializer(
            data=request.data,
        )
        if serializer.is_valid():

            serializer.save(
                reporting_user=request.user, reported_user=post.author, post=post
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
