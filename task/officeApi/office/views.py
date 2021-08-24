from datetime import datetime

from django.contrib.postgres.aggregates import ArrayAgg
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import datetime
from .models import (
    Office, Room, Place, UserPlace, User
)
from .serializers import PlaceListSerializer, RoomSerializer, OfficeListSerializer, BookingPlaceSerializer, \
    UserPlaceListSerializer, UserAllPlacesSerializer


class PlaceView(ListModelMixin, RetrieveModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_classes_by_action = {
        'retrieve': PlaceListSerializer,
        'list': PlaceListSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes_by_action.get(self.action, PlaceListSerializer)

    def get_queryset(self, *args, **kwargs):
        return Place.objects.all()

    @action(methods=['get'], detail=False, url_path='free-places')
    def free_places_definite_date(self, request):
        # занятые места в определенный день
        up_definite = UserPlace.objects.exclude(
            Q(start_date__date=datetime.date(2021, 8, 19)),
            Q(end_date__date=datetime.date(2021, 8, 19))
        ).values('place')

        # все места, которые свободны в определенный день, их id
        place_free = Place.objects.filter(id__in=up_definite)

        serializer = PlaceListSerializer(place_free, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='user-places')
    def user_places(self, request):
        user_places = User.objects.annotate(places=ArrayAgg('user__place', distinct=True))
        serializer = UserAllPlacesSerializer(user_places, many=True)
        return Response(serializer.data)


class BookingPlaceView(ListModelMixin, RetrieveModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)

    serializer_classes_by_action = {
        'create': BookingPlaceSerializer,
        'retrieve': UserPlaceListSerializer,
        'list': UserPlaceListSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes_by_action.get(self.action, UserPlaceListSerializer)

    def get_queryset(self, *args, **kwargs):
        return UserPlace.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            request.data['user'] = request.user.id
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except ObjectDoesNotExist as e:
            return Response(getattr(e, 'message', repr(e)), status=status.HTTP_400_BAD_REQUEST)


class RoomView(ListModelMixin, RetrieveModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = RoomSerializer

    def get_queryset(self, *args, **kwargs):
        return Room.objects.all()


class OfficeView(ListModelMixin, RetrieveModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = OfficeListSerializer

    def get_queryset(self, *args, **kwargs):
        return Office.objects.all()


