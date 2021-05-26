import numpy

from randomgen import flow2

n = 5
p, d = flow2(n, 123123)


class Task:
    def __init__(self, n):
        self.n = n
        self.m = 3

    def Cmax(self, data, n, m=3):
        C = numpy.zeros((int(n + 1), int(m + 1)))
        for j in range(1, n + 1):
            for k in range(1, m + 1):
                C[j][k] = max(C[j - 1][k], C[j][k - 1]) + data[j - 1][k - 1]
        return C

    def totalFlowtime(self, Cmax_tab):
        return sum(Cmax_tab[i][3] for i in range(self.n + 1))

    def maxTardiness(self, Cmax_tab, d):
        return max([max(0, Cmax_tab[i][3] - d[i]) for i in range(self.n)])

    def totalTardiness(self, Cmax_tab, d):
        return sum([max(0, Cmax_tab[i][3] - d[i]) for i in range(self.n)])

    def maxLateness(self, Cmax_tab, d):
        return max([Cmax_tab[i][3] - d[i] for i in range(self.n)])


t = Task(n)
print(p)
a = t.Cmax(p, 5)
print(a)
tt = t.totalFlowtime(a)
print(tt)
ttt = t.maxTardiness(a, d)
print(ttt)
tttt = t.totalTardiness(a, d)
print(tttt)
ttttt = t.maxLateness(a, d)
print(ttttt)
