from accounts.models import AppUser
from playlist.models import Song, Genre, Artist


def _create_default_2_users():
    user_1 = AppUser.objects.create(apple_id='1', username='1', email='1@1')
    user_2 = AppUser.objects.create(apple_id='2', username='2', email='2@2')

    return user_1, user_2


def _create_default_2_artists():
    artist_1 = Artist.objects.create(value='1', apple_id='1')
    artist_2 = Artist.objects.create(value='2', apple_id='2')

    return artist_1, artist_2


def _create_default_2_genres():
    genre_1 = Genre.objects.create(value='1', apple_id='1')
    genre_2 = Genre.objects.create(value='2', apple_id='2')

    return genre_1, genre_2


def _create_default_2_songs():
    genre_1, genre_2 = _create_default_2_genres()
    artist_1, artist_2 = _create_default_2_artists()

    song_1 = Song.objects.create(apple_id='1', title='1', genre=genre_1, artist=artist_1, image_url='1')
    song_2 = Song.objects.create(apple_id='2', title='2', genre=genre_2, artist=artist_2, image_url='2')

    return song_1, song_2


def main():
    _create_default_2_artists()
    _create_default_2_artists()
    _create_default_2_genres()
    _create_default_2_songs()


if __name__ == '__main__':
    main()
