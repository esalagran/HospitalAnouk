from typing import List, Optional

from .solution import Solution

_SEPARATOR_ = "*"


class ResultImprovement:
    def __init__(self, of: float, cpu_time: float):
        self.of: float = of
        self.cpu_time: float = cpu_time


class Result:
    def __init__(self):
        self.improvements: List[ResultImprovement] = []
        self.best_sol: Optional[Solution] = None

    def add_improvement(self, of: float, cpu_time: float) -> None:
        self.improvements.append(ResultImprovement(of=of, cpu_time=cpu_time))

    def add_best(self, sol: Solution) -> None:
        self.best_sol = sol

    def __str__(self) -> str:
        result_str = ""
        for improvement in self.improvements[:-1]:
            result_str += str(improvement.of) + _SEPARATOR_ + str(improvement.cpu_time) + "\n"
        result_str += str(len(self.improvements) - 2) + "\n"
        result_str += str(self.improvements[-1].of) + _SEPARATOR_ + str(self.improvements[-1].cpu_time) + "\n"
        result_str += str(self.best_sol)
        return result_str
