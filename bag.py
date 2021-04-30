import matplotlib.pyplot as plt
import heapq
import igraph
from igraph import Graph, EdgeSeq
from randomgen import bag
import plotly.graph_objects as go
import time
import (bheap "https://github.com/Arafatk/DataViz/tree/master/trees/binaryheap")

# nr_vertices = 25
# v_label = list(map(str, range(nr_vertices)))
# print(v_label)
# G = Graph.Tree(nr_vertices, 2)  # 2 stands for children number
# lay = G.layout('rt')
#
# position = {k: lay[k] for k in range(nr_vertices)}
# print(position)
# Y = [lay[k][1] for k in range(nr_vertices)]
# M = max(Y)
#
# es = EdgeSeq(G)  # sequence of edges
# E = [e.tuple for e in G.es]  # list of edges
#
# L = len(position)
# Xn = [position[k][0] for k in range(L)]
# Yn = [2 * M - position[k][1] for k in range(L)]
# Xe = []
# Ye = []
# for edge in E:
#     Xe += [position[edge[0]][0], position[edge[1]][0], None]
#     Ye += [2 * M - position[edge[0]][1], 2 * M - position[edge[1]][1], None]
#
# labels = v_label
# fig = go.Figure()
# fig.add_trace(go.Scatter(x=Xe,
#                          y=Ye,
#                          mode='lines',
#                          line=dict(color='rgb(210,210,210)', width=1),
#                          hoverinfo='none'
#                          ))
# fig.add_trace(go.Scatter(x=Xn,
#                          y=Yn,
#                          mode='markers',
#                          name='bla',
#                          marker=dict(symbol='circle-dot',
#                                      size=18,
#                                      color='#6175c1',  # '#DB4551',
#                                      line=dict(color='rgb(50,50,50)', width=1)
#                                      ),
#                          text=labels,
#                          hoverinfo='text',
#                          opacity=0.8
#                          ))
#
#
# def make_annotations(pos, text, font_size=10, font_color='rgb(250,250,250)'):
#     L = len(pos)
#     if len(text) != L:
#         raise ValueError('The lists pos and text must have the same len')
#     annotations = []
#     for k in range(L):
#         annotations.append(
#             dict(
#                 text=labels[k],  # or replace labels with a different list for the text within the circle
#                 x=pos[k][0], y=2 * M - position[k][1],
#                 xref='x1', yref='y1',
#                 font=dict(color=font_color, size=font_size),
#                 showarrow=False)
#         )
#     return annotations
#
#
# axis = dict(showline=True,  # hide axis line, grid, ticklabels and  title
#             zeroline=True,
#             showgrid=True,
#             showticklabels=True,
#             )
#
# fig.update_layout(title='Tree with Reingold-Tilford Layout',
#                   annotations=make_annotations(position, v_label),
#                   font_size=12,
#                   showlegend=False,
#                   xaxis=axis,
#                   yaxis=axis,
#                   margin=dict(l=40, r=40, b=85, t=100),
#                   hovermode='closest',
#                   plot_bgcolor='rgb(248,248,248)')
# fig.show()


n = 10
profit, weight, capacity = bag(n, 145143)
print("c -", profit, " w -", weight, " B -", capacity)


class Node:
    def __init__(self, value):
        self.value = value
        self.h_score = None

    def generate_children(self, p):
        children = [Node(self.value), Node(self.value + p)]
        return children


class Knapsack():
    def __init__(self, n, value, weight, capacity):
        self.n = n                  # liczba przedmiotów
        self.values = value         # tablica kosztów
        self.weights = weight       # tablica wag przedmiotów
        self.capacity = capacity    # pojemność
        self.heap = []              # kopiec
        self.currentWeight = 0      # current sum of weight
        self.currentValue = 0       # current sum of profits
        self.bestValues = 0         # optimal sum of values
        self.bests = []             # bitstring of optimal set of items
        self.i = 0                  # current node
        self.upper = self.maxbound(self.i)
        self.x = ''

    # Upper bound function: calculating the upper bound of value under the current node
    def maxbound(self, k):
        limit = self.capacity - self.currentWeight  # aktualizacja ograniczenia górnego
        bound = self.currentValue  # best sum of values in current node
        while k < self.n and self.weights[k] <= limit:
            limit -= self.weights[k]
            # print("limit: ", limit, k)
            bound += self.values[k]
            k += 1
        return bound if k >= self.n else bound + (self.values[k] / self.weights[k]) * limit
        # the maximum value that can be attained with weight

    def Beam(self, origin, k=5):
        while True:
            wt = self.currentWeight + self.weights[self.i]
            if wt <= self.capacity:
                self.checkBestProfit()
                self.addItemToHeap()
            self.upper = self.maxbound(self.i + 1)
            self.notAddItemToHeap()
            if len(self.heap) == 0:
                print("%d Status of items (1 is loaded in backpack, 0 is not loaded in backpack):%s" % (
                    self.n, self.bests))
                print("The best price value is: %d" % self.bestValues)
                print(self.bests)
                break
            node = heapq.heappop(self.heap)
            print("after", self.heap)
            self.upper = 1 / node[0]
            self.currentWeight = node[1]
            # print("cw", self.currentWeight)
            self.currentValue = node[2]
            # print("cv", self.currentValue)
            self.i = node[3]
            self.x = node[4]

    def heuristic(self, node, goal=100):
        node.h_score = abs(node.value - goal)  # Evaluate the node
        return node.h_score, node

    def B_B(self):
        while True:
            wt = self.currentWeight + self.weights[self.i]
            if wt <= self.capacity:
                self.checkBestProfit()
                self.addItemToHeap()
            self.upper = self.maxbound(self.i + 1)
            self.notAddItemToHeap()
            if len(self.heap) == 0:
                print("%d Status of items (1 is loaded in backpack, 0 is not loaded in backpack):%s" % (
                    self.n, self.bests))
                print("The best price value is: %d" % self.bestValues)
                print(self.bests)
                break
            node = heapq.heappop(self.heap)
            print("after", self.heap)
            self.upper = 1 / node[0]
            self.currentWeight = node[1]
            # print("cw", self.currentWeight)
            self.currentValue = node[2]
            # print("cv", self.currentValue)
            self.i = node[3]
            self.x = node[4]


    def checkBestProfit(self):
        if self.currentValue + self.values[self.i] > self.bestValues:
            self.bestValues = self.currentValue + self.values[self.i]
            self.bests = self.x + '1'
            self.bests = self.bests + '0' * (self.n - len(self.bests))

    def addItemToHeap(self):
        if self.i + 1 < self.n:
            heapq.heappush(self.heap,
                           [1 / self.upper, self.currentWeight + self.weights[self.i],
                            self.currentValue + self.values[self.i], self.i + 1, self.x + '1'])

    def notAddItemToHeap(self):
        if self.upper >= self.bestValues:
            if self.i + 1 < self.n:
                heapq.heappush(self.heap,
                               [1 / self.upper, self.currentWeight, self.currentValue, self.i + 1, self.x + '0'])


N = [10, 15, 20, 30, 50, 100, 500, 1000, 5000, 10000, 50000]
Seed = [1, 11, 111, 1111, 11111, 111111, 1111111, 11111111, 111111111, 1111111111]
TabtochartN = []
TabtochartS = []
VALN = []
VALS = []
ba = Knapsack(n, profit, weight, capacity)
ba.B_B()
# for n in N:
#     profit, weight, capacity = bag(n, 145143)
#     ba = Knapsack(n, profit, weight, capacity)
#     start = time.time()
#     ba.B_B()
#     end = time.time()
#     TabtochartN.append(end - start)
#
#
# for seed in Seed:
#     profit, weight, capacity = bag(n, seed)
#     ba = Knapsack(n, profit, weight, capacity)
#     start = time.time()
#     ba.B_B()
#     end = time.time()
#     TabtochartS.append(end - start)

# bs = Knapsack(n, profit, weight, capacity)
# bs.Beam(Node(profit[0]))
# print('node:')
# print(node)

# x = N
# y = TabtochartN
# plt.plot(x, y)
# plt.xlabel('n')
# plt.ylabel('time of calc')
# plt.title('czas obliczeń w zależności od n')
# plt.show()
#
# x = Seed
# y = TabtochartS
# plt.plot(x, y)
# plt.xlabel('seed')
# plt.ylabel('time of calc')
# plt.title('czas obliczeń w zależności od seed')
# plt.show()
