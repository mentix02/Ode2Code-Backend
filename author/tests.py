import json
import typing
import random

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from rest_framework.authtoken.models import Token

from author.models import Author
from author.serializers import (
    AuthorSerializer,
    AuthorListSerializer,
)
# noinspection PyProtectedMember
from author.management.commands._create_author import create_author
from author.views import (
    AuthorListAPIView,
    AuthorDetailAPIView,
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
        self.factory = RequestFactory()

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

        # setting admin user to make authenticated request
        request.user = self.admin_user

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

        # setting simple user to make authenticated request
        request.user = self.authors[random.randint(0, 48)].user

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
