import httpx
from django.conf import settings

OMDB_API_KEY = settings.OMDB_API_KEY


def get_imdb_id_movie_list() -> list:
    with open("movies") as file:
        movies = file.read().split("\n")[:-1]
    return movies


def get_movie(imdb_number: str):
    params = {"apikey": OMDB_API_KEY, "i": imdb_number}
    response = httpx.get("https://www.omdbapi.com/", params=params)
    return response
