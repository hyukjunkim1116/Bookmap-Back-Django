from rest_framework.views import exception_handler
from rest_framework import status

"""
code: 400
detail: "잘못된 요청입니다."
status: "error"
"""


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        print("response", response)
        response.data["code"] = response.status_code
        response.data["status"] = exc.default_code
        if response.status_code == 401:
            response.data["detail"] = "인증이 필요합니다"
        elif response.status_code == 404:
            response.data["detail"] = "존재하지 않는 데이터"
        elif response.status_code == 500:
            response.data["detail"] = "Something went wrong"
    return response
