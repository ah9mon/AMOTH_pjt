from django.shortcuts import get_object_or_404, get_list_or_404

# DRF
from rest_framework.response import Response
from rest_framework.decorators import api_view
'''
DRF의 @api_view 데코레이터는 CSRF 보호를 위한 토큰을 자동으로 처리해주는 기능을 제공 
이를 통해 DELETE 및 PATCH와 같은 메서드에 대한 CSRF 보호를 간단하게 구현
'''
from rest_framework import status

#Model
from .models import Article, Comment

#Serializer
from .serializers import ArticleSerializer, CommentSerializer

# Create your views here.
@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        # articles = Article.objects.all()
        articles = get_list_or_404(Article)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST': 
        # movie_id랑 title만 받아서 저장하자 
        # print(request.data)
        serializer = ArticleSerializer(data = request.data) # 역직렬화
        if serializer.is_valid(raise_exception=True): # 유효성 검사 / 실패하면 400code 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) # 직렬화해서 상태코드랑 같이 보내기

@api_view(['GET','DELETE','PUT'])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    # 게시글 상세 조회
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        print(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 게시글 삭제
    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # 게시글 수정
    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data= request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
@api_view(['GET', 'POST'])
def comment_list(request, article_pk):
    # 해당 게시글의 댓글 불러오기 
    if request.method == 'GET':
        comments = get_list_or_404(Comment, article = article_pk)
        print(comments)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 댓글 생성
    elif request.method == 'POST':
        print('>>>')
        article = get_object_or_404(Article, pk=article_pk)
        serializer = CommentSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE', 'PATCH']) 
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk = comment_pk)

    # 댓글 삭제 
    if request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # 댓글 수정
    elif request.method == 'PATCH':
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    
