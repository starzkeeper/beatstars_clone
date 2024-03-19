from django.urls import path
from .views import DetailPost, SongsAPIView, SearchView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', SearchView.as_view(), name='index'),
    path('post/<slug:post_slug>/', DetailPost.as_view(), name='post'),
    path('api/v1/songslist/', SongsAPIView.as_view(), name='songslist'),
    path('api/v1/songslist/<int:pk>/', SongsAPIView.as_view(), name='songslist'),
    # path('search/', SearchView.as_view(), name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

