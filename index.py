import networkx as nx
import matplotlib.pyplot as plt
import random


def draw_graph(graph):
    nx.draw(graph, with_labels=True, edge_color=[
        ('red' if 'in_matching' in graph.edges[edge] and graph.edges[edge]['in_matching'] else 'black')
        for edge in graph.edges
    ])
    plt.show()


def dumb_search(graph):
    e_in_matching = []
    v_in_matching = []
    for v in list(graph.nodes):
        if v in v_in_matching:
            continue
        for w in graph[v]:
            if v == w:
                continue
            if w in v_in_matching:
                continue
            if (v, w) not in e_in_matching and (w, v) not in e_in_matching:
                e_in_matching.append((v, w))
                v_in_matching.append(w)
                v_in_matching.append(v)
                graph[v][w]['in_matching'] = True
                print('added ', v, w)
                break
    print('cardinality ', len(e_in_matching))
    return len(e_in_matching)


def test(search_f, edges=10, nodes=10, draw=True):
    graph = nx.Graph()
    for i in range(1, edges):
        graph.add_edge(random.randint(1, nodes), random.randint(1, nodes))
    search_f(graph)
    if draw:
        draw_graph(graph)


while True:
    test(dumb_search)
