from ._id import Id

_CAPACITY_ = 2


class UceRoom(Id):
    def __init__(self, id_uce: int):
        super().__init__(id_uce)
        self.capacity: int = _CAPACITY_
        self._sex = 0

    def __repr__(self) -> str:
        return f"<id={self.id}>"

    @property
    def sex(self) -> int:
        return self._sex

    @sex.setter
    def sex(self, sex: int) -> None:
        if self._sex == 0:
            self._sex = sex
