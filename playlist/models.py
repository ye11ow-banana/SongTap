from django.db import models
from accounts.models import AppUser


class Genre(models.Model):
    value = models.CharField(verbose_name="Жанр", unique=True, max_length=50)
    apple_id = models.BigIntegerField(verbose_name="ID жанра", default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = "Жанры"


class Artist(models.Model):
    value = models.CharField(verbose_name="Исполнитель", unique=True, max_length=200)
    apple_id = models.BigIntegerField(verbose_name="ID артиста", default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = "Исполнители"


class Song(models.Model):
    apple_id = models.CharField(verbose_name="Apple ID", blank=True, null=True, max_length=200)
    title = models.CharField(verbose_name="Название", max_length=200)
    genre = models.ForeignKey(Genre, verbose_name="Жанр", related_name="genre", on_delete=models.DO_NOTHING)
    artist = models.ForeignKey(Artist, verbose_name="Исполнитель", related_name="artist", on_delete=models.DO_NOTHING)
    image_url = models.URLField(verbose_name="Image Url", blank=True, null=True)

    view_count = models.IntegerField(verbose_name="Счётчик прослушиваний", default=0)

    def __str__(self):
        return f"Песня {self.title}"

    class Meta:
        verbose_name = 'Песня'
        verbose_name_plural = "Песни"


class Playlist(models.Model):
    song = models.ManyToManyField(Song, verbose_name='Песни', related_name='playlist')
    owner = models.ForeignKey(
        AppUser, on_delete=models.CASCADE,
        verbose_name='Пользователь', related_name='playlist_owner'
    )
    apple_id = models.CharField(verbose_name='Apple ID плейлиста', blank=True, null=True, max_length=1000)

    def __str__(self):
        if self.owner.email:
            return f"Плейлист юзера {self.owner.email}"
        elif self.owner.username:
            return f"Плейлист юзера {self.owner.username}"
        else:
            return f"Плейлист юзера {self.owner.apple_id}"

    class Meta:
        verbose_name = "Плейлист"
        verbose_name_plural = "Плейлисты"


class LikedSongs(models.Model):
    song = models.ForeignKey(Song, verbose_name="Понравившаяся песня", related_name='liked_song',
                             on_delete=models.CASCADE)
    user = models.ForeignKey(AppUser, verbose_name='Пользователь', related_name='liked_user', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Понравившиеся песни"
        verbose_name = "Понравившаяся песня"


class DislikedSongs(models.Model):
    song = models.ForeignKey(Song, verbose_name="Не понравившаяся песня", related_name='disliked_song',
                             on_delete=models.CASCADE)
    user = models.ForeignKey(AppUser, verbose_name='Пользователь', related_name='disliked_user', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Не понравившиеся песни"
        verbose_name = "Не понравившаяся песня"


class Rating(models.Model):
    """Рейтинг"""
    likes = models.IntegerField(verbose_name="Всего лайков", default=0)
    dislikes = models.IntegerField(verbose_name="Всего дизлайков", default=0)
    value = models.DecimalField(verbose_name="Рейтинг", decimal_places=5, max_digits=6, default=5.00000)
    song = models.OneToOneField(
        Song,
        on_delete=models.CASCADE,
        verbose_name="Песня",
        related_name="ratings",
    )

    def __str__(self):
        return f"{self.song}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class UserGenres(models.Model):
    user = models.ForeignKey(AppUser, verbose_name='Пользователь', related_name='user_genres', on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, verbose_name='Жанр', related_name='genre_fans', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Предпочтение'
        verbose_name_plural = 'Предпочтения'


class Advertising(models.Model):
    '''Трек для рекламы'''
    song = models.OneToOneField(Song, verbose_name='Песня для рекламы', on_delete=models.CASCADE)
    needed_views_number = models.IntegerField(verbose_name='Нужное количество просмотров', default=0)

    class Meta:
        verbose_name = 'Трек для рекламы'
        verbose_name_plural = 'Треки для рекламы'