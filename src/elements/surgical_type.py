from ._id import Id

_CLEANING_TIME_ = 1
_URPA_MAX_WAITING_TIME_ = 12


class SurgicalType(Id):
    def __init__(self, id_st: int, operation_time: int, urpa_time: int, uce_time: int):
        super().__init__(id_st)
        self.operation_time: int = operation_time
        self.cleaning_time: int = _CLEANING_TIME_
        self.urpa_time: int = urpa_time
        self.urpa_max_waiting_time = _URPA_MAX_WAITING_TIME_
        self.uce_time: int = uce_time

    def __repr__(self) -> str:
        return f"<id={self.id}, operation={self.operation_time}h, urpa={self.urpa_time}h, uce={self.uce_time}h>"
