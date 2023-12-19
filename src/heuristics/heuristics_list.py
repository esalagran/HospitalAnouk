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
        return sorted(patients, key=lambda patient: patient.priority, reverse=True)


class SortByMinimumUceTime(HeuristicBase):
    @classmethod
    def sort(cls, patients: List[Patient]) -> List[Patient]:
        return sorted(patients, key=lambda patient: (patient.surgical_type.uce_time, patient.priority))


class SortByMaximumUceTime(HeuristicBase):
    @classmethod
    def sort(cls, patients: List[Patient]) -> List[Patient]:
        return sorted(patients, key=lambda patient: (patient.surgical_type.uce_time, patient.priority), reverse=True)


class SortByMinimumTimeToUceThenPriority(HeuristicBase):
    @classmethod
    def sort(cls, patients: List[Patient]) -> List[Patient]:
        first_list = sorted(
            patients, key=lambda patient: patient.surgical_type.urpa_time + patient.surgical_type.operation_time
        )
        return first_list[:8] + SortByPriority().sort(first_list[8:])


class SortByMinimumTimeToUceThenMinimumUCE(HeuristicBase):
    @classmethod
    def sort(cls, patients: List[Patient]) -> List[Patient]:
        first_list = sorted(
            patients, key=lambda patient: patient.surgical_type.urpa_time + patient.surgical_type.operation_time
        )
        return first_list[:8] + SortByMinimumUceTime().sort(first_list[8:])


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
        return [
            SortByPriority,
            SortByMinimumUceTime,
            SortByMaximumUceTime,
            SortByMinimumTimeToUceThenMinimumUCE,
            SortByMinimumTimeToUceThenPriority,
            *[RandomOrder for _ in range(self.num_random)],
        ]
