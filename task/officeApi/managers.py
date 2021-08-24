import datetime

from django.db import models

from django.contrib.auth.models import User


class PlaceTodayManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(start_date__date=datetime.datetime.today().date(),
                                             end_date__date=datetime.datetime.today().date())
