from utils import *
import math


class GeneticAlgorithm:

    def __init__(self, graph):
        self._edges = list(graph.edges)
        self._chromosome_length = len(self._edges)

        self._iterations = 1000                             # Maksimalni dozvoljeni broj iteracija
        self._generation_size = 5000                        # Broj jedinki u jednoj generaciji
        self._mutation_rate = 0.01                          # Verovatnoca da se desi mutacija
        self._reproduction_size = 1000                      # Broj jedinki koji ucestvuje u reprodukciji
        self._current_iteration = 0                         # Trenutna iteracija

        #najbolji hromozom
        self._best_chromosome = Chromosome([0 for i in range(self._chromosome_length)], math.inf)


    def optimize(self):
        for chrom in self.initial_population():
            print(chrom)
        print("Best is ", self._best_chromosome)
        return


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


if __name__ == "__main__":
    graph = create_graph()
    ga = GeneticAlgorithm(graph)
    solution = ga.optimize()
    print(solution)
