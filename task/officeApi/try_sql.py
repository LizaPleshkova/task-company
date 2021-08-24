import officeApi
import office
from office.models import (
    Office, Room, Place, UserPlace, User
)
from django.db.models import Count, F, Q, Value, Sum
from datetime import datetime
from importlib import reload
import datetime


def test_ex1():
    test_date1 = {
        'start': datetime.datetime.strptime('2021-08-22T09:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
        'end': datetime.datetime.strptime('2021-08-22T10:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    }
    test_date2 = {
        'start': datetime.datetime.strptime('2021-08-22T09:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
        'end': datetime.datetime.strptime('2021-08-22T11:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    }
    test_date3 = {
        'start': datetime.datetime.strptime('2021-08-22T11:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
        'end': datetime.datetime.strptime('2021-08-22T13:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    }
    test_date4 = {
        'start': datetime.datetime.strptime('2021-08-22T12:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
        'end': datetime.datetime.strptime('2021-08-22T15:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    }
    test_date5 = {
        'start': datetime.datetime.strptime('2021-08-22T14:00:00Z', '%Y-%m-%dT%H:%M:%SZ'),
        'end': datetime.datetime.strptime('2021-08-22T18:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    }

    test_date_list = [test_date1, test_date2, test_date3, test_date4, test_date5]
    for td in test_date_list:
        ex1(td['start'], td['end'])
        # up_free = UserPlace.objects.filter(Q(start_date__date=td['start'].date(), end_date__date=td['end'].date()))
        # up1 = up_free.exclude(
        #     Q(start_date__time__range=(td['start'].time(), td['end'].time())) | Q(
        #         end_date__time__range=(td['start'].time(), td['end'].time()))
        # )
        # print('the place is suitable! OK! ', up1)
        print('test_date for 1 test date is end' + '\n\n')


def ex1(start, end):
    # def ex1():
    # время начала и конца , которое хочет пользователь для бронирования места
    # start = datetime.datetime.strptime('2021-08-22T17:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    # end = datetime.datetime.strptime('2021-08-22T18:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    print(start, end)
    # заброннированные места в определенный день
    up_free = UserPlace.objects.filter(Q(start_date__date=start.date(), end_date__date=end.date()))

    # up1 = up_free.filter(
    #     Q(start_date__time__range=(start.time(), end.time())))

    for i in up_free:
        print(i)
        print(i.start_date.time(), start.time(), end.time())
        print(i.end_date.time(), start.time(), end.time())
        # if not (
        #         (
        #                 i.start_date.time() > start.time() or i.start_date.time() >= start.time()
        #         ) and
        #         (
        #                 i.start_date.time() < end.time() or i.start_date.time() <= end.time()
        #         )
        # ) \
        #         and not (
        #         (
        #                 i.end_date.time() > start.time() or i.end_date.time() >= start.time()
        #         ) and
        #         (
        #                 i.end_date.time() < end.time() or i.end_date.time() <= end.time()
        #         )
        # ):


        # и нначало, и конец не внутри промежутка
        if not (start.time() >= i.start_date.time() and end.time() <= i.end_date.time()):
            print(1)
            # начало вне промежутка
            if not (start.time() <= i.start_date.time() and start.time() <= i.end_date.time()
                    and end.time() >= i.start_date.time() and end.time() <= i.end_date.time()):
                print(2)
                print(" ------ OKS ----------- ")
            # конец вне промежутка
            elif not (start.time() >= i.start_date.time() and start.time() <= i.end_date.time()
                  and end.time() > i.end_date.time()):
                print(3)
                print(" ------ OKS ----------- ")

# # когда или start_date или end_date входят в промежуток [start,end]
# if i.start_date.time() != start.time() and i.end_date.time() != start.time():
#     print(1)
#     if not i.start_date.time() > start.time() and i.start_date.time() < end.time():
#         print('first if')
#         if not i.end_date.time() > start.time() and i.end_date.time() < end.time():
#             print('second if')
#     print('the place is suitable! OK! ', i, end='\n----\n')
