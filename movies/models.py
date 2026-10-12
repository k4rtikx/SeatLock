from django.db import models  # Imports Django's database tools — needed to work with models
from django.db.models import (  # Imports specific field types we will use as columns in our database tables
    Model,                 # Base class — every model (database table) must inherit from this
    CharField,             # A short text field (with a max_length limit)
    TextField,             # A long unlimited text field (for descriptions, plots, etc.)
    ImageField,            # Stores the PATH to an uploaded image file on disk
    PositiveIntegerField,  # A whole number that must be 0 or greater
    ManyToManyField,       # Links one model to MULTIPLE rows of another model (e.g. movie ↔ many genres)
    DateField,             # Stores a calendar date: YYYY-MM-DD
    DateTimeField,         # Stores date + time: YYYY-MM-DD HH:MM:SS
    TextChoices,           # Helper for creating a fixed list of allowed text values (like an enum)
    URLField,              # A text field that validates the value is a proper URL (http://...)
    DecimalField,          # A number with decimal places, e.g. 8.4 for a movie rating
)


# ─────────────────────────────────────────────────────────────────
#  GENRE MODEL  →  Becomes the database table: movies_genre
#  Purpose: stores category names like Action, Comedy, Thriller
# ─────────────────────────────────────────────────────────────────
class Genre(Model):  # Defines the Genre table; inheriting Model tells Django to manage it in the database
    name = CharField(max_length=50, unique=True)  # Column: genre name (e.g. "Action"), max 50 chars; unique=True means NO two rows can have the same name

    def __str__(self):  # Special method — Django/Python calls this when it needs to display this object as text
        return self.name  # e.g. prints "Action" instead of the ugly default "Genre object (1)"


# ─────────────────────────────────────────────────────────────────
#  MOVIE MODEL  →  Becomes the database table: movies_movie
#  Purpose: stores all information about a single movie
# ─────────────────────────────────────────────────────────────────
class Movie(Model):  # Defines the Movie table; each row = one movie in the cinema system

    class AgeRating(TextChoices):  # Inner class: a fixed list of allowed age rating values — only these 5 are valid
        G    = 'G',     'General'                      # Stored as 'G'     in DB | shown as 'General' in admin/API
        PG   = 'PG',    'Parental Guidance'            # Stored as 'PG'    in DB
        PG13 = 'PG-13', 'Parents Strongly Cautioned'  # Stored as 'PG-13' in DB
        R    = 'R',     'Restricted'                   # Stored as 'R'     in DB
        NC17 = 'NC-17', 'Adults Only'                  # Stored as 'NC-17' in DB

    title            = CharField(max_length=255)                               # Column: the movie title, e.g. "Inception"; up to 255 characters; REQUIRED
    description      = TextField()                                             # Column: full plot summary; no length limit; REQUIRED
    poster           = ImageField(upload_to='movie_posters/', blank=True, null=True)     # Column: portrait poster image; file saved in media/movie_posters/; OPTIONAL (blank & null allowed)
    backdrop         = ImageField(upload_to='movie_backdrops/', blank=True, null=True)   # Column: wide landscape banner (different from portrait poster — used in hero sections); saved in media/movie_backdrops/; OPTIONAL
    trailer_url      = URLField(blank=True)                                    # Column: link to YouTube/official trailer; must be a valid URL; OPTIONAL
    duration_minutes = PositiveIntegerField()                                  # Column: length of movie in minutes (e.g. 148); must be a positive integer; REQUIRED
    genres           = ManyToManyField('movies.Genre')                         # Relationship: one movie can belong to MANY genres — stored in a separate join table automatically by Django
    release_date     = DateField()                                             # Column: the date the movie released, e.g. 2024-07-19; REQUIRED
    age_rating       = CharField(max_length=10, choices=AgeRating)             # Column: age rating stored as text; only values from AgeRating above are accepted; REQUIRED
    rating           = DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)  # Column: audience score like 8.4 or 7.0; 3 digits total, 1 after decimal; OPTIONAL
    created_at       = DateTimeField(auto_now_add=True)                        # Column: timestamp auto-set to NOW when movie is first created — Django never lets you change this manually

    class Meta:  # Inner class to set extra database-level settings for Movie
        ordering = ['-release_date']  # Default sort: newest movies first (the '-' means descending / reverse order)

    def __str__(self):  # When you print a Movie object, show its title instead of "Movie object (1)"
        return self.title  # e.g. prints "Inception"
