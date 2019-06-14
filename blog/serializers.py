from rest_framework.serializers import (
    DateTimeField,
    ModelSerializer,
    StringRelatedField,
)

from blog.models import Post
from author.serializers import AuthorSerializer


class PostListSerializer(ModelSerializer):

    author = StringRelatedField()
    timestamp = DateTimeField(format='%dth %b, %Y')

    class Meta:

        model = Post
        fields = ('id', 'title', 'slug', 'description', 'timestamp', 'thumbnail', 'author', 'num_vote_up',
                  'num_vote_down')


class PostDetailSerializer(ModelSerializer):

    author = AuthorSerializer()
    timestamp = DateTimeField(format='%dth %b, %Y')

    class Meta:

        model = Post
        fields = '__all__'
