from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from src.heuristics import HeuristicBase, SortByPriority
from src.instance import get_instance
from src.solution import Result, Solution
from src.tester import tester

FOLDER_INSTANCES = Path.cwd() / "data" / "Exemplars" / "data"
FOLDER_RESULTS = Path.cwd() / "data" / "Exemplars" / "solutions"


def find_result(path_input: Path, path_output: Path) -> Tuple[float, float]:
    cpu_time = datetime.now()
    result = Result()
    heuristics_list: List[HeuristicBase] = [SortByPriority()]
    for heuristic in heuristics_list:
        instance = get_instance(path_input)
        solution = Solution(instance)
        solution.find_solution(heuristic)
        if result.best_sol is None or result.best_sol.value() < solution.value():
            result.add_improvement(
                solution.value(), (datetime.now() - cpu_time).seconds
            )
            result.add_best(solution)

    assert result.best_sol is not None
    # Visualizer(result.best_sol).visualize()
    with open(path_output, "w+") as f:
        f.write(str(result))

    is_correct, message = tester(path_input, path_output)
    if not is_correct:
        print(path_input)
        print(message)

    return result.best_sol.value(), (datetime.now() - cpu_time).seconds


if __name__ == "__main__":
    path_instance = FOLDER_INSTANCES / "ejemplar_calibrado_1.txt"
    path_result = FOLDER_RESULTS / "sol_ejemplar_calibrado_1.txt"
    print(find_result(path_instance, path_result))
