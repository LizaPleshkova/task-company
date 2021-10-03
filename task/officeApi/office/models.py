from django.contrib.auth.models import User
from django.db import models


class Office(models.Model):
    name = models.CharField("Name of office", max_length=50, null=True, blank=True)
    address = models.CharField("Address of office", max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Room(models.Model):
    number_room = models.IntegerField(null=True, blank=True)
    office = models.ForeignKey(Office, on_delete=models.SET_NULL, null=True, blank=True, related_name='office_rooms')
    counts_seats = models.IntegerField("Numbers of seats", null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.number_room} - [{self.office.id} - {self.office.name}] - {self.counts_seats}'


class Place(models.Model):
    number_place = models.IntegerField(null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='room_places')

    def __str__(self):
        return f'{self.id} - {self.number_place} - {self.room}'


class UserPlace(models.Model):
    # todays_place = PlaceTodayManager()
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='user')
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True, related_name='place')
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.user.username} - [{self.place.number_place}-{self.place.room.number_room}] - [{self.start_date}- {self.end_date}]'
