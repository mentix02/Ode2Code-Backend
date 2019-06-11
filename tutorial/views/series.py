from django.shortcuts import get_list_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)

from tutorial.models import Tutorial, Series
from tutorial.serializers import (
    SeriesListSerializer,
    SeriesDetailSerializer,
    TutorialListSerializer,
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
        query = get_list_or_404(Tutorial, series__slug=series_slug)
        return query
