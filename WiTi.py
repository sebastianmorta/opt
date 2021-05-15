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
        if len(self.best) and len(self.medium):
            a = dict[randint(1, 2)]
        elif len(self.best) and not len(self.medium):
            a = dict[1]
        elif not len(self.best) and len(self.medium):
            a = dict[2]
        elif len(self.weak) > 1:
            a = dict[3]
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
        if a == b:
            if len(a) > 1:
                t, a, b = self.rmvItem(a, b)
                self.R.append(t)
            else:
                pass
        else:
            t, a, b = self.rmvItem(a, b)
            self.R.append(t)

    def pickParents(self, perms):
        idx1, idx2 = int(len(perms) / 3), int(len(perms) / 3 * 2)
        perms.sort(key=takeSecond)
        self.best, self.medium, self.weak = perms[:idx1], perms[idx1:idx2], perms[idx2:]
        while (len(self.best) + len(self.medium) + len(self.weak)) > 1:
            self.makeParents()

    def updateBestForChild(self):
        for c in self.C:
            if c[1] < self.best_value:
                print("bm", c)
                self.best_value = c[1]
                self.best_sequence = list.copy(c[0])
            c_perm, c_val,boo = self.mutating(c)
            if boo:
                self.C.append((c_perm, c_val))
                print("am", c)
                if c_val < self.best_value:
                    self.best_value = c_val
                    self.best_sequence = list.copy(c_perm)

    # def swapInsert(self, perm):
    #     x1, x2 = randint(0, len(perm) - 1), randint(0, len(perm) - 1)
    #     print("x1,x2", x1, x2)
    #     print(perm)
    #     perm.insert(x1, data.pop(x2))
    #     print("perminsert",perm)
    #     return perm

    def swap(self, data):
        x1, x2 = randint(0, len(data) - 1), randint(0, len(data) - 1)
        data[x1], data[x2] = data[x2], data[x1]
        return data

    def mutating(self, child):
        if randint(1, 100) < 5:
            c = self.swap(child[0])
            print("patrztu", c)
            c_val = self.purposeFunc(c)
            return c, c_val,True
        else:
            return child[0], child[1],False


def initialPerm(Pi, p, sol):
    old_sequence = list.copy(Pi)
    sol.best_sequence = list.copy(Pi)
    old_value = sol.purposeFunc(old_sequence)
    sol.best_value = old_value
    sol.X.append((old_sequence, old_value))
    for i in range(1, p):
        new_sequence = list.copy(old_sequence)
        shuffle(new_sequence)
        new_value = sol.purposeFunc(new_sequence)
        sol.X.append((new_sequence, new_value))
        if new_value < old_value:
            sol.best_value = new_value
            sol.best_sequence = list.copy(new_sequence)
        old_sequence, old_value = list.copy(new_sequence), new_value


def makeChildren(p, Pi, data):
    sol = Genetic(data)
    initialPerm(Pi, p, sol)
    sol.pickParents(sol.X)
    for i in range(len(sol.R)):
        c1, c2 = sol.crossingOperator(sol.R[i][0][0], sol.R[i][1][0])
        c1_val, c2_val = sol.purposeFunc(c1), sol.purposeFunc(c2)
        sol.C.append((c1, c1_val))
        sol.C.append((c2, c2_val))
    sol.updateBestForChild()


if __name__ == '__main__':
    result_tab = []

    data = ReadFile()
    makeChildren(10, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], data)

    # print(len(data))
    # a = [1, 2, 3, 4, 5, 6, 7, 8]
    # shuffle(a)
    # print(a)
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
    A = [([1, 2, 13, 41, 5, 61, 7], 7), ([1, 2, 13, 41, 51, 6, 71], 6), ([11, 2, 13, 4, 51, 6, 7], 3),
         ([1, 21, 3, 41, 5, 61, 7], 4), ([1, 2, 3, 4, 15, 6, 17], 1), ([1, 12, 3, 41, 5, 6, 7], 2),
         ([1, 12, 3, 41, 5, 6, 7], 9)]

    # g = Genetic(data)
    # g.pickParents(A)
# a = ['asd', 'asdf', 'asdft4', 'urihhs']
# b = ['11', '22', '3', '44']
# v = set(a)
# print(v)
#
# print([[x, c] for x, c in zip(a, b)])

# a = [1]
# a += [a[i]+1 for i in range(10)]
# print(a)
