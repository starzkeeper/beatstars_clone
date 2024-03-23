from django.urls import path
from .views import DetailPost, SongsAPIView, SearchView, profile_view, RegisterView, Home, AddSong
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', Home.as_view(), name='index'),
    path('post/<slug:post_slug>/', DetailPost.as_view(), name='post'),
    path('api/v1/songslist/', SongsAPIView.as_view(), name='songs_list'),
    path('api/v1/songslist/<int:pk>/', SongsAPIView.as_view(), name='songs_list'),
    path('profile/', profile_view, name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('search/', SearchView.as_view(), name='search'),
    path('addsong/', AddSong.as_view(), name='add_song')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


