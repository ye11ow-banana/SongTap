from django.urls import path
from friends import views

urlpatterns = [
    path('create_friend/', views.create_friend, name='create_friend'),
    path('view_friends_likes/<path:apple_id>/', views.view_friends_likes, name='view_friends_likes'),
    path('get_friends/<path:apple_id>/', views.get_friends, name='get_friends'),
    path('get_similar_users/<int:user_number>/<int:step>/<path:apple_id>/', views.get_similar_users,
         name='get_similar_users'),
    path('get_friends_songs/<path:apple_id>/', views.get_friends_songs, name='get_friends_songs'),
    path('delete_friend/', views.delete_friend, name='delete_friend')
]
