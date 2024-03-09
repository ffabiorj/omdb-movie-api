from random import randint

from django.core.paginator import EmptyPage, Paginator
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Movie
from api.movie_serializer import IdSerializer, MovieSerializer, TitleSerializer
from api.services.fetch_movie import get_imdb_id_movie_list, get_movie


class PopulateDatabase(APIView):
    """A class view for populate database with 100 mvoies"""

    def get(self, request):
        movies = Movie.objects.count()
        if movies >= 100:
            return Response("The database already has 100 movies")
        quantity = 0
        movie_id_list = get_imdb_id_movie_list()
        while quantity < 100:
            id_movie = movie_id_list[randint(0, 99)]
            try:
                movie = get_movie(id_movie)
            except Exception:
                continue
            movie = movie.json()
            movie_dict = {
                "title": movie.get("Title"),
                "year": movie.get("Year"),
                "rated": movie.get("Rated"),
                "released": movie.get("Released"),
                "runtime": movie.get("Runtime"),
                "genre": movie.get("Genre"),
                "director": movie.get("Director"),
                "writer": movie.get("Writer"),
                "actors": movie.get("Actors"),
                "plot": movie.get("Plot"),
                "language": movie.get("Language"),
                "country": movie.get("Country"),
                "awards": movie.get("Awards"),
                "poster": movie.get("Poster"),
                "ratings": movie.get("Ratings"),
                "metascore": movie.get("Metascore"),
                "imdbrating": movie.get("imdbRating"),
                "imdbvotes": movie.get("imdbVotes"),
                "imdbid": movie.get("imdbID"),
                "type": movie.get("Type"),
                "dvd": movie.get("DVD"),
                "boxoffice": movie.get("BoxOffice"),
                "production": movie.get("Production"),
                "website": movie.get("Website"),
                "response": movie.get("Response"),
            }
            movie_serializer = MovieSerializer(data=movie_dict)
            movie_serializer.is_valid(raise_exception=True)
            movie_serializer.save()
            quantity += 1
        return Response("Insertion complete", status=status.HTTP_201_CREATED)


class GetMovies(APIView):
    """A class base view to get movies"""

    def get(self, request):
        movies = Movie.objects.all().order_by("title")
        if not movies:
            return Response([])

        page_number = request.query_params.get("page_number", 1)
        page_size = request.query_params.get("page_size", 10)
        paginator = Paginator(movies, page_size)
        try:
            movies = paginator.page(page_number)
        except EmptyPage:
            return Response("Page not found")
        serializer = MovieSerializer(movies, many=True)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        response["total"] = paginator.count
        response["number_pages"] = paginator.num_pages
        response["per_page"] = paginator.per_page
        response["page_number"] = page_number

        return response


class GetMovie(APIView):
    """A class base view to get a movie"""

    def get(self, request):
        title = TitleSerializer(data=request.query_params)
        title.is_valid(raise_exception=True)
        title = title.validated_data["title"]
        try:
            movie = Movie.objects.get(title=title)
        except Movie.DoesNotExist:
            return Response("Movie not found", status=status.HTTP_404_NOT_FOUND)
        return Response(MovieSerializer(movie).data, status=status.HTTP_200_OK)


class AddMovie(APIView):
    """A class base view for add a movie"""

    def post(self, request):
        movie = MovieSerializer(data=request.data)
        try:
            movie.is_valid(raise_exception=True)
        except ValidationError:
            return Response(
                {"invalid_data": request.data}, status=status.HTTP_400_BAD_REQUEST
            )
        movie.save()
        return Response(movie.validated_data, status=status.HTTP_201_CREATED)


class DeleteMovie(APIView):
    """A class base view to delete a movie"""

    def delete(self, request):
        id = IdSerializer(data=request.data)
        id.is_valid(raise_exception=True)
        id = id.validated_data["id"]
        try:
            movie = Movie.objects.get(id=id)
        except Movie.DoesNotExist:
            return Response("Movie not found", status=status.HTTP_404_NOT_FOUND)
        movie.delete()
        return Response(status=status.HTTP_200_OK)
