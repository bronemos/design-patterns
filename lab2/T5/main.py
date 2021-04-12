from copy import deepcopy
from typing import Callable
import datetime


class Izvor:
    def next(self):
        raise NotImplementedError

    def attach_observer(self):
        raise NotImplementedError

    def detach_observer(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError


class TargetClass:
    def get_state(self):
        raise NotImplementedError


class Promatrac:
    def __init__(self, source: TargetClass, action: Callable):
        self.__source = source
        self.__action = action

    def update(self):
        return self.__action(self.__source.get_state())


def write_to_file(path, data):
    with open(path, 'w') as f:
        f.write(f'{datetime.datetime.now()},{data}')


def calculate_sum(sequence):
    print(f'Sum: {sum(sequence)}')


def calcualte_mean(sequence):
    print(f'Mean: {sum(sequence) / len(sequence)}')


def calculate_median(sequence):
    index = int(len(sequence) / 2)
    median = float(sequence[index] + sequence[index + 1])/2
    print(f'Median: {median}')


class TipkovnickiIzvor(Izvor):
    def next(self):
        return int(input())


class DatotecniIzvor(Izvor):
    def __init__(self, path):
        self.__current_index = -1
        with open(path) as f:
            self.__lines = [int(x) for x in f.readlines()]
            self.__lines.append(-1)

    def next(self):
        self.__current_index += 1
        return self.__lines[self.__current_index]


class SlijedBrojeva(TargetClass):
    def __init__(self, source: Izvor):
        self.__sequence = list()
        self.__source = source
        self.__observers = list()

    def get_state(self):
        return deepcopy(self.__sequence)

    def kreni(self):
        while (number := self.__source.next()) != -1:
            print(number)
            self.update()
        print('Terminating')

    def attach_observer(self, observer: Promatrac):
        self.__observers.append(observer)

    def detach_observer(self, observer: Promatrac):
        self.__observers.remove(observer)

    def update(self):
        for observer in self.__observers:
            observer.update()


def main():
    sequence = SlijedBrojeva(TipkovnickiIzvor())


if __name__ == '__main__':
    main()
