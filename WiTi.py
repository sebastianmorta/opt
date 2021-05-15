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
from random import randint, shuffle
import random
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


# for i in range(10):
#     print(5 & (1 << i))


def takeSecond(elem):
    return elem[1]


class Genetic():
    def __init__(self, data):
        self.R = []
        self.X = []
        self.C = []
        self.best_value = 99999999
        self.best_sequence = []
        self.data = data
        self.n = len(data)
        self.best=[]
        self.medium=[]
        self.weak=[]


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

    def rmvItem(self, list1, list2):
        rm1, rm2 = random.choice(list1), random.choice(list2)
        list1.remove(rm1)
        list2.remove(rm2)
        return (rm1, rm2), list1, list2

    def tmp(self):
        dict = {1: self.best, 2: self.medium, 3: self.weak}
        if len(self.best) and len(self.medium):
            a = dict[randint(1, 2)]
        elif len(self.best) and not len(self.medium):
            a = dict[1]
        elif not len(self.best) and  len(self.medium):
            a = dict[2]
        elif len(self.weak)>1:
            a=dict[3]
        else:
            return "xd"
        if len(self.best) and len(self.medium) and len(self.weak):
            b = dict[randint(1, 3)]
        elif len(self.best) and len(self.medium):
            b = dict[randint(1, 2)]
        elif len(self.weak) and len(self.best):
            b = dict[random.randrange(1, 4, 2)]
        elif len(self.weak) and len(self.best):
            b = dict[randint(2, 3)]
        elif len(self.weak):
            b = dict[3]
        else:
            return "xd"

        self.R, a, b = self.rmvItem(a, b)

    def pickParents(self, perms):
        idx1, idx2 = int(len(perms) / 3), int(len(perms) / 3 * 2)
        perms.sort(key=takeSecond)
        self.best, self.medium, self.weak = perms[:idx1], perms[idx1:idx2], perms[idx2:]
        print("best",self.best)
        print("med", self.medium)
        print("weak",self.weak)
        print(idx1, idx2, len(perms))
        # a, best, weak = self.rmvItem(best, weak)
        print("------------------------")

        # a=(random.choice(best),random.choice(weak))
        while (len(self.best) +len(self.medium) + len(self.weak))>1:
            self.tmp()
            # self.R, a, b = self.rmvItem(a, b)
        print("best", self.best)
        print("med",  self.medium)
        print("weak", self.weak)
        print(idx1, idx2, len(perms))
        print('a', a)
        print(self.R)


print(random.randrange(1, 3, 2))


def initialPerm(Pi, p, data):
    sol = Genetic(data)
    sol.best_sequence = old_sequence = Pi
    sol.best_value = old_value = sol.purposeFunc(old_sequence)
    sol.X.append([old_sequence, old_value])
    for i in range(1, p):
        new_sequence = old_sequence
        shuffle(new_sequence)
        new_value = sol.purposeFunc(new_sequence)
        if new_value < old_value:
            sol.best_value = new_value
        old_sequence, old_value = new_sequence, new_value
        sol.X.append([new_sequence, new_value])


def alg(p, Pi):
    x = 1


if __name__ == '__main__':
    result_tab = []

    data = ReadFile()
    print(len(data))
    a = [1, 2, 3, 4, 5, 6, 7, 8]
    shuffle(a)
    print(a)
    # n = len(data)
    # print(data)
    # result = WiTi(n, data)
    # result_tab.append(result)
    # print(toCe(data, n))
    # print('wynikiWITI: ')
    # print(result_tab)
    # number_list = [7, 14, 21, 28, 35, 42, 49, 56, 63, 70]
    # print("Original list : ", number_list)
    #
    # random.shuffle(number_list)  # shuffle method
    # print("List after shuffle  : ", number_list)
    # print(crossingOperator([10, 11, 12, 13, 14, 15, 16, 17, 18, 19], [*range(20, 30)]))
    A = [[[1, 2, 13, 41, 5, 61, 7], 7], [[1, 2, 13, 41, 51, 6, 71], 6], [[11, 2, 13, 4, 51, 6, 7], 3],
         [[1, 21, 3, 41, 5, 61, 7], 4], [[1, 2, 3, 4, 15, 6, 17], 1], [[1, 12, 3, 41, 5, 6, 7], 2],
         [[1, 12, 3, 41, 5, 6, 7], 9], ]

    g = Genetic(data)
    g.pickParents(A)
# a = ['asd', 'asdf', 'asdft4', 'urihhs']
# b = ['11', '22', '3', '44']
# v = set(a)
# print(v)
#
# print([[x, c] for x, c in zip(a, b)])

# a = [1]
# a += [a[i]+1 for i in range(10)]
# print(a)
