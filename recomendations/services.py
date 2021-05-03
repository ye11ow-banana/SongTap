from random import shuffle
from typing import Union

from playlist.models import (
    AppUser, Playlist, DislikedSongs,
    LikedSongs, Song, Advertising
)
from work_with_apple.creating import get_apple_songs_info_by_ids
from work_with_apple.getting import get_apple_recommendations, get_db_songs_info
from .models import MusicUserToken


def get_similar_users(ordinary_users: list, current_user: object) -> dict:
    """Находим юзера с похожими вкусами для создания рекомендаций"""
    current_user_liked_songs = list(LikedSongs.objects.filter(user=current_user))
    similar_users = {}

    for user in ordinary_users:
        similarity_coefficient = calculate_similarity_coefficient(
            user, current_user_liked_songs
        )

        if similarity_coefficient >= 0.8:
            similar_users[str(user.apple_id)] = similarity_coefficient

    return similar_users


def calculate_similarity_coefficient(
        user: object, current_user_liked_songs: list
) -> float:
    """
    Помогает найти похожего юзера,
    рассчитывая коэффициент схожести
    """
    user_liked_songs = list(LikedSongs.objects.filter(user=user))

    coincidences = 0

    for song in user_liked_songs:
        for cu_song in current_user_liked_songs:
            if str(song.song) == str(cu_song.song):
                coincidences += 1
    try:
        return coincidences / (len(current_user_liked_songs))
    except ZeroDivisionError:
        return 0


def delete_repeated_recommendations(recommendations: list) -> list:
    """Удаляет повторяющиеся песни"""
    dont_repeated_recommendations = []

    for song in recommendations:
        if song not in dont_repeated_recommendations:
            dont_repeated_recommendations.append(song)

    return dont_repeated_recommendations


def delete_repeated_songNames(recommendations: list) -> list:
    """Удаляет повторяющиеся песни по названию"""
    songNames = list(set([song['songName'] for song in recommendations]))

    dont_repeated_recommendations = []
    for songName in songNames:
        for song in recommendations:
            if songName == song['songName']:
                dont_repeated_recommendations.append(song)
                break

    return dont_repeated_recommendations


def transform_dict(data: list) -> list:
    """Преобразовывает dict-ы в массиве на другие dict-ы"""
    result = []

    for _dict in data:
        info = {
            'songId': _dict['song_id'],
            'artistName': _dict['artist_name'],
            'songImageUrl': _dict['image_url'],
            'songName': _dict['song_name']
        }

        result.append(info)

    return result


def get_recommendations(similar_users: dict, music_user_token: str) -> list:
    """Рассчитывает рекомендации для юзера"""
    if similar_users:
        recommendations = []

        for apple_id in similar_users.keys():
            user = AppUser.objects.get(apple_id=apple_id)

            user_liked_songs = [obj.song.apple_id for obj in list(LikedSongs.objects.filter(user=user))]
            user_disliked_songs = [obj.song.apple_id for obj in list(DislikedSongs.objects.filter(user=user))]
            user_songs_in_playlist = [obj.song.apple_id for obj in list(Playlist.objects.filter(owner=user))]

            recommendations = list(
                set(
                    recommendations + list(
                        set(user_songs_in_playlist + user_liked_songs)
                    )
                )
            )

        recommendations = get_db_songs_info(list(set(recommendations) - set(user_disliked_songs)))

        if len(recommendations) < 20:
            recommendations += get_apple_recommendations(music_user_token)

        return recommendations

    else:
        return get_apple_recommendations(music_user_token)


def remove_listened_songs(songs: list, current_user: object) -> list:
    """Убирает (диз)лайкнутые песни из рекомендаций"""
    current_user_liked_songs = [obj.song.apple_id for obj in list(LikedSongs.objects.filter(user=current_user))]
    current_user_disliked_songs = [obj.song.apple_id for obj in list(DislikedSongs.objects.filter(user=current_user))]

    def remove_dict_list_from_dict_list(current_user_songs: list, songs: list) -> list:
        for c_song in current_user_songs:
            for song in songs:
                if str(c_song) == str(song['songId']):
                    songs.remove(song)

        return songs

    new_songs = remove_dict_list_from_dict_list(current_user_liked_songs, songs)
    result = remove_dict_list_from_dict_list(current_user_disliked_songs, new_songs)

    return result


def choice_new_recommendations_with_advertisings(
        songs: list, song_number: int, step: int, current_user
) -> list:
    """
    Делает вырез нужного кол-ва рекомендаций. Добавляет рекламу
    Убирает прослушанные и повторные композиции.
    """
    advertisings = Advertising.objects.all()
    advertising_songs_id = []

    if len(advertisings) > 0:
        for advertising in advertisings:

            try:
                view_count = Song.objects.get(title=advertising.song.title).view_count
            except Song.DoesNotExist:
                continue

            if view_count < advertising.needed_views_number:
                needed_datas = transform_dict(get_apple_songs_info_by_ids([advertising.song.apple_id, ]))
                for needed_data in needed_datas:
                    advertising_songs_id.append(needed_data)

    recommendations = delete_repeated_recommendations(songs)

    start_index = song_number - 1
    end_index = start_index + step

    try:
        excess = len(advertising_songs_id)

        recs_songs_with_listened_songs = recommendations[start_index:end_index - excess] + advertising_songs_id
        recs_songs = remove_listened_songs(delete_repeated_recommendations(recs_songs_with_listened_songs),
                                           current_user)

        index = len(recs_songs_with_listened_songs) - len(recs_songs)
        recs_songs += recommendations[end_index - excess:end_index - excess + index]

        return recs_songs

    except IndexError:
        excess = step - len(advertising_songs_id)

        if excess <= 0:
            recs_songs_with_listened_songs = recommendations[start_index + excess:] + advertising_songs_id
            return remove_listened_songs(delete_repeated_recommendations(recs_songs_with_listened_songs), current_user)
        else:
            recs_songs_with_listened_songs = recommendations[start_index:] + advertising_songs_id
            return remove_listened_songs(delete_repeated_recommendations(recs_songs_with_listened_songs), current_user)


def solve_recommendations(apple_id: str, song_number: int, step: int) -> Union[list, dict]:
    """Рассчитывает и возвращает рекомендации"""
    try:
        current_user = AppUser.objects.get(apple_id=apple_id)
        music_user_token = MusicUserToken.objects.get(user=current_user).music_user_token

        ordinary_users = list(set(AppUser.objects.filter(is_superuser=False)) - {current_user})

        if not ordinary_users:
            return get_apple_recommendations(music_user_token)

        similar_users = get_similar_users(ordinary_users, current_user)
        recommendations = get_recommendations(similar_users, music_user_token)

        recommendations = choice_new_recommendations_with_advertisings(
            recommendations, song_number, step, current_user
        )

        recommendations = delete_repeated_recommendations(recommendations)
        recommendations = delete_repeated_songNames(recommendations)

        shuffle(recommendations)

        return recommendations

    except AppUser.DoesNotExist:
        return {'result': False, 'msg': 'Не существует юзера с таким apple_id'}

    except MusicUserToken.DoesNotExist:
        return {'result': False, 'msg': 'Не существует юзера с таким music_user_token'}
