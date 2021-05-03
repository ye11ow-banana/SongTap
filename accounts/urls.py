from django.urls import path
from . import views

urlpatterns = [
    path('get_or_create_or_update_account/', views.get_or_create_or_update_account,
         name='get_or_create_or_update_account'),
    path('update_login/', views.update_login, name='update_login'),
    path('update_main_user_photo/<path:photo_name>/<path:apple_id>/', views.update_main_user_photo),
    path('is_invite_code_true/<path:invite_code>/', views.is_invite_code_true),
    path('privacy_policy/', views.show_privacy_policy),
    path('rules/', views.show_rules),
    path('view_user_likes/<path:apple_id>/', views.view_user_likes),
    path('get_filtered_users/', views.get_filtered_users)
]
