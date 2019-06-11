"""

API views for posts in the blog models. Room for
cache can be made with caching PostDetailAPIView.

TODO creating blog posts with POST based API views.
     Can be implemented with ListCreateAPIView but need
     for authentication will have to be figured out.

TODO write a view listing blog posts for authenticated
     users to delete or update or simply view drafts
     or posted material. Same as PostCreateAPIView,
     authentication will have to be covered much later.

"""
from rest_framework.permissions import AllowAny
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)

from blog.models import Post
from blog.serializers import (
    PostListSerializer,
    PostDetailSerializer
)


class PostListAPIView(ListAPIView):
    """
    Lists all posts that aren't drafted True
    in JSON format with AllowAny permissions.
    """

    permission_classes = (AllowAny,)
    serializer_class = PostListSerializer
    queryset = Post.objects.filter(draft=False)


class PostDetailAPIView(RetrieveAPIView):
    """
    Gets details of blog posts in drafted False
    queryset. Optimisation using id as lookup_field
    instead of slug needs to be further tested.
    """
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    permission_classes = (AllowAny,)
    serializer_class = PostDetailSerializer
    queryset = Post.objects.filter(draft=False)
