from enum import Enum


class PlaceChoice(Enum):
    FREE = 'free'
    BOOKED = 'booked'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
