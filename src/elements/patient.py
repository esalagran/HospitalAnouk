from ._id import Id
from .surgical_type import SurgicalType


class Patient(Id):
    def __init__(
        self, id_patient: int, priority: int, sex: int, surgical_type: SurgicalType
    ):
        super().__init__(id_patient)
        self.priority: int = priority
        self.sex: int = sex
        self.surgical_type: SurgicalType = surgical_type

    def __repr__(self) -> str:
        return f"<id={self.id}, priority={self.priority}, sex={self.sex}, surgical_type={self.surgical_type.id}>"
