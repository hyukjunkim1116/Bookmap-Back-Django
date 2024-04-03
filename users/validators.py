import re
from django.forms import ValidationError
from rest_framework import status
from rest_framework.response import Response
from users.models import User
from config.custom_exception import InvalidPassword


class UserValidator:
    def validate_password(self, password):
        if len(password) < 8:
            raise ValidationError("비밀번호는 8자리 이상이어야 합니다.")
        if not re.search(r"[a-zA-Z]", password):
            raise ValidationError("비밀번호는 하나 이상의 영문이 포함되어야 합니다.")

        if not re.search(r"\d", password):
            raise ValidationError("비밀번호는 하나 이상의 숫자가 포함되어야 합니다.")

        if not re.search(r"[!@#$%^&*()]", password):
            raise ValidationError(
                "비밀번호는 적어도 하나 이상의 특수문자(!@#$%^&*())가 포함되어야 합니다."
            )

    def validate_passwords_match(self, password, password2):
        if password != password2:
            raise ValidationError("비밀번호가 일치하지 않습니다!")

    def validate_unique_user(self, email, username):
        if User.objects.filter(email=email).exists():
            raise ValidationError("해당 이메일을 가진 유저가 이미 있습니다!")

        if User.objects.filter(username=username).exists():
            raise ValidationError("해당 닉네임을 가진 유저가 이미 있습니다!")
