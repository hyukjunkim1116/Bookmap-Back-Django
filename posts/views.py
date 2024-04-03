import boto3
import uuid
from .serializers import PostSerializer, CommentReadSerializer, CommentCreateSerializer
from rest_framework.views import APIView
from rest_framework import status, generics
from django.db.models import Count
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Post, Comment
from .paginations import PostPagination, CommentPagination
from django.conf import settings
from webchat.models import Notification
import datetime
from rest_framework_simplejwt.authentication import JWTAuthentication
from config import custom_exception


class PostImageReactView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_s3_client(self):
        # S3 클라이언트 생성 및 반환
        return boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )

    def post(self, request, post_id):
      
        unique_id = uuid.uuid4()
        s3_client = self.get_s3_client()
        image_file = request.data["image"]

        s3_client.upload_fileobj(
            image_file,
            settings.AWS_STORAGE_BUCKET_NAME,
            f"posts/{unique_id}{image_file.name}",
        )
        # S3로부터 이미지의 URL 받아오기
        image_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/posts/{unique_id}{image_file.name}"
        post = get_object_or_404(Post, id=post_id)
        post.image = image_url
        post.save()
        return Response(image_url, status=status.HTTP_200_OK)

    def delete(self, request, post_id):
        s3_client = self.get_s3_client()
    
        url = request.GET.get("url")

        s3_client.delete_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=url.split("m/")[-1]
        )
        post = get_object_or_404(Post, id=post_id)
        post.image = None
        post.save()
        return Response(status=status.HTTP_200_OK)


class PostImageView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_s3_client(self):
      
        return boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )

    def post(self, request):
        unique_id = uuid.uuid4()
        s3_client = self.get_s3_client()
        image_file = request.data["image"]

        s3_client.upload_fileobj(
            image_file,
            settings.AWS_STORAGE_BUCKET_NAME,
            f"posts/{unique_id}{image_file.name}",
        )

        # S3로부터 이미지의 URL 받아오기
        image_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/posts/{unique_id}{image_file.name}"
        return Response(image_url, status=status.HTTP_200_OK)

    def delete(self, request):
        s3_client = self.get_s3_client()
        # 폴더 안의 객체 리스트업
        url = request.GET.get("url")

        s3_client.delete_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=url.split("m/")[-1]
        )
        return Response(status=status.HTTP_200_OK)


class PostView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PostPagination
    serializer_class = PostSerializer

    def get_queryset(self):
        title = self.request.GET.get("search", "")
        queryset = Post.objects.filter(title__icontains=title)
        sort = self.request.GET.get("sort", "-updated_at")
        match sort:
            case "likeCount":
                queryset = queryset.annotate(likes_count=Count("like")).order_by(
                    "-likes_count"
                )
            case "readCount":
                queryset = queryset.order_by("-read_count")
            case "bookMark":
                queryset = queryset.filter(bookmark=True).order_by("-updated_at")

            case _:
                queryset = queryset.order_by("-updated_at")
        return queryset

    def post(self, request):
        serializer = PostSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save(author=request.user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise custom_exception.InvalidRequest


class PostDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, post_id):

        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(
            post,
            context={"request": request},
        )
        response = Response(serializer.data, status=status.HTTP_200_OK)
        # 쿠키 읽기 & 생성
        if request.COOKIES.get("hit") is not None:  # 쿠키에 hit 값이 이미 있을 경우

            cookies = request.COOKIES.get("hit")
            cookies_list = cookies.split("|")  # '|'는 다르게 설정 가능 ex) '.'

            if str(post_id) not in cookies_list:
                response.set_cookie(
                    "hit", cookies + f"|{str(post_id)}", max_age=60
                )  # 쿠키 생성
                post.read_count += 1
                Post.objects.filter(id=post_id).update(read_count=post.read_count)
        else:  # 쿠키에 hit 값이 없을 경우(즉 현재 보는 게시글이 첫 게시글임)

            response.set_cookie("hit", str(post_id), max_age=60)
            post.read_count += 1
            Post.objects.filter(id=post_id).update(read_count=post.read_count)
        return response

    def put(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if request.user == post.author:
            serializer = PostSerializer(
                post, data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            raise custom_exception.InvalidRequest

    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if request.user == post.author:
            post.delete()
            return Response(
                {"message": "게시글이 삭제되었습니다"},
                status=status.HTTP_204_NO_CONTENT,
            )
        raise custom_exception.ForbiddenPost


class CommentView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CommentPagination
    serializer_class = CommentReadSerializer

    def get_queryset(self):
        post_id = self.kwargs["post_id"]

        queryset = Comment.objects.filter(post__id=post_id).order_by("-updated_at")
        return queryset

    def post(self, request, post_id):

        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post_id=post_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise custom_exception.InvalidRequest


class CommentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.author:
            serializer = CommentCreateSerializer(
                comment, data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        raise custom_exception.ForbiddenComment

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)

        if request.user == comment.author:
            comment.delete()
            return Response("댓글이 삭제되었습니다", status=status.HTTP_204_NO_CONTENT)
        raise custom_exception.ForbiddenComment


class PostLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        """게시글 좋아요 누르기"""
        post = get_object_or_404(Post, id=post_id)
        if post.like.filter(id=request.user.id).exists():
            post.like.remove(request.user)

        else:
            post.like.add(request.user)
            Notification.objects.create(
                message=f"{request.user.username}님이 회원님의 {post.title}게시글에 좋아요를 눌렀습니다",
                reciever=post.author,
            )

        serializer = PostSerializer(post, context={"request": request})
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class PostDisikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        """게시글 싫어요 누르기"""
        post = get_object_or_404(Post, id=post_id)
        if post.dislike.filter(id=request.user.id).exists():
            post.dislike.remove(request.user)

        else:
            post.dislike.add(request.user)

        serializer = PostSerializer(post, context={"request": request})
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class BookmarkView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post, context={"request": request})
        if post.bookmark.filter(id=request.user.id).exists():
            post.bookmark.remove(request.user)
        else:
            post.bookmark.add(request.user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
