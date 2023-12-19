import random
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from src.elements.patient import Patient
from src.heuristics import EvolutionaryAlgorithm, HeuristicBase, HeuristicGenerator, PredefinedOrder
from src.instance import get_instance
from src.solution import Result, Solution
from src.tester import tester

FOLDER_INSTANCES = Path.cwd() / "data" / "Exemplars" / "data"
FOLDER_RESULTS = Path.cwd() / "data" / "Exemplars" / "solutions"


def get_best_order(
    result: Result, path_input: Path, heuristic: HeuristicBase, cpu_time: float
) -> Tuple[List[Patient], float]:
    instance = get_instance(path_input)
    solution = Solution(instance)
    solution_list = solution.find_solution(heuristic)
    if result.best_sol is None or result.best_sol.value() < solution.value():
        result.add_improvement(solution.value(), (datetime.now() - cpu_time).seconds)
        result.add_best(solution)
        print(solution.value())
    return solution_list, solution.value()


def find_result(path_input: Path, path_output: Path) -> Tuple[float, float]:
    cpu_time = datetime.now()
    result = Result()
    random.seed(0)

    patients_list: List[Tuple[List[Patient], float]] = []
    for heuristic in HeuristicGenerator().get_heuristics():
        patients_list.append(get_best_order(result, path_input, heuristic, cpu_time))

    for _ in range(30):
        optimization = EvolutionaryAlgorithm(patients_list)
        patients_list = []
        for child in optimization.get_population():
            patients_list.append(get_best_order(result, path_input, PredefinedOrder(child), cpu_time))
        patients_list.append((optimization.get_best_exemplar()))

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
    path_instance = FOLDER_INSTANCES / "ejemplar_calibrado_3.txt"
    path_result = FOLDER_RESULTS / "sol_ejemplar_calibrado_3.txt"
    print(find_result(path_instance, path_result))
