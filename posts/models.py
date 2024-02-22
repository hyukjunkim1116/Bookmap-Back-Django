from django.db import models
from users.models import User


class Post(models.Model):
    class Meta:
        db_table = "Post"

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=40,
        default="",
        null=False,
    )
    content = models.TextField(
        max_length=5000,
        default="",
        null=False,
    )
    like = models.ManyToManyField(
        User,
        related_name="likes",
        blank=True,
    )
    dislike = models.ManyToManyField(
        User,
        related_name="dislikes",
        blank=True,
    )
    bookmark = models.ManyToManyField(
        User,
        related_name="bookmarks",
        blank=True,
    )
    read_count = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    class meta:
        db_table = "Comment"

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="post_comment",
    )
    comment = models.TextField(
        max_length=300,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return str(self.comment)
