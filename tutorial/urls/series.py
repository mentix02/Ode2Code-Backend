from django.urls import path

from tutorial.views.series import (
    SeriesListAPIView,
    SeriesDetailAPIView,
    SeriesTutorialsListAPIView,
)

urlpatterns = (
    path('', SeriesListAPIView.as_view()),
    path('detail/<slug:slug>/', SeriesDetailAPIView.as_view()),
    path('detail/<slug:slug>/tutorials/', SeriesTutorialsListAPIView.as_view()),
)
