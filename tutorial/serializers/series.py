from tutorial.models import Series

from rest_framework.serializers import (
    ModelSerializer,
    StringRelatedField,
)


class SeriesListSerializer(ModelSerializer):

    creator = StringRelatedField()

    class Meta:

        model = Series
        fields = ('id', 'name', 'slug', 'creator', 'type_of', 'description')
