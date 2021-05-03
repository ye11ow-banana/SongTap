from accounts.services import get_user_or_error
from core.check_post import check_json
from recomendations import services as rec_services
from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import AppUser
from rest_framework import status

from work_with_apple.getting import get_db_songs_info
from . import services
import logging
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser

from .services import get_friend_or_error

logger = logging.getLogger(__name__)


@parser_classes(JSONParser)
@api_view(['POST'])
@check_json
def create_friend(request):
    """Создает друга для пользователя"""
    user = get_user_or_error(request.data['user_apple_id'])

    if type(user) is dict:
        return Response(user, status=status.HTTP_200_OK)

    friend = services.get_user_by_username_or_email(request.data['friend_data'])

    if friend and friend != user:
        services.create_friend(user, friend)

        return Response({'result': True}, status=status.HTTP_200_OK)

    return Response({'result': False, 'msg': 'Что-то не то с запросом'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def view_friends_likes(request, apple_id: str):
    """Показывает отлайканые песни друга"""
    user = get_user_or_error(apple_id)

    if type(user) is dict:
        return Response(user, status=status.HTTP_200_OK)

    friends = services.get_friends(user)
    songs_id = services.get_friends_likes_song_id(friends)
    songs_info = get_db_songs_info(songs_id)

    return Response(songs_info, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_friends(request, apple_id: str):
    """Показывает друзей"""
    user = get_user_or_error(apple_id)

    if type(user) is dict:
        return Response(user, status=status.HTTP_200_OK)

    friends_obj = services.get_friends(user)
    friends = services.get_info_about_users(friends_obj, user)

    return Response(friends, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_similar_users(request, user_number: int, step: int, apple_id: str):
    """Сортирует юзеров по совпадениям"""
    user = get_user_or_error(apple_id)

    if type(user) is dict:
        return Response(user, status=status.HTTP_200_OK)

    ordinary_users = list(set(AppUser.objects.all()) - {user})

    similar_users = services.get_sorted_user_by_similarity(ordinary_users, user)
    similar_users = services.slice_users(user_number, step, ordinary_users, similar_users)

    if type(similar_users) is dict:
        return Response(similar_users, status=status.HTTP_200_OK)

    return Response(similar_users, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_friends_songs(request, apple_id: str):
    """Дает песни из плейлистов друзей"""
    user = get_user_or_error(apple_id)

    if type(user) is dict:
        return Response(user, status=status.HTTP_200_OK)

    friends = services.get_friends(user)
    songs_id = services.get_friends_songs_from_playlist(friends)
    songs_info = get_db_songs_info(songs_id)

    return Response(songs_info, status=status.HTTP_200_OK)


@parser_classes(JSONParser)
@api_view(['POST'])
@check_json
def delete_friend(request):
    """Удаляет друга для пользователя"""
    user = AppUser.objects.get(apple_id=request.data['user_apple_id'])

    friend = services.get_user_by_username_or_email(request.data['friend_data'])

    if friend and friend != user:
        result = get_friend_or_error(user, friend)

        if type(result) is not dict:
            result.delete()

        return Response({'result': True}, status=status.HTTP_200_OK)

    return Response({'result': False, 'msg': 'Что-то не то с запросом'}, status=status.HTTP_200_OK)
