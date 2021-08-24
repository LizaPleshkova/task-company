from office.models import (
    Office, Room, Place, UserPlace, User
)
from django.db.models import Count, F, Q, Value, Sum
from datetime import datetime
from importlib import reload
import datetime
from django.contrib.postgres.aggregates import ArrayAgg


def test_ex1():
    test_date1 = {
        'start': datetime.datetime.strptime('2021-08-23T08:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
        'end': datetime.datetime.strptime('2021-08-23T09:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    }
    test_date11 = {
        'start': datetime.datetime.strptime('2021-08-23T08:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
        'end': datetime.datetime.strptime('2021-08-23T10:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    }
    test_date2 = {
        'start': datetime.datetime.strptime('2021-08-23T09:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
        'end': datetime.datetime.strptime('2021-08-23T10:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    }
    test_date3 = {
        'start': datetime.datetime.strptime('2021-08-23T10:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
        'end': datetime.datetime.strptime('2021-08-23T11:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    }

    test_date31 = {
        'start': datetime.datetime.strptime('2021-08-23T10:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
        'end': datetime.datetime.strptime('2021-08-23T12:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    }

    test_date3 = {
        'start': datetime.datetime.strptime('2021-08-23T10:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
        'end': datetime.datetime.strptime('2021-08-23T11:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    }

    test_date32 = {
        'start': datetime.datetime.strptime('2021-08-23T12:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
        'end': datetime.datetime.strptime('2021-08-23T14:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    }

    test_date33 = {
        'start': datetime.datetime.strptime('2021-08-23T12:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
        'end': datetime.datetime.strptime('2021-08-23T16:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    }

    test_date34 = {
        'start': datetime.datetime.strptime('2021-08-23T14:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
        'end': datetime.datetime.strptime('2021-08-23T16:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    }

    # test_date_list = [test_date1, test_date2, test_date3, test_date4, test_date5]
    test_date_list = [test_date1, test_date2, test_date3, test_date11, test_date3,
                      test_date31,
                      test_date32,
                      test_date33,
                      test_date34]
    for td in test_date_list:
        ex1(td['start'], td['end'])
        print('test_date for 1 test date is end' + '\n\n')


def ex1(start, end):

    print(start, end)
    # заброннированные места в определенный день
    up_free = UserPlace.objects.filter(Q(start_date__date=start.date(), end_date__date=end.date()))

    for i in up_free:
        print(i)
        print(i.start_date.time(), start.time(), end.time())
        print(i.end_date.time(), start.time(), end.time())

        if ((start.time() >= i.start_date.time() and end.time() <= i.end_date.time())
                or (
                        (start.time() > i.start_date.time() and start.time() < i.end_date.time())
                        or (end.time() > i.start_date.time() and end.time() < i.end_date.time()))
                or (start.time() < i.start_date.time() and end.time() == i.end_date.time())
        ):
            print('-------- OK --------')


def user_places():
    up = UserPlace.objects.annotate(places=ArrayAgg('place')).values('user')
    u = User.objects.values('user').annotate(places=ArrayAgg('user__place'))
    u = User.objects.annotate(places=ArrayAgg('user__place', distinct=True))
    return None