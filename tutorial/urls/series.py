from django.urls import path

from tutorial.views.series import (
    SeriesListAPIView,
    SeriesDetailAPIView,
    SeriesCreateAPIView,
    SeriesBookmarkAPIView,
    SeriesTutorialsListAPIView,
)

urlpatterns = (
    path('', SeriesListAPIView.as_view()),
    path('detail/<slug:slug>/', SeriesDetailAPIView.as_view()),
    path('detail/<slug:slug>/tutorials/', SeriesTutorialsListAPIView.as_view()),

    # CRUD operations on series
    path('new/', SeriesCreateAPIView.as_view()),
    path('bookmark/', SeriesBookmarkAPIView.as_view())

)
