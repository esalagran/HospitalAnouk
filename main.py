import multiprocessing
import random
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from tqdm import tqdm

from src.elements.patient import Patient
from src.heuristics import EvolutionaryAlgorithm, HeuristicBase, HeuristicGenerator, PredefinedOrder
from src.instance import get_instance
from src.solution import Result, Solution
from src.tester import tester

FOLDER_INSTANCES = Path.cwd() / "data" / "Exemplars" / "data"
FOLDER_RESULTS = Path.cwd() / "data" / "Exemplars" / "solutions"


def get_best_order_par(heuristic_path: Tuple[HeuristicBase, Path]) -> Tuple[List[Patient], Solution]:
    heuristic, path_input = heuristic_path
    instance = get_instance(path_input)
    solution = Solution(instance)
    solution_list = solution.find_solution(heuristic)
    return solution_list, solution


def run_parallel(
    heuristics: List[HeuristicBase], result: Result, path_input: Path, cpu_time: float
) -> List[Tuple[List[Patient], float]]:
    solutions: List[Tuple[List[Patient], Solution]] = []
    heuristics_to_process = [(heuristic, path_input) for heuristic in heuristics]
    with multiprocessing.Pool() as pool:
        solutions = pool.map(get_best_order_par, heuristics_to_process)

    returning_value: List[Tuple[List[Patient], float]] = []
    for list_patients, solution in solutions:
        returning_value.append((list_patients, solution.value()))
        if result.best_sol is None or result.best_sol.value() < solution.value():
            result.add_improvement(solution.value(), (datetime.now() - cpu_time).seconds)
            result.add_best(solution)
    return returning_value


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

    patients_list: List[Tuple[List[Patient], float]] = run_parallel(
        HeuristicGenerator().get_heuristics(), result, path_input, cpu_time
    )
    with tqdm(total=10) as progress_bar:
        for _ in range(10):
            optimization = EvolutionaryAlgorithm(patients_list)
            algorithms_list = [PredefinedOrder(child) for child in optimization.get_population()]
            patients_list = run_parallel(algorithms_list, result, path_input, cpu_time)
            patients_list.append((optimization.get_best_exemplar()))
            progress_bar.set_postfix_str(optimization.get_data_progress_bar())
            progress_bar.update(1)

    assert result.best_sol is not None
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
