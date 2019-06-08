import networkx as nx
import matplotlib.pyplot as plt
import random
import itertools
import time
import math


def draw_graph(graph):
    nx.draw(graph, with_labels=True, edge_color=[
        ('red' if 'in_matching' in graph.edges[edge] and graph.edges[edge]['in_matching'] else 'black')
        for edge in graph.edges
    ])
    plt.show()


def create_graph(edges=10, nodes=10):
    if nodes <= 1:
        raise Exception('2 or more nodes required')

    graph = nx.Graph()
    while len(graph.edges) < edges:
        node_a = random.randint(1, nodes)
        node_b = random.randint(1, nodes)
        while node_a == node_b:
            node_b = random.randint(1, nodes)
        if node_a > node_b:
            node_a, node_b = node_b, node_a
        if (node_a, node_b) in graph.edges:
            continue
        graph.add_edge(node_a, node_b)
    return graph


def test(search_fs, edges=10, nodes=10, draw=True):
    print('Creating graph')
    graph = create_graph(edges, nodes)

    for search_f in search_fs:
        print()
        print('Testing', search_f.__name__)
        start = time.time()

        result = search_f(graph)

        end = time.time()
        print('{3} with {0} nodes and {1} edges took {2:.3f}s'.format(nodes, edges, end - start, search_f.__name__))
        print('Final result', result)

        if draw:
            draw_graph(graph)

        for (v, w) in graph.edges:
            graph[v][w]['in_matching'] = False


def compare(search_f_1, search_f_2, edges=10, nodes=10, iterations=100):
    print('Comparing {0} and {1}'.format(search_f_1.__name__, search_f_2.__name__))
    results = {
        search_f_1.__name__: 0,
        search_f_2.__name__: 0,
        'equal': 0
    }
    for i in range(0, iterations):
        graph = create_graph(edges, nodes)
        res_1 = search_f_1(graph)
        res_2 = search_f_2(graph)

        if res_1 < res_2:
            results[search_f_1.__name__] += 1
        elif res_2 < res_1:
            results[search_f_2.__name__] += 1
        else:
            results['equal'] += 1
    print(results)


def brute_force_search(graph):
    edges = list(graph.edges)
    edges.sort()
    permutations = itertools.permutations(edges)
    best_card = math.inf
    best_solution = []
    for permutation in permutations:
        # print(permutation)
        e_in_matching = []
        v_in_matching = []
        for (v, w) in permutation:
            if v in v_in_matching or w in v_in_matching:
                continue
            e_in_matching.append((v, w))
            v_in_matching.append(w)
            v_in_matching.append(v)
        cardinality = len(e_in_matching)
        if cardinality < best_card:
            best_card = cardinality
            best_solution = e_in_matching
            # print('New best', cardinality)
    for (v, w) in best_solution:
        graph[v][w]['in_matching'] = True
    return best_card


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


def random_search(graph):
    e_in_matching = []
    v_in_matching = []
    for (v, w) in graph.edges:
        if v in v_in_matching or w in v_in_matching:
            continue
        e_in_matching.append((v, w))
        v_in_matching.append(w)
        v_in_matching.append(v)
        graph[v][w]['in_matching'] = True
    cardinality = len(e_in_matching)
    return cardinality


# test([brute_force_search], nodes=15, edges=15)
# test([node_degree_heuristic_search], nodes=10, edges=10)
# test([brute_force_search, node_degree_heuristic_search], nodes=10, edges=10, draw=False)
# compare(random_search, node_degree_heuristic_search, edges=200, nodes=50, iterations=1000)
# compare(random_search, node_degree_heuristic_search_noiter, edges=200, nodes=50, iterations=1000)
# compare(node_degree_heuristic_search, node_degree_heuristic_search_noiter, edges=15, nodes=10, iterations=1000)
# compare(brute_force_search, node_degree_heuristic_search, edges=10, nodes=10, iterations=20)
