from django.urls import path
from recomendations import views


urlpatterns = [
    path('get_songs/', views.get_songs),
    path('get_genres/', views.get_genres),
    path('get_songs_to_choose/', views.get_songs_to_choose),
    path('get_recommendations/<int:song_number>/<int:step>/<path:apple_id>/', views.get_recommendations),
]
