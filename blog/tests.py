import json
import typing
import random

import faker

from django.test import TestCase
from django.utils.text import slugify

from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, APIClient

from blog.models import Post
from blog.management.commands._create_post import create_post
from author.management.commands._create_author import create_author
from blog.serializers import PostListSerializer, PostDetailSerializer
from blog.views import PostListAPIView, PostDetailAPIView, PostCreateAPIView


BASE_URL = '/api/blog'


class PostListAndDetailTest(TestCase):

    def setUp(self):

        # create factory and url
        self.url = BASE_URL
        self.factory = APIRequestFactory()

        # create fake authors and posts
        self.authors = [create_author() for _ in range(20)]
        self.posts: typing.List[Post] = [create_post(draft=False) for _ in range(50)]

    def test_post_list(self):
        """
        Compares paginated data against 5
        separate incremental (?page={1,2,3,4,5})
        response contents with self.posts
        """

        for page in range(1, 6):

            # make request to specific page
            request = self.factory.get(f'{self.url}/?page={page}')

            # get response and render it
            response = PostListAPIView.as_view()(request)
            response.render()

            # check ok status
            self.assertEqual(response.status_code, 200)

            # decode response and check serialized data
            content = json.loads(response.content.decode())
            posts = reversed(self.posts[-(page*10):50-(10*(page-1))])
            serialized_data = PostListSerializer(posts, many=True).data

            self.assertEqual(content['results'], serialized_data, msg=f'{page}')

    def test_post_details(self):

        # select random post
        post = random.choice(self.posts)

        # make request
        request = self.factory.get(f'{self.url}/detail/{post.slug}/')

        # get response and render it
        response = PostDetailAPIView.as_view()(request, slug=post.slug)
        response.render()

        # check ok status
        self.assertEqual(response.status_code, 200)

        # decode response and check serialized data
        content = json.loads(response.content.decode())
        serialized_data = PostDetailSerializer(post).data

        self.assertEqual(content, serialized_data)


class PostCreateTest(TestCase):

    def setUp(self):
        self.fake = faker.Faker()
        self.url = f'{BASE_URL}/new/'
        self.factory = APIRequestFactory()
        self.authors = [create_author() for _ in range(4)]
        self.data = {
            'draft': random.random() < 0.10,
            'description': self.fake.text(150),
            'title': self.fake.text(50).title()[:-1],
            'thumbnail': f'https://picsum.photos/1900/1080/?image=201',
            'body': '\n\n'.join([self.fake.sentence(170) for _ in range(random.randint(7, 10))]),
        }

    def test_create_post_header_token(self):

        author = random.choice(self.authors)
        token = Token.objects.get(user_id=author.user_id)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        response = client.post(self.url, self.data)

        # check status code
        self.assertEqual(response.status_code, 201)

        # get json data and check serialized data
        content = response.json()
        serialized_data = PostDetailSerializer(Post.objects.get(
            slug__exact=slugify(self.data['title'])
        )).data
        self.assertEqual(content['details'], serialized_data)

    def test_create_post_with_token(self):

        data = self.data.copy()
        author = random.choice(self.authors)
        data['token'] = Token.objects.get(user_id=author.user_id).key

        request = self.factory.post(self.url, data)

        response = PostCreateAPIView.as_view()(request)
        response.render()

        # check status code
        self.assertEqual(response.status_code, 201)

        # decode content and check serialized data
        content = json.loads(response.content.decode())
        serialized_data = PostDetailSerializer(Post.objects.get(
            slug__exact=slugify(self.data['title'])
        )).data
        self.assertEqual(content['details'], serialized_data)

    def test_create_post_without_authentication(self):

        request = self.factory.post(self.url, self.data)

        response = PostCreateAPIView.as_view()(request)
        response.render()

        # check status code
        self.assertEqual(response.status_code, 401)

        # decode content and check error message
        content = json.loads(response.content.decode())
        self.assertEqual(content, {'error': 'You need to be authenticated to create a new post.'})

    def test_create_post_incomplete_data_no_title(self):

        author = random.choice(self.authors)
        data = self.data.copy()
        data['token'] = Token.objects.get(user_id=author.user_id)
        del data['title']

        request = self.factory.post(self.url, data)

        response = PostCreateAPIView.as_view()(request)
        response.render()

        # check status code
        self.assertEqual(response.status_code, 400)

        # decode content and check error message
        content = json.loads(response.content.decode())
        self.assertEqual(content, {'error': "'title' field not provided."})

    def test_create_post_incomplete_data_no_body(self):

        author = random.choice(self.authors)
        data = self.data.copy()
        data['token'] = Token.objects.get(user_id=author.user_id)
        del data['body']

        request = self.factory.post(self.url, data)

        response = PostCreateAPIView.as_view()(request)
        response.render()

        # check status code
        self.assertEqual(response.status_code, 400)

        # decode content and check error message
        content = json.loads(response.content.decode())
        self.assertEqual(content, {'error': "'body' field not provided."})
