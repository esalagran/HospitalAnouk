from ._id import Id
from .surgical_type import SurgicalType


class OperatingRoom(Id):
    def __init__(self, id_or: int, surgical_type: SurgicalType):
        super().__init__(id_or)
        self.surgical_type: SurgicalType = surgical_type

    def __repr__(self) -> str:
        return f"<id={self.id}, surgical_type={self.surgical_type.id}>"
