import json
import typing
import random

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from rest_framework.authtoken.models import Token
from rest_framework.test import (
    APIRequestFactory,
    force_authenticate,
)

from blog.models import Post
from author.models import Author
from tutorial.models import Tutorial, Series
from blog.serializers import PostListSerializer
from blog.management.commands._create_post import create_post
from author.management.commands.new_author import create_author
from tutorial.management.commands._create_series import create_one_series
from tutorial.management.commands._create_tutorial import create_tutorial
from tutorial.serializers import (
    SeriesListSerializer,
    TutorialListSerializer,
)
from author.serializers import (
    AuthorSerializer,
    AuthorListSerializer,
)
from author.views import (
    AuthorListAPIView,
    AuthorDetailAPIView,
    AuthorPostListAPIView,
    AuthorSeriesListAPIView,
    AuthorTutorialListAPIView,
    GetTokenAndAuthorDetailsAPIView
)


class AuthorListTest(TestCase):
    """
    Tests for listing for 50 authors' JSON serialized data
    against expected output by make admin authenticated,
    anonymous user, and simple user authenticated requests.
    """

    def setUp(self):
        # create request factory
        # and assign base url property
        self.url = '/api/authors/'
        self.factory = APIRequestFactory()

        # create admin user (and subsequently author)
        self.admin_user = User.objects.create_superuser('admin', 'admin@admin.com', 'aaaa')
        self.admin = Author.objects.create(
            authenticated=True,
            user=self.admin_user,
            bio='Admin of Ode2Code.',
        )

        # create 49 authors
        self.authors: typing.List[Author] = [create_author() for _ in range(49)]

    def test_authenticated_admin_request(self):
        """
        Makes an authenticated request to /api/authors/
        by manually setting request.user to an admin user.
        """

        request = self.factory.get(self.url)

        # forcing admin user to make authenticated request
        force_authenticate(request, self.admin_user)

        # make request and render response
        response = AuthorListAPIView.as_view()(request)
        response.render()

        # assert status code
        self.assertEqual(response.status_code, 200)

        # decode content and compare it against
        # self serialized AuthorListSerializer data
        content = response.content.decode()
        authors = Author.objects.all()
        serialized_data = AuthorListSerializer(authors, many=True).data

        self.assertEqual(json.loads(content), serialized_data)

    def test_authenticated_normal_user_request(self):
        """
        Makes an authenticated request to /api/authors/
        by manually setting request.user to a simple user.
        """

        request = self.factory.get(self.url)

        # forcing simple user to make authenticated request
        force_authenticate(request, random.choice(self.authors).user)

        # make request and render response
        response = AuthorListAPIView.as_view()(request)
        response.render()

        # assert status_code
        self.assertEqual(response.status_code, 403)

        # decode content and assert error message
        content = response.content.decode()
        self.assertEqual(content, '{"detail":"You do not have permission to perform this action."}')

    def test_unauthenticated_admin_request(self):
        """
        Makes an unauthenticated request to
        /api/authors/. Expects an unauthorized error.
        """
        request = self.factory.get(self.url)

        # make actual request and render response
        response = AuthorListAPIView.as_view()(request)
        response.render()

        # assert status code
        self.assertEqual(response.status_code, 401)

        # decode content and assert error message
        content = response.content.decode()
        self.assertEqual(content, '{"detail":"Authentication credentials were not provided."}')


class AuthorTokenAndDetailTest(TestCase):

    def setUp(self):
        # create request factory
        # and assign base url property
        self.url = '/api/authors'
        self.factory = RequestFactory()

        # create authors for testing
        self.authors = [create_author() for _ in range(5)]

    def test_author_details(self):
        """
        Makes an unauthenticated request to
        /api/authors/detail/<slug:username>/ to
        compare internal serialized data vs
        content from the view.
        """

        # random author to perform request against
        author = random.choice(self.authors)
        username = author.user.username

        request = self.factory.get(f'{self.url}/detail/{username}')

        # make request and render response
        response = AuthorDetailAPIView.as_view()(request, username=username)
        response.render()

        # check successful status_code
        self.assertEqual(response.status_code, 200)

        # decode content and get JSON
        # serialized data for random author
        content = response.content.decode()
        data = AuthorSerializer(author).data

        self.assertEqual(json.loads(content), data)

    def test_successful_custom_authentication_view(self):
        """
        Unit test for GetTokenAndAuthorDetailsAPIView
        that compares data when username and password
        are provided correctly.
        """

        author = random.choice(self.authors)
        password = 'aaa'
        username = author.user.username

        # create post request
        request = self.factory.post(f'{self.url}/auth/', {
            'password': password,
            'username': username,
        })

        # send post request and render response
        response = GetTokenAndAuthorDetailsAPIView.as_view()(request)
        response.render()

        # check successful status_code
        self.assertEqual(response.status_code, 200)

        # decode content and construct JSON
        # response with authtoken and author details
        content = response.content.decode()

        data = {
            'author': AuthorSerializer(author).data,
            'token': Token.objects.get(user_id__exact=author.user_id).key,
        }

        # check response and data
        self.assertEqual(json.loads(content), data)

    def test_unsuccessful_custom_authentication(self):
        """
        Same as test_successful_custom_authentication_view
        but instead of providing correct valid username &
        password combo to check 401 status code & error message.
        """

        author = random.choice(self.authors)
        password = 'incorrect_password'
        username = author.user.username

        # create post request with invalid data
        request = self.factory.post(f'{self.url}/auth/', {
            'password': password,
            'username': username,
        })

        # send post and render response
        response = GetTokenAndAuthorDetailsAPIView.as_view()(request)
        response.render()

        # check unsuccessful status_code
        self.assertEqual(response.status_code, 401)

        content = response.content.decode()

        expected_error_message = '{"error":"Invalid credentials."}'
        self.assertEqual(content, expected_error_message)

    def test_unsuccessful_incomplete_data_custom_authentication(self):
        """
        Tests GetTokenAndAuthorDetailsAPIView when POST
        data doesn't have either the username or password
        """

        # no author can be selected since view would
        # send an unsuccessful response either way.
        username = 'aaaa'
        password = 'aaaa'

        # create post request with password missing
        request_with_no_password = self.factory.post(f'{self.url}/auth/', {
            'username': username
        })

        # create post request with username missing
        request_with_no_username = self.factory.post(f'{self.url}/auth/', {
            'password': password
        })

        # send both requests and render responses

        view = GetTokenAndAuthorDetailsAPIView.as_view()

        response_with_password_error = view(request_with_no_password)
        response_with_username_error = view(request_with_no_username)

        # render responses
        response_with_password_error.render()
        response_with_username_error.render()

        # check unsuccessful status_codes
        self.assertEqual(response_with_password_error.status_code, 422)
        self.assertEqual(response_with_username_error.status_code, 422)

        # decode contents
        content_with_password_error = response_with_password_error.content.decode()
        content_with_username_error = response_with_username_error.content.decode()

        self.assertEqual(content_with_password_error, '{"error":"Password not provided."}')
        self.assertEqual(content_with_username_error, '{"error":"Username not provided."}')


class AuthorContentListingTest(TestCase):
    """
    Collection of tests that check functioning of
    the ListAPIView over the content that are related
    to specific Author instances as ForeignKeys.
    """

    @staticmethod
    def generate_fake_data_for_author(author_id: int) -> typing.Dict[str, typing.List[typing.Any]]:
        return {
            'posts': [create_post(author_id) for _ in range(20)],
            'series': [create_one_series(author_id) for _ in range(20)],
            'tutorials': [create_tutorial(author_id) for _ in range(20)],
        }

    def generate_author_content_url(self, username: str, model_type: str, page: int = 1) -> str:
        return f'{self.url}/{username}/{model_type}/?page={page}'

    def setUp(self):
        """
        creates an author and multiple posts,
        tutorials, as well as series created
        by the above mentioned author.
        """

        # create factory and set base url
        self.factory = RequestFactory()
        self.url = '/api/authors/detail'

        # create first author
        self.author_1 = create_author()
        self.author_2 = create_author()

        # generate posts, series, and tutorials
        self.author_1_content = self.generate_fake_data_for_author(self.author_1.id)
        self.author_2_content = self.generate_fake_data_for_author(self.author_2.id)

    def test_author_posts(self):
        """
        Compares list of author post against
        JSON response of AuthorTutorialListAPIView
        in proper format - JSON data.
        """

        # get pages 1 and 2 - due to page 
        # number based pagination with a limit
        # of 10 objects per page, we need to
        # make 2 requests to get all the
        # content in any view that uses ListAPIView
        # TODO make a more generic method to get paginated data

        username_1, username_2 = self.author_1.user.username, self.author_2.user.username

        # request page 1 & 2 for author 1
        request_author_1_page_1 = self.factory.get(self.generate_author_content_url(username_1, 'posts'))
        request_author_1_page_2 = self.factory.get(self.generate_author_content_url(username_1, 'posts', 2))

        # request page 1 & 2 for author 2
        request_author_2_page_1 = self.factory.get(self.generate_author_content_url(username_2, 'posts'))
        request_author_2_page_2 = self.factory.get(self.generate_author_content_url(username_2, 'posts', 2))

        # get responses for requests

        response_author_1_page_1 = AuthorPostListAPIView.as_view()(request_author_1_page_1, username=username_1)
        response_author_1_page_2 = AuthorPostListAPIView.as_view()(request_author_1_page_2, username=username_1)
        response_author_1_page_1.render()
        response_author_1_page_2.render()

        response_author_2_page_1 = AuthorPostListAPIView.as_view()(request_author_2_page_1, username=username_2)
        response_author_2_page_2 = AuthorPostListAPIView.as_view()(request_author_2_page_2, username=username_2)
        response_author_2_page_1.render()
        response_author_2_page_2.render()

        # decode contents
        author_1_post_list_page_1 = json.loads(response_author_1_page_1.content.decode())
        author_1_post_list_page_2 = json.loads(response_author_1_page_2.content.decode())

        author_2_post_list_page_1 = json.loads(response_author_2_page_1.content.decode())
        author_2_post_list_page_2 = json.loads(response_author_2_page_2.content.decode())

        # perform actual test

        # check OK responses
        self.assertEqual(response_author_1_page_1.status_code, 200)
        self.assertEqual(response_author_1_page_2.status_code, 200)

        self.assertEqual(response_author_2_page_1.status_code, 200)
        self.assertEqual(response_author_2_page_2.status_code, 200)

        # check content

        # get serialized values

        author_1_post_list_page_1_serialized_data = PostListSerializer(
            Post.objects.filter(author=self.author_1)[:10],
            many=True
        ).data

        author_1_post_list_page_2_serialized_data = PostListSerializer(
            Post.objects.filter(author=self.author_1)[10:],
            many=True
        ).data

        author_2_post_list_page_1_serialized_data = PostListSerializer(
            Post.objects.filter(author=self.author_2)[:10],
            many=True
        ).data

        author_2_post_list_page_2_serialized_data = PostListSerializer(
            Post.objects.filter(author=self.author_2)[10:],
            many=True
        ).data

        # check consistent count
        self.assertEqual(author_1_post_list_page_1['count'], 20)
        self.assertEqual(author_1_post_list_page_2['count'], 20)

        self.assertEqual(author_2_post_list_page_1['count'], 20)
        self.assertEqual(author_2_post_list_page_2['count'], 20)

        # check actual JSON content
        self.assertEqual(author_1_post_list_page_1['results'], author_1_post_list_page_1_serialized_data, '1st')
        self.assertEqual(author_1_post_list_page_2['results'], author_1_post_list_page_2_serialized_data, '2nd')

        self.assertEqual(author_2_post_list_page_1['results'], author_2_post_list_page_1_serialized_data, '3rd')
        self.assertEqual(author_2_post_list_page_2['results'], author_2_post_list_page_2_serialized_data, '4th')

    def test_author_series(self):
        """
        Compares list of author series against
        JSON response of AuthorSeriesListAPIView
        in proper format - JSON data.
        """

        username_1, username_2 = self.author_1.user.username, self.author_2.user.username

        # request page 1 & 2 for author 1
        request_author_1_page_1 = self.factory.get(self.generate_author_content_url(username_1, 'series'))
        request_author_1_page_2 = self.factory.get(self.generate_author_content_url(username_1, 'series', 2))

        # request page 1 & 2 for author 2
        request_author_2_page_1 = self.factory.get(self.generate_author_content_url(username_2, 'series'))
        request_author_2_page_2 = self.factory.get(self.generate_author_content_url(username_2, 'series', 2))

        # get responses for requests

        response_author_1_page_1 = AuthorSeriesListAPIView.as_view()(request_author_1_page_1, username=username_1)
        response_author_1_page_2 = AuthorSeriesListAPIView.as_view()(request_author_1_page_2, username=username_1)
        response_author_1_page_1.render()
        response_author_1_page_2.render()

        response_author_2_page_1 = AuthorSeriesListAPIView.as_view()(request_author_2_page_1, username=username_2)
        response_author_2_page_2 = AuthorSeriesListAPIView.as_view()(request_author_2_page_2, username=username_2)
        response_author_2_page_1.render()
        response_author_2_page_2.render()

        # decode contents
        author_1_series_list_page_2 = json.loads(response_author_1_page_2.content.decode())
        author_1_series_list_page_1 = json.loads(response_author_1_page_1.content.decode())

        author_2_series_list_page_1 = json.loads(response_author_2_page_1.content.decode())
        author_2_series_list_page_2 = json.loads(response_author_2_page_2.content.decode())

        # perform actual test

        # check OK responses
        self.assertEqual(response_author_1_page_1.status_code, 200)
        self.assertEqual(response_author_1_page_2.status_code, 200)

        self.assertEqual(response_author_2_page_1.status_code, 200)
        self.assertEqual(response_author_2_page_2.status_code, 200)

        # check content

        # get serialized values

        author_1_series_list_page_1_serialized_data = SeriesListSerializer(
            Series.objects.filter(creator=self.author_1)[:10],
            many=True
        ).data

        author_1_series_list_page_2_serialized_data = SeriesListSerializer(
            Series.objects.filter(creator=self.author_1)[10:],
            many=True
        ).data

        author_2_series_list_page_1_serialized_data = SeriesListSerializer(
            Series.objects.filter(creator=self.author_2)[:10],
            many=True
        ).data

        author_2_series_list_page_2_serialized_data = SeriesListSerializer(
            Series.objects.filter(creator=self.author_2)[10:],
            many=True
        ).data

        # check consistent count
        self.assertEqual(author_1_series_list_page_1['count'], 20)
        self.assertEqual(author_1_series_list_page_2['count'], 20)

        self.assertEqual(author_2_series_list_page_1['count'], 20)
        self.assertEqual(author_2_series_list_page_2['count'], 20)

        # check actual JSON content
        self.assertEqual(author_1_series_list_page_1['results'], author_1_series_list_page_1_serialized_data)
        self.assertEqual(author_1_series_list_page_2['results'], author_1_series_list_page_2_serialized_data)

        self.assertEqual(author_2_series_list_page_1['results'], author_2_series_list_page_1_serialized_data)
        self.assertEqual(author_2_series_list_page_2['results'], author_2_series_list_page_2_serialized_data)

    def test_author_tutorials(self):
        """
        Compares list of author tutorials against
        JSON response of AuthorTutorialListAPIView
        in proper format - JSON data.
        """

        username_1, username_2 = self.author_1.user.username, self.author_2.user.username

        # request page 1 & 2 for author 1
        request_author_1_page_1 = self.factory.get(self.generate_author_content_url(username_1, 'tutorials'))
        request_author_1_page_2 = self.factory.get(self.generate_author_content_url(username_1, 'tutorials', 2))

        # request page 1 & 2 for author 2
        request_author_2_page_1 = self.factory.get(self.generate_author_content_url(username_2, 'tutorials'))
        request_author_2_page_2 = self.factory.get(self.generate_author_content_url(username_2, 'tutorials', 2))

        # get responses for requests

        response_author_1_page_1 = AuthorTutorialListAPIView.as_view()(request_author_1_page_1, username=username_1)
        response_author_1_page_2 = AuthorTutorialListAPIView.as_view()(request_author_1_page_2, username=username_1)
        response_author_1_page_1.render()
        response_author_1_page_2.render()

        response_author_2_page_1 = AuthorTutorialListAPIView.as_view()(request_author_2_page_1, username=username_2)
        response_author_2_page_2 = AuthorTutorialListAPIView.as_view()(request_author_2_page_2, username=username_2)
        response_author_2_page_1.render()
        response_author_2_page_2.render()

        # decode contents
        author_1_tutorial_list_page_1 = json.loads(response_author_1_page_1.content.decode())
        author_1_tutorial_list_page_2 = json.loads(response_author_1_page_2.content.decode())

        author_2_tutorial_list_page_1 = json.loads(response_author_2_page_1.content.decode())
        author_2_tutorial_list_page_2 = json.loads(response_author_2_page_2.content.decode())

        # perform actual test

        # check OK responses
        self.assertEqual(response_author_1_page_1.status_code, 200)
        self.assertEqual(response_author_1_page_2.status_code, 200)

        self.assertEqual(response_author_2_page_1.status_code, 200)
        self.assertEqual(response_author_2_page_2.status_code, 200)

        # check content

        # get serialized values

        author_1_tutorial_list_page_1_serialized_data = TutorialListSerializer(
            Tutorial.objects.filter(author=self.author_1)[:10],
            many=True
        ).data

        author_1_tutorial_list_page_2_serialized_data = TutorialListSerializer(
            Tutorial.objects.filter(author=self.author_1)[10:],
            many=True
        ).data

        author_2_tutorial_list_page_1_serialized_data = TutorialListSerializer(
            Tutorial.objects.filter(author=self.author_2)[:10],
            many=True
        ).data

        author_2_tutorial_list_page_2_serialized_data = TutorialListSerializer(
            Tutorial.objects.filter(author=self.author_2)[10:],
            many=True
        ).data

        # check consistent count
        self.assertEqual(author_1_tutorial_list_page_1['count'], 20)
        self.assertEqual(author_1_tutorial_list_page_2['count'], 20)

        self.assertEqual(author_2_tutorial_list_page_1['count'], 20)
        self.assertEqual(author_2_tutorial_list_page_2['count'], 20)

        # check actual JSON content
        self.assertEqual(author_1_tutorial_list_page_1['results'], author_1_tutorial_list_page_1_serialized_data)
        self.assertEqual(author_1_tutorial_list_page_2['results'], author_1_tutorial_list_page_2_serialized_data)

        self.assertEqual(author_2_tutorial_list_page_1['results'], author_2_tutorial_list_page_1_serialized_data)
        self.assertEqual(author_2_tutorial_list_page_2['results'], author_2_tutorial_list_page_2_serialized_data)
