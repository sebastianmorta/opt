from randomgen import witi


def getData(n):
    p, d, w = witi(n, 123123)
    __data__ = [Task(p[i], d[i], w[i]) for i in range(n)]
    print(__data__)
    return __data__


class Task:
    def __init__(self, p, d, w):
        self.p = p
        self.d = d
        self.w = w


def Wi(c, w, d):
    return max(0, c - d) * w


def WiTi(n, data):
    OPT_tab = [0]
    perm = 2 ** n
    for j in range(1, perm):
        OPT_tab.append(1000000)
        C = 0
        for i in range(n):
            if j & (1 << i):
                C += data[i].p
        for i in range(n):
            print(perm, "========", j, "-------", i)
            if j & (1 << i):
                OPT = OPT_tab[j & ~(1 << i)] + Wi(C, data[i].w, data[i].d)
                if OPT < OPT_tab[j]:
                    OPT_tab[j] = OPT
    return OPT_tab[perm - 1]


if __name__ == '__main__':
    n = 20
    data = getData(n)
    result = WiTi(n, data)
    print('wynikiWITI: ')
    print(result)
