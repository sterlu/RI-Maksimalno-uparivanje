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


def detailed_compare(search_fs, edges=10, nodes=10, iterations=100):
    results = {}
    for search_f in search_fs:
        results[search_f.__name__] = []
    for i in range(0, iterations):
        graph = create_graph(edges, nodes)
        for search_f in search_fs:
            res = search_f(graph)
            results[search_f.__name__].append(res)
        #     print(search_f.__name__, res)
        # print()

    fig, ax = plt.subplots()
    for search_f in search_fs:
        line, = ax.plot(
            range(1, iterations + 1),
            results[search_f.__name__]
        )
        line.set_label(search_f.__name__)
    ax.set_ylim(bottom=0)
    ax.legend()
    plt.title('{0} nodes/{1} edges'.format(nodes, edges))
    fig.show()



def test_permutation(permutation):
    e_in_matching = []
    v_in_matching = []
    for (v, w) in permutation:
        if v in v_in_matching or w in v_in_matching:
            continue
        e_in_matching.append((v, w))
        v_in_matching.append(w)
        v_in_matching.append(v)
    cardinality = len(e_in_matching)
    return cardinality, e_in_matching


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
            print('New best', curr_card)
    for (v, w) in best_solution:
        graph[v][w]['in_matching'] = True
    return best_card


def node_degree_heuristic_search(graph, iterations=1000):
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


def random_search(graph):
    cardinality, solution = test_permutation(list(graph.edges))
    return cardinality


def simulated_annealing_search(graph, iterations=1000):
    best_perm = list(graph.edges)
    best_card, best_sol = test_permutation(best_perm)
    for i in range(1, iterations):
        curr_perm = best_perm
        a = random.randint(1, len(best_perm)) - 1
        b = random.randint(1, len(best_perm)) - 1
        curr_perm[a], curr_perm[b] = curr_perm[b], curr_perm[a]
        curr_card, curr_sol = test_permutation(curr_perm)
        if (curr_card < best_card) or (1 / i > random.random()):
            best_sol = curr_sol
            best_card = curr_card
            best_perm = curr_perm
    return best_card


def simulated_annealing_heuristic_search(graph, iterations=1000):
    v_degree = {}
    for v in graph.nodes:
        v_degree[v] = len(graph[v])
    edges_with_weight = []
    for (v, w) in graph.edges:
        edges_with_weight.append((v_degree[v] + v_degree[w], v, w))
    edges_with_weight.reverse()
    edges_with_weight.sort(key=lambda x: -x[0])

    best_perm = list(map(lambda edge: (edge[1], edge[2]), edges_with_weight))
    best_card, best_solution = test_permutation(best_perm)
    for i in range(1, iterations):
        curr_perm = best_perm
        a = random.randint(1, len(best_perm)) - 1
        b = random.randint(1, len(best_perm)) - 1
        curr_perm[a], curr_perm[b] = curr_perm[b], curr_perm[a]
        curr_card, curr_sol = test_permutation(curr_perm)
        if (curr_card < best_card) or (1 / i > random.random()):
            best_sol = curr_sol
            best_card = curr_card
            best_perm = curr_perm
    return best_card


# test([brute_force_search], nodes=10, edges=12, draw=False)
# test([node_degree_heuristic_search], nodes=10, edges=10, draw=False)
# test([brute_force_search, node_degree_heuristic_search], nodes=10, edges=10, draw=False)
# test([simulated_annealing_search], nodes=10, edges=12, draw=False)
# test([simulated_annealing_heuristic_search], nodes=10, edges=12, draw=False)
# compare(random_search, node_degree_heuristic_search, edges=200, nodes=50, iterations=1000)
# compare(random_search, node_degree_heuristic_search_noiter, edges=200, nodes=50, iterations=1000)
# compare(brute_force_search, node_degree_heuristic_search, edges=10, nodes=10, iterations=20)
# compare(node_degree_heuristic_search, node_degree_heuristic_search_noiter, edges=100, nodes=70, iterations=1000)
# compare(node_degree_heuristic_search, simulated_annealing_search, edges=100, nodes=70, iterations=1000)
# compare(node_degree_heuristic_search_noiter, simulated_annealing_search, edges=100, nodes=70, iterations=1000)
# compare(simulated_annealing_heuristic_search, simulated_annealing_search, edges=100, nodes=70, iterations=1000)
# compare(simulated_annealing_heuristic_search, node_degree_heuristic_search_noiter, edges=100, nodes=70, iterations=1000)
# compare(simulated_annealing_heuristic_search, node_degree_heuristic_search, edges=100, nodes=70, iterations=100)
# compare(simulated_annealing_search, simulated_annealing_heuristic_search, edges=100, nodes=70, iterations=100)
detailed_compare([
    random_search,
    simulated_annealing_search,
    node_degree_heuristic_search,
    simulated_annealing_heuristic_search,
], edges=200, nodes=40, iterations=10)