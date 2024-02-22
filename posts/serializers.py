from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"

    def get_author(self, obj):
        return {
            "username": obj.author.username,
            "uid": obj.author.id,
            "image": obj.author.image,
        }

    def get_likes_count(self, obj):
        return obj.like.count()

    def get_dislikes_count(self, obj):
        return obj.dislike.count()

    def get_comments_count(self, obj):
        return obj.post_comment.count()

    def get_is_liked(self, obj):

        request = self.context["request"]

        return obj.like.filter(id=request.user.id).exists()

    def get_is_disliked(self, obj):
        request = self.context["request"]
        return obj.dislike.filter(id=request.user.id).exists()

    def get_is_bookmarked(self, obj):
        request = self.context["request"]
        return obj.bookmark.filter(id=request.user.id).exists()


class CommentReadSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    # comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "comment",
            "author",
            "post",
            "created_at",
            "updated_at",
            "username",
            "image",
            # "comment_count",
        ]
        extra_kwargs = {
            "author": {
                "read_only": True,
            },
            "id": {
                "read_only": True,
            },
            "post": {
                "read_only": True,
            },
        }

    def get_username(self, obj):
        return obj.author.username

    def get_image(self, obj):
        return obj.author.image


class CommentCreateSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "comment",
            "author",
            "post",
            "created_at",
            "updated_at",
            "username",
        ]
        extra_kwargs = {
            "author": {
                "read_only": True,
            },
            "id": {
                "read_only": True,
            },
            "post": {
                "read_only": True,
            },
        }

    def get_username(self, obj):
        return obj.author.username
