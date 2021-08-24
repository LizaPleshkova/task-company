import datetime
import json

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.migrations import serializer
from django.db.models import Q
from rest_framework import serializers
from .models import (
    Office, Room, Place, UserPlace
)

User = get_user_model()


class UserAllPlacesSerializer(serializers.ModelSerializer):
    places = serializers.ListField()

    class Meta:
        model = User
        fields = ['id', 'username', 'places']


class BookingPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPlace
        fields = '__all__'

    def validate(self, data):
        """ checking quantity seller's stocks """
        try:
            place_id = data.get('place')
            start = data.get('start_date')
            end = data.get('end_date')

            # проверяет все user place, которые в тот же день, но не в тоже время
            up_free = UserPlace.objects.filter(Q(start_date__date=start.date(), end_date__date=end.date()))

            if start.date() < datetime.datetime.today().date() or end.date() < datetime.datetime.today().date():
                raise serializers.ValidationError('the date for booking a seat is incorrect!', code='invalid')
            else:
                for i in up_free:

                    if ((start.time() >= i.start_date.time() and end.time() <= i.end_date.time())
                            or (
                                    (start.time() > i.start_date.time() and start.time() < i.end_date.time())
                                    or (end.time() > i.start_date.time() and end.time() < i.end_date.time()))
                            or (start.time() < i.start_date.time() and end.time() == i.end_date.time())
                    ):
                        raise serializers.ValidationError('This time is already taken', code='invalid')
            return data
        except UserPlace.DoesNotExist or Place.DoesNotExist:
            raise ObjectDoesNotExist('No UserPlace or Place matches the given query')


class UserPlaceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPlace
        fields = ('id', 'place', 'start_date', 'end_date')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        pl_id = representation['id']
        room = Room.objects.get(room_places=pl_id)
        representation['room'] = RoomForPlaceSerializer(room).data
        return representation


class PlaceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class OfficeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = '__all__'


class RoomForPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'number_room', 'office')


class RoomSerializer(serializers.ModelSerializer):
    counts_seats = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = '__all__'

    def get_counts_seats(self, obj):
        return obj.room_places.count()
