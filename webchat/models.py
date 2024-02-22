from django.db import models
from users.models import User



class Notification(models.Model):
    message = models.CharField(max_length=100)
    reciever = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return str(self.reciever)
    
    # def save(self, *args, **kwargs):
    #     # 모델이 생성될 때만 작동하도록 함
    #     if not self.pk:
    #         # 현재 시간을 isoformat으로 변환하여 저장
    #         self.created_at = datetime.now().isoformat()
    #     super().save(*args, **kwargs)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
