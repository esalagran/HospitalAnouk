import random
from abc import abstractmethod
from typing import List

from ..elements.patient import Patient


class HeuristicBase:
    @abstractmethod
    def sort(cls, patients: List[Patient]) -> List[Patient]:
        """Sort the patients list by a predefined criterion"""


class SortByPriority(HeuristicBase):
    @classmethod
    def sort(cls, patients: List[Patient]) -> List[Patient]:
        return sorted(
            patients,
            key=lambda patient: (patient.priority, -patient.time_to_uce(), -patient.time_to_leave(), patient.sex),
            reverse=True,
        )


class SortByMinimumUceTime(HeuristicBase):
    @classmethod
    def sort(cls, patients: List[Patient]) -> List[Patient]:
        return sorted(patients, key=lambda patient: (patient.surgical_type.uce_time, -patient.priority))


class SortByMaximumUceTime(HeuristicBase):
    @classmethod
    def sort(cls, patients: List[Patient]) -> List[Patient]:
        return sorted(patients, key=lambda patient: (patient.surgical_type.uce_time, patient.priority), reverse=True)


class SortByMinimumTimeToUceThenPriority(HeuristicBase):
    @classmethod
    def sort(cls, patients: List[Patient]) -> List[Patient]:
        first_list = sorted(patients, key=lambda patient: patient.time_to_uce())
        return first_list[:8] + SortByPriority().sort(first_list[8:])


class SortByMinimumTime(HeuristicBase):
    @classmethod
    def sort(cls, patients: List[Patient]) -> List[Patient]:
        return sorted(
            patients,
            key=lambda patient: (-patient.priority + 0.1 * (patient.time_to_leave())),
        )


class SortByMinimumTimeToUceThenMinimumUCE(HeuristicBase):
    @classmethod
    def sort(cls, patients: List[Patient]) -> List[Patient]:
        first_list = sorted(patients, key=lambda patient: patient.time_to_uce())
        return first_list[:8] + SortByMinimumUceTime().sort(first_list[8:])


class SortByOperationTypeSexPriority(HeuristicBase):
    @classmethod
    def sort(cls, patients: List[Patient]) -> List[Patient]:
        return sorted(
            patients,
            key=lambda patient: (
                patient.time_to_leave(),
                patient.sex,
                patient.priority,
            ),
        )


class RandomOrder(HeuristicBase):
    @classmethod
    def sort(cls, patients: List[Patient]) -> List[Patient]:
        random.shuffle(patients)
        return patients


class PredefinedOrder(HeuristicBase):
    def __init__(self, patients_order: List[Patient]) -> None:
        self.predefined_order = patients_order

    def sort(self, _: List[Patient]) -> List[Patient]:
        return self.predefined_order


class HeuristicGenerator:
    def __init__(self, num_random=20) -> None:
        self.num_random = num_random

    def get_heuristics(self) -> List[HeuristicBase]:
        not_random = self.get_heuristics_without_random()
        not_random.extend([RandomOrder for _ in range(self.num_random)])
        return not_random

    def get_heuristics_without_random(self) -> List[HeuristicBase]:
        return [
            SortByPriority,
            SortByMinimumUceTime,
            SortByMaximumUceTime,
            SortByMinimumTimeToUceThenMinimumUCE,
            SortByMinimumTimeToUceThenPriority,
        ]
