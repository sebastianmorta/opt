import random
from itertools import combinations
from random import shuffle, randint
from matplotlib.path import Path
from randomgen import flow2
import matplotlib.pyplot as plt
import numpy
import numpy as np
import plotly
import matplotlib.patches as patches

c1 = 0.0481156
c2 = 0.6681845
c3 = 0.2836999


def init(n):
    p, delay = flow2(n, 123123)
    __data__ = [Task(i, p[i], delay[i]) for i in range(n)]
    return __data__


class Parameter:
    def __init__(self, solution, last_task, name):
        self.name = name
        self.last_task = last_task
        self.solution = solution
        self.benchmark1 = self.calculateBenchmark(self.last_task.totalFlowtime)
        self.benchmark2 = self.calculateBenchmark(self.last_task.maxTardiness)
        self.benchmark3 = self.calculateBenchmark(self.last_task.totalTardiness)
        self.benchmark4 = self.calculateBenchmark(self.last_task.maxLateness)

    def calculateBenchmark(self, func):
        return func(self.last_task.Cmax(self.last_task.returnP(self.solution), True),
                    self.last_task.returnDelay(self.solution))


class Task:
    def __init__(self, task_number, p, delay):
        self.task_number = task_number
        self.p = p
        self.d = delay


class Draw:
    def __init__(self, P, F, last_task):
        self.last_task = last_task
        self.P = P
        self.F = F
        self.X_axis_P, self.Y_axis_P = self.makeChartSpace(P)
        self.X_axis_F, self.Y_axis_F = self.makeChartSpace(F)
        self.X_axis_P3d, self.Y_axis_P3d, self.Z_axis_P3d = self.makeChartSpace3d(P)
        self.X_axis_F3d, self.Y_axis_F3d, self.Z_axis_F3d = self.makeChartSpace3d(F)

    def makeChartSpace(self, tab):
        X_axis, Y_axis = [], []
        for t in tab:
            X_axis.append(self.last_task.totalFlowtime(self.last_task.Cmax(self.last_task.returnP(t), True),
                                                       self.last_task.returnDelay(t)))
            Y_axis.append(self.last_task.maxTardiness(self.last_task.Cmax(self.last_task.returnP(t), True),
                                                      self.last_task.returnDelay(t)))
        return sorted(X_axis), [x for _, x in sorted(zip(X_axis, Y_axis))]

    def makeChartSpace3d(self, tab):
        X_axis, Y_axis, Z_axis = [], [], []
        for t in tab:
            X_axis.append(self.last_task.totalFlowtime(self.last_task.Cmax(self.last_task.returnP(t), True),
                                                       self.last_task.returnDelay(t)))
            Y_axis.append(self.last_task.maxTardiness(self.last_task.Cmax(self.last_task.returnP(t), True),
                                                      self.last_task.returnDelay(t)))
            Z_axis.append(self.last_task.totalTardiness(self.last_task.Cmax(self.last_task.returnP(t), True),
                                                        self.last_task.returnDelay(t)))
        return sorted(X_axis), [y for _, y in sorted(zip(X_axis, Y_axis))], [z for _, z in sorted(zip(X_axis, Z_axis))]


class LastTask:
    def __init__(self, n, data):
        self.n = n
        self.m = 3
        self.data = data
        self.P = []
        self.F = []
        self.black_list = []
        self.benchmark = {
            "totalFlowtime": self.totalFlowtime,
            "maxTardiness": self.maxTardiness,
            # "totalTardiness": self.totalTardiness,
            # "maxLateness": self.maxLateness
        }

    def returnPerm(self, perm):
        return [number.task_number for number in perm]

    def returnP(self, perm):
        return [self.data[i].p for i in perm]

    def returnDelay(self, perm):
        return [self.data[i].d for i in perm]

    def Cmax(self, p_values, return_tab, n=10, m=3):
        C = numpy.zeros((int(n + 1), int(m + 1)))
        for j in range(1, n + 1):
            for k in range(1, m + 1):
                C[j][k] = max(C[j - 1][k], C[j][k - 1]) + p_values[j - 1][k - 1]
        return np.delete(np.delete(C, 0, 0), 0, 1) if return_tab else C[n][m]

    def totalFlowtime(self, purpose, d):
        return sum(purpose[i][2] for i in range(self.n))

    def maxTardiness(self, purpose, d):
        return int(max([max(0, purpose[i][2] - d[i]) for i in range(self.n)]))

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
            b1, b2 = func(c1, d1), func(c2, d2)
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
        self.P = [x for x in self.P if x not in self.F]
        return self.P, self.F

    def cleaner(self):
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
        shuffle(old_solution)  # start solution - random
        old_x = self.scalar(old_solution)  # x_best <- scalar(x)
        self.best_x = old_x  # print(new_solution)
        self.best_solution = list.copy(old_solution)

        for it in range(depth):
            new_solution = self.swapInsert(list.copy(old_solution))
            new_x = self.scalar(new_solution)
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
        # print(self.best_x, self.best_solution)
        return self.best_x


def calcHVI(fpx, fpy, Z, iter):
    field = (Z[1] - fpy[0]) * (Z[0] - fpx[0])
    for i in range(len(fpx) - 1):
        field += (fpy[i] - fpy[i + 1]) * (Z[0] - fpx[i + 1])
    return print(f"field of HVI for iter={iter}", field)


def drawChartPareto(iter, t):
    P, F = t.simulatedAnnealing(iter)
    d = Draw(P, F, t)
    plt.plot(d.X_axis_P, d.Y_axis_P, 'bo', label='P')
    plt.plot(d.X_axis_F, d.Y_axis_F, 'ro-', label='F')
    plt.grid(1, 'major')
    plt.title("iter=" + str(iter))
    plt.xlabel("Total Flowtime", size=16)
    plt.ylabel("Max Tardiness", size=16)
    plt.legend()
    plt.savefig(f"plots/1task{iter}.png")
    plt.show()
    t.cleaner()


def calcShape(fronts_pareto_X, fronts_pareto_Y):
    tmpx, tmpy = [], []
    for xxx, yyy in zip(list.copy(fronts_pareto_X), list.copy(fronts_pareto_Y)):
        tmptmpx, tmptmpy = [xxx[0]], []
        for i in range(len(xxx) - 1):
            tmptmpx.append(xxx[i + 1])
            tmptmpx.append(xxx[i + 1])
            tmptmpy.append(yyy[i])
            tmptmpy.append(yyy[i])
        tmptmpy.append(yyy[len(yyy) - 1])
        tmpx.append(tmptmpx)
        tmpy.append(tmptmpy)
    return tmpx, tmpy


def drawHVI():
    worst_F_X, worst_F_Y, fronts_pareto_X, fronts_pareto_Y = [], [], [], []
    for iter in iter_Tab:
        P, F = t.simulatedAnnealing(iter)
        d = Draw(P, F, t)
        fronts_pareto_X.append(d.X_axis_F)
        fronts_pareto_Y.append(d.Y_axis_F)
        worst_F_X.append(max(d.X_axis_F))
        worst_F_Y.append(max(d.Y_axis_F))
        t.cleaner()
    Z = [max(worst_F_X), max(worst_F_Y)]
    fronts_pareto_X_shape, fronts_pareto_Y_shape = calcShape(fronts_pareto_X, fronts_pareto_Y)

    for x_shape, y_shape, x_fp, y_fp, it in zip(fronts_pareto_X_shape, fronts_pareto_Y_shape, fronts_pareto_X,
                                                fronts_pareto_Y, iter_Tab):
        calcHVI(x_fp, y_fp, Z, it)
        x_shape.insert(0, Z[0])
        y_shape.insert(0, Z[1])
        if y_shape[1] < Z[1]:
            x_shape.insert(1, x_shape[1])
            y_shape.insert(1, Z[1])
        if x_shape[len(x_shape) - 1] < Z[0]:
            x_shape.insert(len(x_shape), Z[0])
            y_shape.insert(len(y_shape), y_shape[len(y_shape) - 1])
    drawChartHVI(fronts_pareto_X_shape, fronts_pareto_Y_shape, fronts_pareto_X, fronts_pareto_Y, Z)


def drawChartHVI(front_pareto_X_shape, front_pareto_Y_shape, fronts_pareto_X, fronts_pareto_Y, Z):
    colors = ['magenta', 'green', 'blue', 'yellow', 'red']
    markers_shape = ["m-", "g-", 'b-', 'y-', 'r-']
    markers2 = ["m*", "g1", 'bx', 'y^', 'rP']
    maxx, maxy, minx, miny = 0, 0, 999999, 9999999
    fig, ax = plt.subplots()
    for fpx, fpy, x, y, color, mark, mark2, iter in zip(front_pareto_X_shape, front_pareto_Y_shape, fronts_pareto_X,
                                                        fronts_pareto_Y, colors, markers_shape,
                                                        markers2, iter_Tab):
        verts = [(x, y) for x, y in zip(fpx, fpy)]
        codes = [Path.LINETO for _ in range(len(verts) - 1)]
        verts.append((0., 0.))
        codes.append(Path.CLOSEPOLY)
        codes.insert(0, Path.MOVETO)
        path = Path(verts, codes)
        patch = patches.PathPatch(path, facecolor=color, lw=1, alpha=.2)
        plt.plot(fpx[2:-1], fpy[2:-1], mark)
        plt.plot(x, y, mark2, label=f'F for {iter}', alpha=.6)
        ax.add_patch(patch)
        miny, minx, maxy, maxx = min(fpy) if min(fpy) < miny else miny, min(fpx) if min(fpx) < minx else minx, max(
            fpy) if max(fpy) > maxy else maxy, max(fpx) if max(fpx) > maxx else maxx
    ax.set_xlim(minx - 10, maxx + 40)
    ax.set_ylim(miny - 10, maxy + 20)
    plt.xlabel("Total Flowtime", size=16)
    plt.ylabel("Max Tardiness", size=16)
    plt.grid(1, 'major')
    plt.plot(Z[0], Z[1], 'k^')
    plt.annotate("Z", (Z[0], Z[1]), size=16)
    plt.title("HVI", size=16)
    plt.legend()
    plt.savefig(f"plots/HVI.png")
    plt.show()


def drawChart3d(iter, t):
    plotly.offline
    P, F = t.simulatedAnnealing(iter)
    d = Draw(P, F, t)
    ax = plt.axes(projection='3d')
    ax.scatter3D(d.X_axis_F3d, d.Y_axis_F3d, d.Z_axis_F3d, c=d.Z_axis_F3d, cmap='Reds', label='F')
    ax.scatter3D(d.X_axis_P3d, d.Y_axis_P3d, d.Z_axis_P3d, c=d.Z_axis_P3d, cmap='Blues', label='P')
    ax.plot3D(d.X_axis_F3d, d.Y_axis_F3d, d.Z_axis_F3d, 'red')
    plt.title("iter=" + str(iter))
    ax.set_xlabel("Total Flowtime", size=16)
    ax.set_ylabel("Max Tardiness", size=16)
    ax.set_zlabel("Total Tardiness", size=16)
    plt.legend()
    plt.show()
    t.cleaner()


def drawScalar():
    x_ax, y_ax = [], []
    for it in iter_Tab:
        x, y = [], []
        for i in range(100):
            y.append(t.scalarAlgorithm(it))
            x.append(it)
        y_ax.append(sum(y) / len(y))
        x_ax.append(sum(x) / len(x))
    plt.plot(x_ax, y_ax, 'go-', label='scalar')
    plt.xlabel("iter")
    plt.ylabel("best s(x)")
    plt.grid(1, 'major')
    plt.legend()
    plt.savefig("plots/scalar.png")
    # plt.show()


def wiz2(solutions):
    BM = ['krit1', 'krit2', 'krit3', 'krit4']
    norm1, norm2, norm3, norm4 = 0.028849, 0.4, 0.17, 0.4
    colors = ["m-", "g-", 'b-', 'y-', 'r-']
    fig, ax = plt.subplots(figsize=(10, 6))
    for sol, color in zip(solutions, colors):
        values = [sol.benchmark1 * norm1, sol.benchmark2 * norm2, sol.benchmark3 * norm3, sol.benchmark4 * norm4]
        ax.plot(BM, values, color, label=sol.name)
        plt.grid(1, 'major')
        plt.legend()
    plt.savefig("plots/wiz2.png")
    plt.show()


def wiz3(solutions):
    BM = [['$krit1_1$', '$krit2_1$', '$krit3_1$', '$krit4_1$'], ['$krit1_2$', '$krit2_2$', '$krit3_2$', '$krit4_2$'],
          ['$krit1_3$', '$krit2_3$', '$krit3_3$', '$krit4_3$'], ['$krit1_w$', '$krit2_w$', '$krit3_w$', '$krit4_w$']]
    print(BM)
    norm1, norm2, norm3, norm4 = 0.028849, 0.4, 0.17, 0.4
    colors = ["m-", "g-", 'b-', 'r-']
    values = []
    names = []
    fig, ax = plt.subplots(figsize=(10, 10))
    for sol, color in zip(solutions, colors):
        values.append([sol.benchmark1 * norm1, sol.benchmark2 * norm2, sol.benchmark3 * norm3, sol.benchmark4 * norm4])
        names.append(sol.name)
    for v, b, c, n in zip(values, BM, colors, names):
        ax.scatter(v, b, label=n)
    plt.grid(axis='y', linestyle='dotted')
    plt.legend()
    plt.savefig("plots/wiz3.png")
    plt.show()


n = 10
iter_Tab = [100, 200, 400, 800, 1600]
# iter_Tab = [100, 200, 400]
p, delay = flow2(n, 123123)
t = LastTask(n, init(n))
for it in iter_Tab:
    drawChartPareto(it, t)

drawHVI()

t.benchmark["totalTardiness"] = t.totalTardiness
for it in iter_Tab:
    drawChart3d(it, t)

drawScalar()

k = LastTask(n, init(n))

k.benchmark["totalTardiness"] = k.totalTardiness
k.benchmark["maxLateness"] = k.maxLateness
print(k.benchmark)
k.simulatedAnnealing(600)

task3 = random.sample(k.F, 3) + [random.choice(k.P)]
names = ['FP1', 'FP2', 'FP3', 'weak']
t3 = [Parameter(sol, k, name) for sol, name in zip(task3, names)]
wiz2(t3)
wiz3(t3)
# drawChart3d(5, t)

# drawChartHVI(100, t)


# a=[1,2,3,4,5,6]
# b=[11,22,33,44]
#
# for i, j in zip(a,b):
#     print(i,j)


#
# b1 = a1[0::4] + a2[0::4]
# b2 = a1[1::4] + a2[1::4]
# b3 = a1[2::4] + a2[2::4]
# b4 = a1[3::4] + a2[3::4]
#
# print("kryterium1 średnia", sum(b1) / len(b1))
# print("kryterium2 średnia", sum(b2) / len(b2))
# print("kryterium3 średnia", sum(b3) / len(b3))
# print("kryterium4 średnia", sum(b4) / len(b4))
#
# kryt1 = sum(b1) / len(b1)
# kryt2 = sum(b2) / len(b2)
# kryt3 = sum(b3) / len(b3)
#
# print(kryt1 * c1)
# print(kryt2 * c2)
#
# print(kryt3 * c3)

# tt = t.totalFlowtime(a)
# print(tt)
# ttt = t.maxTardiness(a, d)
# print(ttt)
# tttt = t.totalTardiness(a, d)
# print(tttt)
# ttttt = t.maxLateness(a, d)
# print(ttttt)
