import random
from utils import test_permutation


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


def test_permutation_with_node_degree_heuristic(graph, permutation):
    e_in_matching = []
    v_in_matching = []
    degree_sum = 0
    for (v, w) in permutation:
        if v in v_in_matching or w in v_in_matching:
            continue
        e_in_matching.append((v, w))
        v_in_matching.append(w)
        v_in_matching.append(v)
        degree_sum += len(graph[v])
        degree_sum += len(graph[w])
    cardinality = len(e_in_matching)
    heuristic_rating = degree_sum / cardinality
    return cardinality, e_in_matching, heuristic_rating


def simulated_annealing_heuristic_search(graph, iterations=1000):
    best_perm = list(graph.edges)
    best_card, best_sol, best_rating = test_permutation_with_node_degree_heuristic(graph, best_perm)
    for i in range(1, iterations):
        curr_perm = best_perm
        a = random.randint(1, len(best_perm)) - 1
        b = random.randint(1, len(best_perm)) - 1
        curr_perm[a], curr_perm[b] = curr_perm[b], curr_perm[a]
        curr_card, curr_sol, curr_rating = test_permutation_with_node_degree_heuristic(graph, curr_perm)
        if (curr_rating > best_rating) or (1 / i > random.random()):
            best_sol = curr_sol
            best_card = curr_card
            best_perm = curr_perm
    return best_card
