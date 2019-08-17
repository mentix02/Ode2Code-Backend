from django.utils.text import slugify
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.generics import (
    ListAPIView,
    DestroyAPIView,
    RetrieveAPIView,
)

from tutorial.views.utils import bookmark_exists
from author.models import Bookmark
from tutorial.models import Tutorial, Series
from tutorial.serializers import (
    SeriesListSerializer,
    SeriesDetailSerializer,
    TutorialListSerializer,
    SeriesNameAndIdSerializer,
)


class SeriesDetailAPIView(RetrieveAPIView):

    @method_decorator(cache_page(60 * 60 * 12, key_prefix='SeriesDetailAPIView'))
    def dispatch(self, *args, **kwargs):
        return super(SeriesDetailAPIView, self).dispatch(*args, **kwargs)

    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    queryset = Series.objects.all()
    serializer_class = SeriesDetailSerializer


class SeriesListAPIView(ListAPIView):

    @method_decorator(cache_page(60 * 5, key_prefix='SeriesListAPIView'))
    def dispatch(self, *args, **kwargs):
        return super(SeriesListAPIView, self).dispatch(*args, **kwargs)

    serializer_class = SeriesListSerializer
    queryset = Series.objects.all()


class SeriesTutorialsListAPIView(ListAPIView):
    """
    This view gets all the tutorials belonging
    to a particular series according to its slug.
    """

    @method_decorator(cache_page(60 * 5, key_prefix='SeriesTutorialsListAPIView'))
    def dispatch(self, *args, **kwargs):
        return super(SeriesTutorialsListAPIView, self).dispatch(*args, **kwargs)

    serializer_class = TutorialListSerializer

    def get_queryset(self):

        series_slug = self.kwargs['slug']
        series = get_object_or_404(Series, slug=series_slug)
        query = Tutorial.objects.filter(series=series, draft=False)
        return query


class SeriesCreateAPIView(APIView):
    """
    Creates a new series if POST request
    is authenticated with proper token or
    session authentication.

    Requires form data =>
        token?: uuid
        name!: short string
        type_of!: short string
        thumbnail: string (url)
        description!: long string

    Returns JSON => {
        "details": {
            "id": id,
            "name": name,
            "slug": slug,
            "type_of": type_of,
            "tutorial_count": 0,
            "description": description,
            "creator": author__user__username,
        }
    }

    """

    parser_classes = (FormParser, MultiPartParser)

    @staticmethod
    def post(request):

        # get required parameters
        try:
            name = request.POST['name']
            type_of = request.POST['type_of']
            description = request.POST['description']
            thumbnail = request.POST.get('thumbnail', None)
        except Exception as e:
            return Response({
                'error': f'{str(e)} field not provided.'
            }, status=405)

        token = request.POST.get('token')

        if not token and not request.user.is_authenticated:
            return Response({
                'error': 'You need to be authenticated to create a new series.'
            }, status=405)

        try:

            if token:
                creator_id = Token.objects.get(key=token).user.author.id
            else:
                creator_id = request.user.author.id

            series = Series.objects.create(
                name=name,
                type_of=type_of,
                thumbnail=thumbnail,
                creator_id=creator_id,
                description=description,
            )

            data = SeriesDetailSerializer(series).data
            return Response({
                'details': data
            })

        except Exception as e:
            return Response({
                'error': str(e)
            }, status=500)


class SeriesBookmarkAPIView(APIView):
    """
    Bookmarks a Series by an authenticated user if
    existing bookmarks are not found for the object
    """

    parser_classes = (FormParser, MultiPartParser)

    @staticmethod
    def get(request):
        return Response({
            'error': 'Method "GET" not allowed. Provide a token and a series id number.'
        }, status=405)

    @staticmethod
    def post(request):

        token = request.POST.get('token')
        series_id = request.POST.get('series_id')

        if not token:
            return Response({
                'error': 'Unauthorized to view response.'
            }, status=401)

        if not series_id:
            return Response({
                'error': 'Tutorial id not provided.'
            }, status=401)

        try:

            series = Series.objects.get(id=series_id)
            author_id = Token.objects.get(key=token).user.author.id

            if bookmark_exists(author_id, series.id):
                Bookmark.objects.get(model_pk=series_id,
                                     author_id=author_id,
                                     model_type='series').delete()
                return Response({
                    'action': -1
                })
            else:
                Bookmark.objects.create(
                    author_id=author_id,
                    model_type='series',
                    model_pk=series_id
                ).save()
                return Response({
                    'action': 1
                })

        except ObjectDoesNotExist:
            return Response({
                'error': 'Invalid auth token provided or tutorial does not exist.'
            }, status=401)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=500)


class SeriesAvailabilityAPIView(APIView):
    """
    Takes a name from POST request data
    and checks if a Series with the slug
    for that name exists - returns True
    if it does not and False for otherwise.
    """

    @staticmethod
    def post(request):
        name = request.POST.get('name')

        if not name:
            return Response({
                'error': 'Please provide a name for series to check if it\'s taken.'
            })

        if name:

            available = False

            try:
                series = Series.objects.get(slug=slugify(name))
            except ObjectDoesNotExist:
                available = True
            finally:
                return Response({
                    'available': available
                })


class SeriesTypeListAPIView(ListAPIView):

    serializer_class = SeriesListSerializer

    def get_queryset(self):
        type_of_slug = self.kwargs['slug']
        series = Series.objects.filter(type_of=type_of_slug)
        return series


class SeriesNameAndIdListAPIView(APIView):

    renderer_classes = (JSONRenderer,)

    @method_decorator(cache_page(60 * 5, key_prefix='SeriesNameList'))
    def dispatch(self, *args, **kwargs):
        return super(SeriesNameAndIdListAPIView, self).dispatch(*args, **kwargs)

    @staticmethod
    def get(request):
        series = Series.objects.all()
        data = SeriesNameAndIdSerializer(series, many=True).data
        return Response(data)


class SeriesDeleteAPIView(DestroyAPIView):
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    serializer_class = SeriesListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Series.objects.filter(creator__user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'deleted': True}, status=204)
