from itertools import combinations
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

    def removeDuplicates(self,rmv):
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
            print("----------new----------")
            print("old1", old_solution)
            new_solution = self.swapInsert(list.copy(old_solution))
            if new_solution == old_solution:
                continue
            print("new", new_solution)
            tmp = self.comparePerms(old_solution, new_solution)
            self.appendToP(new_solution, tmp[0], tmp[1])
            old_solution = list.copy(new_solution)
            print("old2", old_solution)
        print(self.P)
        self.P=self.removeDuplicates(self.P)
        self.F = list.copy(self.P)
        for perm1, perm2 in combinations(self.P, 2):
            scr = self.comparePerms(perm1, perm2)
            self.removeFromF(perm1, perm2, scr[0], scr[1])
        print(self.P)
        print("F ",self.F)
        print("black",self.black_list)
        self.black_list=self.removeDuplicates(self.black_list)
        for rmv in self.black_list:
            print("afasfasdfasf")
            self.F.remove(rmv)
        print(self.F)


n = 10
p, delay = flow2(n, 123123)
t = LastTask(n, init(n))
print(p)
a = t.Cmax(p, 5)
print(a)
t.simulatedAnnealing(100)
# tt = t.totalFlowtime(a)
# print(tt)
# ttt = t.maxTardiness(a, d)
# print(ttt)
# tttt = t.totalTardiness(a, d)
# print(tttt)
# ttttt = t.maxLateness(a, d)
# print(ttttt)
