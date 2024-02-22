import re
from rest_framework import status
from rest_framework.response import Response
from users.models import User

class UserValidator:
    def validate_required_fields(self, **kwargs):
        for field_name, field_value in kwargs.items():
            if not field_value:
                return Response(
                    {"error": f"{field_name} 입력은 필수입니다!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
    def validate_password(self, password):
        if len(password) < 8:
            return Response(
                {"error": "비밀번호는 8자리 이상이어야 합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not re.search(r"[a-zA-Z]", password):
            return Response(
                {"error": "비밀번호는 하나 이상의 영문이 포함되어야 합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not re.search(r"\d", password):
            return Response(
                {"error": "비밀번호는 하나 이상의 숫자가 포함되어야 합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not re.search(r"[!@#$%^&*()]", password):
            return Response(
                {"error": "비밀번호는 적어도 하나 이상의 특수문자(!@#$%^&*())가 포함되어야 합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    
    def validate_passwords_match(self, password, password2):
        if password != password2:
            return Response(
                {"error": "비밀번호가 일치하지 않습니다!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def validate_unique_user(self, email, username):
        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "해당 이메일을 가진 유저가 이미 있습니다!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "해당 닉네임을 가진 유저가 이미 있습니다!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

