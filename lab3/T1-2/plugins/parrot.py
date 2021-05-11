class Parrot:
    def __init__(self, name):
        self._name = name

    def name(self):
        return self._name

    def greet(self):
        return "Sto mu gromova!"

    def menu(self):
        return "brazilske orahe"


def create(name):
    return Parrot(name)