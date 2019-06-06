from django.urls import path, include

urlpatterns = [
    path('blog/', include('blog.urls')),
    path('authors/', include('author.urls')),
    path('series/', include('tutorial.urls.series')),
    path('tutorials/', include('tutorial.urls.tutorials')),
]
