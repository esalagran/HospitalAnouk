from typing import List

from ..elements.patient import Patient


class HeuristicBase:
    def sort(self, patients: List[Patient]) -> List[Patient]:
        raise NotImplementedError


class SortByPriority(HeuristicBase):
    def sort(self, patients: List[Patient]) -> List[Patient]:
        return sorted(patients, key=lambda patient: patient.priority, reverse=True)
