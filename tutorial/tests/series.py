import json
import random
import typing

from django.test import TestCase

from rest_framework.test import APIRequestFactory

from author.models import Author
from tutorial.models import Series, Tutorial
from tutorial.serializers.tutorials import TutorialListSerializer
from author.management.commands._create_author import create_author
from tutorial.management.commands._create_series import create_one_series
from tutorial.management.commands._create_tutorial import create_tutorial
from tutorial.views.series import (
    SeriesListAPIView,
    SeriesDetailAPIView,
    SeriesTutorialsListAPIView,
)
from tutorial.serializers.series import (
    SeriesListSerializer,
    SeriesDetailSerializer,
)

BASE_URL = '/api/series'


class SeriesListTest(TestCase):

    def setUp(self):
        self.url = f'{BASE_URL}'
        self.factory = APIRequestFactory()
        self.authors: typing.List[Author] = [create_author() for _ in range(10)]
        self.series: typing.List[Series] = [create_one_series() for _ in range(50)]
        self.tutorials: typing.List[Tutorial] = [create_tutorial() for _ in range(250)]

    def test_series_list(self):

        for page in range(1, 6):

            # make request to specific page
            request = self.factory.get(f'{self.url}/?page={page}')

            # get response and render it
            response = SeriesListAPIView.as_view()(request)
            response.render()

            # check status
            self.assertEqual(response.status_code, 200)

            # decode content and check serialized data
            data = json.loads(response.content.decode())
            series = self.series[-(page*10):50-(10*(page-1))]
            serialized_data = reversed(SeriesListSerializer(series, many=True).data)

            self.assertEqual(data['results'], list(serialized_data), msg=f'\n{[i.id for i in series]}\n{[i["id"] for i in data["results"]]}')

    def test_series_tutorial_list(self):

        for series in self.series:

            # make request for series details - tutorial list page
            request = self.factory.get(f'{self.url}/detail/{series.slug}/tutorials/')

            # get response and render it
            response = SeriesTutorialsListAPIView.as_view()(request, slug=series.slug)
            response.render()

            # check status
            self.assertEqual(response.status_code, 200)

            # decode content and check serialized for tutorials filtered by list comprehensions
            data = json.loads(response.content.decode())

            tutorials = []
            for tutorial in self.tutorials:
                if tutorial.series_id == series.id and tutorial.draft == False:
                    tutorials.append(tutorial)

            serialized_data = TutorialListSerializer(reversed(tutorials), many=True).data

            self.assertEqual(data['results'], serialized_data)


class SeriesDetailTest(TestCase):

    def setUp(self):
        self.url = f'{BASE_URL}/detail'
        self.factory = APIRequestFactory()
        self.authors = create_author(), create_author()
        self.series: typing.Tuple[Series, Series] = (create_one_series(), create_one_series())

    def test_series_detail_0(self):
        series = self.series[0]

        request = self.factory.get(f'{self.url}/{series.slug}/')

        response = SeriesDetailAPIView.as_view()(request, slug=series.slug)
        response.render()

        # check status code
        self.assertEqual(response.status_code, 200)

        # check content against serialized data
        data = json.loads(response.content.decode())
        serialized_data = SeriesDetailSerializer(series).data
        self.assertEqual(data, serialized_data)

    def test_series_detail_1(self):
        series = self.series[1]

        request = self.factory.get(f'{self.url}/{series.slug}/')

        response = SeriesDetailAPIView.as_view()(request, slug=series.slug)
        response.render()

        # check status code
        self.assertEqual(response.status_code, 200)

        # check content against serialized data
        data = json.loads(response.content.decode())
        serialized_data = SeriesDetailSerializer(series).data
        self.assertEqual(data, serialized_data)
