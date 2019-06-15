import itertools

from utils import *
import math
import networkx as nx
import numpy as np


class GeneticAlgorithm:

    def __init__(self, graph):
        self._graph = graph
        self._edges = list(graph.edges)
        self._chromosome_length = self._num_of_edges = len(self._edges)


        #TODO eksperimentalno odrediti(u odonosu na E?)

        self._iterations = 1000                             # Maksimalni dozvoljeni broj iteracija
        self._generation_size = 500                         # Broj jedinki u jednoj generaciji
        self._mutation_rate = 0.01                          # Verovatnoca da se desi mutacija
        self._reproduction_size = 100                       # Broj jedinki koji ucestvuje u reprodukciji
        self._current_iteration = 0                         # Trenutna iteracija

        #najbolji hromozom
        self._best_chromosome = Chromosome(None, math.inf)


    def optimize(self):
        chromosomes = self.initial_population()
        while not self.stop_condition():

            for_reproduction = self.selection(chromosomes)
            chromosomes = self.create_generation(for_reproduction)
            self._current_iteration += 1
            if self._current_iteration % 10 == 0:
                print("Iteration: %d" % self._current_iteration)
                print("Best chromosome: ", self._best_chromosome, "\n")

        print("Best is ", self._best_chromosome)
        return self._best_chromosome


    def create_generation(self, for_reproduction):
        new_generation = []

        while len(new_generation) < self._generation_size:

            #TODO prebrzo konvergira?
            try:
                parents = random.sample(for_reproduction, 2)
            except ValueError as e:
                print("Ostao je samo jedan hromozom!")
                print("Najbolji: ", self._best_chromosome)
                exit()
            #TODO
            #child1, child2 = self.crossover(parents[0].content, parents[1].content)
            child1, child2 = parents[0], parents[1]

            # Vrsimo mutaciju nakon ukrstanja
            child1 = self.mutation(child1)
            child2 = self.mutation(child2)

            # Dodajemo nove hromozome u novu generaciju
            new_generation.append(child1)
            new_generation.append(child2)

        return new_generation


    def selection(self, chromosomes):
        chromosomes_fitness_sum = sum(1/chromosome.fitness for chromosome in chromosomes)

        selected_chromosomes = []

        pick = random.uniform(0, chromosomes_fitness_sum)
        value = 0
        i = 0
        for chromosome in chromosomes:
            value += 1/chromosome.fitness
            if i >= self._reproduction_size:
                break
            if value >= pick:
                selected_chromosomes.append(chromosome)
                i += 1

        return selected_chromosomes



    def crossover(self, parent1, parent2):
        """order 1 crossover"""
        parent1_content = parent1.content
        parent2_content = parent2.content

        swath_size = random.randint(1, self._chromosome_length)
        swath_pos = random.randint(0, self._chromosome_length - swath_size)

        child1_content = child2_content = list(range(self._chromosome_length))

        for i in range(swath_size):
            child1_content[swath_pos + i] = parent1_content[swath_pos + i]
        i = list(range(swath_pos)) + list(range(swath_pos + swath_size, self._chromosome_length))
        print(i)
        for edge in parent2_content:
            if not edge in child1_content:
                child1_content[i.pop(0)] = edge

        for i in range(swath_size):
            child2_content[swath_pos + i] = parent2_content[swath_pos + i]
        i = list(range(swath_pos)) + list(range(swath_pos + swath_size, self._chromosome_length))
        print(i)
        for edge in parent1_content:
            if not edge in child2_content:
                child1_content[i.pop(0)] = edge


        child1 = Chromosome(child1_content, self.fitness(child1_content))
        child2 = Chromosome(child2_content, self.fitness(child2_content))
        return (child1, child2)


    def mutation(self, chromosome):
        """Vrsi mutaciju nad hromozomom sa verovatnocom self._mutation_rate"""
        t = random.random()
        if t < self._mutation_rate:
            i1 = random.randint(0, self._chromosome_length-1)
            i2 = random.randint(0, self._chromosome_length-1)

            chromosome_content = chromosome.content

            tmp = chromosome_content[i1]
            chromosome_content[i1] = chromosome_content[i2]
            chromosome_content[i2] = tmp

            chromosome.content = chromosome_content
            chromosome.fitness = self.fitness(chromosome_content)

        return chromosome


    def initial_population(self):
        init_population = []
        for i in range(self._generation_size):
            permutation = np.random.permutation(self._edges).tolist()
            init_population.append(Chromosome(permutation, self.fitness(permutation)))
        return init_population


    def fitness(self, permutation):
        cardinality = test_permutation(permutation)[0]
        if cardinality < self._best_chromosome.fitness:
            self._best_chromosome.fitness = cardinality
            self._best_chromosome.content = permutation
        return cardinality


    def stop_condition(self):
        return self._current_iteration > self._iterations


class Chromosome:
    def __init__(self, content, fitness):
        self.content = content
        self.fitness = fitness

    def __str__(self):
        return f"{self.content} \nfitness = {self.fitness}"

    def __repr__(self):
        return f"{self.content} \nfitness = {self.fitness}"


def genetic_search(graph): #TODO
    ga = GeneticAlgorithm(graph)
    ga._generation_size = 2
    chrom1, chrom2 = ga.initial_population()
    print(chrom1, "\n", chrom2)
    chrom1, chrom2 = ga.crossover(chrom1, chrom2)
    print()
    print(chrom1, "\n", chrom2)
    #return GeneticAlgorithm(graph).optimize()


if __name__ == "__main__":
    genetic_search(create_graph(200, 300))

