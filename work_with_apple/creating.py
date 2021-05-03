from multiprocessing.pool import ThreadPool

import requests

from SongTap.settings import headers
from playlist.models import Genre
from playlist.services import create_song, create_artist
from work_with_apple.getting import split_songs_into_need_to_add_to_db_and_not, get_db_songs_info


def solve_songs(songs_id: list) -> list:
    """1) Решает какие песни надо добавить в бд.
    2) Берет информацию про песни от эпл.
    3) Добавляет песни в бд.
    4) Возвращает информацию про песни из бд"""
    songs_id_need_to_add_to_db, songs_id_in_db = split_songs_into_need_to_add_to_db_and_not(songs_id)
    songs_info = get_apple_songs_info_by_ids(songs_id_need_to_add_to_db)
    add_apple_songs_info_to_db(songs_info)
    return get_db_songs_info(songs_id)


def get_apple_songs_info_by_ids(songs_id: list) -> list:
    """Берет информацию про песни от Apple"""
    pool = ThreadPool(4)
    songs_info = []

    def parser(song_id):
        url = 'https://api.music.apple.com/v1/catalog/us/songs/' + str(song_id)
        return requests.get(url, headers=headers)

    responses = pool.map(parser, songs_id)
    pool.close()
    pool.join()

    for response in responses:
        response = response.json()
        try:
            img = response['data'][0]['attributes']['artwork']['url'].replace(
                '{w}', str(response['data'][0]['attributes']['artwork']['width'])
            )
            img = img.replace('{h}', str(response['data'][0]['attributes']['artwork']['height']))

            needed_data = {
                'song_id': response['data'][0]['id'],
                'artist_name': response['data'][0]['attributes']['artistName'],
                'artist_id': response['data'][0]['relationships']['artists']['data'][0]['id'],
                'image_url': img,
                'song_name': response['data'][0]['attributes']['name'],
                'genre_names': response['data'][0]['attributes']['genreNames']
            }
        except KeyError:
            continue

        songs_info.append(needed_data)

    return songs_info


def add_apple_songs_info_to_db(songs_info: list) -> None:
    """Добавляет песни в бд"""
    for song_info in songs_info:
        artist_name = song_info['artist_name']
        artist_id = song_info['artist_id']

        artist = create_artist(artist_name, artist_id)

        genre_name = choose_song_genre(song_info['genre_names'])
        genre = Genre.objects.get(value_en=genre_name)

        create_song(
            apple_id=song_info['song_id'],
            title=song_info['song_name'],
            genre=genre,
            artist=artist,
            image_url=song_info['image_url']
        )


def choose_song_genre(genre_names: list) -> str:
    """Выбирает жанр для песни"""
    for genre_name in genre_names:
        if genre_name != 'Worldwide' and genre_name != 'Alternative' and genre_name != 'Music':
            return genre_name

    return 'Worldwide'


def get_all_apple_genres() -> list:
    """Берет все жанры из Apple Music"""
    url = 'https://api.music.apple.com/v1/catalog/us/genres/'
    genres_info = requests.get(url, headers=headers).json()['data']

    result = []
    for item in genres_info:
        if item['attributes']['name'] not in ['Music', 'Worldwide', 'Alternative']:
            result.append({'genre_name': item['attributes']['name'], 'genre_id': item['id']})

    return result


def add_genres_to_db(genres: list) -> True:
    """Записывает жанры в бд"""
    for genre in genres:
        try:
            Genre.objects.get(value_en=genre['genre_name'], apple_id=genre['genre_id'])
        except Genre.DoesNotExist:
            Genre.objects.create(value_en=genre['genre_name'], apple_id=genre['genre_id'])

    return True
