from .. import portion as P
from ..elements.operating_room import OperatingRoom
from ..elements.patient import Patient
from ..elements.uce_room import UceRoom


class Assignment:
    def __init__(
        self,
        patient: Patient,
        operating_room: OperatingRoom,
        operation_start: int,
        uce_room: UceRoom,
        uce_start: int,
    ):
        self.patient: Patient = patient
        self.operating_room: OperatingRoom = operating_room
        self.operation_interval: P.interval = P.closedopen(
            operation_start, operation_start + patient.surgical_type.operation_time
        )
        self.operation_cleaning_interval: P.interval = P.closedopen(
            operation_start,
            operation_start + patient.surgical_type.operation_time + patient.surgical_type.cleaning_time,
        )
        self.uce_room: UceRoom = uce_room
        self.uce_interval: P.interval = P.closedopen(uce_start, uce_start + patient.surgical_type.uce_time)

    @property
    def urpa_interval(self) -> P.Interval:
        return P.closedopen(self.operation_interval.upper, self.uce_interval.lower)

    @property
    def cleaning_interval(self) -> P.Interval:
        return self.operation_cleaning_interval - self.operation_interval

    @property
    def waiting_time(self) -> int:
        return self.uce_interval.lower - (self.operation_interval.upper + self.patient.surgical_type.urpa_time)
