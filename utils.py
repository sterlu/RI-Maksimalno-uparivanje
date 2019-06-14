import networkx as nx
import matplotlib.pyplot as plt
import random


def draw_graph(graph):
    plt.figure(figsize=(8, 8))
    nx.draw(graph, with_labels=False, node_size=40, edge_color=[
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
