'''
Genetic algorithm implementation to find shortest path.
Under development.
@author Fernando Felix do Nascimento Junior


http://geneticalgorithms.ai-depot.com/Tutorial/Overview.html
http://stackoverflow.com/questions/1575061/ga-written-in-java
http://stackoverflow.com/questions/177271/roulette%20-selection-in-genetic-algorithms/177278#177278
http://stackoverflow.com/questions/12687963/genetic-algorithms-crossover-and-mutation-operators-for-paths
'''
import random
import json


def read_graph(path):
    """
    Open a json file that contains the edge costs
    """
    with open(path) as f:  # open match
        return json.load(f)  # read match


class Graph:
    def __init__(self, graph):
        self.graph = graph

    def cost(self, from_node, to_node):
        return self.graph[from_node][to_node]

    def vertex(self, position):
        return self.vertices()[position]

    def vertices(self):
        return list(self.graph.keys())


class Individual:

    def __init__(self, genes, graph):
        self.genes = genes
        self.graph = graph

    def __eq__(self, other):
        return self.fitness() == other.fitness()

    def __lt__(self, other):
        return self.fitness() < other.fitness()

    def __repr__(self):
        return str(self.genes)

    def fitness(self):
        fitness = 0
        chromosome_size = len(self.genes)
        for j in range(chromosome_size):
            if j < chromosome_size - 1:
                from_gene = self.genes[j]
                to_gene = self.genes[j + 1]
                cost = self.graph.cost(from_gene, to_gene)
                fitness += cost
        return fitness


def difference(list1, list2):
    '''
    Return a list based on difference between list1 and list2 (list1 - list2)
    '''
    difference = []
    for x in list1:
        if x not in list2:
            difference.append(x)
    return difference


def intersection(list1, list2):
    return list(set(list1).intersection(set(list2)))


def replace(a, b, l):
    '''
    In a list l, find all elements equals to a and replace with b
    '''
    for n, i in enumerate(l):
        if i == a:
            l[n] = b


def switch(a, b, l):
    '''
    Switch two elements of a list.
    @param a Index of an element
    @param b Index of another element
    @param l A list
    '''
    l[b], l[a] = l[a], l[b]


class Population:
    def __init__(self, graph, **kargs):
        self.graph = graph
        self.population_size = kargs['population_size'] if 'population_size' in kargs else 1000
        self.crossover_rate = kargs['crossover_rate'] if 'crossover_rate' in kargs else 0.7
        self.elitism_rate = kargs['elitism_rate'] if 'elitism_rate' in kargs else 0.1
        self.mutation_rate = kargs['mutation_rate'] if 'mutation_rate' in kargs else 0.05
        self.population = self.random_population(self.population_size)

    def __repr__(self):
        return str(self.population)

    def crossover(self, individual1, individual2):
        '''
        Crossover is based on indexes of common values between individuals
        '''

        # genes1 = [4, 9, 2, 0, 6, 3, 1, 8, 7, 5]
        genes1 = list(individual1.genes)
        # genes2 = [3, 2, 8, 7, 5, 6, 0, 1, 9, 4]
        genes2 = list(individual2.genes)

        # cut_point = 4
        cut_point = random.randint(0, self.chromosome_size() - 1)

        # common values in first slices [2]
        common_values1 = intersection(genes1[:cut_point], genes2[:cut_point])

        # crossover first slice, [4, 2, 9, 0, 6, 3, 1, 8, 7, 5]
        for value in common_values1:
            from_index = genes1.index(value)
            to_index = genes2.index(value)
            switch(from_index, to_index, genes1)

        # common values in second slice, [1, 5, 6]
        common_values2 = intersection(genes1[cut_point:], genes2[cut_point:])

        # 1: [3, 2, 8, 7, 5, 6, 1, 0, 9, 4]
        # 5: [3, 2, 8, 7, 4, 6, 1, 0, 9, 5]
        # 6: [3, 2, 8, 7, 6, 4, 1, 0, 9, 5]
        for value in common_values2:
            from_index = genes2.index(value)
            to_index = genes1.index(value)
            switch(from_index, to_index, genes2)

        return Individual(genes1, self.graph), Individual(genes2, self.graph)

    def chromosome_size(self):
        return len(self.graph.vertices())

    def fitness(self):
        '''
        Sum of all individual fitness
        '''
        fitness = 0
        for individual in self.population:
            fitness += individual.fitness()
        return fitness

    def random_population(self, population_size):
        '''
        Generates a random population with a predefined size
        '''
        population = []
        genes_population = []

        while len(population) < population_size:
            genes = self.random_genes()
            if(genes not in genes_population):  # preventing twins
                individual = Individual(genes, self.graph)
                population.append(individual)

        return population

    def random_genes(self):
        '''
        Generate random genes for an individual.
        '''
        genes = []
        vertices = self.graph.vertices()
        missing_genes = list(vertices)  # copy
        for i in range(len(vertices)):
            gene = random.choice(missing_genes)  # choosing a distinct gene
            genes.append(gene)
            missing_genes.remove(gene)  # removing already choosed gene
        return genes

    def random_gene(self, vertices):
        return random.choice(vertices)

    def roulette_wheel_selection(self):
        '''
        Select an individual based on roulette wheel selection strategy
        '''
        cumulative_fitness = 0.0
        total_fraction = self.fitness() * random.random()  # random [0.0, 1.0]
        for individual in self.population:
            cumulative_fitness += individual.fitness()
            if cumulative_fitness >= total_fraction:
                return individual

    def best_individual(self, population=None):
        '''
        Returns best individual of the population (with minimal fitness).
        '''
        population = population or self.population
        return min(population)

    def solve(self):

        population = list(self.population)  # copy

        new_population = []

        elitism_len = int(self.population_size * self.elitism_rate)

        while len(new_population) < elitism_len:
            best_individual = self.best_individual(population)
            new_population.append(best_individual)
            population.remove(best_individual)  # remove already computed

        return new_population


# distances of edges
graph = read_graph('data/brazil58.json')
graph = Graph(graph)
population = Population(graph)
print(population.population[0].fitness())

# TODO: linkar individuals e population
# TODO: crossover deve ser feito no escopo do individuo
