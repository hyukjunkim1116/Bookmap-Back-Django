from django.db import models
from users.models import User
from posts.models import Post


class Report(models.Model):
    class Meta:
        db_table = "Report"

    reporting_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reporting_user", null=True
    )
    reported_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reported_user", null=True
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
    )
    title = models.CharField(
        max_length=40,
    )
    content = models.TextField(
        max_length=5000,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return str(self.title)
