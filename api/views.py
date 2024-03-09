from django.core.paginator import EmptyPage, Paginator
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Movie
from api.movie_serializer import MovieSerializer, TitleSerializer


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
