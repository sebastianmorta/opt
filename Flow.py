import numpy

from randomgen import flow
import random
import numpy as np


def optimize(function, dimensions, lower_boundary, upper_boundary, max_iter, maximize=False):
    best_solution = np.array([float()] * dimensions)

    for i in range(dimensions):
        best_solution[i] = random.uniform(lower_boundary[i], upper_boundary[i])

    for _ in range(max_iter):

        solution1 = function(best_solution)

        new_solution = [lower_boundary[d] + random.random() * (upper_boundary[d] - lower_boundary[d]) for d in
                        range(dimensions)]

        if np.greater_equal(new_solution, lower_boundary).all() and np.less_equal(new_solution, upper_boundary).all():
            solution2 = function(new_solution)
        elif maximize:
            solution2 = -100000.0
        else:
            solution2 = 100000.0

        if solution2 > solution1 and maximize:
            best_solution = new_solution
        elif solution2 < solution1 and not maximize:
            best_solution = new_solution

    best_fitness = function(best_solution)

    return best_fitness, best_solution


n = 10
m = 5
data = flow(n, m, 123123)


def Cmax(data, n, m):
    C = numpy.zeros((int(n + 1), int(m + 1)))
    for j in range(1, n + 1):
        for k in range(1, m + 1):
            if j > 1 and k > 1:
                C[j][k] = max(C[j - 1][k], C[j][k - 1]) + data[j - 1][k - 1]
            elif j == 1 and k > 1:
                C[j][k] = C[j][k - 1] + data[j - 1][k - 1]
            elif k == 1 and j > 1:
                C[j][k] = C[j - 1][k] + data[j - 1][k - 1]
            elif k == 1 and j == 1:
                C[j][k] = data[j - 1][k - 1]
    print(n, m, C)
    return C


def SumSortP(data, n, m):
    permutation = []
    result = []
    for i in range(n):
        permutation.append(i)
    temp = sorted(permutation, key=lambda x: Psum(data, x, m), reverse=True)
    for i in temp:
        result.append(data[i])
    return result


def Psum(data, n, m):
    sumP = 0
    for i in range(m):
        sumP += data[n][i]
    return sumP


def RS(data, n, m):
    SortedList = SumSortP(data, n, m)
    CurrentTask = SortedList[0]
    sequence = [CurrentTask]
    best_sequence = []
    for i in range(1, n):  # dla każdego zadania
        BestCmax = float("inf")  # bardzo duża liczba
        for j in range(i + 1):  # dla każdej pozycji w permutacji
            temp_sequence = sequence[:]
            temp_sequence.insert(j, SortedList[i])
            n = len(temp_sequence)
            CurrentCmax = Cmax(temp_sequence, n, m)[n][m]
            if CurrentCmax < BestCmax:
                best_sequence = temp_sequence
                BestCmax = CurrentCmax
        sequence = best_sequence
    return int(BestCmax)


if __name__ == '__main__':
    result_tab = []
    data = flow(n, m, 123123)
    result = RS(data, n, m)
    result_tab.append(result)
    print('wyniki obliczone: ')
    print(result_tab)
