import random


class Psychic:
    def __init__(self, name, level=0):
        self.name = name
        self.answers = []
        self.level = level

    def get_answer(self):
        self.answers.append(random.randint(10, 100))
        return self.answers[-1]

    def change_level(self, increase=False):
        if increase:
            self.level += 1
        else:
            self.level -= 1


class Player:
    def __init__(self):
        self.numbers = []
