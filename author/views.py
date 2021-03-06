from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.authtoken.models import Token
from rest_framework.views import APIView, Response
from drf_multiple_model.views import FlatMultipleModelAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination

from blog.models import Post
from author.models import Author, Bookmark
from author.permissions import IsSuperUser
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


class AuthenticateAuthorView(APIView):
    """
    Gets an Author from the secret key
    provided in the url to authenticate user.
    """

    @staticmethod
    def get(request, uuid):
        author = get_object_or_404(Author, secret_key__exact=uuid)
        author.authenticate()
        return Response({
            'authenticated': True
        })


class GetTokenAndAuthorDetailsAPIView(APIView):
    """
    Takes in a POST request with form data
    containing username and password and if
    valid, returns a JSON response containing
    authtoken and Author details (to be saved
    in localStorage on frontend).
    """

    @staticmethod
    def post(request):

        # get username and password
        username = request.POST.get('username')
        password = request.POST.get('password')

        # check if both were provided
        if not username:
            return Response({
                'error': 'Username not provided.'
            }, status=422)
        elif not password:
            return Response({
                'error': 'Password not provided.'
            }, status=422)

        user = authenticate(username=username, password=password)

        # if username & password combo succeeds
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
    """
    Purely for administrative purposes.
    Only admin is allowed to view list
    of registered authors and details.
    """
    queryset = Author.objects.all()

    # permission_classes to contain only
    # admin viewing rights was a conscious
    # decision that lets only me to view
    # the number of authors (and their
    # details) for analytical purposes, etc.
    permission_classes = (IsSuperUser,)

    # no pagination is applied since
    # this is not a frequently called
    # view and this data will mostly
    # be used for purposes that aren't
    # meant for the common user and also
    # no pagination makes TestCase asserting
    # response content a lot more easy.
    pagination_class = None

    serializer_class = AuthorListSerializer


class AuthorDetailAPIView(RetrieveAPIView):
    lookup_url_kwarg = 'username'
    lookup_field = 'user__username'
    queryset = Author.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AuthorSerializer


class AuthorPostListAPIView(ListAPIView):
    """
    This view gets the list of posts by the author username
    provided in the url as a slug - '<slug:username>/author/'
    """

    serializer_class = PostListSerializer

    def get_queryset(self):

        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        queryset = Post.objects.filter(author__user=user)
        return queryset


class AuthorTutorialListAPIView(ListAPIView):
    """
    This view gets the list of tutorials by the author username
    provided in the url as a slug - '<slug:username>/tutorials/'
    """

    serializer_class = TutorialListSerializer

    def get_queryset(self):

        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        queryset = Tutorial.objects.filter(author__user=user)
        return queryset


class AuthorSeriesListAPIView(ListAPIView):
    """
    Same as AuthorTutorialListAPIView but for tutorial.Series.
    """

    serializer_class = SeriesListSerializer

    def get_queryset(self):

        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        queryset = Series.objects.filter(creator__user=user)
        return queryset


class AuthorLikedTutorialIdsAPIView(APIView):
    """
    Returns a list of ids of tutorials liked by the user.
    Required an authtoken to verify only the user can view
    his / her liked tutorials. No justification found yet.
    """

    parser_classes = (FormParser, MultiPartParser)

    @staticmethod
    def get(request):

        if request.user.is_authenticated:
            user_id = request.user.id
            tutorials = Tutorial.votes.all(user_id)
            return Response([
                tutorial.pk for tutorial in tutorials
            ])
        else:
            return Response({
                'error': 'Unauthorized to view response.'
            }, status=401)

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

            return Response({
                'count': len(tutorials),
                'results': [tutorial.pk for tutorial in tutorials]
            })

        except ObjectDoesNotExist:
            return Response({
                'error': 'Invalid auth token provided.'
            }, status=401)


class AuthorBookmarkedSeriesIdsAPIView(APIView):
    """
    Returns a list of ids of series bookmarked by the user.
    Required an authtoken to verify only the user can view
    his / her liked tutorials.
    """

    parser_classes = (FormParser, MultiPartParser)

    @staticmethod
    def get(request):

        if request.user.is_authenticated:
            user = request.user
            series = Bookmark.objects.filter(author_id=user.author.id, model_type='series')
            return Response([
                s.model_pk for s in series
            ])
        else:
            return Response({
                'error': 'Unauthorized to view response.'
            }, status=401)

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

            series = Bookmark.objects.filter(author__user_id=user_id, model_type='series')

            return Response({
                'count': len(series),
                'results': [s.id for s in series]
            })

        except ObjectDoesNotExist:
            return Response({
                'error': 'Invalid auth token provided.'
            }, status=401)


class AuthorContentAPIView(FlatMultipleModelAPIView):
    sorting_field = '-timestamp'
    permission_classes = (IsAuthenticated,)
    pagination_class = MultipleModelLimitOffsetPagination

    def get_querylist(self):
        return [
            {
                'serializer_class': PostListSerializer,
                'queryset': Post.objects.filter(author__user=self.request.user),
            },
            {
                'serializer_class': TutorialListSerializer,
                'queryset': Tutorial.objects.filter(author__user=self.request.user),
            },
            {
                'serializer_class': SeriesListSerializer,
                'queryset': Series.objects.filter(creator__user=self.request.user),
            }
        ]
