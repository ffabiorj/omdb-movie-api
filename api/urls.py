from django.urls import path

from api import views as view

urlpatterns = [
    path("movies", view.GetMovies.as_view(), name="get-movies"),
    path("add-movie", view.AddMovie.as_view(), name="add-movie"),
]
