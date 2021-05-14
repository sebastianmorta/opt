# def read(nb):
#     lst = []
#     counter = 0
#     #lst.append(Task(0, 0, 0, 0)) # zerowe zadanie
#     with open('data\\dane' + str(nb) + '.txt') as f:
#         f.readline()  # pominięcie n
#         for i in f:
#             if not i.isspace():  # zapezpieczenie przed linią złożoną z samych białych znaków
#                 p, w, d = i.split()
#                 lst.append(Task(counter, int(p), int(w), int(d)))
#                 counter += 1
#     return lst
#
# def read_wyniki(nb):
#     with open('data\\wyniki' + str(nb) + '.txt') as f:
#         return int(f.readline())
#
# class Task:
#     def __init__(self, nr, p, w, d):
#         self.nr = nr # numer zadania - od 0
#         self.p = p # czas wykonania zadania
#         self.w = w # współczynnik kary za spóźnienie zadania
#         self.d = d # żądany termin zakończenia zadania
#     def __repr__(self):
#         return "{0} {1} {2} {3}".format(self.nr, self.p, self.w, self.d)
#         # return "{0}".format(self.nr)
#     def __str__(self):
#         return "{0} {1} {2} {3}".format(self.nr, self.p, self.w, self.d)
#         # return "{0}".format(self.nr)
#
# # class Permutations:
# #     perm = []
# #
# #     def calculate(self, lst, left, right):
# #         if left == right:
# #             self.perm.append(lst)
# #             return lst
# #         for i in range(left, right + 1):
# #             swapped = lst.copy()
# #             self.swap(swapped, left, i)
# #             self.calculate(swapped, left + 1, right)
# #
# #     def swap(self, lst, j, i):
# #         lst[j], lst[i] = lst[i], lst[j]
#
# def punish(lst):
#     n = len(lst) # ilość zadań
#     temp = 0
#     C = [] # tablica z czasami zakończenia zadań
#     F = [] # tablica z karami za spóźnienia
#     for i in range(n):
#         temp += lst[i].p
#         C.append(temp)
#     for i in range(n):
#         if C[i] > lst[i].d: # jeżeli zadanie jest spóźnione
#             t = C[i] - lst[i].d # policz spóźnienie
#             F.append(t * lst[i].w) # pomnóż razy karę i dodaj je do listy
#     return sum(F)
#
# # ustawia bit na pozycji index, na wartość x(0/1), dla value
# def modify_bit(value, index, x):
#     mask = 1 << index
#     return (value & ~mask) | ((x << index) & mask)
#
# # I - liczba podzbiorów zbioru zadań
# # lst - lista zadań
# # F - tablica spóźnień dla danej permutacji
# def calculate(I, lst, F):
#     permutations_amount = bin(I).replace('0b', '') # liczba podzbiorów binarnie
#     max_val_tab = [] #
#     for j in range(len(permutations_amount)): # dla każdego elementu w permutacji
#         modified = modify_bit(I, j, 0) # ustaw bit dla elementu j na 0
#         modified_binary = bin(modified).replace('0b', '') # zamień reprezentacje zbioru na licznę binarną
#         reversed_string = ''.join(reversed(permutations_amount)) # odwraca aby można było później zwrócić na których pozycjach bit jest ustawiony
#         p = [pos for pos, char in enumerate(reversed_string) if char == '1'] # zwraca pozycje na których bit jest ustawiony
#         if permutations_amount != modified_binary: # sprawdź czy jakiś bit został zmodyfikowany
#             time = 0
#             for m in range(len(p)): # dla każdego zadania w tej permutacji
#                 time += lst[p[m]].p # policz czas wykonywania (moment zakończenia w danej permutacji)
#             current_F = F[modified] # przypisz wartość funkcji celu dla danej permutacji z tablicy
#             if current_F == -1: # jeśli jest równa -1 (nie została jeszcze policzona), to ją policz
#                 current_F = calculate(modified, lst, F) # wylicz rekurencyjnie wartość funkcji celu dla danej permutacji
#             max_val = max(time - lst[j].d, 0) * lst[j].w + current_F # wylicza funkcję celu włączając j zadanie / opt_j
#             max_val_tab.append(max_val)
#     min_val = min(max_val_tab)
#     F[I] = min_val
#     return min_val
#
#
# if __name__ == '__main__':
#     wyniki_tab = []
#     result_tab = []
#     for file in range(1, 10):
#         data = read(file)
#         n = len(data)
#         permutations = 2 ** n
#         F = [0]
#         for i in range(permutations - 1):
#             F.append(-1)
#         result = calculate(permutations - 1, data, F)
#         result_tab.append(result)
#         wyniki_tab.append(read_wyniki(file))
#
#
#     print('Obliczonko: ')
#     print(result_tab)
#     print('Oczekiwane: ')
#     print(wyniki_tab)
from random import randint

from randomgen import witi


def ReadFile():
    p, d, w = witi(10, 5, 123123)
    data = [Task(p[i], d[i], w[i]) for i in range(10)]
    return data


class Task:
    def __init__(self, p, d, w):
        self.p = p
        self.d = d
        self.w = w


# def Ce(j, data, n):
#     # return sum([data[i].p for i in range(n) if j & (1 << i)])
#     C = [data[i].p for i in range(n)]
#     C.insert(0, 0)
#     B = [data[i].p + C[i - 1] for i in range(1, n) if j & (1 << i)]
#     print(C)
#     print(B)
#     return sum(B)


# C += [data[i].p + C[i - 1] for i in range(1, n) if j & (1 << i)]
# return sum(C)
# return sum([data[i].p for i in range(n) if j & (1 << i)])


def SMTWT(n, data):
    OPT_tab = [0]
    perm = 2 ** n
    for j in range(1, perm):
        OPT_tab.append(1000000)
        C = Ce(j, data, n)
        for i in range(n):
            if j & (1 << i):
                OPT = OPT_tab[j & ~(1 << i)] + witi(C, data[i].w, data[i].d)
                if OPT < OPT_tab[j]:
                    OPT_tab[j] = OPT
    return OPT_tab[perm - 1]


def old(n, data):
    OPT_tab = [0]
    perm = 2 ** n
    for j in range(1, perm):
        OPT_tab.append(1000000)
        C = 0
        for i in range(n):
            if j & (1 << i):
                C += data[i].p
        for i in range(n):
            if j & (1 << i):
                OPT = OPT_tab[j & ~(1 << i)] + Wi(C, data[i].w, data[i].d)
                if OPT < OPT_tab[j]:
                    OPT_tab[j] = OPT
    return OPT_tab[perm - 1]


for i in range(10):
    print(5 & (1 << i))


class Genetic():
    def __init__(self, data):
        self.R = []
        self.X = []
        self.C = []
        self.best_value = 99999999
        self.best_sequence = []
        self.data = data
        self.n = len(data)

    def WiTi(self, C, w, d):
        return max(0, C - d) * w

    def cFunc(self, perm):
        pe = [self.data[perm[i]].p for i in range(self.n)]
        return [sum(pe[:i]) for i in range(1, self.n + 1)]

    def crossingOperator(self, r1, r2):
        idx1, idx2 = 2, 6
        return r1[:idx1] + r2[idx1:idx2] + r1[idx2:], r2[:idx1] + r1[idx1:idx2] + r2[idx2:]

    def purposeFunc(self, Pi):
        c = self.cFunc(Pi)
        return sum([self.WiTi(c[i], data[Pi[i].w], data[Pi[i]].d)])


def initialPerm(Pi, p):
    sol = Genetic()
    sol.best_sequence = sol.old_sequence = Pi

    best_value = old_value = 9999999
    for i in range(2, p):
        x = randint(0, len(data) - 1)
        C.append(0)


def alg(p, Pi):
    x = 1


if __name__ == '__main__':
    result_tab = []

    data = ReadFile()
    print(len(data))
    # n = len(data)
    # print(data)
    # result = WiTi(n, data)
    # result_tab.append(result)
    # print(toCe(data, n))
    # print('wynikiWITI: ')
    # print(result_tab)

    # print(crossingOperator([10, 11, 12, 13, 14, 15, 16, 17, 18, 19], [*range(20, 30)]))

# a = ['asd', 'asdf', 'asdft4', 'urihhs']
# b = ['11', '22', '3', '44']
# v = set(a)
# print(v)
#
# print([[x, c] for x, c in zip(a, b)])

# a = [1]
# a += [a[i]+1 for i in range(10)]
# print(a)
