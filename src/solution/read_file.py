from pathlib import Path
from typing import List

from ..instance.instance import Instance
from .assignment import Assignment
from .result import Result
from .solution import Solution

_SEPARATOR_ = "*"


class FormatException(Exception):
    """Exception raised when format is incorrect."""


def read_file(path: Path, instance: Instance) -> Result:
    # Dictionaries of patients, operating rooms and uce rooms by id
    dict_patients = {patient.id: patient for patient in instance.patients}
    dict_operating_rooms = {
        operating_room.id: operating_room for operating_room in instance.operating_rooms
    }
    dict_uce_rooms = {uce_room.id: uce_room for uce_room in instance.uce_rooms}
    # Read the content of the file
    with open(path, "r") as f:
        lines = f.readlines()
    # Construct the result with improvements and the solution...
    res = Result()
    # ...improvements
    idx_number_improvements = next(
        idx for idx, line in enumerate(lines) if _SEPARATOR_ not in line
    )
    for line in lines[:idx_number_improvements]:
        values = _get_float_values(text=line, expected_size_list=2)
        res.add_improvement(of=values[0], cpu_time=values[1])
    # ...best improvement
    values = _get_float_values(
        text=lines[idx_number_improvements + 1], expected_size_list=2
    )
    res.add_improvement(of=values[0], cpu_time=values[1])
    # ...solution
    sol = Solution(instance=instance)
    ntpo = len(lines[idx_number_improvements + 2].split(_SEPARATOR_))
    values_patient_ids = _get_int_values(
        text=lines[idx_number_improvements + 2], expected_size_list=ntpo
    )
    values_operating_room_ids = _get_int_values(
        text=lines[idx_number_improvements + 3], expected_size_list=ntpo
    )
    values_operation_starts = _get_int_values(
        text=lines[idx_number_improvements + 4], expected_size_list=ntpo
    )
    values_uce_room_ids = _get_int_values(
        text=lines[idx_number_improvements + 5], expected_size_list=ntpo
    )
    values_uce_starts = _get_int_values(
        text=lines[idx_number_improvements + 6], expected_size_list=ntpo
    )
    zipper_values = zip(
        values_patient_ids,
        values_operating_room_ids,
        values_operation_starts,
        values_uce_room_ids,
        values_uce_starts,
    )
    for patient_id, oper_room_id, oper_start, uce_room_id, uce_start in zipper_values:
        assignment = Assignment(
            patient=dict_patients[patient_id],
            operating_room=dict_operating_rooms[oper_room_id],
            operation_start=oper_start,
            uce_room=dict_uce_rooms[uce_room_id],
            uce_start=uce_start,
        )
        sol.assign(assignment=assignment)
    res.add_best(sol=sol)
    return res


def _get_float_values(text: str, expected_size_list: int) -> List[float]:
    split_text = text.split(_SEPARATOR_)
    if len(split_text) != expected_size_list:
        raise (FormatException(""))
    try:
        values = [float(value) for value in split_text]
    except ValueError:
        raise FormatException("")
    else:
        return values


def _get_int_values(text: str, expected_size_list: int) -> List[int]:
    split_text = text.split(_SEPARATOR_)
    if len(split_text) != expected_size_list:
        raise (FormatException(""))
    try:
        values = [int(value) for value in split_text]
    except ValueError:
        raise FormatException("")
    else:
        return values
