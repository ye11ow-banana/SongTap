from rest_framework import serializers
from playlist.models import Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('value', 'apple_id')
