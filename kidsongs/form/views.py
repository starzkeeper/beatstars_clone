from django.contrib.postgres.search import TrigramSimilarity
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from rest_framework import generics
from .models import Songs, Author
from .serializers import SongsSerializer


# Главная страница (не настроено)
class Home(ListView):
    model = Songs
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        num_visits = self.request.session.get('num_visits', 0)
        self.request.session['num_visits'] = num_visits + 1
        context['num_visits'] = num_visits
        return context


# Детальный просмотр объекта модели Songs
class DetailPost(DetailView):
    model = Songs
    template_name = 'details_song.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'


# Поиск
class SearchView(View):
    model = Songs
    template_name = 'search.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('search', None)
        songs_results = Songs.objects.annotate(
            similarity=TrigramSimilarity('name', query),
        ).filter(similarity__gt=0.3).order_by('-similarity')
        author_results = Author.objects.filter(search_vector=query)

        return render(
            request=request,
            template_name=self.template_name,
            context={
                'search': query or '',
                'songs_results': songs_results[:3],
                'songs_results_count': songs_results.count(),
                'author_results': author_results[:3],
                'author_results_count': author_results.count(),
            }
        )


# Представление API
class SongsAPIView(generics.ListCreateAPIView):
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer
