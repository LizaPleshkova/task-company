from django.db import migrations
from django.db import migrations
from office import apps


def delete_user_places(apps, schema_editor):
    UserPlace = apps.get_model('office', 'UserPlace')
    user_places = UserPlace.objects.all().delete()


def delete_places(apps, schema_editor):
    Place = apps.get_model('office', 'Place')
    places = Place.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('office', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(delete_user_places),
        migrations.RunPython(delete_places),
    ]
