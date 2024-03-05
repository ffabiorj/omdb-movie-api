from django.core.paginator import EmptyPage, Paginator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Movie
from api.movie_serializer import MovieSerializer


class GetMovies(APIView):
    """A class base view to get movies"""

    def get(self, request):
        movies = Movie.objects.objects.all().order_by("title")
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
