from django.urls import path

from tutorial.views.tutorials import (
    RecentTutorialAPIView,
    TutorialDetailAPIView,
    TutorialCreateAPIView,
    TutorialDeleteAPIView,
    TutorialLikeUnlikeAPIView,
)

urlpatterns = (
    path('recent/', RecentTutorialAPIView.as_view()),
    path('detail/<slug:slug>/', TutorialDetailAPIView.as_view(), name='api-tutorial-detail'),

    # CRUD operations on tutorials
    path('new/', TutorialCreateAPIView.as_view()),
    path('like/', TutorialLikeUnlikeAPIView.as_view()),
    path('delete/<slug:slug>/', TutorialDeleteAPIView.as_view()),

)
