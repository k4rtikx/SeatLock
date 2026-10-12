from django_filters import CharFilter  # A filter type that filters by a text/character field
from django_filters.rest_framework import FilterSet  # Base class for creating custom filter sets that work with DRF views

from movies.models import Movie  # Imports the Movie model so we know which fields we can filter on


# ─────────────────────────────────────────────────────────────────
#  MovieModelFilterset
#  Purpose: defines HOW URL query params map to database filters
#  Example: GET /movies/?title=inc  →  finds movies with 'inc' anywhere in the title (case-insensitive)
#           GET /movies/?genres=1   →  finds movies that belong to genre with ID=1
# ─────────────────────────────────────────────────────────────────
class MovieModelFilterset(FilterSet):  # Defines a custom filterset for the Movie model; DjangoFilterBackend in views.py uses this class
    title = CharFilter(lookup_expr='icontains')  # Overrides the default title filter: use 'icontains' (case-insensitive partial match) instead of exact match. So ?title=inc matches 'Inception', 'Invincible', etc.

    class Meta:  # Configuration for this filterset
        model = Movie  # Tells FilterSet which model's table this works on
        fields = ['title', 'genres']  # Which URL params are allowed as filters — 'title' uses our custom CharFilter above; 'genres' uses the default (exact match by ID)