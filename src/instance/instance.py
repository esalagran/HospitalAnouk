from typing import List

from .. import portion as P
from ..elements.operating_room import OperatingRoom
from ..elements.patient import Patient
from ..elements.uce_room import UceRoom

_UCE_ROOMS_ = 10

_FIRST_HOUR_ = 0  # 0:00 Monday

_OPERATING_HOUR_OPEN_ = _FIRST_HOUR_ + 8
_OPERATING_HOUR_CLOSE_ = _FIRST_HOUR_ + 20
_OPERATING_NUMBER_DAYS_OPEN = 4
_UCE_HOUR_OPEN_ = _FIRST_HOUR_ + 12
_UCE_NUMBER_DAYS_OPEN_ = 6


def _calculate_operation_interval() -> P.Interval:
    interval = P.empty()
    for day in range(_OPERATING_NUMBER_DAYS_OPEN):
        interval = interval | P.closedopen(
            _OPERATING_HOUR_OPEN_ + 24 * day, _OPERATING_HOUR_CLOSE_ + 24 * day
        )
    return interval


class Instance:
    def __init__(self, patients: List[Patient], operating_rooms: List[OperatingRoom]):
        self.patients = patients
        self.operating_rooms = operating_rooms
        self.operation_interval = _calculate_operation_interval()
        self.uce_rooms = [
            UceRoom(id_uce=id_uce) for id_uce in range(1, _UCE_ROOMS_ + 1)
        ]
        self.uce_interval = P.closedopen(
            _UCE_HOUR_OPEN_, _UCE_HOUR_OPEN_ + 24 * _UCE_NUMBER_DAYS_OPEN_
        )

    def operable_patients(self) -> List[Patient]:
        set_available_surgical_types = set(
            room.surgical_type for room in self.operating_rooms
        )
        patients = [
            patient
            for patient in self.patients
            if patient.surgical_type in set_available_surgical_types
        ]
        return patients

    def feasible_operating_rooms(self, patient: Patient) -> List[OperatingRoom]:
        rooms = [
            room
            for room in self.operating_rooms
            if room.surgical_type == patient.surgical_type
        ]
        return rooms
