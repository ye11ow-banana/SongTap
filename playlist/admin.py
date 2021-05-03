from django.contrib import admin
from .models import Genre, Artist, Song, Playlist, LikedSongs, DislikedSongs, UserGenres, Advertising
from modeltranslation.admin import TranslationAdmin


@admin.register(Advertising)
class AdvertisingAdmin(admin.ModelAdmin):
    list_display = ['song', 'needed_views_number']


@admin.register(UserGenres)
class UserGenresAdmin(admin.ModelAdmin):
    list_display = ['user', 'genre']


@admin.register(Genre)
class GenreAdmin(TranslationAdmin):
    list_display = ['value']


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['value']


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'apple_id', 'artist', 'genre', 'view_count', 'id']
    search_fields = ['title', 'apple_id', 'artist__value', 'genre__value']


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['owner', 'apple_id']
    search_fields = ['song__title', 'owner__email', 'owner__apple_id']


@admin.register(LikedSongs)
class LikedSongsAdmin(admin.ModelAdmin):
    list_display = ['user', 'song']
    search_fields = ['song__title', 'owner__email', 'owner__apple_id']


@admin.register(DislikedSongs)
class DislikedSongsAdmin(admin.ModelAdmin):
    list_display = ['user', 'song']
    search_fields = ['song__title', 'owner__email', 'owner__apple_id']

