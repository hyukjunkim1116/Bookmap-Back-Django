from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        try:
            user = User.objects.get(username=username)
            raise ValueError("해당 닉네임이 이미 존재합니다!")
        except User.DoesNotExist:
            pass
        user = self.create_user(
            email,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    image = models.URLField(null=True, blank=True)
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    password = models.CharField(max_length=256)
    username = models.CharField(
        max_length=23,
        unique=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    is_admin = models.BooleanField(
        default=False,
    )
    is_verified = models.BooleanField(
        default=False,
    )
    is_social_login = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = UserManager()

    def __str__(self):
        return str(self.username)

    class Meta:
        verbose_name_plural = "Users"
