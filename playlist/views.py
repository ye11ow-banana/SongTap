from accounts.services import get_user_or_error
from core.check_post import check_json
from rest_framework.decorators import parser_classes
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status

from work_with_apple.creating import solve_songs, get_all_apple_genres, add_genres_to_db
from . import services
import logging

from .services import add_or_delete_dislike_or_like, delete_or_create_advertising_for_songs

logger = logging.getLogger(__name__)


@api_view(['GET'])
def add_or_delete_like(request, song_id: str, apple_id: str):
    """Меняет положения лайка, удаляя или создавая его"""
    user = get_user_or_error(apple_id)

    if type(user) is dict:
        return Response(user, status=status.HTTP_200_OK)

    solve_songs([song_id, ])
    add_or_delete_dislike_or_like('like', song_id, user)

    return Response({'result': True}, status=status.HTTP_200_OK)


@api_view(['GET'])
def add_or_delete_dislike(request, song_id: int, apple_id: str):
    """Меняет положения дизлайка, удаляя или создавая его"""
    user = get_user_or_error(apple_id)

    if type(user) is dict:
        return Response(user, status=status.HTTP_200_OK)

    solve_songs([song_id, ])
    add_or_delete_dislike_or_like('dislike', song_id, user)

    return Response({'result': True}, status=status.HTTP_200_OK)


@api_view(['GET'])
def put_all_genres_from_apple(request):
    """Берет и записывает в бд жанры от Apple"""
    genres = get_all_apple_genres()
    add_genres_to_db(genres)

    return Response({'result': True}, status=status.HTTP_200_OK)


@parser_classes(JSONParser)
@api_view(['POST'])
@check_json
def create_advertising(request):
    """Создает песни, которые надо рекламировать"""
    solve_songs(request.data['songs_id'])
    delete_or_create_advertising_for_songs(request.data['songs_id'], request.data['needed_views_number'])

    return Response({'result': True}, status=status.HTTP_200_OK)


@parser_classes(JSONParser)
@api_view(['POST'])
@check_json
def delete_advertising(request):
    """Удаляет песни, которые надо рекламировать"""
    solve_songs(request.data['songs_id'])
    delete_or_create_advertising_for_songs(request.data['songs_id'])

    return Response({'result': True}, status=status.HTTP_200_OK)


@parser_classes(JSONParser)
@api_view(['POST'])
@check_json
def create_playlist(request):
    """Создает плейлист"""
    user = get_user_or_error(request.data['user_apple_id'])

    if type(user) is dict:
        return Response(user, status=status.HTTP_200_OK)

    solve_songs(request.data['songs_id'])

    songs = services.get_songs_from_db_by_ids(request.data['songs_id'])
    services.create_playlist(songs, request.data['playlist_apple_id'], user)

    return Response({'result': True}, status=status.HTTP_200_OK)


@api_view(['POST'])
def plus_one_view(request, song_id: int):
    """+1 к просмотрам трека"""
    solve_songs([song_id, ])
    song = services.get_songs_from_db_by_ids([song_id, ])[0]

    song.view_count += 1
    song.save()

    return Response({'result': True}, status=status.HTTP_200_OK)
