from django.urls import path

from tutorial.views.tutorials import (
    RecentTutorialAPIView,
    TutorialDetailAPIView,
)

urlpatterns = (
    path('recent/', RecentTutorialAPIView.as_view()),
    path('detail/<slug:slug>/', TutorialDetailAPIView.as_view()),
)
