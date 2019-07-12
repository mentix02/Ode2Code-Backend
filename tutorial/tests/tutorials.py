import json
import random

import faker

from django.test import TestCase
from django.utils.text import slugify

from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, APIClient

from tutorial.models import Tutorial
from author.management.commands._create_author import create_author
from tutorial.management.commands._create_series import create_one_series
from tutorial.management.commands._create_tutorial import create_tutorial
from tutorial.views.tutorials import (
    RecentTutorialAPIView,
    TutorialDetailAPIView,
    TutorialCreateAPIView,
)
from tutorial.serializers.tutorials import (
    TutorialListSerializer,
    TutorialDetailSerializer,
)


BASE_URL = '/api/tutorials'


class TutorialListAndDetailTest(TestCase):

    def setUp(self):

        self.url = BASE_URL
        self.factory = APIRequestFactory()

        self.authors = [create_author() for _ in range(5)]
        self.series = [create_one_series() for _ in range(10)]
        self.tutorials = [create_tutorial(draft=False) for _ in range(130)]

    def test_recent_tutorial_list(self):

        request = self.factory.get(f'{self.url}/recent/')

        # get response and render content
        response = RecentTutorialAPIView.as_view()(request)
        response.render()

        # check status code
        self.assertEqual(response.status_code, 200)

        # decode data and get serialized data
        data = json.loads(response.content.decode())
        serialized_data = TutorialListSerializer(
            reversed(self.tutorials[-12:]), many=True
        ).data

        # check data count
        self.assertEqual(data['count'], 12)

        # check results with data
        self.assertEqual(data['results'], serialized_data)

    def test_tutorial_detail(self):

        tutorial = random.choice(self.tutorials)

        # construct url and make request
        request = self.factory.get(f'{self.url}/detail/{tutorial.slug}/')

        # get response and render content
        response = TutorialDetailAPIView.as_view()(request, slug=tutorial.slug)
        response.render()

        # check status code
        self.assertEqual(response.status_code, 200)

        # decode data and get serialized data
        data = json.loads(response.content.decode())
        serialized_data = TutorialDetailSerializer(tutorial).data
        self.assertEqual(data, serialized_data)


class TutorialCreateTest(TestCase):

    def setUp(self):
        self.fake = faker.Faker()
        self.url = f'{BASE_URL}/new/'
        self.factory = APIRequestFactory()
        self.authors = [create_author() for _ in range(4)]
        self.series = [create_one_series() for _ in range(12)]
        self.data = {
            'draft': random.random() < 0.10,
            'description': self.fake.text(150),
            'title': self.fake.text(50).title()[:-1],
            'content': '\n\n'.join([self.fake.sentence(170) for _ in range(random.randint(7, 10))]),
        }

    def test_create_tutorial_header_token(self):

        # generate fake data
        data = self.data.copy()
        if random.random() >= 0.15:
            data['series_id'] = random.choice(self.series).id
        author = random.choice(self.authors)
        token = Token.objects.get(user_id=author.user_id)

        # initialize client
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        # get response
        response = client.post(self.url, data)

        # check status code
        self.assertEqual(response.status_code, 201)

        # get json data and check serialized data
        content = response.json()
        serialized_data = TutorialDetailSerializer(Tutorial.objects.get(
            slug__exact=slugify(self.data['title'])
        )).data
        self.assertEqual(content['details'], serialized_data)

    def test_create_post_with_token(self):

        data = self.data.copy()

        author = random.choice(self.authors)
        if random.random() >= 0.15:
            data['series_id'] = random.choice(self.series).id
        data['token'] = Token.objects.get(user_id=author.user_id).key

        request = self.factory.post(self.url, data)

        response = TutorialCreateAPIView.as_view()(request)
        response.render()

        # check status code
        self.assertEqual(response.status_code, 201)

        # decode content and check serialized data
        content = json.loads(response.content.decode())
        serialized_data = TutorialDetailSerializer(Tutorial.objects.get(
            slug__exact=slugify(self.data['title'])
        )).data
        self.assertEqual(content['details'], serialized_data)
