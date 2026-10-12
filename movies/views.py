from django.shortcuts import render  # Django helper — not used here but auto-added by Django when the file was created
from django_filters.rest_framework import DjangoFilterBackend  # Enables URL-based filtering, e.g. /movies/?genres=1
from drf_spectacular.utils import extend_schema  # Decorator that adds metadata for the auto-generated API documentation (Swagger/OpenAPI)
from rest_framework.filters import SearchFilter  # Enables text search via URL, e.g. /movies/?search=inception
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListCreateAPIView  # Pre-built generic views that handle common API patterns (list, detail, create, etc.)
from rest_framework.permissions import AllowAny  # A permission class that lets ANYONE access the endpoint — no login required

from movies.filters import MovieModelFilterset  # Our custom filter class (defined in filters.py) for filtering movies by title/genre
from movies.models import Movie, Genre  # The database models for movies and genres
from movies.serializers import MovieSerializer, GenreSerializer  # The serializers that convert models ↔ JSON
from permissions import IsSuperUser  # Our custom permission class — only allows superadmin users to perform certain actions


# ─────────────────────────────────────────────────────────────────
#  GET /movies/   →  Returns a LIST of all movies (with search & filter support)
#  Anyone can call this — no login needed
# ─────────────────────────────────────────────────────────────────
@extend_schema(tags=['movies'])  # Groups this endpoint under the 'movies' section in Swagger documentation
class MoviesListAPIView(ListAPIView):  # Handles GET /movies/ — ListAPIView only supports GET; it returns a list
    queryset = Movie.objects.all()  # The database query: fetch ALL movie rows — this is the data pool the view works with
    serializer_class = MovieSerializer  # Tells the view to use MovieSerializer to convert each Movie object to JSON
    permission_classes = [AllowAny]  # No authentication required — anyone (even anonymous users) can list movies
    filter_backends = [SearchFilter, DjangoFilterBackend]  # Enables TWO filter systems: (1) text search, (2) URL parameter filters
    search_fields = ['title', 'genres__name']  # SearchFilter will search inside these fields when ?search=... is used; 'genres__name' crosses the relationship to search genre names
    filterset_class = MovieModelFilterset  # DjangoFilterBackend will use our custom MovieModelFilterset class for field-level filters like ?title=inception or ?genres=1


# ─────────────────────────────────────────────────────────────────
#  GET    /movies/<id>   →  Returns ONE specific movie (anyone can view)
#  PUT    /movies/<id>   →  Updates a movie (superadmin only)
#  DELETE /movies/<id>   →  Deletes a movie (superadmin only)
# ─────────────────────────────────────────────────────────────────
@extend_schema(tags=['movies'])  # Groups this endpoint under 'movies' in Swagger documentation
class MoviesDetailAPIView(RetrieveUpdateDestroyAPIView):  # Handles GET/PUT/DELETE for a single movie; RetrieveUpdateDestroyAPIView = detail view
    queryset = Movie.objects.all()  # Data pool: all movies — Django will auto-filter to the one matching the ID in the URL
    serializer_class = MovieSerializer  # Use MovieSerializer to convert the movie object to/from JSON
    lookup_url_kwarg = 'id'  # The URL pattern uses <int:id> — this tells Django to look for the pk using 'id' from the URL, not the default 'pk'
    http_method_names = ['get', 'put', 'delete']  # Only these three HTTP methods are allowed — PATCH (partial update) is deliberately excluded

    def get_permissions(self):  # This method decides which permission rules to apply — it runs on every request
        if self.request.method == "GET":  # If the client is just reading/viewing a movie...
            permission_classes = [AllowAny]  # ...anyone can do it — no login needed
        else:  # If the client is trying to update or delete...
            permission_classes = [IsSuperUser]  # ...only a superadmin is allowed
        return [permission() for permission in permission_classes]  # Instantiate each permission class and return the list — DRF calls .has_permission() on each one



# ─────────────────────────────────────────────────────────────────
#  POST /movies/create   →  Creates a NEW movie (superadmin only)
# ─────────────────────────────────────────────────────────────────
@extend_schema(tags=['movies'])  # Groups this endpoint under 'movies' in Swagger documentation
class MovieCreateAPIView(CreateAPIView):  # Handles POST /movies/create — CreateAPIView only supports POST; it saves a new object
    queryset = Movie.objects.all()  # Data pool (required by DRF even for create views, used internally)
    serializer_class = MovieSerializer  # Uses MovieSerializer to validate and save the incoming JSON body
    permission_classes = [IsSuperUser]  # ONLY a superadmin can create movies — applied to all requests (no per-method logic needed here)



# ─────────────────────────────────────────────────────────────────
#  GET  /genres/   →  Lists all genres (anyone)
#  POST /genres/   →  Creates a new genre (superadmin only)
# ─────────────────────────────────────────────────────────────────
@extend_schema(tags=['movies'])  # Groups this endpoint under 'movies' in Swagger documentation
class GenresListView(ListCreateAPIView):  # Handles GET and POST on /genres/ — ListCreateAPIView supports both listing AND creating in one view
    queryset = Genre.objects.all()  # Data pool: all genre rows from the database
    serializer_class = GenreSerializer  # Uses GenreSerializer to convert Genre objects ↔ JSON

    def get_permissions(self):  # Decides permissions dynamically depending on the HTTP method
        if self.request.method == "GET":  # If someone is just reading the genre list...
            permission_classes = [AllowAny]  # ...no login required
        else:  # If someone is trying to POST (create a new genre)...
            permission_classes = [IsSuperUser]  # ...must be a superadmin
        return [permission() for permission in permission_classes]  # Instantiate and return the list of permission objects

# ─────────────────────────────────────────────────────────────────
#  GET    /genres/<id>   →  Returns ONE specific genre (anyone)
#  PUT    /genres/<id>   →  Updates a genre (superadmin only)
#  DELETE /genres/<id>   →  Deletes a genre (superadmin only)
# ─────────────────────────────────────────────────────────────────
class GenresDetailView(RetrieveUpdateDestroyAPIView):  # Handles GET/PUT/DELETE for a single genre by its ID
    queryset = Genre.objects.all()  # Data pool: all genres — Django will find the one matching the URL ID
    serializer_class = GenreSerializer  # Uses GenreSerializer to convert the Genre object to/from JSON
    lookup_url_kwarg = 'id'  # The URL uses <int:id>, so tell Django to use 'id' from the URL to look up the genre row

    def get_permissions(self):  # Decides permissions dynamically depending on the HTTP method
        if self.request.method == "GET":  # If just viewing a genre...
            permission_classes = [AllowAny]  # ...anyone can view it
        else:  # If updating or deleting...
            permission_classes = [IsSuperUser]  # ...must be a superadmin
        return [permission() for permission in permission_classes]  # Instantiate and return the list of permission objects









