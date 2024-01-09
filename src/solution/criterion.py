from abc import abstractmethod

from .assignment import Assignment


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
    def evaluate(self, assignment: Assignment):
        """Checks if the assignment is better than the best assignment"""

    def is_first_assignment(self) -> bool:
        return self.best_assignment is None

    def update(self, assignment: Assignment, criterion: int):
        self.best_assignment = assignment
        self._criterion = criterion


class MinTime(Criterion):
    def __init__(self) -> None:
        super().__init__()
        self._criterion: int = float("inf")

    def evaluate(self, assignment: Assignment, _=None):
        if self.is_first_assignment() or self._criterion > assignment.uce_interval.lower:
            self.update(assignment, assignment.operation_interval.lower)


class MaxTime(Criterion):
    def __init__(self) -> None:
        super().__init__()
        self._criterion: int = -1
        self.minimum_time = 144

    def evaluate(self, assignment: Assignment, _=None):
        if assignment.uce_interval.upper < self.minimum_time:
            return
        if self.is_first_assignment() or self._criterion < assignment.uce_interval.lower:
            self.update(assignment, assignment.operation_interval.lower)


class MinWhiteSpaces(Criterion):
    def __init__(self) -> None:
        super().__init__()
        self._criterion: int = float("inf")

    def evaluate(self, assignment: Assignment, external_factor: int):
        if self.is_first_assignment() or self._criterion > external_factor:
            self.update(assignment, external_factor)
