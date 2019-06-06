from django.urls import path

from tutorial.views.series import (
    SeriesListAPIView,
    SeriesTutorialsListAPIView
)

urlpatterns = (
    path('', SeriesListAPIView.as_view()),
    path('<slug:slug>/tutorials/', SeriesTutorialsListAPIView.as_view()),
)
