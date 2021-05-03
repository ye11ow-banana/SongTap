from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from playlist.models import Genre, Song
from work_with_apple.getting import get_db_songs_info, get_start_songs
from rest_framework import status
from .serializers import GenreSerializer
from .services import solve_recommendations


@api_view(['GET'])
def get_songs(request):
    """Возвращает все песни из бд"""
    songs_id = Song.objects.values_list('apple_id', flat=True)

    return Response(get_db_songs_info(songs_id), status=status.HTTP_200_OK)


@api_view(['GET'])
@csrf_exempt
def get_genres(request):
    """Возвращает жанры"""
    snippets = Genre.objects.all()
    serializer = GenreSerializer(snippets, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_songs_to_choose(request):
    """Берем чарты из Apple Music и записывает в бд"""
    songs = get_start_songs()

    return Response(songs, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_recommendations(request, song_number: int, step: int, apple_id: str):
    """Возвращает рекомендации для конкретного юзера"""
    recommendations = solve_recommendations(apple_id, song_number, step)

    return Response(recommendations, status=status.HTTP_200_OK)
