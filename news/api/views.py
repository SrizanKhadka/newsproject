from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from news.models import Article, Journalist
from news.api.serializer import ArticleSerializer, JournalistSerializer


# class based views
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

class createJournalistAPIView(APIView):

    def get(self,request):
        authors = Journalist.objects.all()
        serializer = JournalistSerializer(authors,many=True,context={'request':request})
        return Response(serializer.data)
    
    def post(self,request):
        serializer = JournalistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)


class createArticleListAPIView(APIView):

    def get(self, request):
        article = Article.objects.all()
        serializer = ArticleSerializer(article, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class articleDetailAPIView(APIView):
    def get_object(self, articleId):
        article = get_object_or_404(Article, id=articleId)
        return article

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, articleId):
        article = self.get_object(articleId)
        serializer = ArticleSerializer(instance=article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,articleId):
        article = self.get_object(articleId)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# function based views
@api_view(["GET", "POST"])
def getArticleList(request):
    if request.method == "GET":
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "DELETE", "PUT"])
def getArticleDetails(request, articleId):
    try:
        article = Article.objects.get(id=articleId)
    except Article.DoesNotExist:
        return Response(
            {
                "error": {
                    "code": 404,
                    "message": f"The article with id {articleId} is not available!",
                }
            },
            status=status.HTTP_404_NOT_FOUND,
        )
    if request.method == "GET":
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    elif request.method == "DELETE":
        article.delete()
        return Response(
            {
                "result": {
                    "code": 204,
                    "message": f"The article with id {articleId} is deleted!",
                }
            },
            status=status.HTTP_204_NO_CONTENT,
        )
    elif request.method == "PUT":
        serializer = ArticleSerializer(instance=article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
