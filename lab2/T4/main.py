import random
import math


class DistributionTester:
    def __init__(self,
                 generator_function=None,
                 percentile_function=None,
                 *args):

        self._sequence = sorted(generator_function(*args))
        self.percentile_function = percentile_function

    @property
    def sequence(self):
        return self._sequence

    def calculate_percentile(self, p):
        return self.percentile_function(self.sequence, p)


class Generator:
    @staticmethod
    def step_generator(first, last, step):
        return list(range(first, last, step))

    @staticmethod
    def random_generator(count, mean, variance):
        return [random.gauss(mean, variance) for _ in range(count)]

    @staticmethod
    def fibonacci_generator(count):
        fibonacci_sequence = list()

        for i in range(count):
            if i < 2:
                fibonacci_sequence.append(i)
            else:
                fibonacci_sequence.append(
                    fibonacci_sequence[i-1] + fibonacci_sequence[i-2])

        return fibonacci_sequence


class Percentile:
    @staticmethod
    def nearest_rank(seq, p):
        return seq[int(math.ceil(float(p)/100 * len(seq))) - 1]

    @staticmethod
    def closest_ranks_interpolation(seq, p):
        percentiles = list()

        for i, _ in enumerate(seq):
            percentiles.append(100. * (i - 0.5)/len(seq))

        if p < percentiles[0]:
            return percentiles[0]

        elif p > percentiles[-1]:
            return percentiles[-1]

        else:
            idx = 0
            for i, num in enumerate(seq):
                if num > p:
                    idx = i - 1
                    break

            return round(seq[idx] + len(seq) * (p - percentiles[idx]) * (percentiles[idx + 1] - percentiles[idx]) / 100.)


def test():
    d1 = DistributionTester(Generator.step_generator,
                            Percentile.nearest_rank, 0, 10, 1)
    d2 = DistributionTester(Generator.random_generator,
                            Percentile.closest_ranks_interpolation, 10, 1, 0)
    d3 = DistributionTester(
        Generator.fibonacci_generator, Percentile.nearest_rank, 10)
    print(d1.calculate_percentile(80), d2.calculate_percentile(
        80), d3.calculate_percentile(80), sep='\n')


def main():
    test()


if __name__ == '__main__':
    main()
