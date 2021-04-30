# import heapq
# from graphviz import Graph
#
# g = Graph('G', filename='process.gv', engine='sfdp')
# from randomgen import bag
#
# n = 10
# cost, weight, capacity = bag(n, 145143)
# print("c -", cost, " w -", weight, " B -", capacity)
#
#
# heap = []
# currentWeight = 0
# currentValue = 0
# bestv = 0
# bests = []
# num = 0
#
#
# def maxbound(i):
#     limit = capacity - currentWeight  # aktualizacja maximum podczas iteracji
#     b = currentValue
#     while i < n and weight[i] <= limit:  #
#         limit -= weight[i]
#         b += cost[i]
#         i += 1
#     if i < n:
#         b += (cost[i] / weight[i]) * limit
#     # print("b:", b,'i',i)
#     return b
#
#
# # Branch and bound algorithm for 01 knapsack
# i = 0
# upper = maxbound(i)
# str = ''
# g.edge('run', 'intr')
# while True:
#     wt = currentWeight + weight[i]
#     # print("wt:", wt)
#     if wt <= capacity:
#         # print("-1---------if wt <= capacity:")
#         if currentValue + cost[i] > bestv:
#             # print("-2---------if currentValue + cost[i] > bestv:")
#             # print("i=%d" % i)
#             bestv = currentValue + cost[i]
#             # print("bestv=%d" % bestv)
#
#             # The optimal path to store the current optimal value
#             bests = str + '1'
#             # print(bests, "bests = str + '1'")
#             bests = bests + '0' * (n - len(bests))
#             # print(bests, "bests = bests + '0' * (n - len(bests))")
#         # In the heap: because python has only a small root heap, the upper bound value is large and the priority is high by inverting the upper bound value
#         if i + 1 < n:
#             # print("-3---------if i + 1 < n:")
#             heapq.heappush(heap, [1 / upper, currentWeight + weight[i], currentValue + cost[i], i + 1, str + '1'])
#
#     upper = maxbound(i + 1)
#     print('+++++++++++++++++++++i',i)
#     if upper >= bestv:
#         # print("-4---------if upper >= bestv:")
#         if i + 1 < n:
#             # print("-5---------if i + 1 < n:")
#             heapq.heappush(heap, [1 / upper, currentWeight, currentValue, i + 1, str + '0'])
#
#     if len(heap) == 0:
#         print("%d Status of items (1 is loaded in backpack, 0 is not loaded in backpack):%s" % (n, bests))
#         print("The best price value is: %d" % bestv)
#         print(n, bests)
#
#         break
#
#     # print("heap:", heap)
#     node = heapq.heappop(heap)
#     # print('node=', node)
#     upper = 1 / node[0]
#
#     currentWeight = node[1]
#     currentValue = node[2]
#     i = node[3]
#
#     str = node[4]
#     print("-------------------------------------------------------------")
# # print('node:')
# # print(node)


import heapq
import random

"""
Beam search
* The goal value must be set in the heuristic parameter.
"""


class Node:
    def __init__(self, value):
        self.value = value
        self.h_score = None

    def generate_children(self, ):
        """
        Implement: generating children
        """
        children = []
        for i in range(100900):
            children.append(Node(self.value + random.randint(-5, 5)))
        return children


# end Node


def heuristic(node, goal=100):
    """
    Implement: calculating heuristic
    """
    node.h_score = abs(node.value - goal)  # Evaluate the node
    return node.h_score, node


# end heuristic


def beam_search(origin, max_iterations=1000, max_children=12):
    node_list = [(-1, origin)]
    current_node = Node(None)  # init for while loop

    while current_node.h_score != None:
        a, current_node = heapq.heappop(node_list) # select the best node.
        print(current_node.h_score)
        filter(
            # Add newly generated children to the node list.
            lambda node: heapq.heappush(node_list, node),
            map(heuristic, current_node.generate_children())
        )

        node_list = node_list[:max_children]
    # endwhile

    return current_node


# end beam_search


print(beam_search(Node(1)))
