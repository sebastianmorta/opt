from itertools import combinations
from random import shuffle, randint

import numpy
import numpy as np

from randomgen import flow2

c1 = 0.0481156
c2 = 0.6681845
c3 = 0.2836999
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


a1 = []
a2 = []


class LastTask:
    def __init__(self, n, data):
        self.n = n
        self.m = 3
        self.perm = [*range(n)]
        self.data = data
        self.P = []
        self.F = []
        self.black_list = []
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

    def returnDelay(self, perm):
        return [self.data[i].d for i in perm]

    def Cmax(self, data, return_tab, n=5, m=3):
        C = numpy.zeros((int(n + 1), int(m + 1)))
        for j in range(1, n + 1):
            for k in range(1, m + 1):
                C[j][k] = max(C[j - 1][k], C[j][k - 1]) + data[j - 1][k - 1]
        return np.delete(np.delete(C, 0, 0), 0, 1) if return_tab else C[n][m]

    def totalFlowtime(self, purpose, d):
        return sum(purpose[i][2] for i in range(self.n))

    def maxTardiness(self, purpose, d):
        return max([max(0, purpose[i][2] - d[i]) for i in range(self.n)])

    def totalTardiness(self, purpose, d):
        return sum([max(0, purpose[i][2] - d[i]) for i in range(self.n)])

    def maxLateness(self, purpose, d):
        return max([purpose[i][2] - d[i] for i in range(self.n)])

    def swapInsert(self, data):
        x1, x2 = randint(0, len(data) - 1), randint(0, len(data) - 1)
        data.insert(x1, data.pop(x2))
        return data

    def comparePerms(self, perm1, perm2):
        c1, c2 = self.Cmax(self.returnP(perm1), True, n=self.n), self.Cmax(self.returnP(perm2), True, n=self.n)
        d1, d2 = self.returnDelay(perm1), self.returnDelay(perm2)
        c1_score, c2_score = [], []
        for bench_id, bench_name in enumerate(self.benchmark):
            func = self.benchmark[bench_name]
            b1, b2 = func(c2, d2), func(c1, d1)

            a1.append(b1)
            a2.append(b2)
            if b2 < b1:
                c2_score.append(2)
                c1_score.append(0)
            elif b2 > b1:
                c1_score.append(2)
                c2_score.append(0)
            else:
                c1_score.append(1)
                c2_score.append(1)

        return [c1_score, c2_score]

    def removeDuplicates(self, rmv):
        res = []
        for i in rmv:
            if i not in res:
                res.append(i)
        return res

    def appendToP(self, perm, c1_score, c2_score):
        permiss = True
        for i in range(len(c2_score)):
            if (c2_score[i] - c1_score[i]) < 0:
                if randint(1, 100) < 10 * sum(c2_score):
                    self.P.append(perm)
                permiss = False
                break
        if permiss:
            self.P.append(perm)

    def removeFromF(self, perm1, perm2, c1_score, c2_score):
        scr1, scr2 = max(c1_score), max(c2_score)
        if scr1 == 2 and scr2 == 2:
            return
        else:
            if sum(c1_score) > sum(c2_score):
                self.black_list.append(perm2)
            else:
                self.black_list.append(perm1)

    def simulatedAnnealing(self, depth):
        old_solution = self.returnPerm(self.data)
        shuffle(old_solution)
        self.P.append(old_solution)
        for it in range(depth):
            new_solution = self.swapInsert(list.copy(old_solution))
            if new_solution == old_solution:
                continue
            tmp = self.comparePerms(old_solution, new_solution)
            self.appendToP(new_solution, tmp[0], tmp[1])
            old_solution = list.copy(new_solution)
        self.P = self.removeDuplicates(self.P)
        self.F = list.copy(self.P)
        for perm1, perm2 in combinations(self.P, 2):
            scr = self.comparePerms(perm1, perm2)
            self.removeFromF(perm1, perm2, scr[0], scr[1])
        self.black_list = self.removeDuplicates(self.black_list)
        for rmv in self.black_list:
            self.F.remove(rmv)
        print(self.P)
        print(self.F)
        self.P.clear()
        self.F.clear()
        self.black_list.clear()

    def scalar(self, perm):
        purpose = self.Cmax(self.returnP(perm), True, n=self.n)
        d = self.returnDelay(perm)
        return c1 * self.totalFlowtime(purpose, d) + c2 * self.maxTardiness(purpose, d) + c3 * \
               self.totalTardiness(purpose, d)

    def scalarAlgorithm(self, depth):
        old_solution = self.returnPerm(self.data)

        # start solution - random
        shuffle(old_solution)

        # x_best <- scalar(x)
        old_x = self.scalar( old_solution)
        # print(new_solution)
        self.best_x = old_x
        self.best_solution = list.copy(old_solution)

        for it in range(depth):
            new_solution = self.swapInsert(list.copy(old_solution))
            new_x = self.scalar( new_solution)
            if new_x < old_x:
                old_solution = list.copy(new_solution)
                old_x = new_x
                if new_x < self.best_x:
                    self.best_solution = list.copy(new_solution)
                    self.best_x = new_x
            else:
                if randint(1, 100) < 0.2:
                    old_solution = list.copy(new_solution)
                    old_x = new_x
                    if new_x < self.best_x:
                        self.best_solution = list.copy(new_solution)
                        self.best_x = new_x
        print(self.best_x, self.best_solution)


n = 10
p, delay = flow2(n, 123123)
t = LastTask(n, init(n))

t.simulatedAnnealing(1000)
t.scalarAlgorithm(100)

b1 = a1[0::4] + a2[0::4]
b2 = a1[1::4] + a2[1::4]
b3 = a1[2::4] + a2[2::4]
b4 = a1[3::4] + a2[3::4]

print("kryterium1 średnia", sum(b1) / len(b1))
print("kryterium2 średnia", sum(b2) / len(b2))
print("kryterium3 średnia", sum(b3) / len(b3))
print("kryterium4 średnia", sum(b4) / len(b4))

kryt1 = sum(b1) / len(b1)
kryt2 = sum(b2) / len(b2)
kryt3 = sum(b3) / len(b3)


print(kryt1*c1)
print(kryt2*c2)
print(kryt3*c3)


# tt = t.totalFlowtime(a)
# print(tt)
# ttt = t.maxTardiness(a, d)
# print(ttt)
# tttt = t.totalTardiness(a, d)
# print(tttt)
# ttttt = t.maxLateness(a, d)
# print(ttttt)