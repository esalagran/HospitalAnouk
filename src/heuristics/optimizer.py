import random
from typing import List, Set, Tuple

from ..elements.patient import Patient


class EvolutionaryAlgorithm:
    def __init__(self, population: List[Tuple[List[Patient], float]]) -> None:
        self.patients_orders, self.fitness = [list(x) for x in zip(*population)]
        self.elite_index = max(range(len(self.fitness)), key=self.fitness.__getitem__)
        self.crossover_rate = 0.9
        self.mutation_rate = 0.1
        self.tournament_size = 3

    def get_population(self) -> List[List[Patient]]:
        population: List[List[Patient]] = []
        for _ in range(1, len(self.patients_orders)):
            parent_1 = self.roulette_selection()
            parent_2 = self.tournament_selection()
            child = self.crossover(parent_1, parent_2)
            population.append(self.mutate(child))
        return population

    def roulette_selection(self) -> List[Patient]:
        idx = random.choices(population=list(range(len(self.patients_orders))), weights=self.fitness, k=1)[0]
        return self.patients_orders[idx]

    def tournament_selection(self) -> List[Patient]:
        tournament_contestants = random.sample(range(len(self.patients_orders)), self.tournament_size)
        winner = max(tournament_contestants, key=lambda x: self.fitness[x])
        return self.patients_orders[winner]

    def crossover(self, parent_1: List[Patient], parent_2: List[Patient]) -> List[Patient]:
        crossover_point = random.randint(0, len(parent_1))
        remaining_patients = [patient for patient in parent_2 if patient not in parent_1[:crossover_point]]
        child = parent_1[:crossover_point] + remaining_patients
        return child

    def uniform_crossover(self, parent_1: List[Patient], parent_2: List[Patient]) -> List[Patient]:
        mask = [random.choice([True, False]) for _ in range(len(parent_1))]
        child: List[Patient] = []
        used: Set[Patient] = set()

        p1, p2 = 0, 0

        for m in mask:
            if m:
                p1 = self._find_next(used, parent_1, p1)
                self._add_patient_to_child(parent_1, p1, used, child)
                p1 += 1
            else:
                p2 = self._find_next(used, parent_2, p2)
                self._add_patient_to_child(parent_2, p2, used, child)
                p2 += 1

        self._add_remaining(parent_1[p1:], used, child)
        self._add_remaining(parent_2[p2:], used, child)

        return child

    def _find_next(self, used: Set[Patient], parent: List[Patient], pointer: int) -> int:
        while pointer < len(parent) and parent[pointer] in used:
            pointer += 1
        return pointer

    def _add_patient_to_child(self, parent: List[Patient], pointer: int, used: Set[Patient], child: List[Patient]):
        if pointer < len(parent):
            used.add(parent[pointer])
            child.append(parent[pointer])

    def _add_remaining(self, remaining_patients: List[Patient], used: Set[Patient], child: List[Patient]):
        for patient in remaining_patients:
            if patient not in used:
                used.add(patient)
                child.append(patient)

    def mutate(self, child: List[Patient]) -> List[Patient]:
        if random.random() > self.mutation_rate:
            return child
        idx_1, idx_2 = random.sample(range(len(child)), 2)
        child[idx_1], child[idx_2] = child[idx_2], child[idx_1]
        return child

    def get_best_exemplar(self) -> Tuple[List[Patient], float]:
        return (self.patients_orders[self.elite_index], self.fitness[self.elite_index])

    def get_data_progress_bar(self) -> str:
        return (
            f"fitness: {round(sum(self.fitness) / len(self.fitness), 2)}, "
            + f"max_fitness: {self.fitness[self.elite_index]}"
        )
