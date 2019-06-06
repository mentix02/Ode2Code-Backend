from django.contrib.auth.models import User

from rest_framework.serializers import (
    DateTimeField,
    ModelSerializer,
    StringRelatedField,
)

from author.models import Author


class UserDetailSerializer(ModelSerializer):

    date_joined = DateTimeField(format='%dth %b, %Y')

    class Meta:

        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'date_joined')


class AuthorSerializer(ModelSerializer):

    user = UserDetailSerializer()

    class Meta:

        model = Author
        fields = ('user', 'bio', 'authenticated')


class AuthorListSerializer(ModelSerializer):

    user = StringRelatedField()

    class Meta:

        model = Author
        fields = ('user', 'bio', 'authenticated')
