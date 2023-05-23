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
from .models import Article, Comment, Like

#Serializer
from .serializers import ArticleSerializer, CommentSerializer, LikeSerializer

# Create your views here.
@api_view(['GET', 'POST'])
def article_list(request):
    # 게시글 데이터 READ 요청
    if request.method == 'GET':
        '''
        user_id를 
        params에 넣어서 보내기
        '''
        user_id = request.GET.get('user_id')

        # user_id가 요청에 섞여왔으면 -> 마이페이지의 내가 쓴 게시글, 좋아요한 게시글 전체보기
        if user_id :
            my_articles = get_list_or_404(Article, user_id = user_id) # 나의 게시글
            liked_article = get_list_or_404(Like, user_id = user_id) # 내가 좋아요한 게시글

            my_serializer = ArticleSerializer(my_articles, many=True)
            liked_serializer = LikeSerializer(liked_article, many=True)

            serializer_data = {
                "my_articles" : my_serializer.data,
                "liked_articles" : liked_serializer.data,
            }
        
        # user_id가 없이 왔으면 -> 게시글 전체보기
        else:
            articles = get_list_or_404(Article)

            serializer = ArticleSerializer(articles, many=True)
            serializer_data = serializer.data

        return Response(serializer_data, status=status.HTTP_200_OK)
    
    # 게시글 데이터 CREATE 요청
    elif request.method == 'POST': 
        # movie_id랑 title만 받아서 저장하자 
        serializer = ArticleSerializer(data = request.data) # 역직렬화
        if serializer.is_valid(raise_exception=True): # 유효성 검사 / 실패하면 400code 
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED) # 직렬화해서 상태코드랑 같이 보내기

@api_view(['GET','DELETE','PUT'])
def article_detail(request, article_pk):
    '''
    DELETE, PUT에선 user_id 같이 보내줘야함
    DELETE -> params에 넣어서 보내기 -> request.GET 으로 읽기
    PUT -> body에 넣어서 보내기 -> request.POST or request.data 으로 읽기
    '''
    article = get_object_or_404(Article, pk=article_pk)
    user_id = request.GET.get('user_id')
    # print(article.user_id)
    '''
    print(request.GET) # params에 있는거 request를 사전형 객체로 만들어줌 
    print(request.POST) # body에 있는거 request를 사전형 객체로 만들어줌 
    print(request.data) # body에 있는거 request를 사전형 객체로 만들어줌
    '''
    # print(user_id)

    # 게시글 상세 조회
    if request.method == 'GET':
        liked = False
        likes = article.like_set.all()
        # 현재 유저의 좋아요 여부 찾기
        for liked_article in likes:
            if liked_article.user_id == user_id:
                liked = True
                break
        
        liked_count = len(likes)
        
        serializer = ArticleSerializer(article)

        data = {
                "article" : serializer.data,
                "liked_count" : liked_count,
                "liked" : liked,
            }
        return Response(data, status=status.HTTP_200_OK)
    
    # 게시글 삭제
    elif request.method == 'DELETE':
        
        # 게시글 작성자 == 요청 user 면
        if article.user_id == user_id: 
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            print('권한없어서 삭제 불가')
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    # 게시글 수정
    elif request.method == 'PUT':
        # 게시글 작성자 == 요청 user 면 
        if article.user_id == user_id:
            serializer = ArticleSerializer(article, data= request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
@api_view(['GET', 'POST'])
def comment_list(request, article_pk):
    # 해당 게시글의 댓글 불러오기 
    if request.method == 'GET': 
        comments = Comment.objects.filter(article = article_pk)
        print(comments)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 댓글 생성
    elif request.method == 'POST':
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
        user_id = request.GET.get('user_id')
        if comment.user_id == user_id:           
            comment.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    # 댓글 수정
    elif request.method == 'PATCH':
        user_id = request.POST.get('user_id')
        if comment.user_id == user_id:
            serializer = CommentSerializer(comment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
def like_article(request,article_pk):
    '''
    좋아요/좋아요 취소 
    '''
    if request.method =='POST':
        user_id = request.data.get('user_id')
        print(user_id)
        article_id = article_pk
        likes = Like.objects.filter(user_id = user_id) # 요청 보낸 유저가 좋아요한 게시글 리스트 다 받기 
        
        # 해당 게시글 좋아요 여부 체크
        for like in likes:

            # 좋아요 했으면 좋아요 취소 
            if like.article.id == int(article_id):
                like.delete()
                return Response(status=status.HTTP_200_OK)

        # 좋아요 안했으면 좋아요
        article = get_object_or_404(Article, pk = int(article_id))
        data = {
            'user_id' : user_id,
        }
        serializer = LikeSerializer(data = data)
        if serializer.is_valid():
            serializer.save(article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# 