from pathlib import Path
from typing import List

from ..elements.operating_room import OperatingRoom
from ..elements.patient import Patient
from ..elements.surgical_type import SurgicalType
from .instance import Instance

_SEPARATOR_ = "*"


def _parse(line: str) -> List[int]:
    values = [int(value) for value in line.split(_SEPARATOR_)]
    return values


def read_file(path: Path) -> Instance:
    file = open(path, "r")
    # Read the content of the file...
    # ...patients
    _ = int(file.readline())
    PPr = _parse(file.readline())
    PSe = _parse(file.readline())
    PTi = _parse(file.readline())
    # ...surgical types
    ITIn = _parse(file.readline())
    ITAn = _parse(file.readline())
    ITCu = _parse(file.readline())
    # ...operating rooms
    QTI = _parse(file.readline())
    # Construct and return the instance
    surgical_types = [
        SurgicalType(id_st=id_st, operation_time=opet, urpa_time=urpat, uce_time=ucet)
        for id_st, (opet, urpat, ucet) in enumerate(zip(ITIn, ITAn, ITCu), start=1)
    ]
    dict_surgical_types_by_id = {st.id: st for st in surgical_types}
    patients = [
        Patient(
            id_patient=id_p,
            priority=pr,
            sex=sex,
            surgical_type=dict_surgical_types_by_id[st],
        )
        for id_p, (pr, sex, st) in enumerate(zip(PPr, PSe, PTi), start=1)
    ]
    operating_rooms = [
        OperatingRoom(id_or=id_or, surgical_type=dict_surgical_types_by_id[st]) for id_or, st in enumerate(QTI, start=1)
    ]
    return Instance(patients=patients, operating_rooms=operating_rooms)
