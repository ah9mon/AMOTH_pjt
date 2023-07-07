from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("articles", views.ArticleListCreateView.as_view(), name="article_list"),
    path("articles/<int:pk>", views.ArticleRetrieveUpdateDeleteView.as_view(), name="article_detail"),
    path("articles/<int:article_pk>/comments", views.CommentListCreateView.as_view(), name="comment_list"),
    path("comments/<int:pk>", views.CommentRetrieveUpdateDeleteView.as_view(), name="comment_detail"),
    path("articles/<int:article_pk>/likes", views.LikeArticleView.as_view(), name="like_article"),
]
