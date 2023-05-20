from dataclasses import dataclass
from typing import NamedTuple
from collections import Counter


class NutritionStats(NamedTuple):
    calories: float = 0.0
    carbs: float = 0.0
    fats: float = 0.0
    protein: float = 0.0

    def __add__(self, other):
        return NutritionStats(*(x + y for x, y in zip(self, other)))


@dataclass(frozen=True, eq=True)
class Meal:
    name: str
    description: str
    stats: NutritionStats


class ShoppingList(Counter):
    def add(self, meal):
        self[meal] += 1
