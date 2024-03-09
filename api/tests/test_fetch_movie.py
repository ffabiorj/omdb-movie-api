import json
from unittest.mock import patch

import httpx
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.services.fetch_movie import get_imdb_id_movie_list, get_movie


class GetListTitleImdbTestCase(APITestCase):

    def test_sould_return_a_list_ids(self):
        self.assertTrue(get_imdb_id_movie_list())
        self.assertEqual(len(get_imdb_id_movie_list()), 100)


class FetchMovieTestCase(APITestCase):

    def setUp(self):
        with open("/home/fabio/workspace/omdb-movie-api/api/tests/movie.json") as file:
            self.movie = file.read()

    # unitary test
    @patch("httpx.get")
    def test_get_one_movie_by_id_imdb(self, mocke_movie):
        return_value = json.loads(self.movie)
        mocke_movie.return_value = return_value
        response = get_movie(imdb_number="tt000000")

        title = "Guardians of the Galaxy Vol. 2"
        year = "2017"
        rated = "PG-13"
        released = "05 May 2017"
        runtime = "136 min"
        genre = "Action, Adventure, Comedy"
        director = "James Gunn"

        self.assertEqual(response["Title"], title)
        self.assertEqual(response["Year"], year)
        self.assertEqual(response["Rated"], rated)
        self.assertEqual(response["Released"], released)
        self.assertEqual(response["Runtime"], runtime)
        self.assertEqual(response["Genre"], genre)
        self.assertEqual(response["Director"], director)

    @patch("httpx.get")
    def test_populate_database(self, mocke_movie):
        mocke_movie.return_value = httpx.Response(200, json=json.loads(self.movie))
        url = reverse("populate-database")
        response = self.client.get(url)
        self.assertEqual(response.data, "Insertion complete")

    @patch("api.models.Movie.objects.count")
    def test_should_response_already_has_100_movies(self, mock_value):
        mock_value.return_value = 100
        url = reverse("populate-database")
        response = self.client.get(url)
        self.assertEqual(response.data, "The database already has 100 movies")
