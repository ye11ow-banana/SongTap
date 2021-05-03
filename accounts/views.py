from django.db.models import Q
from django.shortcuts import render
from core.check_post import check_json
from friends.services import get_friends_likes_song_id, get_info_about_users
from work_with_apple.getting import get_db_songs_info
from .models import InviteCode, AppUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import logging
from friends import services as friends_services
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from . import services
from io import BytesIO
import os


logger = logging.getLogger(__name__)


@parser_classes(JSONParser)
@api_view(['POST'])
@check_json
def get_or_create_or_update_account(request):
    """
    Возвращает профиль, обновляет его,
    или создает аккаунт
    """
    result = services.get_error_or_create_or_update_account(request)

    if type(result) is dict:
        return Response(result, status=status.HTTP_200_OK)

    user_info = friends_services.get_info_about_users([result, ])

    return Response(user_info[0], status=status.HTTP_200_OK)


@parser_classes(JSONParser)
@api_view(['POST'])
@check_json
def update_login(request):
    """Обновляет username"""
    user = services.get_user_or_error(request.data['apple_id'])

    if type(user) is dict:
        return Response(user, status=status.HTTP_200_OK)

    result = services.get_error_or_update_username(request.data['username'], user)

    if result:
        return Response(result, status=status.HTTP_200_OK)

    return Response({'result': True}, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_main_user_photo(request, apple_id: str, photo_name: str):
    """Обновляет аватарку пользователя"""
    chunk = list(request.FILES[photo_name].chunks())[0]

    buf = BytesIO()
    buf.write(chunk)

    user = services.get_user_or_error(apple_id)

    if type(user) is dict:
        return Response(user, status=status.HTTP_200_OK)

    if user.photo and user.photo != 'accounts/default.jpg':
        os.remove(user.photo.path)

    user.photo.save(photo_name, buf, save=True)

    return Response({'result': True}, status=status.HTTP_200_OK)


@api_view(['GET'])
def is_invite_code_true(request, invite_code: str):
    """Проверяет инвайт код"""
    try:
        InviteCode.objects.get(invite_code=invite_code)
    except InviteCode.DoesNotExist:
        return Response({'result': False}, status=status.HTTP_200_OK)

    return Response({'result': True}, status=status.HTTP_200_OK)


@api_view(['GET'])
def show_privacy_policy(request):
    """Показывает политику приватности"""
    return render(request, 'privacy_policy.html')


@api_view(['GET'])
def show_rules(request):
    """Показывает правила приложения"""
    return render(request, 'rules.html')


@api_view(['GET'])
def view_user_likes(request, apple_id: str):
    """Показывает отлайканые песни юзера"""
    user = services.get_user_or_error(apple_id)

    if type(user) is dict:
        return Response(user, status=status.HTTP_200_OK)

    songs_id = get_friends_likes_song_id([user, ])
    songs_info = get_db_songs_info(songs_id)

    return Response(songs_info, status=status.HTTP_200_OK)


@parser_classes(JSONParser)
@api_view(['GET'])
@check_json
def get_filtered_users(request):
    """Возвращает юзеров по логину или фио"""
    data = request.data['data'].split('_')

    users = AppUser.objects.all()
    users_all = users

    for item in data:
        if item:
            users = users.filter(Q(first_name=item) | Q(last_name=item) | Q(username=item))

    if users == users_all:
        return Response([], status=status.HTTP_200_OK)

    users_info = get_info_about_users(users)

    return Response(users_info, status=status.HTTP_200_OK)
