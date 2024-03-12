# omdb-movie-api

## How to run locally?

1. Clone the repository.
2. Create a virtualenv with python 3.10
3. Active the virtualenv.
4. Instalall the dependencies.
5. setting .env
6. Execute tests.

```
git clone git@github.com:ffabiorj/omdb-movie-api.git
cd omdb-movie-api
python3 -m venv .venv
sourch .venv/bin/activate
pip install -r requirements.txt
cp contrib/env-sample .env
python manage.py test
```

## 🧪 How to test in production

- To get all the movies.
- if you want to get movies from other pages, you need to use query params in the final URL (?page_number=2) or ?page_size=20, to change the quantity the API returns. 
```
curl --location 'https://omdb-api-movie-416922.oa.r.appspot.com/api/movies/'
```

To filter a movie by title.
```
curl --location 'https://omdb-api-movie-416922.oa.r.appspot.com/api/movies/?title=3+Idiots'
```

To add a movie.
```
curl --location 'https://omdb-api-movie-416922.oa.r.appspot.com/api/add-movie/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "4 Idiots",
    "year": "2009",
    "rated": "PG-13",
    "released": "25 Dec 2009",
    "runtime": "170 min",
    "genre": "Comedy, Drama",
    "director": "Rajkumar Hirani",
    "writer": "Abhijat Joshi, Rajkumar Hirani, Vidhu Vinod Chopra",
    "actors": "Aamir Khan, Madhavan, Mona Singh",
    "plot": "Two friends are searching for their long lost companion. They revisit their college days and recall the memories of their friend who inspired them to think differently, even as the rest of the world called them \"idiots\".",
    "language": "Hindi, English",
    "country": "India",
    "awards": "64 wins & 30 nominations",
    "poster": "https://m.media-amazon.com/images/M/MV5BNTkyOGVjMGEtNmQzZi00NzFlLTlhOWQtODYyMDc2ZGJmYzFhXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg",
    "ratings": [
        {
            "Source": "Internet Movie Database",
            "Value": "8.4/10"
        },
        {
            "Source": "Rotten Tomatoes",
            "Value": "100%"
        },
        {
            "Source": "Metacritic",
            "Value": "67/100"
        }
    ],
    "metascore": "67",
    "imdbrating": "8.4",
    "imdbvotes": "429,262",
    "imdbid": "tt1187043",
    "type": "movie",
    "dvd": "29 Nov 2016",
    "boxoffice": "$6,532,874",
    "production": "N/A",
    "website": "N/A",
    "response": "True"
}'
```

To delete a movie, you must be logged in.

```
curl --location --request DELETE 'https://omdb-api-movie-416922.oa.r.appspot.com/api/delete-movie/?id=20' \
--header 'Authorization: Token 2e33a758f15caaf78c11f78f36ef1416b94f9124'
```
To create a user e.g
```
curl --location 'https://omdb-api-movie-416922.oa.r.appspot.com/api/signup/' \
--header 'Content-Type: application/json' \
--data '{"username": "teste", "password": "teste"}'
```
When you already have a username, you can log in to generate a token number

```
curl --location 'https://omdb-api-movie-416922.oa.r.appspot.com/api/login/' \
--header 'Content-Type: application/json' \
--data '{"username": "teste", "password": "teste"}'
```

