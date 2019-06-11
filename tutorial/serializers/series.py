from tutorial.models import Series

from rest_framework.serializers import (
    IntegerField,
    DateTimeField,
    ModelSerializer,
    StringRelatedField,
    HyperlinkedIdentityField,
)


class SeriesListSerializer(ModelSerializer):

    creator = StringRelatedField()
    timestamp = DateTimeField(format='%dth %b, %Y')
    tutorial_count = IntegerField(source='get_tutorial_count')

    class Meta:

        model = Series
        fields = ('id', 'name', 'slug', 'creator', 'type_of', 'timestamp', 'tutorial_count')


class SeriesDetailSerializer(ModelSerializer):

    creator = StringRelatedField()
    tutorial_count = IntegerField(source='get_tutorial_count')
    tutorials = HyperlinkedIdentityField(many=True,
                                         lookup_field='slug',
                                         source='get_tutorials',
                                         lookup_url_kwarg='slug',
                                         view_name='api-tutorial-detail')

    class Meta:

        model = Series
        fields = ('id', 'name', 'slug', 'creator', 'type_of', 'description', 'tutorial_count', 'tutorials')
