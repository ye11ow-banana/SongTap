from django.db.models import Q
from playlist.models import LikedSongs, Playlist
from recomendations import services as rec_services
from accounts.models import AppUser
from recomendations.services import calculate_similarity_coefficient
from .models import Friend
from typing import Optional, Union


def get_friends(user: object) -> list:
    """Дает друзей пользователя из бд"""
    friend_obj = Friend.objects.filter(user=user)

    return [friend.friend for friend in friend_obj if friend_obj]


def get_friends_likes_song_id(friends: list) -> list:
    """Дает apple_id лайкнутых песен друга из бд"""
    friends_likes_song_id = []

    for friend in friends:
        liked_songs = LikedSongs.objects.filter(user=friend)

        if liked_songs:
            for liked_song in liked_songs:
                friends_likes_song_id.append(liked_song.song.apple_id)

    return friends_likes_song_id


def get_info_about_users(users_obj: list, current_user: object=0) -> list:
    """Дает информацию про пользователя из бд"""
    users = []

    for user_obj in users_obj:
        data = {
            'email': '' if user_obj.email is None else str(user_obj.email),
            'username': '' if user_obj.username is None else str(user_obj.username),
            'first_name': '' if user_obj.first_name is None else str(user_obj.first_name),
            'last_name': '' if user_obj.last_name is None else str(user_obj.last_name),
            'gender': '' if user_obj.gender is None else str(user_obj.gender),
            'age': '' if user_obj.age is None else str(user_obj.age), 'apple_id': user_obj.apple_id,
            'photo': user_obj.photo.url
        }

        if current_user:
            current_user_liked_songs = list(LikedSongs.objects.filter(user=current_user))

            similarity_coefficient = rec_services.calculate_similarity_coefficient(
                user_obj, current_user_liked_songs
            )        
            data['similarity_coefficient'] = str(similarity_coefficient*100) + '%'

        users.append(data)

    return users


def get_user_by_username_or_email(username_or_email: str) -> Optional[object]:
    """Дает пользователя по почте или логину"""
    return AppUser.objects.filter(
        Q(email=username_or_email) | Q(username=username_or_email)
    )[0]


def get_friends_songs_from_playlist(friends: list):
    """Дает песни из плейлиста друзей"""
    songs_id = []

    for friend in friends:
        try:
            playlist = Playlist.objects.get(owner=friend)
            songs_id.append(playlist.song.apple_id)
        except Playlist.DoesNotExist:
            pass

    return songs_id


def create_friend(user: object, friend: object) -> None:
    """Создает друга для user"""
    Friend.objects.get_or_create(
        user=user,
        friend=friend
    )


def get_friend_or_error(user: object, friend: object) -> Union[object, dict]:
    """Возвращает либо друга, либо ошибку об отсутствии оного"""
    try:
        return Friend.objects.get(user=user, friend=friend)
    except Friend.DoesNotExist:
        return {'result': False, 'msg': 'Этот пользователь не является Вашим другом'}


def get_sorted_user_by_similarity(ordinary_users: list, user: object) -> list:
    """Сортирует юзеров по схожести"""
    similar_users = get_info_about_users(ordinary_users, user)

    similar_users = sorted(similar_users, key=lambda k: float(k['similarity_coefficient'].replace('%', '')))
    similar_users.reverse()

    return similar_users


def slice_users(user_number: int, step: int, ordinary_users: list, similar_users: list) -> Union[dict, list]:
    """Делает срез пользователей"""
    start_index = user_number - 1
    end_index = start_index + step

    if user_number > len(ordinary_users):
        return {'result': False, 'msg': 'user_number больше кол-ва юзеров'}
    else:
        try:
            return similar_users[start_index:end_index]
        except IndexError:
            return similar_users[start_index:]
