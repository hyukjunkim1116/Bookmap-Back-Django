from django.urls import path
from . import views


urlpatterns = [
    path(
        "",
        views.BookView.as_view(),
        name="books",
    ),
    path(
        "detail",
        views.BookDetailView.as_view(),
        name="books",
    ),
    path(
        "crawling",
        views.BookCrawlingView.as_view(),
        name="books",
    ),
]
