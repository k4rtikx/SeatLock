from rest_framework.relations import PrimaryKeyRelatedField  # A field type that represents a related object using just its ID number (e.g. genre id=3 instead of the full genre object)
from rest_framework.serializers import ModelSerializer  # Base class that auto-generates serializer fields from a Django model — saves you writing each field manually

from movies.models import Movie, Genre  # Imports our two database models so the serializers know which tables/fields to use


# ──────────────────────────────────────────────────────────────────
#  GenreSerializer
#  Converts a Genre database row  →  JSON  (and back)
#  Example output: {"id": 1, "name": "Action"}
# ──────────────────────────────────────────────────────────────────
class GenreSerializer(ModelSerializer):  # Creates a serializer linked to the Genre model; inheriting ModelSerializer auto-builds most of the work
    class Meta:  # Inner class that tells ModelSerializer which model and which fields to include
        model = Genre          # Points to the Genre database table
        fields = ['id', 'name']  # Only expose these two columns in the API response — 'id' is auto-added by Django, 'name' is our custom column


# ──────────────────────────────────────────────────────────────────
#  MovieSerializer
#  Converts a Movie database row  →  JSON  (and back)
#  Example output: {"id": 5, "title": "Inception", "genres": [{"id":1,"name":"Action"}], ...}
# ──────────────────────────────────────────────────────────────────
class MovieSerializer(ModelSerializer):  # Creates a serializer linked to the Movie model
    genres = PrimaryKeyRelatedField(many=True, queryset=Genre.objects.all())  # Override the default genres field: accept a LIST of genre ID numbers on WRITE (e.g. [1, 3]); queryset tells it which genres are valid

    class Meta:  # Configuration for this serializer
        model = Movie  # Points to the Movie database table
        fields = [  # List of columns/fields to include in API input & output
            'id', 'title', 'description', 'poster', 'backdrop', 'trailer_url',  # Basic movie info fields
            'duration_minutes', 'genres', 'release_date', 'age_rating', 'rating', 'created_at',  # More movie detail fields
        ]
        read_only_fields = ['id', 'created_at']  # These two fields are OUTPUT-ONLY — the API will never let a client set or change them

    def to_representation(self, instance):  # This method is called every time a Movie object is CONVERTED TO JSON for a response
        rep = super().to_representation(instance)  # First, let the parent class do its normal job and produce the default JSON dictionary
        rep['genres'] = GenreSerializer(instance.genres.all(), many=True).data  # Then REPLACE the genres field: instead of just [1, 3] (IDs), now return [{"id":1,"name":"Action"}, {"id":3,"name":"Thriller"}] (full objects)
        return rep  # Return the modified JSON dictionary — this is what the API will send back to the client