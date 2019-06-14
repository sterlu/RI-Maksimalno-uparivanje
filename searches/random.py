from utils import test_permutation


def random_search(graph):
    cardinality, solution = test_permutation(list(graph.edges))
    return cardinality
