from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
import requests
from config.custom_exception import BookFetchFail


class BookView(APIView):
    def get_books_or_404(self):
        try:
            response = requests.get(
                "https://openapi.naver.com/v1/search/book.json?query=책&start=1",
                headers={
                    "X-Naver-Client-Id": settings.NAVER_BOOK_CLIENT_ID,
                    "X-Naver-Client-Secret": settings.NAVER_BOOK_SECRET,
                },
            )
        except Exception as e:
            print(e)
            raise BookFetchFail
        return response.json()

    def get(self, request):
        result = self.get_books_or_404()
        return Response(result, status=status.HTTP_200_OK)


class BookDetailView(APIView):
    def get_book_detail_or_404(self, isbn):
        try:
            response = requests.get(
                "https://openapi.naver.com/v1/search/book_adv.json?isbn=${isbn}",
                headers={
                    "X-Naver-Client-Id": settings.NAVER_BOOK_CLIENT_ID,
                    "X-Naver-Client-Secret": settings.NAVER_BOOK_SECRET,
                },
            )
        except Exception as e:
            print(e)
            raise BookFetchFail
        return response.json()

    def get(self, request):
        result = self.get_book_detail_or_404()
        return Response(result, status=status.HTTP_200_OK)


class BookCrawlingView(APIView):
    pass
    # def get_book_detail_or_404(self, isbn):
    #     try:
    #         response = requests.get(
    #             "https://openapi.naver.com/v1/search/book_adv.json?isbn=${isbn}",
    #             headers={
    #                 "X-Naver-Client-Id": settings.NAVER_BOOK_CLIENT_ID,
    #                 "X-Naver-Client-Secret": settings.NAVER_BOOK_SECRET,
    #             },
    #         )
    #     except Exception as e:
    #         print(e)
    #         raise BookFetchFail
    #     return response.json()

    # def get(self, request):
    #     result = self.get_book_detail_or_404()
    #     return Response(result, status=status.HTTP_200_OK)
