from multiprocessing.pool import ThreadPool
from typing import Tuple

import requests

from SongTap.settings import playlists_for_genres, headers
from playlist.models import Song


def get_db_songs_info(songs_id: list) -> list:
    """Возвращает dict с информацией про песню"""
    songs_info = []

    for song_id in songs_id:
        song = Song.objects.get(apple_id=song_id)

        song_info = {
            'songId': song_id,
            'artistName': song.artist.value,
            'songImageUrl': song.image_url,
            'songName': song.title
        }

        songs_info.append(song_info)

    return songs_info


def split_songs_into_need_to_add_to_db_and_not(songs_id: list) -> Tuple[list, list]:
    """Разделяет на песни, которые надо добавить в бд
    и песни, которые уже есть в бд"""
    songs_id_in_db = []
    songs_id_need_to_add_to_db = []

    for song_id in songs_id:
        song = Song.objects.filter(apple_id=song_id)

        if song:
            songs_id_in_db.append(song_id)
        else:
            songs_id_need_to_add_to_db.append(song_id)

    return songs_id_need_to_add_to_db, songs_id_in_db


def get_data_from_response_charts(info: dict) -> list:
    """Парсит ответ Apple для рекомендаций"""
    songs = info['data'][0]['relationships']['tracks']['data']

    results = []

    for song in songs:
        apple_id = song['id']
        artist_name = song['attributes']['artistName']
        img = song['attributes']['artwork']['url'].replace(
            '{w}', str(song['attributes']['artwork']['width'])
        )
        img = img.replace('{h}', str(song['attributes']['artwork']['height']))
        song_name = song['attributes']['name']

        dictionary = {
            'songId': apple_id,
            'artistName': artist_name,
            'songImageUrl': img,
            'songName': song_name,
        }

        results.append(dictionary)

    return results


def get_start_songs() -> list:
    """Подборка первых песен"""
    url = 'https://api.music.apple.com/v1/catalog/us/playlists/' + playlists_for_genres['common']
    response = requests.get(url, headers=headers).json()

    return get_data_from_response_charts(response)


def get_apple_recommendation_json(music_user_token: str) -> dict:
    """Рекомендации от Apple Music"""
    url = 'https://api.music.apple.com/v1/me/recommendations/'

    return requests.get(
        url, headers={**headers, **{'Music-User-Token': music_user_token}}
    ).json()


def get_playlists_id(data: dict) -> list:
    """
    Находим id плейлиста из ответа Apple Music
    касательно рекомендаций
    """
    ids = []
    for rec in data['data']:
        try:
            for el in rec['relationships']['contents']['data']:
                if el['id'].startswith('pl'):
                    ids.append(el['id'])
        except KeyError:
            pass

    try:
        return ids[:12]
    except IndexError:
        return ids


def get_songs_from_playlists(ids: list) -> list:
    """Получаем инфу про треки в плейлисте по id"""
    pool = ThreadPool(4)
    result = []

    def parser(rec_id):
        url = 'https://api.music.apple.com/v1/catalog/us/playlists/' + rec_id
        return requests.get(url, headers=headers)

    responses = pool.map(parser, ids)
    pool.close()
    pool.join()

    for response in responses:
        try:
            songs = get_data_from_response_charts(response.json())
        except KeyError:
            continue

        try:
            result += songs
        except IndexError:
            result += songs

    return result


def get_apple_recommendations(music_user_token: str) -> list:
    """Получаем нужную инфу про рекомендованные треки от Apple Music"""
    data = get_apple_recommendation_json(music_user_token)
    ids = get_playlists_id(data)

    return get_songs_from_playlists(ids)
