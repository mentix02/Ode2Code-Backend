from django.urls import path

from author.views import (
    AuthorListAPIView,
    AuthorDetailAPIView,
    AuthorPostListAPIView,
    AuthorSeriesListAPIView,
    AuthorTutorialListAPIView,
    GetTokenAndAuthorDetailsAPIView,
)

urlpatterns = (
    path('', AuthorListAPIView.as_view()),
    path('auth/', GetTokenAndAuthorDetailsAPIView.as_view()),
    path('detail/<slug:username>/', AuthorDetailAPIView.as_view()),
    path('<slug:username>/posts/', AuthorPostListAPIView.as_view()),
    path('<slug:username>/series/', AuthorSeriesListAPIView.as_view()),
    path('<slug:username>/tutorials/', AuthorTutorialListAPIView.as_view()),
)
