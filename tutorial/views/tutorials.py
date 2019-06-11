from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView
)

from tutorial.models import Tutorial
from tutorial.serializers import (
    TutorialListSerializer,
    TutorialDetailSerializer
)


class RecentTutorialAPIView(APIView):

    @staticmethod
    def get(request):

        query = Tutorial.objects.filter(draft=False).order_by('-pk')[:10]
        data = TutorialListSerializer(query, many=True).data

        return Response(data)


class TutorialDetailAPIView(RetrieveAPIView):
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    serializer_class = TutorialDetailSerializer
    queryset = Tutorial.objects.filter(draft=False)
