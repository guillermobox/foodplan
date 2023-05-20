from argparse import ArgumentParser
from itertools import chain

from persistency import from_database, menu_from_file
from models import ShoppingList, NutritionStats, Meal


def create_nutrition_report(menu_path):
    FMT_HDR = "{:12}{:>6}  {:>6}  {:>6}  {:>6}"
    FMT_ROW = "{:12}{:6.1f}  {:6.1f}  {:6.1f}  {:6.1f}"
    menu = menu_from_file(menu_path)

    print(" Nutritional values ".center(42, "-"))
    print(FMT_HDR.format("", "Energy", "Carbs", "Fats", "Prots"))
    for section, meals in menu.items():
        stats = NutritionStats()
        for meal in meals:
            meal = from_database(Meal, meal)
            stats += meal.stats
        print(FMT_ROW.format(section, *stats))
    print("-" * 42)


def create_shopping_report(menu_path):
    shopping_list = ShoppingList()
    menu = menu_from_file(menu_path)

    for meal in chain(*(meals for meals in menu.values())):
        meal = from_database(Meal, meal)
        shopping_list.add(meal)

    print(" Shopping list ".center(42, "-"))
    for meal, ammount in shopping_list.items():
        print(f" {ammount} x {meal.name} ({meal.description})")
    print("-" * 42)


def main():
    parser = ArgumentParser()
    parser.add_argument("type", help="Report type", choices=["nutrition", "shopping"])
    parser.add_argument("menu", help="Menu file")
    args = parser.parse_args()

    if args.type == "nutrition":
        return create_nutrition_report(args.menu)
    elif args.type == "shopping":
        return create_shopping_report(args.menu)


if __name__ == "__main__":
    exit(main())
