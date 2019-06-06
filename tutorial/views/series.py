from django.shortcuts import get_list_or_404

from rest_framework.generics import ListAPIView
from rest_framework.exceptions import APIException

from tutorial.models import Tutorial, Series
from tutorial.serializers import (
    SeriesListSerializer,
    TutorialListSerializer,
)


class SeriesListAPIView(ListAPIView):

    serializer_class = SeriesListSerializer
    queryset = Series.objects.all()


class SeriesTutorialsListAPIView(ListAPIView):
    """
    This view gets all the tutorials belonging
    to a particular series according to its slug.
    """

    serializer_class = TutorialListSerializer

    def get_queryset(self):

        series_slug = self.kwargs['slug']
        query = get_list_or_404(Tutorial, series__slug=series_slug)
        return query
