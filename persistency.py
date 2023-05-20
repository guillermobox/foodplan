import csv


def menu_from_file(path: str) -> dict:
    section = None
    menu = {}
    for token, value in tokenize_menu_file(path):
        if token == "section":
            menu[value] = []
            section = value
        elif token == "meal":
            menu[section].append(value)
        elif token == "eof":
            break
    return menu


def tokenize_menu_file(path):
    with open(path, "r") as fh:
        for line in fh:
            if line.startswith(" "):
                for meal in line.strip().split(","):
                    yield "meal", meal.strip()
            else:
                yield "section", line.strip()
    yield "eof", None


def from_database(cls, name):
    with open("ingredients.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for meal in reader:
            if meal["name"] == name:
                break
        else:
            raise Exception(f"Meal {name} not in DB")
    name = meal.pop("name")
    description = meal.pop("description")
    stats_cls = cls.__dataclass_fields__["stats"].type
    stats = {k: float(v) for k, v in meal.items() if k in stats_cls._fields}
    return cls(name, description, stats_cls(**stats))
