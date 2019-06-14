from rest_framework.serializers import (
    URLField,
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
    thumbnail = URLField(source='get_series_thumbnail')

    class Meta:

        model = Tutorial
        fields = ('id', 'thumbnail', 'timestamp', 'title', 'series', 'author', 'slug', 'description', 'draft')


class TutorialDetailSerializer(ModelSerializer):

    author = AuthorSerializer()
    series = StringRelatedField()
    timestamp = DateTimeField(format='%dth %b, %Y')
    thumbnail = URLField(source='get_series_thumbnail')

    class Meta:

        model = Tutorial
        fields = '__all__'
