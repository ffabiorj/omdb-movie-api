from django.db import models

# Create your models here.


class Movie(models.Model):

    title = models.CharField(max_length=200)
    year = models.CharField(max_length=10)
    rated = models.CharField(max_length=100)
    released = models.CharField(max_length=50)
    runtime = models.CharField(max_length=50)
    genre = models.CharField(max_length=100)
    director = models.CharField(max_length=200)
    writer = models.CharField(max_length=200)
    actors = models.TextField()
    plot = models.TextField()
    language = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    awards = models.CharField(max_length=200)
    poster = models.TextField()
    ratings = models.JSONField()
    metascore = models.CharField(max_length=20)
    imdbrating = models.CharField(max_length=10)
    imdbvotes = models.CharField(max_length=50)
    imdbid = models.CharField(max_length=20)
    type = models.CharField(max_length=10)
    dvd = models.CharField(max_length=50)
    boxoffice = models.CharField(max_length=200)
    production = models.CharField(max_length=100)
    website = models.TextField()
    response = models.CharField(max_length=10)

    def __repr__(self):
        return f"Title: {self.title}"
