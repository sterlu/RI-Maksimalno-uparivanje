from utils import *
import math
import networkx as nx


class GeneticAlgorithm:

    def __init__(self, graph):
        self._graph = graph
        self._edges = list(graph.edges)
        self._chromosome_length = self._num_of_edges = len(self._edges)

        self._iterations = 1000                             # Maksimalni dozvoljeni broj iteracija
        self._generation_size = 5000                        # Broj jedinki u jednoj generaciji
        self._mutation_rate = 0.01                          # Verovatnoca da se desi mutacija
        self._reproduction_size = 1000                      # Broj jedinki koji ucestvuje u reprodukciji
        self._current_iteration = 0                         # Trenutna iteracija

        #najbolji hromozom
        self._best_chromosome = Chromosome([0 for i in range(self._chromosome_length)], math.inf)


    def optimize(self):
        chromosomes = self.initial_population()
        while not self.stop_condition():
            print("Iteration: %d" % self._current_iteration)

            for_reproduction = self.selection(chromosomes)

            i = 0
            for chromo in for_reproduction:
                i+=1
                print(i, " for_repr ", chromo)

            break

        print("Best is ", self._best_chromosome)
        return self._best_chromosome


    def selection(self, chromosomes):
        chromosomes_fitness_sum = sum(1/chromosome.fitness for chromosome in chromosomes)

        selected_chromosomes = [
            self.roulette_selection_pick_one(chromosomes, chromosomes_fitness_sum)
            for i in range(self._reproduction_size)
        ]

        return selected_chromosomes

    def roulette_selection_pick_one(self, chromosomes, chromosomes_fitness_sum):

        pick = random.uniform(0, chromosomes_fitness_sum)
        value = 0
        for chromosome in chromosomes:
            value += 1/chromosome.fitness
            if value > pick:
                return chromosome





    def crossover(self, a, b):
        cross_point = random.randint(0, self._chromosome_length)
        ab = a[:cross_point] + b[cross_point:]
        ba = b[:cross_point] + a[cross_point:]
        return (ab, ba)


    def initial_population(self):
        init_population = []
        for i in range(self._generation_size):
            chromosome_content = random.choices([0, 1], k = self._chromosome_length)
            init_population.append(Chromosome(chromosome_content, self.fitness(chromosome_content)))
        return init_population


    def fitness(self, chromosome_content):
        if self.is_a_maximal_matching(chromosome_content) is False:
            return math.inf
        else:
            this_fitness = sum(chromosome_content)
            if (this_fitness < self._best_chromosome.fitness):
                self._best_chromosome.content = chromosome_content
                self._best_chromosome.fitness = this_fitness
            return this_fitness


    def is_a_maximal_matching(self, chromosome_content):
        included_edges = []
        for i in range(self._chromosome_length):
            if chromosome_content[i] == 1:
                included_edges.append(self._edges[i])

        # ako hromozom nije uparivanje sledi da nije maksimalno uparivanje
        if self.is_a_matching(included_edges) is False:
            return False

        # ako mozemo da dodamo ivicu u uparivanje tako da i dalje bude uparivanje, nije maksimalno uparivanje
        for (v, w) in self._edges:
            if not (v, w) in included_edges:
                included_edges.append((v, w))
                if self.is_a_matching(included_edges):
                    return False
                included_edges.pop()
        return True


    def is_a_matching(self, included_edges):
        for (v, w) in included_edges:
            for (x, y) in included_edges:
                if (x == v and y == w) or (x == w and y == v):
                    continue
                if (x == v and y != w) or (x == w and y != v):
                    return False
        return True


    def stop_condition(self):
        return self._current_iteration > self._iterations


class Chromosome:
    def __init__(self, content, fitness):
        self.content = content
        self.fitness = fitness

    def __str__(self):
        if self.fitness == math.inf:
            return f"{self.content} fitness = inf"
        return f"{self.content} fitness = {self.fitness}"

    def __repr__(self):
        if self.fitness == math.inf:
            return f"{self.content} fitness = inf"
        return f"{self.content} fitness = {self.fitness}"


def genetic_search(graph):
    return GeneticAlgorithm(graph).optimize()


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


if __name__ == "__main__":
    genetic_search(create_graph(30, 40))

