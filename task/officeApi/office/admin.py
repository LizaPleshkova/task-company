import datetime
from django.contrib import admin
from django import forms
from .models import (
    Office, Room, Place, UserPlace
)


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = '__all__'

    def clean(self):
        up_count = Place.objects.filter(room=int(self.data.get('room'))).count()
        print(up_count)
        room_place_count = Room.objects.get(id=int(self.data.get('room'))).counts_seats
        if up_count > room_place_count:
            raise forms.ValidationError("there is a limited number of seats in the room")


class UserPlaceForm(forms.ModelForm):
    class Meta:
        model = UserPlace
        fields = '__all__'

    def clean(self):
        start_data = self.cleaned_data['start_date']
        end_data = self.cleaned_data['end_date']
        if start_data.date() < datetime.date.today() or end_data.date() < datetime.date.today():
            raise forms.ValidationError("the date for booking a seat is incorrect!")
        if start_data.time() < datetime.time(9) or end_data.time() > datetime.time(18):
            raise forms.ValidationError("the office is closed at this time!")
        return self.cleaned_data


class UserPlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'place', 'start_date', 'end_date',)
    list_filter = ['id', 'user', 'place']
    search_fields = ['user', 'place', ]
    form = UserPlaceForm


class OfficeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_filter = ['id']
    search_fields = ['name']


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'number_room', 'office', 'counts_seats',)
    list_filter = ['number_room', 'office', ]
    search_fields = ['office', ]


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'number_place', 'room',)
    # list_display = ('id', 'room',)
    list_filter = ['id', 'room', ]
    search_fields = ['room', ]
    form = PlaceForm


admin.site.register(Office, OfficeAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(UserPlace, UserPlaceAdmin)
