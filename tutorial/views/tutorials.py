from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView
)

from tutorial.models import Tutorial
from tutorial.paginators import RecentTutorialPaginator
from tutorial.serializers import (
    TutorialListSerializer,
    TutorialDetailSerializer
)


class RecentTutorialAPIView(ListAPIView):
    serializer_class = TutorialListSerializer
    pagination_class = RecentTutorialPaginator
    queryset = Tutorial.objects.order_by('-pk')[:12]


class TutorialDetailAPIView(RetrieveAPIView):
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    serializer_class = TutorialDetailSerializer
    queryset = Tutorial.objects.filter(draft=False)


class TutorialLikeUnlikeAPIView(APIView):
    """
    Likes a tutorial by an authenticated user if
    no existing like is found or else removes the like.
    """

    parser_classes = (FormParser, MultiPartParser)

    @staticmethod
    def get(request):
        return Response({
            'detail': 'Method "GET" not allowed. Provide a token and a tutorial id number.'
        }, status=405)

    @staticmethod
    def post(request):

        token = request.POST.get('token')
        tutorial_id = request.POST.get('tutorial_id')

        if not token:
            return Response({
                'error': 'Unauthorized to view response.'
            }, status=401)

        if not tutorial_id:
            return Response({
                'error': 'Tutorial id not provided.'
            }, status=401)

        try:

            user_id = Token.objects.get(key=token).user_id
            tutorial = Tutorial.objects.get(id=tutorial_id)

            if not tutorial.votes.exists(user_id):
                tutorial.votes.up(user_id)
                return Response({
                    'action': 1,
                    'voted': 'Liked by user.'
                })
            else:
                tutorial.votes.delete(user_id)
                return Response({
                    'action': -1,
                    'voted': 'Unliked by uer.'
                })

        except ObjectDoesNotExist:
            return Response({
                'error': 'Invalid auth token provided or tutorial does not exist.'
            }, status=401)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=500)
