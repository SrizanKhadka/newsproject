from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from news.models import Article
from news.api.serializer import ArticleSerializer

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
