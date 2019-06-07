import networkx as nx
import matplotlib.pyplot as plt
import random
import itertools
import time


def draw_graph(graph):
    nx.draw(graph, with_labels=True, edge_color=[
        ('red' if 'in_matching' in graph.edges[edge] and graph.edges[edge]['in_matching'] else 'black')
        for edge in graph.edges
    ])
    plt.show()


def brute_force(graph):
    edges = list(graph.edges)
    edges.sort()
    permutations = itertools.permutations(edges)
    best_card = 0
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
            # print('added ', v, w)
        cardinality = len(e_in_matching)
        if cardinality > best_card:
            best_card = cardinality
            best_solution = e_in_matching
            print('New best', cardinality)
    for (v, w) in best_solution:
        graph[v][w]['in_matching'] = True
    return best_card


def test(search_f, edges=10, nodes=10, draw=True):
    if nodes <= 1:
        raise Exception('2 or more nodes required')

    print('Creating graph')
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

    print('Starting test')
    start = time.time()

    search_f(graph)

    end = time.time()
    print('Test with {0} nodes and {1} edges took {2:.3f}s'.format(nodes, edges, end - start))

    if draw:
        draw_graph(graph)


test(brute_force, nodes=10, edges=10)
