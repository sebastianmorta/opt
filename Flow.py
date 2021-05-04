from itertools import permutations, combinations

import numpy
from matplotlib import pyplot as plt
from numpy.lib import math
from numpy.random import permutation

from randomgen import flow, floww
import random
import numpy as np
from random import randint, uniform
from numpy import e
import matplotlib


class FlowShop:
    def __init__(self, n, m, seed):
        self.n = n
        self.m = m
        self.data = flow(n, m, seed)
        self.Tmax = 1000
        self.permutation = permutation([*range(self.n)])

    def Cmax(self, data, n, m):
        C = numpy.zeros((int(n + 1), int(m + 1)))
        for j in range(1, n + 1):
            for k in range(1, m + 1):
                C[j][k] = max(C[j - 1][k], C[j][k - 1]) + data[j - 1][1][k - 1]
        return C[n][m]

    def randomSearch(self, iteration_depth):
        #           754.0 [3 0 9 2 8 6 5 4 7 1]
        best_cmax = 999999
        temp_sequence = self.data
        best_sequence = []
        for _ in range(iteration_depth):
            temp_cmax = self.Cmax(temp_sequence, self.n, self.m)
            temp_sequence = self.swapPositions(temp_sequence)
            if temp_cmax < best_cmax:
                best_sequence = temp_sequence
                best_cmax = temp_cmax
            temp_sequence = best_sequence  # this line if we should reset seq when Cmax is worse
        print(best_cmax, best_sequence[:, 0])
        return best_cmax

    def swapPositions(self, data):
        x1, x2 = randint(0, len(data) - 1), randint(0, len(data) - 1)
        data[[x1, x2]] = data[[x2, x1]]
        return data

    def swapNeighbour(self, data):
        x1 = randint(0, len(data) - 1)
        x2 = x1 + (-1 ** randint(0, 1)) if (len(data) - 1) > x1 > 0 else x1 - 1 if x1 > 0 else x1 + 1
        data[[x1, x2]] = data[[x2, x1]]
        return data

    def swapInsert(self, data):
        x1, x2 = 3,6
        idx = list(data[:, 0])
        data = self.convertData(data)
        data.insert(x1, data.pop(x2))
        idx.insert(x1, idx.pop(x2))
        return self.reconvertData(data, idx)

    def simulatedAnnealing(self, T, depth):
        best_sequence = old_sequence = self.data
        best_cmax = old_cmax = 9999999
        while T > 0.01:
            for _ in range(depth):
                new_sequence = self.swapPositions(old_sequence)
                old_cmax = self.Cmax(new_sequence, self.n, self.m)
                new_cmax = self.Cmax(new_sequence, self.n, self.m)
                if new_cmax < old_cmax:
                    old_sequence = new_sequence
                    old_cmax = new_cmax
                else:
                    delta = new_cmax - old_cmax
                    p = uniform(0, 1)
                    if p <= self.getProbability(delta, T):
                        old_sequence = new_sequence
                        old_cmax = new_cmax
            T *= 0.95
            if best_cmax > old_cmax:
                best_cmax = old_cmax
                best_sequence = old_sequence
        print(best_cmax, best_sequence[:, 0])
        return best_cmax

    def getProbability(self, delta, t):
        return e ** (-delta / t)

    def makeChart(self):
        a = [10, 20, 50, 100, 200, 500, 1000, 2000]
        iterDepth = T = [val for val in a for _ in range(10)]
        t_sa = np.array([[T[i], self.simulatedAnnealing(T[i], 100)] for i in range(len(T))])
        d_sa = np.array([[iterDepth[i], self.simulatedAnnealing(1000, iterDepth[i])] for i in range(len(T))])
        d_rs = np.array([[iterDepth[i], self.randomSearch(iterDepth[i])] for i in range(len(T))])
        return [t_sa, d_sa, d_rs]

    def drawChart(self, tab):
        ttt = ["temperature", "depth-SA", "depth-RS"]
        yyy = "Cmax"
        xxx = ["T", "iterations", "iterations"]
        i = 0
        for t in tab:
            x = t[:, 0]
            y = t[:, 1]
            plt.scatter(x, y, label="stars", color="green",
                        marker="*", s=30)

            plt.xlabel(xxx[i])
            plt.ylabel(yyy)
            plt.title(ttt[i])
            plt.legend()
            plt.show()
            i += 1

    def SumSortP(self, n):
        return [self.data[i] for i in sorted([*range(n)], key=lambda x: self.Psum(x), reverse=True)]

    def Psum(self, n):
        return sum(self.convertData(self.data)[n])

    def convertData(self, data):
        return [i[1] for i in data]
        # return np.array([i[1] for i in data])

    def reconvertData(self, data, idx):
        return np.array([[idx[i], data[i]] for i in range(len(idx))], dtype='object')

    def Neh(self, n, m):
        SortedList = self.SumSortP(n)
        CurrentTask = SortedList[0]
        sequence = [CurrentTask]
        best_sequence = []
        for i in range(1, n):  # dla każdego zadania
            BestCmax = float("inf")  # bardzo duża liczba
            for j in range(i + 1):  # dla każdej pozycji w permutacji
                temp_sequence = sequence[:]
                temp_sequence.insert(j, SortedList[i])
                n = len(temp_sequence)
                CurrentCmax = self.Cmax(temp_sequence, n, m)
                if CurrentCmax < BestCmax:
                    best_sequence = temp_sequence
                    BestCmax = CurrentCmax
            sequence = best_sequence
        return int(BestCmax)


if __name__ == '__main__':
    result_tab = []
    data = flow(10, 5, 123123)
    print(data)
    f = FlowShop(10, 5, 123123)
    # f.Cmax(data, 10, 5)
    # print("aaa")
    # f.randomSearch(100)
    # print(f.simulatedAnnealing(10000))
    #
    # print(f.Neh(10, 5))
    # perm = combinations([*range(10)], 2)
    # for i in list(perm):
    #     print(i)
    # f.drawChart(f.makeChart())
    # a = range(10)
    # a = [val for val in a for _ in range(4)]
    # print(a)
    print()
    print(f.swapInsert(data))
    # print()
    # x = f.convertData(data)
    # print(x)
    # print()
    # print(f.reconvertData(x, [*range(10)]))
