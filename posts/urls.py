from django.urls import path
from . import views


urlpatterns = [
    path(
        "",
        views.PostView.as_view(),
        name="post_root",
    ),
    path(
        "image/",
        views.PostImageView.as_view(),
        name="post_image",
    ),
    path(
        "image/<int:post_id>/",
        views.PostImageReactView.as_view(),
        name="only_react_image",
    ),
    path(
        "<int:post_id>/",
        views.PostDetailView.as_view(),
        name="post_detail",
    ),
    path(
        "<int:post_id>/comment/",
        views.CommentView.as_view(),
        name="comment",
    ),
    path(
        "comment/<int:comment_id>/",
        views.CommentDetailView.as_view(),
        name="comment",
    ),
    path(
        "<int:post_id>/like/",
        views.PostLikeView.as_view(),
        name="post_like",
    ),
    path(
        "<int:post_id>/dislike/",
        views.PostDisikeView.as_view(),
        name="post_dislike",
    ),
    path(
        "<int:post_id>/bookmark/",
        views.BookmarkView.as_view(),
        name="post_bookmark",
    ),
]
