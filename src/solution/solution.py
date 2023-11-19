from typing import Dict, List, Tuple

from .. import portion as P
from ..elements.operating_room import OperatingRoom
from ..elements.patient import Patient
from ..elements.uce_room import UceRoom
from ..heuristics import HeuristicBase
from ..instance.instance import Instance
from .assignment import Assignment

WEIGHT_OBJECTIVE_1 = 100
WEIGHT_OBJECTIVE_2 = 10
WEIGHT_OBJECTIVE_3 = 1

_SEPARATOR_ = "*"


class Solution:
    def __init__(self, instance: Instance):
        self.instance = instance
        self.assignments: List[Assignment] = []
        self.assignments_by_or: Dict[OperatingRoom, List[Assignment]] = {
            operating_room: [] for operating_room in instance.operating_rooms
        }
        self.assignments_by_ur: Dict[UceRoom, List[Assignment]] = {
            uce_room: [] for uce_room in instance.uce_rooms
        }

    def assign(self, assignment: Assignment) -> None:
        self.assignments.append(assignment)
        self.assignments_by_or[assignment.operating_room].append(assignment)
        self.assignments_by_ur[assignment.uce_room].append(assignment)

    def availability_or(self, operating_room: OperatingRoom) -> P.Interval:
        availability = self.instance.operation_interval
        for assignment in self.assignments_by_or[operating_room]:
            availability = availability - assignment.operation_cleaning_interval
        return availability

    def availability_ur(self, uce_room: UceRoom, sex: int) -> P.Interval:
        availability = self.instance.uce_interval
        # Ranges with assignments of different sex are not available
        for assignment in self.assignments_by_ur[uce_room]:
            if assignment.patient.sex != sex:
                availability = availability - assignment.uce_interval
        # Ranges of intersections of same sex (it is assumed that the capacity of the rooms is 2)
        for i, assignment1 in enumerate(self.assignments_by_ur[uce_room]):
            if assignment1.patient.sex == sex:
                for assignment2 in self.assignments_by_ur[uce_room][i + 1 :]:
                    if assignment2.patient.sex == sex:
                        availability = availability - (
                            assignment1.uce_interval & assignment2.uce_interval
                        )
        return availability

    def number_operated_patients(self) -> int:
        return len(self.assignments)

    def weighted_number_operated_patients(self) -> float:
        return sum(assignment.patient.priority for assignment in self.assignments)

    def uce_number_hours(self) -> int:
        return sum(
            assignment.uce_interval.upper - assignment.uce_interval.lower
            for assignment in self.assignments
        )

    def value(self) -> float:
        return (
            WEIGHT_OBJECTIVE_1 * self.number_operated_patients()
            + WEIGHT_OBJECTIVE_2 * self.weighted_number_operated_patients()
            + WEIGHT_OBJECTIVE_3 * self.uce_number_hours()
        )

    def __str__(self) -> str:
        sol_str = ""
        sol_str += (
            _SEPARATOR_.join([str(assig.patient.id) for assig in self.assignments])
            + "\n"
        )
        sol_str += (
            _SEPARATOR_.join(
                [str(assig.operating_room.id) for assig in self.assignments]
            )
            + "\n"
        )
        sol_str += (
            _SEPARATOR_.join(
                [str(assig.operation_interval.lower) for assig in self.assignments]
            )
            + "\n"
        )
        sol_str += (
            _SEPARATOR_.join([str(assig.uce_room.id) for assig in self.assignments])
            + "\n"
        )
        sol_str += _SEPARATOR_.join(
            [str(assig.uce_interval.lower) for assig in self.assignments]
        )
        return sol_str

    def find_solution(self, heuristic: HeuristicBase):
        operable_patients = heuristic.sort(self.instance.operable_patients())
        for patient in operable_patients:
            available_ors = self.find_available_ors(patient)
            available_uces = self.find_available_uces(patient)
            assignments: List[Assignment] = []
            for or_, or_interval in available_ors:
                min_start = (
                    or_interval.lower
                    + patient.surgical_type.operation_time
                    + patient.surgical_type.urpa_time
                )
                max_start = min_start + patient.surgical_type.urpa_max_waiting_time + 1
                for uce, uce_interval in available_uces:
                    for starting_time in range(min_start, max_start):
                        patient_uce_interval = P.closedopen(
                            starting_time,
                            starting_time + patient.surgical_type.uce_time,
                        )
                        if uce_interval.contains(patient_uce_interval):
                            assignments.append(
                                Assignment(
                                    patient=patient,
                                    operating_room=or_,
                                    operation_start=or_interval.lower,
                                    uce_room=uce,
                                    uce_start=starting_time,
                                )
                            )
            if len(assignments) > 0:
                assignments.sort(key=lambda x: x.uce_interval.lower)
                self.assign(assignments[0])
            # else:
            #     print(patient, patient.surgical_type, available_ors, available_uces)

    def find_available_ors(
        self, patient: Patient
    ) -> List[Tuple[OperatingRoom, P.Interval]]:
        available_ors: List[Tuple[OperatingRoom, P.Interval]] = []
        for operating_room in self.instance.feasible_operating_rooms(patient):
            availability_or = self.availability_or(operating_room)
            for inter in availability_or:
                operating_interval = P.closedopen(
                    inter.lower, inter.lower + patient.surgical_type.operation_time
                )
                if inter.contains(operating_interval):
                    available_ors.append((operating_room, inter))
        available_ors.sort(key=lambda x: x[1].lower)
        return available_ors

    def find_available_uces(self, patient: Patient) -> List[Tuple[UceRoom, P.Interval]]:
        available_uces: List[Tuple[UceRoom, P.Interval]] = []
        for uce_room in self.instance.uce_rooms:
            availability_uces = self.availability_ur(uce_room, patient.sex)
            for inter in availability_uces:
                uce_time_interval = P.closedopen(
                    inter.lower, inter.lower + patient.surgical_type.uce_time
                )
                if inter.contains(uce_time_interval):
                    available_uces.append((uce_room, inter))
        available_uces.sort(key=lambda x: x[1].lower)
        return available_uces
