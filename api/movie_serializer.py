from rest_framework import serializers

from api.models import Movie


class RatingsSerializer(serializers.Serializer):
    source = serializers.CharField(required=False, allow_null=True)
    value = serializers.CharField(required=False, allow_null=True)


class MovieSerializer(serializers.Serializer):

    title = serializers.CharField(required=False, allow_null=True)
    year = serializers.CharField(required=False, allow_null=True)
    rated = serializers.CharField(required=False, allow_null=True)
    released = serializers.CharField(required=False, allow_null=True)
    runtime = serializers.CharField(required=False, allow_null=True)
    genre = serializers.CharField(required=False, allow_null=True)
    director = serializers.CharField(required=False, allow_null=True)
    writer = serializers.CharField(required=False, allow_null=True)
    actors = serializers.CharField(required=False, allow_null=True)
    plot = serializers.CharField(required=False, allow_null=True)
    language = serializers.CharField(required=False, allow_null=True)
    country = serializers.CharField(required=False, allow_null=True)
    awards = serializers.CharField(required=False, allow_null=True)
    poster = serializers.CharField(required=False, allow_null=True)
    ratings = RatingsSerializer(required=False, allow_null=True, many=True)
    metascore = serializers.CharField(required=False, allow_null=True)
    imdbrating = serializers.CharField(required=False, allow_null=True)
    imdbvotes = serializers.CharField(required=False, allow_null=True)
    imdbid = serializers.CharField(required=False, allow_null=True)
    type = serializers.CharField(required=False, allow_null=True)
    dvd = serializers.CharField(required=False, allow_null=True)
    boxoffice = serializers.CharField(required=False, allow_null=True)
    production = serializers.CharField(required=False, allow_null=True)
    website = serializers.CharField(required=False, allow_null=True)
    response = serializers.CharField(required=False, allow_null=True)

    def to_internal_value(self, data):
        if "ratings" in data:
            ratings = data["ratings"]
            ratings_list = []
            for rating in ratings:
                ratings_list.append(
                    {"source": rating["Source"], "value": rating["Value"]}
                )

            ratings = RatingsSerializer(data=ratings_list, many=True)
            ratings.is_valid(raise_exception=True)
            data["ratings"] = ratings.validated_data
            return data
        return data

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)