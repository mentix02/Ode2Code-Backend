from django.urls import path

from author.views import (
    AuthorListAPIView,
    AuthorDetailAPIView,
    AuthorContentAPIView,
    AuthorPostListAPIView,
    AuthenticateAuthorView,
    AuthorSeriesListAPIView,
    AuthorTutorialListAPIView,
    AuthorLikedTutorialIdsAPIView,
    GetTokenAndAuthorDetailsAPIView,
    AuthorBookmarkedSeriesIdsAPIView,
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

    # for author bookmarked models
    path('bookmarked/series/', AuthorBookmarkedSeriesIdsAPIView.as_view()),

    # to authenticate authors
    path('authenticate/<uuid:uuid>/', AuthenticateAuthorView.as_view()),

    # to get all content from author
    path('content/', AuthorContentAPIView.as_view()),

)
