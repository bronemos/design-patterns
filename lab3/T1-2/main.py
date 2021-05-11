import os
import importlib


def myfactory(module_name):
    return getattr(importlib.import_module("plugins." + module_name), "create")


def printGreeting(pet):
    print(f"{pet.name()} pozdravlja: {pet.greet()}")


def printMenu(pet):
    print(f"{pet.name()} voli {pet.menu()}.")


def test():
    pets = []
    # obiđi svaku datoteku kazala plugins
    for mymodule in os.listdir("plugins"):
        moduleName, moduleExt = os.path.splitext(mymodule)
        # ako se radi o datoteci s Pythonskim kodom ...
        if moduleExt == ".py":
            # instanciraj ljubimca ...
            ljubimac = myfactory(moduleName)("Ljubimac " + str(len(pets)))
            # ... i dodaj ga u listu ljubimaca
            pets.append(ljubimac)

    # ispiši ljubimce
    for pet in pets:
        printGreeting(pet)
        printMenu(pet)


def main():
    test()


if __name__ == "__main__":
    main()