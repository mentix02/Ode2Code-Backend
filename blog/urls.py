from django.urls import path

from blog.views import (
    PostListAPIView,
    PostDetailAPIView,
)

app_name = 'blog'

urlpatterns = [
    path('', PostListAPIView.as_view()),
    path('detail/<slug:slug>/', PostDetailAPIView.as_view()),
]
