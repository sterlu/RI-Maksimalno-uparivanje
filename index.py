import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(graph):
    nx.draw(graph, with_labels=True, edge_color=[
        ('red' if 'in_matching' in graph.edges[edge] and graph.edges[edge]['in_matching'] else 'black')
        for edge in graph.edges
    ])
    plt.show()


G = nx.Graph()

# G.add_node(1)
G.add_edge(1, 2)
G.add_edge(3, 2)
G[1][2]['in_matching'] = True
G[2][3]['in_matching'] = False

draw_graph(G)
