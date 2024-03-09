import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Movie
from api.movie_serializer import MovieSerializer


class MovieTestCase(APITestCase):
    def setUp(self):
        with open("/home/fabio/workspace/omdb-movie-api/api/tests/movie.json") as file:
            self.movie = file.read()
        self.json_movie = json.loads(self.movie)
        list_movies = []
        movie = {
            "title": self.json_movie.get("Title"),
            "year": self.json_movie.get("Year"),
            "rated": self.json_movie.get("Rated"),
            "released": self.json_movie.get("Released"),
            "runtime": self.json_movie.get("Runtime"),
            "genre": self.json_movie.get("Genre"),
            "director": self.json_movie.get("Director"),
            "writer": self.json_movie.get("Writer"),
            "actors": self.json_movie.get("Actors"),
            "plot": self.json_movie.get("Plot"),
            "language": self.json_movie.get("Language"),
            "country": self.json_movie.get("Country"),
            "awards": self.json_movie.get("Awards"),
            "poster": self.json_movie.get("Poster"),
            "ratings": self.json_movie.get("Ratings"),
            "metascore": self.json_movie.get("Metascore"),
            "imdbrating": self.json_movie.get("imdbRating"),
            "imdbvotes": self.json_movie.get("imdbVotes"),
            "imdbid": self.json_movie.get("imdbID"),
            "type": self.json_movie.get("Type"),
            "dvd": self.json_movie.get("DVD"),
            "boxoffice": self.json_movie.get("BoxOffice"),
            "production": self.json_movie.get("Production"),
            "website": self.json_movie.get("Website"),
            "response": self.json_movie.get("Response"),
        }
        for i in range(1, 12):
            list_movies.append(
                {
                    "title": f"Test {i}",
                    "year": "1988",
                    "rated": self.json_movie.get("Rated"),
                    "released": self.json_movie.get("Released"),
                    "runtime": self.json_movie.get("Runtime"),
                    "genre": self.json_movie.get("Genre"),
                    "director": self.json_movie.get("Director"),
                    "writer": self.json_movie.get("Writer"),
                    "actors": self.json_movie.get("Actors"),
                    "plot": self.json_movie.get("Plot"),
                    "language": self.json_movie.get("Language"),
                    "country": self.json_movie.get("Country"),
                    "awards": self.json_movie.get("Awards"),
                    "poster": self.json_movie.get("Poster"),
                    "ratings": self.json_movie.get("Ratings"),
                    "metascore": self.json_movie.get("Metascore"),
                    "imdbrating": self.json_movie.get("imdbRating"),
                    "imdbvotes": self.json_movie.get("imdbVotes"),
                    "imdbid": self.json_movie.get("imdbID") + str(i),
                    "type": self.json_movie.get("Type"),
                    "dvd": self.json_movie.get("DVD"),
                    "boxoffice": self.json_movie.get("BoxOffice"),
                    "production": self.json_movie.get("Production"),
                    "website": self.json_movie.get("Website"),
                    "response": self.json_movie.get("Response"),
                }
            )
        list_movies.append(movie)
        serializer_movie = MovieSerializer(data=list_movies, many=True)
        serializer_movie.is_valid()
        serializer_movie.save()

    def test_should_return_empty_list(self):
        Movie.objects.all().delete()
        url = reverse("get-movies")
        response = self.client.get(url)
        self.assertEqual(response.data, [])

    def test_get_movies(self):
        url = reverse("get-movies")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0]["title"], "Guardians of the Galaxy Vol. 2")
        self.assertEqual(response.data[0]["year"], "2017")
        self.assertEqual(response.data[0]["rated"], "PG-13")
        self.assertEqual(response.data[0]["released"], "05 May 2017")
        self.assertTrue(response.data[0]["runtime"])
        self.assertTrue(response.data[0]["genre"])
        self.assertEqual(response.data[0]["director"], "James Gunn")
        self.assertTrue(response.data[0]["writer"])
        self.assertTrue(response.data[0]["actors"])
        self.assertTrue(response.data[0]["plot"])
        self.assertTrue(response.data[0]["language"])
        self.assertTrue(response.data[0]["country"])
        self.assertTrue(response.data[0]["awards"])
        self.assertTrue(response.data[0]["poster"])
        self.assertTrue(response.data[0]["ratings"])
        self.assertTrue(response.data[0]["metascore"])
        self.assertTrue(response.data[0]["imdbrating"])
        self.assertTrue(response.data[0]["imdbvotes"])
        self.assertTrue(response.data[0]["imdbid"])
        self.assertTrue(response.data[0]["type"])
        self.assertTrue(response.data[0]["dvd"])
        self.assertTrue(response.data[0]["boxoffice"])
        self.assertTrue(response.data[0]["production"])
        self.assertTrue(response.data[0]["website"])
        self.assertTrue(response.data[0]["response"])

    def test_get_movie_order_by_title(self):
        url = reverse("get-movies")
        response = self.client.get(url)
        self.assertEqual(response.data[0]["title"], "Guardians of the Galaxy Vol. 2")
        self.assertEqual(response.data[0]["id"], 12)
        self.assertEqual(response.data[1]["title"], "Test 1")

    def test_get_pagination_info(self):
        url = reverse("get-movies")
        response = self.client.get(url)
        self.assertEqual(int(response["total"]), 12)
        self.assertEqual(int(response["number_pages"]), 2)
        self.assertEqual(int(response["per_page"]), 10)

    def test_get_response_by_change_page_size(self):
        url = reverse("get-movies")
        response = self.client.get(url, {"page_size": 3})
        self.assertEqual(int(response["total"]), 12)
        self.assertEqual(int(response["number_pages"]), 4)
        self.assertEqual(int(response["per_page"]), 3)

    def test_get_page_by_number(self):
        url = reverse("get-movies")
        response = self.client.get(url, {"page_size": 3, "page_number": 2})
        self.assertEqual(int(response["page_number"]), 2)

    def test_should_raise_error_with_page_number_not_exist(self):
        url = reverse("get-movies")
        response = self.client.get(url, {"page_number": 100})
        self.assertEqual(response.data, "Page not found")

    def test_create_movie(self):
        movie = {
            "title": "Test 100",
            "year": self.json_movie.get("Year"),
            "rated": self.json_movie.get("Rated"),
            "released": self.json_movie.get("Released"),
            "runtime": self.json_movie.get("Runtime"),
            "genre": self.json_movie.get("Genre"),
            "director": self.json_movie.get("Director"),
            "writer": self.json_movie.get("Writer"),
            "actors": self.json_movie.get("Actors"),
            "plot": self.json_movie.get("Plot"),
            "language": self.json_movie.get("Language"),
            "country": self.json_movie.get("Country"),
            "awards": self.json_movie.get("Awards"),
            "poster": self.json_movie.get("Poster"),
            "ratings": self.json_movie.get("Ratings"),
            "metascore": self.json_movie.get("Metascore"),
            "imdbrating": self.json_movie.get("imdbRating"),
            "imdbvotes": self.json_movie.get("imdbVotes"),
            "imdbid": self.json_movie.get("imdbID"),
            "type": self.json_movie.get("Type"),
            "dvd": self.json_movie.get("DVD"),
            "boxoffice": self.json_movie.get("BoxOffice"),
            "production": self.json_movie.get("Production"),
            "website": self.json_movie.get("Website"),
            "response": self.json_movie.get("Response"),
        }
        url = reverse("add-movie")
        response = self.client.post(url, movie, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Test 100")

    def test_try_create_a_movie_and_raise_exception(self):
        movie = {"test": "test"}
        url = reverse("add-movie")
        response = self.client.post(url, movie, format="json")
        self.assertEqual(response.data, {"invalid_data": {"test": "test"}})
