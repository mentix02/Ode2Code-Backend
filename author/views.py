from django.contrib.auth import authenticate
from django.shortcuts import get_list_or_404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.authtoken.models import Token
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.generics import ListAPIView, RetrieveAPIView

from blog.models import Post
from author.models import Author
from tutorial.models import Tutorial, Series
from blog.serializers import PostListSerializer
from author.serializers import (
    AuthorSerializer,
    AuthorListSerializer
)
from tutorial.serializers import (
    SeriesListSerializer,
    TutorialListSerializer
)


UP, DOWN = 1, 0


class GetTokenAndAuthorDetailsAPIView(APIView):

    @staticmethod
    def post(request):

        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username:
            return Response({
                'error': 'Username not provided.'
            }, status=422)
        elif not password:
            return Response({
                'error': 'Password not provided.'
            }, status=422)

        user = authenticate(username=username, password=password)

        if user is not None:
            author = AuthorSerializer(user.author).data
            token = Token.objects.get(user_id__exact=user.id).key
            return Response({
                'token': token,
                'author': author
            })
        else:
            return Response({
                'error': 'Invalid credentials.'
            }, status=401)


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


class AuthorLikedTutorialIdsAPIView(APIView):
    """
    Returns a list of ids of tutorials liked by the user.
    Required an authtoken to verify only the user can view
    his / her liked tutorials. No justification found yet.
    """

    parser_classes = (FormParser, MultiPartParser)

    @staticmethod
    def post(request):

        token = request.POST.get('token')

        if not token and not request.user.is_authenticated:
            return Response({
                'error': 'Unauthorized to view response.'
            }, status=401)

        try:

            if token:
                user_id = Token.objects.get(key=token).user_id
            else:
                user_id = request.user.id

            tutorials = Tutorial.votes.all(user_id)

            return Response([
                tutorial.pk for tutorial in tutorials
            ])

        except ObjectDoesNotExist:
            return Response({
                'error': 'Invalid auth token provided.'
            }, status=401)
