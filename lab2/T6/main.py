from __future__ import annotations
from copy import deepcopy


class Observer:
    def __init__(self, source: Sheet):
        self.__source = source

    def update(self):
        for cell in self.__source.cell_dict.values():
            cell.value = self.__source.evaluate(cell)


class Cell:
    def __init__(self, exp, value=0):
        self.__value = value
        self.__exp = exp

    @property
    def exp(self):
        return deepcopy(self.__exp)

    @exp.setter
    def exp(self, exp):
        self.__exp = exp

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Sheet:
    def __init__(self, width, height):
        self.cell_dict = dict()

        for i in range(width*height):
            self.cell_dict[i] = Cell('0', self)

        self.get_coordinates = dict()
        self.__most_recent_cell = 0
        self.__observer = Observer(self)

    def cell(self, ref):
        if ref in self.get_coordinates:
            return self.cell_dict[self.get_coordinates[ref]]

    def set(self, ref, exp):
        def check_circular_dependency(cell):
            queue = list()
            queue.extend(self.getrefs(cell))
            while queue:
                current = queue.pop(0)
                if current == cell:
                    raise RuntimeError('Circular dependency')
                queue.extend(self.getrefs(current))
        cell = self.cell(ref)
        if cell is None:
            cell = Cell(exp, self)
            check_circular_dependency(cell)
            cell.value = self.evaluate(cell)
            self.get_coordinates[ref] = self.__most_recent_cell
            self.__most_recent_cell += 1
        else:
            cell.exp = exp
            check_circular_dependency(cell)
            cell.value = self.evaluate(cell)

        self.__observer.update()

        self.cell_dict[self.get_coordinates[ref]] = cell

    def getrefs(self, cell: Cell):
        return [self.cell(x) for x in cell.exp.split('+') if self.cell(x) is not None]

    def evaluate(self, cell: Cell):
        try:
            return int(eval(cell.exp))
        except:
            return sum([self.evaluate(self.cell_dict[self.get_coordinates[x]]) for x in cell.exp.split('+')])

    def print(self):
        for cell_ref in sorted(self.get_coordinates.keys()):
            print(
                f'[{cell_ref}]: {self.cell_dict[self.get_coordinates[cell_ref]].exp}\n')


if __name__ == "__main__":
    s = Sheet(5, 5)
    print()

    s.set('A1', '2')
    s.set('A2', '5')
    s.set('A3', 'A1+A2')
    s.print()
    print()

    s.set('A1', '4')
    s.set('A4', 'A1+A3')
    s.print()
    print()

    try:
        s.set('A1', 'A3')
    except RuntimeError as e:
        print("Caught exception:", e)
    s.print()
    print()
