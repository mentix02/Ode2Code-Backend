from rest_framework.serializers import (
    DateTimeField,
    ModelSerializer,
    StringRelatedField
)

from tutorial.models import Tutorial
from author.serializers import AuthorSerializer


class TutorialListSerializer(ModelSerializer):

    series = StringRelatedField()
    author = StringRelatedField()
    timestamp = DateTimeField(format='%dth %b, %Y')

    class Meta:

        model = Tutorial
        fields = ('id', 'timestamp', 'title', 'series', 'author', 'slug', 'description', 'draft')


class TutorialDetailSerializer(ModelSerializer):

    author = AuthorSerializer()
    series = StringRelatedField()
    timestamp = DateTimeField(format='%dth %b, %Y')

    class Meta:

        model = Tutorial
        fields = '__all__'
