"""

API views for posts in the blog models. Room for
cache can be made with caching PostDetailAPIView.

TODO write a view listing blog posts for authenticated
     users to delete or update or simply view drafts
     or posted material. Same as PostCreateAPIView,
     authentication will have to be covered much later.

"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FormParser, MultiPartParser
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


class PostCreateAPIView(APIView):
    """
    Provides an interface to create new
    only if an authenticated request comes through.
    """

    parser_classes = (FormParser, MultiPartParser)

    @staticmethod
    def post(request):

        # get required params
        try:
            body = request.POST['body']
            title = request.POST['title']
            thumbnail = request.POST['thumbnail']
            draft = request.POST.get('draft', False)
            description = request.POST['description']
        except Exception as e:
            return Response({
                'error': f'{str(e)} field not provided.'
            }, status=400)

        token = request.POST.get('token')

        if not token and not request.user.is_authenticated:
            return Response({
                'error': 'You need to be authenticated to create a new post.'
            }, status=401)

        try:

            if token:
                author_id = Token.objects.get(key=token).user.author.id
            else:
                author_id = request.user.author.id

            post = Post.objects.create(
                body=body,
                title=title,
                draft=draft,
                author_id=author_id,
                thumbnail=thumbnail,
                description=description
            )

            data = PostDetailSerializer(post).data

            return Response({
                'details': data
            }, status=201)

        except Exception as e:
            return Response({
                'error': str(e)
            }, status=500)
