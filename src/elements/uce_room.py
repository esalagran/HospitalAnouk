from ._id import Id

_CAPACITY_ = 2


class UceRoom(Id):
    def __init__(self, id_uce: int):
        super().__init__(id_uce)
        self.capacity: int = _CAPACITY_

    def __repr__(self) -> str:
        return f"<id={self.id}>"
