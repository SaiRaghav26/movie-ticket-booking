from rest_framework import serializers
from .models import Movie,Theatre,Screen,ShowTimings,Seat

class MovieSerializer(serializers.ModelSerializer):
    poster_url = serializers.SerializerMethodField()
    banner_url = serializers.SerializerMethodField()
    class Meta:
        model=Movie
        fields='__all__'

    def get_poster_url(self,obj):
        return obj.posters.url if obj.posters else None
    
    def get_banner_url(self,obj):
        return obj.banners.url if obj.banners else None
    

class TheatreSerializer(serializers.ModelSerializer):
    movies=MovieSerializer(many=True,read_only=True)

    class Meta:
        model=Theatre
        fields='__all__'


class ScreenSerializer(serializers.ModelSerializer):
    theatre=TheatreSerializer(read_only=True)

    class Meta:
        model=Screen
        fields='__all__'
    

class ShowTimingsSerializer(serializers.ModelSerializer):
    theatre=TheatreSerializer(read_only=True)
    movie=MovieSerializer(read_only=True)
    screen=ScreenSerializer(read_only=True)

    class Meta:
        model=ShowTimings
        fields='__all__'

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model=Seat
        fields='__all__'