from django.urls import path

from tutorial.views.series import (
    SeriesListAPIView,
    SeriesDeleteAPIView,
    SeriesDetailAPIView,
    SeriesCreateAPIView,
    SeriesBookmarkAPIView,
    SeriesTypeListAPIView,
    SeriesAvailabilityAPIView,
    SeriesNameAndIdListAPIView,
    SeriesTutorialsListAPIView,
)

urlpatterns = (

    path('', SeriesListAPIView.as_view()),
    path('names/', SeriesNameAndIdListAPIView.as_view()),
    path('type/<slug:slug>/', SeriesTypeListAPIView.as_view()),
    path('detail/<slug:slug>/', SeriesDetailAPIView.as_view()),
    path('detail/<slug:slug>/tutorials/', SeriesTutorialsListAPIView.as_view()),

    # CRUD operations on series
    path('new/', SeriesCreateAPIView.as_view()),
    path('bookmark/', SeriesBookmarkAPIView.as_view()),
    path('is_available/', SeriesAvailabilityAPIView.as_view()),
    path('delete/<slug:slug>/', SeriesDeleteAPIView.as_view()),

)
