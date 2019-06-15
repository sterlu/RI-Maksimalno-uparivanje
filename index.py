from testing import test, compare, detailed_compare, compare_iterations
from utils import create_graph, draw_graph
from searches.brute import brute_force_search
from searches.random import random_search
from searches.heuristic import node_degree_heuristic_search, node_degree_heuristic_search_noiter
from searches.annealing import simulated_annealing_search, simulated_annealing_heuristic_search
from searches.genetic import genetic_search

# test([brute_force_search], nodes=10, edges=10, draw=False)
# test([node_degree_heuristic_search], nodes=10, edges=10, draw=False)
# test([brute_force_search, node_degree_heuristic_search], nodes=10, edges=10, draw=False)
# test([simulated_annealing_search], nodes=10, edges=12, draw=False)
# test([simulated_annealing_heuristic_search], nodes=10, edges=12, draw=False)
# compare(random_search, node_degree_heuristic_search, edges=200, nodes=50, iterations=1000)
# compare(random_search, node_degree_heuristic_search_noiter, edges=200, nodes=50, iterations=1000)
# compare(brute_force_search, node_degree_heuristic_search, edges=10, nodes=10, iterations=20)
# compare(node_degree_heuristic_search, node_degree_heuristic_search_noiter, edges=100, nodes=70, iterations=1000)
# detailed_compare([node_degree_heuristic_search, node_degree_heuristic_search_noiter], edges=100, nodes=70, iterations=1000)
# compare(simulated_annealing_search, simulated_annealing_search_slow, edges=100, nodes=70, iterations=1000)
# detailed_compare([simulated_annealing_search, simulated_annealing_search_slow], edges=100, nodes=70, iterations=1000)
# compare(node_degree_heuristic_search, simulated_annealing_search, edges=100, nodes=70, iterations=1000)
# compare(node_degree_heuristic_search_noiter, simulated_annealing_search, edges=100, nodes=70, iterations=1000)
# compare(simulated_annealing_heuristic_search, simulated_annealing_search, edges=100, nodes=70, iterations=1000)
# compare(simulated_annealing_heuristic_search, node_degree_heuristic_search_noiter, edges=100, nodes=70, iterations=1000)
# compare(simulated_annealing_heuristic_search, node_degree_heuristic_search, edges=100, nodes=70, iterations=100)
# compare(simulated_annealing_search, simulated_annealing_heuristic_search, edges=100, nodes=70, iterations=200)
# compare(simulated_annealing_search, simulated_annealing_heuristic_search, edges=100, nodes=20, iterations=200)

# draw_graph(create_graph(200, 150))
# genetic_search(create_graph(300, 150))
detailed_compare([
    random_search,
    node_degree_heuristic_search,
    simulated_annealing_search,
    simulated_annealing_heuristic_search,
    # genetic_search,
    # brute_force_search,
], edges=50, nodes=30, iterations=200)
# detailed_compare([
#     random_search,
#     node_degree_heuristic_search,
#     simulated_annealing_search,
#     simulated_annealing_heuristic_search,
#     # genetic_search,
#     # brute_force_search,
# ], edges=300, nodes=150, iterations=200)
# detailed_compare([
#     random_search,
#     node_degree_heuristic_search,
#     simulated_annealing_search,
#     simulated_annealing_heuristic_search,
#     # genetic_search,
#     # brute_force_search,
# ], edges=600, nodes=150, iterations=200)
# detailed_compare([
#     random_search,
#     node_degree_heuristic_search,
#     simulated_annealing_search,
#     simulated_annealing_heuristic_search,
#     # genetic_search,
#     # brute_force_search,
# ], edges=50, nodes=50, iterations=200)
# detailed_compare([
#     random_search,
#     node_degree_heuristic_search,
#     simulated_annealing_search,
#     simulated_annealing_heuristic_search,
#     # genetic_search,
#     # brute_force_search,
# ], edges=200, nodes=50, iterations=200)
# detailed_compare([
#     random_search,
#     node_degree_heuristic_search,
#     simulated_annealing_search,
#     simulated_annealing_heuristic_search,
#     # genetic_search,
#     # brute_force_search,
# ], edges=400, nodes=50, iterations=200)
# detailed_compare([
#     random_search,
#     node_degree_heuristic_search,
#     simulated_annealing_search,
#     simulated_annealing_heuristic_search,
#     # genetic_search,
#     # brute_force_search,
# ], edges=300, nodes=300, iterations=200)
# detailed_compare([
#     random_search,
#     node_degree_heuristic_search,
#     simulated_annealing_search,
#     simulated_annealing_heuristic_search,
#     # genetic_search,
#     # brute_force_search,
# ], edges=900, nodes=300, iterations=200)
# detailed_compare([
#     random_search,
#     node_degree_heuristic_search,
#     simulated_annealing_search,
#     simulated_annealing_heuristic_search,
#     # genetic_search,
#     # brute_force_search,
# ], edges=2700, nodes=300, iterations=200)

# detailed_compare([
#     node_degree_heuristic_search,
#     node_degree_heuristic_search_noiter,
# ], edges=200, nodes=50, iterations=50)

# compare_iterations(simulated_annealing_search, edges=200, nodes=50, iterations=500)
# compare_iterations(simulated_annealing_heuristic_search, edges=200, nodes=50, iterations=500)
# compare_iterations(node_degree_heuristic_search, edges=100, nodes=70, iterations=200)
