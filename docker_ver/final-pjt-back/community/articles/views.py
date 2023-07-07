from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Article, Comment, Like
from .serializers import ArticleSerializer, CommentSerializer, LikeSerializer


class ArticleListCreateView(APIView):
    """
    API view for listing and creating articles.
    """

    def get(self, request):
        """
        Handles GET requests to retrieve a list of articles.
        """

        user_id = request.GET.get("user_id")

        if user_id:
            # Get articles created by the user
            my_articles = Article.objects.filter(user_id=user_id)
            liked_articles = Like.objects.filter(user_id=user_id)

            my_serializer = ArticleSerializer(my_articles, many=True)
            liked_serializer = LikeSerializer(liked_articles, many=True)

            serializer_data = {
                "my_articles": my_serializer.data,
                "liked_articles": liked_serializer.data,
            }
        else:
            # Get all articles
            articles = Article.objects.all()
            serializer = ArticleSerializer(articles, many=True)
            serializer_data = serializer.data

        return Response(serializer_data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Handles POST requests to create a new article.
        """

        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticleRetrieveUpdateDeleteView(APIView):
    """
    API view for retrieving, updating, and deleting an article.
    """

    def get(self, request, pk):
        """
        Handles GET requests to retrieve an article by its primary key.
        """

        article = get_object_or_404(Article, pk=pk)
        user_id = request.GET.get("user_id")

        liked = False
        likes = article.like_set.all()
        for liked_article in likes:
            if liked_article.user_id == user_id:
                liked = True
                break

        liked_count = len(likes)

        serializer = ArticleSerializer(article)

        data = {
            "article": serializer.data,
            "liked_count": liked_count,
            "liked": liked,
        }
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """
        Handles DELETE requests to delete an article by its primary key.
        """

        article = get_object_or_404(Article, pk=pk)
        user_id = request.GET.get("user_id")

        if article.user_id == user_id:
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, pk):
        """
        Handles PUT requests to update an article by its primary key.
        """

        article = get_object_or_404(Article, pk=pk)
        user_id = request.GET.get("user_id")

        if article.user_id == user_id:
            serializer = ArticleSerializer(article, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class CommentListCreateView(APIView):
    """
    API view for listing and creating comments for an article.
    """

    def get(self, request, article_pk):
        """
        Handles GET requests to retrieve comments for an article.
        """

        comments = Comment.objects.filter(article=article_pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, article_pk):
        """
        Handles POST requests to create a new comment for an article.
        """

        article = get_object_or_404(Article, id=article_pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentRetrieveUpdateDeleteView(APIView):
    """
    API view for retrieving, updating, and deleting a comment.
    """

    def delete(self, request, pk):
        """
        Handles DELETE requests to delete a comment by its primary key.
        """

        comment = get_object_or_404(Comment, pk=pk)
        user_id = request.GET.get("user_id")

        if comment.user_id == user_id:
            comment.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, pk):
        """
        Handles PATCH requests to update a comment by its primary key.
        """

        comment = get_object_or_404(Comment, pk=pk)
        user_id = request.data.get("user_id")

        if comment.user_id == user_id:
            serializer = CommentSerializer(comment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class LikeArticleView(APIView):
    """
    API view for liking/unliking an article.
    """

    def post(self, request, article_pk):
        """
        Handles POST requests to like/unlike an article.
        """

        user_id = request.data.get("user_id")
        article = get_object_or_404(Article, id=article_pk)

        likes = Like.objects.filter(user_id=user_id, article=article)
        if likes.exists():
            likes.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            data = {
                "user_id": user_id,
                "article": article_pk,
            }
            serializer = LikeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
