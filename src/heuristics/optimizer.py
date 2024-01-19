import random
from typing import List, Tuple

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

    def mutate(self, child: List[Patient]) -> List[Patient]:
        if random.random() > self.mutation_rate:
            return child
        idx_1, idx_2 = random.sample(range(len(child)), 2)
        child[idx_1], child[idx_2] = child[idx_2], child[idx_1]
        return child

    def get_best_exemplar(self) -> Tuple[List[Patient], float]:
        return (self.patients_orders[self.elite_index], self.fitness[self.elite_index])
