from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns


admin.autodiscover()

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
    path('recomendations/', include('recomendations.urls')),
    path('playlist/', include('playlist.urls')),
    path('friends/', include('friends.urls')),
)
