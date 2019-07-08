import json
import typing
import random

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from author.models import Author
from author.serializers import AuthorListSerializer
from author.management.commands._create_author import create_author
from author.views import (
    AuthorListAPIView
)


class AuthorListTest(TestCase):
    """
    Tests for listing for 50 authors' JSON serialized data
    against expected output by make admin authenticated,
    anonymous user, and simple user authenticated requests.
    """

    def setUp(self):
        # create request factory
        # and assign base url variable
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
