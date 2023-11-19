import json
from pathlib import Path
from typing import Callable, List, Tuple

from ..instance.read_file import read_file as read_instance
from ..solution.read_file import FormatException
from ..solution.read_file import read_file as read_result
from ..solution.result import Result

_MAX_SECONDS_ = 300

TestResult = Tuple[bool, str]
TestFunction = Callable[[Result], TestResult]

with open(Path.cwd() / "src" / "tester" / "messages.json", "r") as f:
    messages = json.load(f)


def _format_check(correct: bool) -> str:
    return "OK" if correct else "INCORRECT"


def patient_in_feasible_operating_room(result: Result) -> TestResult:
    sol = result.best_sol
    is_correct = all(
        assig.patient.surgical_type == assig.operating_room.surgical_type
        for assig in sol.assignments
    )
    msg = messages["patient_in_feasible_operating_room"].format(
        _format_check(is_correct)
    )
    return is_correct, msg


def no_overlap_patients_in_same_operating_room(result: Result) -> TestResult:
    sol = result.best_sol
    is_correct = all(
        (assig1.operation_interval & assig2.operation_interval).empty
        for room in sol.instance.operating_rooms
        for idx, assig1 in enumerate(sol.assignments_by_or[room])
        for assig2 in sol.assignments_by_or[room][idx + 1 :]
    )
    msg = messages["no_overlap_patients_in_same_operating_room"].format(
        _format_check(is_correct)
    )
    return is_correct, msg


def no_overlap_operating_and_cleaning_in_same_operating_room(
    result: Result,
) -> TestResult:
    sol = result.best_sol
    is_correct = all(
        (assig1.cleaning_interval & assig2.operation_interval).empty
        for room in sol.instance.operating_rooms
        for idx, assig1 in enumerate(sol.assignments_by_or[room])
        for assig2 in sol.assignments_by_or[room][idx + 1 :]
    )
    msg = messages["no_overlap_operating_and_cleaning_in_same_operating_room"].format(
        _format_check(is_correct)
    )
    return is_correct, msg


def operations_in_allowed_shift(result: Result) -> TestResult:
    sol = result.best_sol
    is_correct = all(
        assig.operation_interval in sol.instance.operation_interval
        for assig in sol.assignments
    )
    msg = messages["operations_in_allowed_shift"].format(_format_check(is_correct))
    return is_correct, msg


def time_in_urpa_room(result: Result) -> TestResult:
    sol = result.best_sol
    is_correct = all(
        (assig.urpa_interval.upper - assig.urpa_interval.lower) - assig.waiting_time
        == assig.patient.surgical_type.urpa_time
        for assig in sol.assignments
    )
    msg = messages["time_in_urpa_room"].format(_format_check(is_correct))
    return is_correct, msg


def maximum_waiting_in_urpa_room(result: Result) -> TestResult:
    sol = result.best_sol
    is_correct = all(
        assig.waiting_time <= assig.patient.surgical_type.urpa_max_waiting_time
        for assig in sol.assignments
    )
    msg = messages["maximum_waiting_in_urpa_room"].format(_format_check(is_correct))
    return is_correct, msg


def uce_in_allowed_shift(result: Result) -> TestResult:
    sol = result.best_sol
    is_correct = all(
        assig.uce_interval in sol.instance.uce_interval for assig in sol.assignments
    )
    msg = messages["uce_in_allowed_shift"].format(_format_check(is_correct))
    return is_correct, msg


def no_exceed_capacity_uce_room(result: Result) -> TestResult:
    sol = result.best_sol
    for room in sol.instance.uce_rooms:
        for hour in range(
            sol.instance.uce_interval.lower, sol.instance.uce_interval.upper + 1
        ):
            total_assigned = sum(
                hour in assig.uce_interval for assig in sol.assignments_by_ur[room]
            )
            if total_assigned > room.capacity:
                is_correct = False
                break

    is_correct = all(
        sum(hour in assig.uce_interval for assig in sol.assignments_by_ur[room])
        <= room.capacity
        for room in sol.instance.uce_rooms
        for hour in range(
            sol.instance.uce_interval.lower, sol.instance.uce_interval.upper + 1
        )
    )
    msg = messages["no_exceed_capacity_uce_room"].format(_format_check(is_correct))
    return is_correct, msg


def no_mixed_sex_in_uce_room(result: Result) -> TestResult:
    sol = result.best_sol
    is_correct = all(
        assig1.patient.sex == assig2.patient.sex
        or (assig1.uce_interval & assig2.uce_interval).empty
        for room in sol.instance.uce_rooms
        for idx, assig1 in enumerate(sol.assignments_by_ur[room])
        for assig2 in sol.assignments_by_ur[room][idx + 1 :]
    )
    msg = messages["no_mixed_sex_in_uce_room"].format(_format_check(is_correct))
    return is_correct, msg


def value_sol(result: Result) -> TestResult:
    sol = result.best_sol
    value_given = int(result.improvements[-1].of)
    is_correct = value_given == sol.value()
    correct_value_str = f"{sol.value()} ({100}*{sol.number_operated_patients()} + {10}*{sol.weighted_number_operated_patients()} + {1}*{sol.uce_number_hours()})"
    msg = messages["value_sol"].format(
        value_given, correct_value_str, _format_check(is_correct)
    )
    return is_correct, msg


def maximum_cpu_time(result: Result) -> TestResult:
    is_correct = result.improvements[-1].cpu_time <= _MAX_SECONDS_
    msg = messages["maximum_cpu_time"].format(_format_check(is_correct))
    return is_correct, msg


_test_functions_: List[TestFunction] = [
    patient_in_feasible_operating_room,
    no_overlap_patients_in_same_operating_room,
    no_overlap_operating_and_cleaning_in_same_operating_room,
    operations_in_allowed_shift,
    time_in_urpa_room,
    maximum_waiting_in_urpa_room,
    uce_in_allowed_shift,
    no_exceed_capacity_uce_room,
    no_mixed_sex_in_uce_room,
    value_sol,
    maximum_cpu_time,
]


def tester(path_instance: Path, path_result: Path) -> Tuple[bool, str]:
    try:
        instance = read_instance(path=path_instance)
        result = read_result(path=path_result, instance=instance)
    except FileNotFoundError as e:
        all_correct = False
        msg = str(e)
    except FormatException:
        all_correct = False
        msg = "Formato del fichero de la solucion incorrect"
    else:
        all_correct, list_msg = True, []
        for test_function in _test_functions_:
            test_is_correct, test_msg = test_function(result)
            all_correct = all_correct and test_is_correct
            list_msg.append(test_msg)
        msg = "\n".join(list_msg)
    finally:
        return all_correct, msg
