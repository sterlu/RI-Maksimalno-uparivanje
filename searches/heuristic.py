import itertools
import math


def node_degree_heuristic_search(graph, iterations=100):
    v_degree = {}
    for v in graph.nodes:
        v_degree[v] = len(graph[v])
    edges_with_weight = []
    for (v, w) in graph.edges:
        edges_with_weight.append((v_degree[v] + v_degree[w], v, w))
    edges_with_weight.sort(key=lambda x: x[0])

    permutations = itertools.permutations(edges_with_weight)
    best_card = math.inf
    best_solution = []
    for i in range(0, iterations):
        permutation = list(permutations.__next__())
        permutation.reverse()
        e_in_matching = []
        v_in_matching = []
        for (weight, v, w) in permutation:
            if v in v_in_matching or w in v_in_matching:
                continue
            e_in_matching.append((v, w))
            v_in_matching.append(w)
            v_in_matching.append(v)
        cardinality = len(e_in_matching)
        if cardinality < best_card:
            best_card = cardinality
            best_solution = e_in_matching
    for (v, w) in best_solution:
        graph[v][w]['in_matching'] = True
    return best_card


def node_degree_heuristic_search_noiter(graph):
    v_degree = {}
    for v in graph.nodes:
        v_degree[v] = len(graph[v])
    edges_with_weight = []
    for (v, w) in graph.edges:
        edges_with_weight.append((v_degree[v] + v_degree[w], v, w))
    edges_with_weight.reverse()
    edges_with_weight.sort(key=lambda x: -x[0])

    e_in_matching = []
    v_in_matching = []
    for (weight, v, w) in edges_with_weight:
        if v in v_in_matching or w in v_in_matching:
            continue
        e_in_matching.append((v, w))
        v_in_matching.append(w)
        v_in_matching.append(v)
        graph[v][w]['in_matching'] = True
    cardinality = len(e_in_matching)
    return cardinality
