from django.urls import path
from news.api import views as api_views

#Urls forfunction based Api views.
"""
urlpatterns = [
    path("article/", api_views.getArticleList, name="article/list"),
    path(
        "article/<int:articleId>", api_views.getArticleDetails, name="article/details"
    ),
]
"""

#Urls for class based api views.
urlpatterns = [
    path("article/", api_views.createArticleListAPIView.as_view(), name="article/list"),
    path(
        "articles/<int:articleId>",
        api_views.articleDetailAPIView.as_view(),
        name="article/details",
    ),
]
