from random import shuffle, randint

import numpy
import numpy as np

from randomgen import flow2


def init(n):
    p, delay = flow2(n, 123123)
    __data__ = [Task(i, p[i], delay[i]) for i in range(n)]
    return __data__


def returnOrder(data):
    return data.task_number


class Task:
    def __init__(self, task_number, p, delay):
        self.task_number = task_number
        self.p = p
        self.d = delay


class LastTask:
    def __init__(self, n, data):
        self.n = n
        self.m = 3
        self.perm = [*range(n)]
        self.data = data
        self.benchmark = {
            "totalFlowtime": self.totalFlowtime,
            "maxTardiness": self.maxTardiness,
            "totalTardiness": self.totalTardiness,
            "maxLateness": self.maxLateness
        }

    def returnPerm(self, perm):
        return [number.task_number for number in perm]

    def returnP(self, perm):
        return [self.data[i].p for i in perm]

    def Cmax(self, data, return_tab, n=5, m=3):
        C = numpy.zeros((int(n + 1), int(m + 1)))
        for j in range(1, n + 1):
            for k in range(1, m + 1):
                C[j][k] = max(C[j - 1][k], C[j][k - 1]) + data[j - 1][k - 1]
        return np.delete(np.delete(C, 0, 0), 0, 1) if return_tab else C[n][m]

    def totalFlowtime(self, purpose, d):
        return sum(purpose[i][3] for i in range(self.n + 1))

    def maxTardiness(self, purpose, d):
        return max([max(0, purpose[i][3] - d[i]) for i in range(self.n)])

    def totalTardiness(self, purpose, d):
        return sum([max(0, purpose[i][3] - d[i]) for i in range(self.n)])

    def maxLateness(self, purpose, d):
        return max([purpose[i][3] - d[i] for i in range(self.n)])

    def swapInsert(self, data):
        x1, x2 = randint(0, len(data) - 1), randint(0, len(data) - 1)
        data.insert(x1, data.pop(x2))
        return data

    def comparePerms(self, perm1, perm2):
        c1, c2 = self.Cmax(self.returnP(perm1), True), self.Cmax(self.returnP(perm2), True)
        c1_score, c2_score = 0, 0
        for bench_id, bench_name in enumerate(self.benchmark):
            func = self.benchmark[bench_name]


    def simulatedAnnealing(self, depth):
        P, i = [], 0
        old_solution = returnOrder(self.data)
        shuffle(old_solution)
        P.append(old_solution)
        for it in range(depth):
            new_solution = self.swapInsert(old_solution)
            shuffle(new_solution)
            self.comparePerms(old_solution, new_solution)


n = 5
p, delay = flow2(n, 123123)
t = LastTask(n)
print(p)
a = t.Cmax(p, 5)
print(a)
# tt = t.totalFlowtime(a)
# print(tt)
# ttt = t.maxTardiness(a, d)
# print(ttt)
# tttt = t.totalTardiness(a, d)
# print(tttt)
# ttttt = t.maxLateness(a, d)
# print(ttttt)