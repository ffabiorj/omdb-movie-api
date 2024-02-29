import json

from rest_framework.test import APITestCase

from api.models import Movie
from api.movie_serializer import MovieSerializer


class SaveMovieTestCase(APITestCase):
    def setUp(self):
        with open("/home/fabio/workspace/omdb-movie-api/api/tests/movie.json") as file:
            self.movie = file.read()

    def test_save_movie_in_db(self):
        json_movie = json.loads(self.movie)
        movie = {
            "title": json_movie.get("Title"),
            "year": json_movie.get("Year"),
            "rated": json_movie.get("Rated"),
            "released": json_movie.get("Released"),
            "runtime": json_movie.get("Runtime"),
            "genre": json_movie.get("Genre"),
            "director": json_movie.get("Director"),
            "writer": json_movie.get("Writer"),
            "actors": json_movie.get("Actors"),
            "plot": json_movie.get("Plot"),
            "language": json_movie.get("Language"),
            "country": json_movie.get("Country"),
            "awards": json_movie.get("Awards"),
            "poster": json_movie.get("Poster"),
            "ratings": json_movie.get("Ratings"),
            "metascore": json_movie.get("Metascore"),
            "imdbrating": json_movie.get("imdbRating"),
            "imdbvotes": json_movie.get("imdbVotes"),
            "imdbid": json_movie.get("imdbID"),
            "type": json_movie.get("Type"),
            "dvd": json_movie.get("DVD"),
            "boxoffice": json_movie.get("BoxOffice"),
            "production": json_movie.get("Production"),
            "website": json_movie.get("Website"),
            "response": json_movie.get("Response"),
        }

        serializer_movie = MovieSerializer(data=movie)
        serializer_movie.is_valid()
        serializer_movie.save()
        count = Movie.objects.count()
        self.assertEqual(count, 1)
