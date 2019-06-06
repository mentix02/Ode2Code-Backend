from django.shortcuts import get_list_or_404

from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.generics import ListAPIView, RetrieveAPIView

from blog.models import Post
from author.models import Author
from tutorial.models import Tutorial, Series
from blog.serializers import PostListSerializer
from author.serializers import AuthorListSerializer
from tutorial.serializers import (
    SeriesListSerializer,
    TutorialListSerializer
)


class AuthorListAPIView(ListAPIView):
    queryset = Author.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = AuthorListSerializer


class AuthorDetailAPIView(RetrieveAPIView):
    lookup_url_kwarg = 'username'
    lookup_field = 'user__username'
    queryset = Author.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AuthorListSerializer


class AuthorPostListAPIView(ListAPIView):
    """
    This view gets the list of posts by the author username
    provided in the url as a slug - '<slug:username>/author/'
    """

    serializer_class = PostListSerializer

    def get_queryset(self):

        username = self.kwargs['username']
        queryset = get_list_or_404(Post, author__user__username=username)
        return queryset


class AuthorTutorialListAPIView(ListAPIView):
    """
    This view gets the list of tutorials by the author username
    provided in the url as a slug - '<slug:username>/tutorials/'
    """

    serializer_class = TutorialListSerializer

    def get_queryset(self):

        username = self.kwargs['username']
        queryset = get_list_or_404(Tutorial, author__user__username=username)
        return queryset


class AuthorSeriesListAPIView(ListAPIView):
    """
    Same as AuthorTutorialListAPIView but for tutorial.Series.
    """

    serializer_class = SeriesListSerializer

    def get_queryset(self):

        username = self.kwargs['username']
        queryset = get_list_or_404(Series, creator__user__username=username)
        return queryset
