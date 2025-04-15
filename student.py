from enum import Enum, auto
import random

class Traits(Enum):
    INTEGRITY = auto()
    AMBITION = auto()
    EMPATHY = auto()
    STUBBORNNESS = auto()
    CONFIDENCE = auto()

class Actions(Enum):
    STRICT = auto()
    LENIENT = auto()
    INDIFFERENT = auto()

class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.Happiness = 50
        self.traits = {trait: random.randint(20, 80) for trait in Traits}
        self.friendship = {}
        self.friends = []

    def add_friend(self, friend, score=None):
        if friend not in self.friends:
            self.friends.append(friend)
        if score is None:
            score = 50  # Default score if not based on trait matching
        self.friendship[friend.name] = score

    def update_happiness(self, action: Actions):
        change = 0
        if action == Actions.STRICT:
            factor = 1 + self.traits[Traits.STUBBORNNESS] / 100
            change = int(-5 * factor)
        elif action == Actions.LENIENT:
            factor = 1 + self.traits[Traits.EMPATHY] / 100
            change = int(5 * factor)
        else:
            factor = 1 + self.traits[Traits.INTEGRITY] / 100
            change = int(-3 * factor)

        self.Happiness = max(0, min(100, self.Happiness + change))
        return change

    def __str__(self):
        traits_string = "\n".join([f"{trait.name.capitalize()}: {value}" for trait, value in self.traits.items()])
        friends_string = ", ".join([friend.name for friend in self.friends]) if self.friends else "None"
        return (
            f"Name: {self.name}\n"
            f"Age: {self.age}\n"
            f"Happiness: {self.Happiness}\n"
            f"Traits:\n{traits_string}\n"
            f"Friends:\n{friends_string}"
        )
