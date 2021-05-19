from random import randint, shuffle
import random
from randomgen import witi


def getData(n):
    p, d, w = witi(n, 123123)
    __data__ = [Task(p[i], d[i], w[i]) for i in range(n)]
    return __data__


class Task:
    def __init__(self, p, d, w):
        self.p = p
        self.d = d
        self.w = w


class Solution:
    def __init__(self, permutation, purpose):
        self.perm = permutation
        self.purpose = purpose

    def __eq__(self, other):
        return True if other.perm == self.perm and other.purpose == self.purpose else False


def takeSecond(elem):
    return elem.purpose


class Genetic:
    def __init__(self, __data__):
        self.R = []
        self.X = []
        self.C = []
        self.best_value = 99999999
        self.best_sequence = []
        self.data = __data__
        self.n = len(__data__)
        self.best = []
        self.medium = []
        self.weak = []

    @staticmethod
    def WiTi(C, w, d):
        return max(0, C - d) * w

    def cFunc(self, perm):
        return [sum(self.pTab(perm)[:i]) for i in range(1, self.n + 1)]

    def pTab(self, perm):
        return [self.data[perm[i]].p for i in range(self.n)]

    def crossingOperator(self, r1, r2):
        tmp1, tmp2 = randint(0, self.n), randint(0, self.n)
        idx1, idx2 = min(tmp1, tmp2), max(tmp1, tmp2)
        return r1[:idx1] + r2[idx1:idx2] + r1[idx2:], r2[:idx1] + r1[idx1:idx2] + r2[idx2:]

    def orderedCrossover(self, r1, r2):
        c1, c2 = [-1] * self.n, [-1] * self.n
        start, end = sorted([random.randrange(self.n) for _ in range(2)])

        c1_inherited, c2_inherited = [], []
        for i in range(start, end + 1):
            c1[i], c2[i] = r1[i], r2[i]
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

    @staticmethod
    def test(r, c, c_inherited, current_r_position, i):
        test_c = c[i]
        if test_c == -1:
            r_trait = r[current_r_position]
            while r_trait in c_inherited:
                current_r_position += 1
                r_trait = r[current_r_position]
            c[i] = r_trait
            c_inherited.append(r_trait)

    def purposeFunc(self, perm):
        return sum(
            [self.WiTi(self.cFunc(perm)[i], self.data[perm[i]].w, self.data[perm[i]].d) for i in range(len(perm))])

    def coupleParents(self, r1, r2):
        rm1 = random.choice(r1)
        r1.remove(rm1)
        rm2 = random.choice(r2)
        r2.remove(rm2)
        self.R.append((rm1, rm2))
        return r1, r2

    def makeParents(self):
        quality_of_perm = {1: self.best, 2: self.medium, 3: self.weak}
        while True:
            if (len(self.best) + len(self.medium) + len(self.weak)) > 1:
                r1 = quality_of_perm[randint(1, 2)]
                r2 = quality_of_perm[randint(1, 3)]
                if len(r1) and len(r2):
                    break
                else:
                    r1 = quality_of_perm[randint(1, 3)]
                    r2 = quality_of_perm[randint(1, 3)]
                    if len(r1) and len(r2):
                        break
            else:
                return 0
        if r1 == r2:
            if len(r1) > 1:
                self.coupleParents(r1, r2)
        else:
            self.coupleParents(r1, r2)
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
            if c.purpose < self.best_value:
                self.best_value = c.purpose
                self.best_sequence = list.copy(c.perm)
            c_perm, c_val, has_mutated = self.mutating(c)
            if has_mutated:
                self.C.append(Solution(c_perm, c_val))
                if c_val < self.best_value:
                    self.best_value = c_val
                    self.best_sequence = list.copy(c_perm)

    def swap(self, perm):
        x1, x2 = randint(0, self.n - 1), randint(0, self.n - 1)
        perm[x1], perm[x2] = perm[x2], perm[x1]
        return perm

    def mutating(self, child):
        if randint(1, 100) < 5:
            c = self.swap(child.perm)
            c_val = self.purposeFunc(c)
            return c, c_val, True
        else:
            return child.perm, child.purpose, False

    def removeDuplicates(self):
        new_X = self.X + self.C
        new_X.sort(key=takeSecond)
        res = []
        for i in new_X:
            if i not in res:
                res.append(i)
        return res

    def selection(self):
        temp = self.removeDuplicates()
        self.X.clear()
        self.C.clear()
        self.R.clear()
        self.X = temp[:int(self.n * 0.2)] + random.sample(temp[int(self.n * 0.2):], int(self.n * 0.81))

    def initSet(self, init_perm, p):
        old_sequence = list.copy(init_perm)
        self.best_sequence = list.copy(init_perm)
        old_value = self.purposeFunc(old_sequence)
        self.best_value = old_value
        self.X.append(Solution(old_sequence, old_value))
        for i in range(1, p):
            new_sequence = list.copy(old_sequence)
            shuffle(new_sequence)
            new_value = self.purposeFunc(new_sequence)
            self.X.append(Solution(new_sequence, new_value))
            if new_value < old_value:
                self.best_value = new_value
                self.best_sequence = list.copy(new_sequence)
            old_sequence, old_value = list.copy(new_sequence), new_value

    def makeChildren(self):
        for i in range(len(self.R)):
            c1, c2 = self.orderedCrossover(self.R[i][0].perm, self.R[i][1].perm)
            c1_val, c2_val = self.purposeFunc(c1), self.purposeFunc(c2)
            self.C.append(Solution(c1, c1_val))
            self.C.append(Solution(c2, c2_val))


def calculate(p, Pi, __data__):
    solution = Genetic(__data__)
    solution.initSet(Pi, p)
    for i in range(1000):
        print(solution.best_value)
        solution.pickParents(solution.X)
        solution.makeChildren()
        solution.updateBestForChild()
        solution.selection()
    print("best is ", solution.best_value, solution.best_sequence)


if __name__ == '__main__':
    n = 10
    calculate(n, [*range(n)], getData(n))
