from random import randint, shuffle
import random
from randomgen import witi


def getData():
    n = 10
    p, d, w = witi(n, 123123)
    data = [Task(p[i], d[i], w[i]) for i in range(n)]
    return data


class Task:
    def __init__(self, p, d, w):
        self.p = p
        self.d = d
        self.w = w


def takeSecond(elem):
    return elem[1]


class Genetic:
    def __init__(self, data):
        self.R = []
        self.X = []
        self.C = []
        self.best_value = 99999999
        self.best_sequence = []
        self.data = data
        self.n = len(data)
        self.best = []
        self.medium = []
        self.weak = []

    def WiTi(self, C, w, d):
        return max(0, C - d) * w

    def cFunc(self, perm):
        pe = [self.data[perm[i]].p for i in range(self.n)]
        return [sum(pe[:i]) for i in range(1, self.n + 1)]

    def crossingOperator(self, r1, r2):
        tmp1, tmp2 = randint(0, self.n), randint(0, self.n)
        idx1 = min(tmp1, tmp2)
        idx2 = max(tmp1, tmp2)
        return r1[:idx1] + r2[idx1:idx2] + r1[idx2:], r2[:idx1] + r1[idx1:idx2] + r2[idx2:]

    def orderedCrossover(self, r1, r2):
        c1, c2 = [-1] * self.n, [-1] * self.n
        start, end = sorted([random.randrange(self.n) for _ in range(2)])

        c1_inherited = []
        c2_inherited = []
        for i in range(start, end + 1):
            c1[i] = r1[i]
            c2[i] = r2[i]
            c1_inherited.append(r1[i])
            c2_inherited.append(r2[i])
        current_r2_position, current_r1_position = 0, 0
        fixed_pos = list(range(start, end + 1))
        i = 0
        while i < self.n:
            if i in fixed_pos:
                i += 1
                continue
            self.test(r2, c1, c1_inherited, current_r2_position, i)
            self.test(r1, c2, c2_inherited, current_r1_position, i)
            i += 1
        return c1, c2

    def test(self, r, c, c_inherited, current_r_position, i):
        test_c = c[i]
        if test_c == -1:
            r_trait = r[current_r_position]
            while r_trait in c_inherited:
                current_r_position += 1
                r_trait = r[current_r_position]
            c[i] = r_trait
            c_inherited.append(r_trait)

    def purposeFunc(self, Pi):
        c = self.cFunc(Pi)
        return sum([self.WiTi(c[i], data[Pi[i]].w, data[Pi[i]].d) for i in range(len(Pi))])

    def rmvItem(self, list1, list2):
        rm1 = random.choice(list1)
        list1.remove(rm1)
        rm2 = random.choice(list2)
        list2.remove(rm2)
        return (rm1, rm2), list1, list2

    def makeParents(self):
        dict = {1: self.best, 2: self.medium, 3: self.weak}
        while True:
            if (len(self.best) + len(self.medium) + len(self.weak)) > 1:
                a = dict[randint(1, 2)]
                b = dict[randint(1, 3)]
                if len(a) > 0 and len(b) > 0:
                    break
                else:
                    a = dict[randint(1, 3)]
                    b = dict[randint(1, 3)]
                    if len(a) > 0 and len(b) > 0:
                        break
            else:
                return 0
        if a == b:
            if len(a) > 1:
                t, a, b = self.rmvItem(a, b)
                self.R.append(t)
        else:
            t, a, b = self.rmvItem(a, b)
            self.R.append(t)
        return 1

    def pickParents(self, perms):
        idx1, idx2 = int(len(perms) / 3), int(len(perms) / 3 * 2)
        perms.sort(key=takeSecond)
        self.best, self.medium, self.weak = perms[:idx1], perms[idx1:idx2], perms[idx2:]
        a = 1
        for _ in range(self.n):
            if a != 0:
                a = self.makeParents()

    def updateBestForChild(self):
        for c in self.C:
            if c[1] < self.best_value:
                self.best_value = c[1]
                self.best_sequence = list.copy(c[0])
            c_perm, c_val, boo = self.mutating(c)
            if boo:
                self.C.append((c_perm, c_val))
                if c_val < self.best_value:
                    self.best_value = c_val
                    self.best_sequence = list.copy(c_perm)

    def swap(self, data):
        x1, x2 = randint(0, len(data) - 1), randint(0, len(data) - 1)
        data[x1], data[x2] = data[x2], data[x1]
        return data

    def mutating(self, child):
        if randint(1, 100) < 5:
            c = self.swap(child[0])
            c_val = self.purposeFunc(c)
            return c, c_val, True
        else:
            return child[0], child[1], False

    def selection(self):
        temp = self.X + self.C
        temp.sort(key=takeSecond)
        self.X.clear()
        self.C.clear()
        self.R.clear()
        self.X = temp[:int(self.n * 0.2)] + random.sample(temp[int(self.n * 0.2):], int(self.n * 0.81))
        shuffle(self.X)

    def initialPerm(self, Pi, p):
        old_sequence = list.copy(Pi)
        self.best_sequence = list.copy(Pi)
        old_value = self.purposeFunc(old_sequence)
        self.best_value = old_value
        self.X.append((old_sequence, old_value))
        for i in range(1, p):
            new_sequence = list.copy(old_sequence)
            shuffle(new_sequence)
            new_value = self.purposeFunc(new_sequence)
            self.X.append((new_sequence, new_value))
            if new_value < old_value:
                self.best_value = new_value
                self.best_sequence = list.copy(new_sequence)
            old_sequence, old_value = list.copy(new_sequence), new_value

    def makeChildren(self):
        for i in range(len(self.R)):
            c1, c2 = self.orderedCrossover(self.R[i][0][0], self.R[i][1][0])
            c1_val, c2_val = self.purposeFunc(c1), self.purposeFunc(c2)
            self.C.append((c1, c1_val))
            self.C.append((c2, c2_val))


def calculate(p, Pi, data):
    sol = Genetic(data)
    sol.initialPerm(Pi, p)
    for i in range(500):
        sol.pickParents(sol.X)
        sol.makeChildren()
        sol.updateBestForChild()
        sol.selection()
    print("best is ", sol.best_value, sol.best_sequence)


if __name__ == '__main__':
    result_tab = []
    data = getData()
    n = len(data)
    calculate(n, [*range(n)], data)
