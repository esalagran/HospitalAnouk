import argparse
import multiprocessing
import random
import time
from pathlib import Path
from typing import List, Tuple

from src.elements.patient import Patient
from src.heuristics import EvolutionaryAlgorithm, HeuristicBase, HeuristicGenerator, PredefinedOrder
from src.instance import get_instance
from src.solution import SOLUTION_PARAMETERS_LIST, Result, Solution, SolutionParameters
from src.tester import tester


def get_best_order_par(
    heuristic_path: Tuple[HeuristicBase, Path, SolutionParameters]
) -> Tuple[List[Patient], Solution]:
    heuristic, path_input, solution_parameters = heuristic_path
    instance = get_instance(path_input)
    solution = Solution(instance, solution_parameters)
    solution_list = solution.find_solution(heuristic)
    return solution_list, solution


def run_parallel(
    heuristics: List[HeuristicBase],
    result: Result,
    path_input: Path,
    cpu_time: float,
    solution_parameters: SolutionParameters,
) -> List[Tuple[List[Patient], float]]:
    solutions: List[Tuple[List[Patient], Solution]] = []
    heuristics_to_process = [(heuristic, path_input, solution_parameters) for heuristic in heuristics]
    with multiprocessing.Pool() as pool:
        solutions = pool.map(get_best_order_par, heuristics_to_process)

    returning_value: List[Tuple[List[Patient], float]] = []
    for list_patients, solution in solutions:
        returning_value.append((list_patients, solution.value()))
        if result.best_sol is None or result.best_sol.value() < solution.value():
            result.add_improvement(solution.value(), int((time.time() - cpu_time)))
            result.add_best(solution)
    return returning_value


def get_best_order(
    result: Result, path_input: Path, heuristic: HeuristicBase, cpu_time: float
) -> Tuple[List[Patient], float]:
    instance = get_instance(path_input)
    solution = Solution(instance)
    solution_list = solution.find_solution(heuristic)
    if result.best_sol is None or result.best_sol.value() < solution.value():
        result.add_improvement(solution.value(), int(time.time() - cpu_time))
        result.add_best(solution)
        print(solution.value())
    return solution_list, solution.value()


def find_result(path_input: Path, path_output: Path) -> Tuple[float, float]:
    cpu_time = time.time()
    result = Result()
    random.seed(0)

    for solution_parameters in SOLUTION_PARAMETERS_LIST:
        patients_list: List[Tuple[List[Patient], float]] = run_parallel(
            HeuristicGenerator().get_heuristics_without_random(), result, path_input, cpu_time, solution_parameters
        )

    while time.time() - cpu_time < 60 * 4:
        optimization = EvolutionaryAlgorithm(patients_list)
        algorithms_list = [PredefinedOrder(child) for child in optimization.get_population()]
        patients_list = run_parallel(algorithms_list, result, path_input, cpu_time, result.best_sol.solution_parameters)
        patients_list.append((optimization.get_best_exemplar()))

    visualize_or(result.best_sol.assignments_by_or)
    visualize_ur(result.best_sol.assignments_by_ur)

    assert result.best_sol is not None
    with open(path_output, "w+") as f:
        f.write(str(result))

    is_correct, message = tester(path_input, path_output)
    if not is_correct:
        print(path_input)
        print(message)

    return result.best_sol.value(), int(time.time() - cpu_time)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--exemplar", required=True)
    parser.add_argument("--solution", required=True)

    args = parser.parse_args()
    print(find_result(args.exemplar, args.solution))
