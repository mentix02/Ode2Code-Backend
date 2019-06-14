from django.urls import path

from author.views import (
    AuthorListAPIView,
    AuthorDetailAPIView,
    AuthorPostListAPIView,
    AuthorSeriesListAPIView,
    AuthorTutorialListAPIView,
    AuthorLikedTutorialIdsAPIView,
    GetTokenAndAuthorDetailsAPIView,
)

urlpatterns = (

    # for admin usage
    path('', AuthorListAPIView.as_view()),

    # for authentication purposes
    path('auth/', GetTokenAndAuthorDetailsAPIView.as_view()),

    # for author detail and related models
    path('detail/<slug:username>/', AuthorDetailAPIView.as_view()),
    path('detail/<slug:username>/posts/', AuthorPostListAPIView.as_view()),
    path('detail/<slug:username>/series/', AuthorSeriesListAPIView.as_view()),
    path('detail/<slug:username>/tutorials/', AuthorTutorialListAPIView.as_view()),

    # for author liked models
    path('liked/tutorials/', AuthorLikedTutorialIdsAPIView.as_view()),
)
