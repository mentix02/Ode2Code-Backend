from django.urls import path

from blog.views import (
    PostListAPIView,
    PostCreateAPIView,
    PostDetailAPIView,
)

app_name = 'blog'

urlpatterns = [
    path('', PostListAPIView.as_view(), name='api-list'),
    path('new/', PostCreateAPIView.as_view(), name='api-new'),
    path('detail/<slug:slug>/', PostDetailAPIView.as_view(), name='api-detail'),
]
