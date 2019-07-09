from django.urls import path

from blog.views import (
    PostListAPIView,
    PostCreateAPIView,
    PostDetailAPIView,
)

app_name = 'blog'

urlpatterns = [
    path('', PostListAPIView.as_view()),
    path('new/', PostCreateAPIView.as_view()),
    path('detail/<slug:slug>/', PostDetailAPIView.as_view()),
]
