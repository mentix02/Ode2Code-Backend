from django.shortcuts import get_object_or_404
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


class TutorialCreateAPIView(APIView):
    """
    Creates a new tutorial if POST
    request is authenticated with
    proper token or session authentication.

    Requires form data =>
        token?: uuid
        title!: string
        series_id!: int
        draft?: bool (False)
        description: long str
    """

    parser_classes = (FormParser, MultiPartParser)

    @staticmethod
    def post(request):

        # get required parameters
        try:
            title = request.POST['title']
            content = request.POST['content']
            series_id = request.POST['series_id']
            draft = request.POST.get('draft', False)
            description = request.POST['description']
        except Exception as e:
            return Response({
                'error': f'"{str(e)}" field not provided.'
            }, status=400)

        token = request.POST.get('token')

        if not token and not request.user.is_authenticated:
            return Response({
                'error': 'You need to be authenticated to create a new tutorial.'
            }, status=401)

        try:

            if token:
                author_id = Token.objects.get(key=token).user.author.id
            else:
                author_id = request.user.author.id

            tutorial = Tutorial.objects.create(
                title=title,
                content=content,
                series_id=series_id,
                author_id=author_id,
                description=description,
            )

            data = TutorialDetailSerializer(tutorial).data
            return Response({
                'details': data
            }, status=201)

        except Exception as e:
            return Response({
                'error': str(e)
            }, status=500)


class TutorialDeleteAPIView(APIView):

    @staticmethod
    def post(request):

        token = request.POST.get('token')
        tutorial_id = request.POST.get('tutorial_id')

        if not token:
            return Response({
                'error': "You are not authenticated to delete a tutorial."
            }, status=401)
        if not tutorial_id:
            return Response({
                'error': "Please provide a tutorial id to delete."
            }, status=405)

        tutorial = get_object_or_404(Tutorial, id=tutorial_id)

        try:

            if token:
                author_id = Token.objects.get(key=token).user.author.id
            else:
                author_id = request.user.author.id

            if tutorial.author.id == author_id or tutorial.author.user.is_superuser:
                tutorial.delete()
                return Response({
                    'deleted': tutorial_id
                }, status=204)
            else:
                return Response({
                    'error': 'You are not authorized to delete this tutorial.'
                }, status=401)

        except Exception as e:
            return Response({
                'error': str(e)
            }, status=405)
