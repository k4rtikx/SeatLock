from django.urls import path  # Django function that maps a URL pattern string to a view
from rest_framework.views import APIView  # Base DRF view class — imported here but not actually used; can be removed safely

from movies.views import MoviesListAPIView, MoviesDetailAPIView, MovieCreateAPIView, GenresListView  # Imports the actual view classes we want to wire up to URLs

# urlpatterns is the special list Django looks for — each entry connects one URL pattern to one view
urlpatterns = [
    path('movies/', MoviesListAPIView.as_view()),       # GET /movies/          →  Lists all movies (searchable & filterable)
    path('movies/<int:id>', MoviesDetailAPIView.as_view()),  # GET/PUT/DELETE /movies/5  →  View, update, or delete movie with ID=5; <int:id> captures the number from the URL
    path('movies/create', MovieCreateAPIView.as_view()),  # POST /movies/create  →  Create a brand-new movie (superadmin only)
    path('genres/', GenresListView.as_view()),          # GET /genres/           →  List all genres | POST /genres/ → Create a genre (superadmin only)
]