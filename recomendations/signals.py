import decimal

from decimal import Decimal

from django.db.models.signals import post_save
from django.dispatch import receiver
from playlist.models import Song, Rating, LikedSongs, DislikedSongs, Playlist
import logging

logger = logging.getLogger(__name__)


def add_view_count(song: Song):
    song.view_count += 1
    song.save()
    return song


# def change_rating(song: Song, value: int = 0):
#     try:
#         rating = song.ratings.get()
#         if not rating:
#             rating = Rating.objects.create(song=song)
#     except Exception as err:
#         logger.info(err)
#         rating = Rating.objects.create(song=song)
#     song = add_view_count(song)
#     if value:

#         decimal.getcontext().prec = 5
#         rate_value = decimal.Decimal(value=f"{value / song.view_count}")
#         rating.value += float(rate_value)
#         if rating.value > 5:
#             rating.value = Decimal("5")
#         rating.save()


# @receiver(post_save, sender=LikedSongs)
# def like_song(sender, instance: LikedSongs, **kwargs):
#     change_rating(instance.song, value=1)


# @receiver(post_save, sender=DislikedSongs)
# def dislike_song(sender, instance: DislikedSongs, **kwargs):
#     change_rating(instance.song, value=-1)


# @receiver(post_save, sender=Playlist)
# def like_song(sender, instance: Playlist, **kwargs):
#     change_rating(instance.song, value=2)
