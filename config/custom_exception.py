from rest_framework.exceptions import APIException
from rest_framework import status


class UserNotFound(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "유저를 찾을 수 없습니다."


class LoginFail(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "아이디 또는 비밀번호가 일치하지 않습니다."


class InvalidRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "잘못된 요청입니다."


class InvalidPassword(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "비밀번호가 맞지 않습니다."


class ForbiddenPost(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "게시글 본인만 접근 가능합니다."


class ForbiddenComment(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "댓글 본인만 접근 가능합니다."


class CustomPermissionDenied(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "접근할 수 없습니다."


class AlreadySignUpWithNormal(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "이미 일반 회원으로 로그인 한 계정입니다"


class RepetitiveEmail(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "이미 있는 이메일입니다."


class EmailNotFound(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "이메일에 일치하는 사용자가 없습니다"


class RepetitiveUsername(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "이미 있는 이름입니다."


class BookFetchFail(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "책 정보를 불러오지 못했습니다."


class InvalidField(APIException):
    def __init__(self, default_detail):
        self.detail = default_detail
        self.status_code = status.HTTP_400_BAD_REQUEST


class BadPasswordRequest(APIException):
    def __init__(self, default_detail):
        self.detail = default_detail
        self.status_code = status.HTTP_400_BAD_REQUEST
