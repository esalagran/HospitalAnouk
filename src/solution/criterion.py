from abc import abstractmethod

from .assignment import Assignment
from ..portion import Interval


class Criterion:
    def __init__(self) -> None:
        self.best_assignment = None
        self._criterion = None

    @property
    def criterion(self):
        return self._criterion

    @criterion.setter
    def criterion(self, value: int):
        self._criterion = value

    @abstractmethod
    def evaluate(self, assignment: Assignment, *args, **kwargs):
        """Checks if the assignment is better than the best assignment"""

    def is_first_assignment(self) -> bool:
        return self.best_assignment is None

    def update(self, assignment: Assignment, criterion: int):
        self.best_assignment = assignment
        self._criterion = criterion


class MinTime(Criterion):
    def __init__(self, maximum_starting_time: int) -> None:
        super().__init__()
        self._criterion: int = float("inf")
        self.maximum_starting_time = maximum_starting_time

    def evaluate(self, assignment: Assignment, *args, **kwargs):
        if assignment.uce_interval.lower < self.maximum_starting_time:
            return
        if self.is_first_assignment() or self._criterion >= assignment.uce_interval.lower:
            self.update(assignment, assignment.operation_interval.lower)


class MaxTime(Criterion):
    def __init__(self, minimum_end_time: int) -> None:
        super().__init__()
        self._criterion: int = -1
        self.minimum_end_time = minimum_end_time

    def evaluate(self, assignment: Assignment, *args, **kwargs):
        if assignment.uce_interval.upper < self.minimum_end_time:
            return
        if self.is_first_assignment() or self._criterion < assignment.uce_interval.lower:
            self.update(assignment, assignment.operation_interval.lower)


class MinWhiteSpaces(Criterion):
    def __init__(self) -> None:
        super().__init__()
        self._criterion: int = float("inf")

    def evaluate(self, assignment: Assignment, blanks: int, uce_interval: Interval):
        distance_to_start = abs(assignment.operation_interval.lower - uce_interval.lower)
        distance_to_end = abs(assignment.operation_interval.lower - uce_interval.upper)
        if uce_interval.lower == 12:
            blanks = distance_to_end
        elif uce_interval.upper == 156:
            blanks = distance_to_start
        else:
            blanks = min(distance_to_start, distance_to_end)
        if self.is_first_assignment() or self._criterion > blanks:
            self.update(assignment, blanks)
