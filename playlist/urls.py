from django.urls import path
from . import views


urlpatterns = [
    path('song/like/add_or_delete/<slug:song_id>/<path:apple_id>/', views.add_or_delete_like),
    path('song/dislike/add_or_delete/<int:song_id>/<path:apple_id>/', views.add_or_delete_dislike),
    path('put_all_genres_from_apple/', views.put_all_genres_from_apple),
    path('create_ad_ing/', views.create_advertising),
    path('delete_ad_ing/', views.delete_advertising),
    path('create_plt/', views.create_playlist),
    path('plus_one_view/<int:song_id>/', views.plus_one_view),
]