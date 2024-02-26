import random
import boto3
import uuid
import requests
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.generics import get_object_or_404
from users.serializers import (
    UserSerializer,
    CustomTokenObtainPairSerializer,
)
from django.contrib.auth.hashers import make_password
from users.models import User
from users.validators import UserValidator
from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied
from django.conf import settings
from django.db import transaction
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from users.email_tokens import account_activation_token
from .send_kakao_message import kakao_message


class UserSignUpVerifyView(APIView):
    # """비밀번호 찾기. 이메일 인증하면 비밀번호 재설정할 기회를 준다. 주석추가에정,이메일 인증 추가예정"""
    def post(self, request, uid):
        try:
            user = User.objects.get(id=uid)
            if user:
                html = render_to_string(
                    "users/email_verify.html",
                    {
                        "backend_base_url": settings.BACKEND_BASE_URL,
                        "uidb64": urlsafe_base64_encode(force_bytes(uid))
                        .encode()
                        .decode(),
                        "token": account_activation_token.make_token(user),
                        "user": user,
                    },
                )
                to_email = user.email
                send_mail(
                    "안녕하세요 FoodMap입니다. 이메일 인증을 진행해주세요!",
                    "_",
                    settings.DEFAULT_FROM_MAIL,
                    [to_email],
                    html_message=html,
                )
                return Response(
                    {"message": "이메일 전송 완료!"}, status=status.HTTP_200_OK
                )
        except User.DoesNotExist:
            return Response(
                {"error": "해당 이메일에 일치하는 사용자가 없습니다!"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserEmailPermitView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
            if account_activation_token.check_token(user, token):
                user.is_verified = True
                user.save()

                return redirect(f"{settings.FRONT_BASE_URL}/verify/{token}")
            return Response({"error": "AUTH_FAIL"}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({"error": "KEY_ERROR"}, status=status.HTTP_400_BAD_REQUEST)


class UserImageView(APIView):
    permission_classes = [IsAuthenticated]

    def get_s3_client(self):
        # S3 클라이언트 생성 및 반환
        return boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )

    def patch(self, request, uid):
        unique_id = uuid.uuid4()
        user = get_object_or_404(User, id=uid)
        if request.user.id == uid:
            s3_client = self.get_s3_client()
            if user.image:
                try:
                    s3_client.delete_object(
                        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                        Key=f"{user.image.split('m/')[-1]}",
                    )
                except Exception as e:
                    print(e)
            image_file = request.data["image"]

            s3_client.upload_fileobj(
                image_file,
                settings.AWS_STORAGE_BUCKET_NAME,
                f"users/{uid}/{unique_id}{image_file.name}",
            )
            image_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/users/{uid}/{unique_id}{image_file.name}"
            user.image = image_url
            user.save()

            return Response({"image": image_url}, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied


class UserView(APIView):
    # 유저 전체보기
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 유저 생성하기
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        password2 = request.data.get("passwordConfirm")
        username = request.data.get("username")

        required_fields_errors = UserValidator.validate_required_fields(
            self, email=email, password=password, password2=password2, username=username
        )
        if required_fields_errors:
            return required_fields_errors
        # 비밀번호 검증
        password_validation_error = UserValidator.validate_password(self, password)
        if password_validation_error:
            return password_validation_error
        # 비밀번호 확인 검증
        password_match_error = UserValidator.validate_passwords_match(
            self, password, password2
        )
        if password_match_error:
            return password_match_error
        # 유저 중복 검사
        unique_user_error = UserValidator.validate_unique_user(self, email, username)
        if unique_user_error:
            return unique_user_error

        serializer = UserSerializer(
            data=request.data,
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class KakaoLogIn(APIView):
    def post(self, request):

        redirect_uri = settings.KAKAO_REDIRECT_URI
        try:
            code = request.data
            try:
                token = requests.post(
                    "https://kauth.kakao.com/oauth/token",
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    data={
                        "grant_type": "authorization_code",
                        "client_id": settings.KAKAO_REST_API_KEY,
                        "redirect_uri": f"{redirect_uri}",
                        "code": str(code),
                        "scope": "talk_message",
                    },
                )
            except Exception as e:
                pass
            access_token = token.json().get("access_token")
            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )
            user_data = user_data.json()

            kakao_account = user_data.get("kakao_account")
            profile = kakao_account.get("profile")
            try:
                kakao_message(access_token, user_data)
            except Exception as e:
                print(e)
            try:
                user = User.objects.get(email=kakao_account.get("email"))
                if user:
                    if user.is_social_login:
                        serializer = CustomTokenObtainPairSerializer(
                            data={
                                "email": user.email,
                                "password": str(user_data["id"]),
                                "username": user.username,
                                "passwordConfirm": None,
                            }
                        )
                        if serializer.is_valid():
                            token = serializer.validated_data

                            return Response(token, status=status.HTTP_200_OK)
                        else:
                            return Response(
                                {"error": serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST,
                            )
                    else:
                        return Response(
                            {"error": "이미 일반 회원으로 로그인 한 계정입니다"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
            except User.DoesNotExist:
                user = User.objects.create(
                    email=kakao_account.get("email"),
                    password=make_password(str(user_data["id"])),
                    username=profile.get("nickname"),
                    image=profile.get("thumbnail_image_url"),
                    is_social_login=True,
                )
                serializer = CustomTokenObtainPairSerializer(
                    data={
                        "email": user.email,
                        "password": str(user_data["id"]),
                        "username": user.username,
                        "passwordConfirm": None,
                    }
                )
                if serializer.is_valid():
                    token = serializer.validated_data

                    return Response(token, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        required_fields_errors = UserValidator.validate_required_fields(
            self, email=email, password=password, password2=password, username="None"
        )
        if required_fields_errors:
            return required_fields_errors

        user = authenticate(
            request,
            email=email,
            password=password,
        )
        if user:

            serializer = CustomTokenObtainPairSerializer(data=request.data)
            if serializer.is_valid():
                token = serializer.validated_data

                return Response(token, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "비밀번호가 틀렸습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_s3_client(self):
        # S3 클라이언트 생성 및 반환
        return boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )

    def get(self, request, uid):

        # """유저 프로필 조회 주석 추가 예정"""
        user = get_object_or_404(User, id=uid)
        if request.user.id == uid:
            serializer = UserSerializer(
                user,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = UserSerializer(
                user,
                context={"request": request},
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, uid):
        # """유저 프로필 수정"""
        print("asdas")
        user = get_object_or_404(User, id=uid)
        print(request.data)
        if request.user.id == uid:
            serializer = UserSerializer(
                user,
                data=request.data,
                partial=True,
                context={"request": request},
            )
            if serializer.is_valid():
                serializer.save()
                print(serializer.data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied

    def delete(self, request, uid):
        user = get_object_or_404(User, id=uid)
        if request.user.id == uid:
            s3_client = self.get_s3_client()
            # 폴더 안의 객체 리스트업

            response = s3_client.list_objects(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME, Prefix=f"users/{uid}"
            )

            if response.get("Contents") is not None:
                # 폴더 안의 모든 객체 삭제

                for obj in response.get("Contents", []):
                    s3_client.delete_object(
                        Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=obj["Key"]
                    )
            s3_client.delete_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=f"users/{uid}/"
            )
            user.delete()
            return Response({"message": "삭제되었습니다!"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "삭제 실패!"}, status=status.HTTP_403_FORBIDDEN)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = get_object_or_404(User, id=request.user.id)
        old_password = request.data.get("oldPassword")
        new_password = request.data.get("newPassword")
        new_password_confirm = request.data.get("newPasswordConfirm")
        if new_password != new_password_confirm:
            return Response(
                {"error": "비밀번호 확인이 맞지 않습니다"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(
                {"message": "비밀번호가 변경되었습니다!"}, status=status.HTTP_200_OK
            )
        else:
            return Response("auth/wrong-password", status=status.HTTP_400_BAD_REQUEST)


class FindPasswordView(APIView):
    def put(self, request):
        try:
            user_email = request.data
            user = User.objects.get(email=user_email)
            if user:
                characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
                new_password = "".join(random.choice(characters) for _ in range(10))
                user.set_password(new_password)
                user.save()
                return Response(
                    {"password": new_password},
                    status=status.HTTP_200_OK,
                )
        except User.DoesNotExist:
            return Response("auth/user-not-found", status=status.HTTP_400_BAD_REQUEST)
