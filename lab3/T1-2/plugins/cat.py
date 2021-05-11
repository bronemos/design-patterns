class Cat:
    def __init__(self, name):
        self._name = name

    def name(self):
        return self._name

    def greet(self):
        return "Mijau!"

    def menu(self):
        return "mlako mlijeko"


def create(name):
    return Cat(name)