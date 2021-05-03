from playlist.models import Song, Artist, Playlist, LikedSongs, DislikedSongs, Advertising


def get_songs_from_db_by_ids(ids: list) -> list:
    """Достает песни из бд по apple id песни"""
    songs = []

    for song_id in ids:
        try:
            songs.append(Song.objects.get(apple_id=song_id))
        except Song.DoesNotExist:
            pass

    return songs


def create_playlist(songs: list, apple_id: str, owner: object) -> None:
    """Создает плейлист"""
    playlist, _ = Playlist.objects.get_or_create(apple_id=apple_id, owner=owner)

    playlist.song.set(songs)

    playlist.save()


def create_song(
        apple_id: str, title: str, genre: object,
        artist: object, image_url: str
) -> object:
    """Создает и возвращает песню"""
    song, _ = Song.objects.get_or_create(
        apple_id=apple_id,
        title=title,
        genre=genre,
        artist=artist,
        image_url=image_url
    )

    return song


def create_artist(artist_name: str, artist_apple_id: str) -> object:
    """Создает и возвращает артиста"""
    artist_obj, _ = Artist.objects.get_or_create(
        value=artist_name, apple_id=artist_apple_id
    )

    return artist_obj


def add_or_delete_dislike_or_like(main: str, song_id: object, user: object) -> None:
    """Создает или удаляет объект в бд лайка или дизлайка"""
    song = Song.objects.get(apple_id=song_id)

    obj_create, obj_delete = LikedSongs, DislikedSongs

    if main != 'like':
        obj_create, obj_delete = obj_delete, obj_create

    try:
        _ = obj_create.objects.get(song=song, user=user)
        _.delete()
    except obj_create.DoesNotExist:
        obj_create.objects.create(song=song, user=user)
        obj_delete.objects.filter(song=song, user=user).delete()


def delete_or_create_advertising_for_songs(songs_id: list, needed_views_number: int = 0) -> None:
    """Создает или удаляет рекламу песен"""
    for song_id in songs_id:
        song = Song.objects.get(apple_id=song_id)

        try:
            if needed_views_number:
                advertising = Advertising.objects.get(song=song)
                advertising.needed_views_number += int(needed_views_number)
                advertising.save()
            else:
                advertising = Advertising.objects.get(song=song)
                advertising.delete()

        except Advertising.DoesNotExist:
            if needed_views_number:
                Advertising.objects.create(song=song, needed_views_number=needed_views_number)
