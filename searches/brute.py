import itertools
import math
from utils import draw_graph, test_permutation


def brute_force_search(graph):
    edges = list(graph.edges)
    edges.sort()
    permutations = itertools.permutations(edges)
    best_card = math.inf
    best_solution = []
    for permutation in permutations:
        # print(permutation)
        curr_card, curr_sol = test_permutation(permutation)
        if curr_card < best_card:
            best_card = curr_card
            best_solution = curr_sol
            for (v, w) in best_solution:
                graph[v][w]['in_matching'] = True
            for (v, w) in best_solution:
                graph[v][w]['in_matching'] = False
    for (v, w) in best_solution:
        graph[v][w]['in_matching'] = True
    return best_card
