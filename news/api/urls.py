from django.urls import path
from news.api import views as api_views

urlpatterns = [
    path("article/", api_views.getArticleList, name="article/list"),
    path(
        "article/<int:articleId>", api_views.getArticleDetails, name="article/details"
    ),
]
