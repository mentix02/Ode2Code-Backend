from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

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


class TutorialDetailAPIView(ListAPIView):

    serializer_class = TutorialListSerializer
    queryset = Tutorial.objects.filter(draft=False)
