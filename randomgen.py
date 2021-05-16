import math
import random
import numpy as np


class RandomNumberGenerator:
    def __init__(self, seedVaule=None):
        self.__seed = seedVaule

    def nextInt(self, low, high):
        m = 2147483647
        a = 16807
        b = 127773
        c = 2836
        k = int(self.__seed / b)
        self.__seed = a * (self.__seed % b) - k * c
        if self.__seed < 0:
            self.__seed = self.__seed + m
        value_0_1 = self.__seed
        value_0_1 = value_0_1 / m
        return low + int(math.floor(value_0_1 * (high - low + 1)))

    def nextFloat(self, low, high):
        low *= 100000
        high *= 100000
        val = self.nextInt(low, high) / 100000.0
        return val


def questions(q, v, seed):
    generator = RandomNumberGenerator(seed)
    values = []
    for i in range(0, q):
        values.append([])
        for j in range(0, v):
            values[i].append(generator.nextInt(0, 9))

    print(values)
    return values


def transport(n, m, seed):
    generator = RandomNumberGenerator(seed)
    K = min(n, m)
    S = []
    D = []
    for i in range(1, K + 1):
        S.append(generator.nextInt(1, 20))
        D.append(S[i - 1])
    if n > m:
        for i in range(K + 1, n + 1):
            r = generator.nextInt(1, 20)
            S.append(r)
            j = generator.nextInt(1, m - 1)
            D[j] += r
    if m > n:
        for j in range(K, m):
            r = generator.nextInt(1, 20)
            D.append(r)
            i = generator.nextInt(1, n - 1)
            S[i] += r

    k = []
    for i in range(n):
        k.append([])
        for j in range(m):
            k[i].append(generator.nextInt(1, 30))

    print(S)
    print(D)
    print(k)
    return S, D, k


def machines(n, m, seed):
    gen = RandomNumberGenerator(seed)
    p = []
    a = []
    for i in range(1, n + 1):
        p.append(gen.nextFloat(1, 20))
        a.append(gen.nextInt(1, m))
    S = gen.nextFloat(m, 2 * m)
    print(p)
    print(a)
    print(S)
    return p, a, S


def assignment(n, seed):
    generator = RandomNumberGenerator(seed)
    t = []
    for i in range(0, n):
        t.append([])
        for j in range(0, n):
            t[i].append(generator.nextInt(1, 50))
    return t


def survey(n, seed):
    generator = RandomNumberGenerator(seed)
    a = []
    b = []
    r = []
    for i in range(n):
        a.append(generator.nextFloat(5, 35))
        b.append(generator.nextFloat(5, 35))
        r.append(generator.nextFloat(1, 4))
    x = generator.nextFloat(5, 35)
    y = generator.nextFloat(5, 35)
    return a, b, r, x, y


def QAP(n, seed):
    generator = RandomNumberGenerator(seed)
    w = []
    d = []
    for i in range(n):
        w.append([generator.nextInt(1, 50) for j in range(n)])
        d.append([generator.nextInt(1, 50) for j in range(n)])
    return w, d


def hex_code_colors():
    a = hex(random.randrange(0, 256))
    b = hex(random.randrange(0, 256))
    c = hex(random.randrange(0, 256))
    a = a[2:]
    b = b[2:]
    c = c[2:]
    if len(a) < 2:
        a = "0" + a
    if len(b) < 2:
        b = "0" + b
    if len(c) < 2:
        c = "0" + c
    z = a + b + c
    return "#" + z.upper()


def bag(n, seed):
    generator = RandomNumberGenerator(seed)
    w = []
    c = []
    for i in range(n):
        c.append(generator.nextInt(1, 30))
        w.append(generator.nextInt(1, 30))
    B = generator.nextInt(5 * n, 10 * n)
    return c, w, B


def flow(n, m, seed):
    generator = RandomNumberGenerator(seed)
    # p = [{f"n-{str(j)} m-{str(i)}": generator.nextInt(1, 99) for i in range(m)} for j in range(n)]
    # p = {str(j): [generator.nextInt(1, 99) for i in range(m)] for j in range(n)}
    p = [[j, [generator.nextInt(1, 99) for i in range(m)]] for j in range(n)]
    # p = [[generator.nextInt(1, 99) for i in range(m)] for j in range(n)]
    return np.array(p, dtype='object')


def floww(n, m, seed):
    generator = RandomNumberGenerator(seed)
    # p = [{f"n-{str(j)} m-{str(i)}": generator.nextInt(1, 99) for i in range(m)} for j in range(n)]
    # p = {str(j): [generator.nextInt(1, 99) for i in range(m)] for j in range(n)}
    # p = [[j, [generator.nextInt(1, 99) for i in range(m)]] for j in range(n)]
    p = [[generator.nextInt(1, 99) for i in range(m)] for j in range(n)]
    return np.array(p, dtype='object')


def witi(n, seed):
    generator = RandomNumberGenerator(seed)
    p, d, w = [], [], []
    for i in range(n):
        p.append(generator.nextInt(1, 30))
        w.append(generator.nextInt(1, 30))
    for i in range(n):
        d.append(generator.nextInt(1, sum(p)))
    return p, d, w

# print(witi(10, 5, 123123))


def rosen(n, seed):
    generator = RandomNumberGenerator(seed)
    x = []
    for i in range(n):
        x.append(generator.nextFloat(-100, 100))
    return x

# ([27, 13, 19, 8, 9], [15, 62, 15, 73, 53], [29, 6, 29, 27, 9])


# print(flow(10, 5, 182128))
# print(assignment(4, seed=123123))
# machines(5, 4, 123123)
# ilog_path = r'C:\Users\WorkPlace\opl\projekcik\dane.dat'
#
# f = open(ilog_path, "w")
# n = int(input("enter n: "))
# m = int(input("enter m: "))
# seed = int(input("enter seed: "))
# # n = 5
# # m = 4
# # seed = 124516
#
# S, D, k = transport(n, m, seed)
#
# f.write("supply = " + str(set([*range(1, n + 1)])) + ";\n")
# f.write("demand = " + str(set([*range(1, m + 1)])) + ";\n")
# f.write("delivery= #[")
# f.write("\n")
# for i in range(n):
#     if i is n - 1:
#         f.write("   " + str(i + 1) + " : < " + str(S[i]) + ", " + str(k[i]) + " >\n")
#     else:
#         f.write("   " + str(i + 1) + " : < " + str(S[i]) + ", " + str(k[i]) + " >,\n")
# f.write("]#;\n")
# f.write("orders = " + str(D) + ";")
#
# f.close()
