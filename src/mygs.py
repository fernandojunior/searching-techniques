'''
Genetic algorithm implementation to find shortest path.

@author Fernando Felix do Nascimento Junior

@links
    http://geneticalgorithms.ai-depot.com/Tutorial/Overview.html
    http://stackoverflow.com/questions/1575061/ga-written-in-java
    http://stackoverflow.com/questions/177271/roulette%20-selection-in-genetic-algorithms/177278#177278
    http://stackoverflow.com/questions/12687963/genetic-algorithms-crossover-and-mutation-operators-for-paths
'''
import random
import json


def read_graph(path):
    '''
    Open a json file that contains the edge costs
    '''
    with open(path) as f:
        return json.load(f)


def intersection(list1, list2):
    '''
    Intersection between two lists
    '''
    return list(set(list1).intersection(set(list2)))


def switch(a, b, l):
    '''
    Switch two elements of a list.
    @a: Index of an element of the list
    @b: Index of another element of the list
    @l: A list
    '''
    l[b], l[a] = l[a], l[b]
    return l


class Graph:
    '''
    Graph with edge costs.
    '''
    def __init__(self, graph):
        self.graph = graph

    def cost(self, from_node, to_node):
        return self.graph[from_node][to_node]

    def vertex(self, position):
        return self.vertices()[position]

    def vertices(self):
        return list(self.graph.keys())


class Individual:
    '''
    A individual with a sequence of genes. Represents any possible solution
    '''

    def __init__(self, genes, graph):
        self.genes = genes
        self.graph = graph

    def __eq__(self, other):
        return self.fitness() == other.fitness()

    def __lt__(self, other):
        return self.fitness() < other.fitness()

    def __repr__(self):
        return str(self.genes)

    def copy(self):
        return self.__class__(list(self.genes), self.graph)

    def crossover(self, other):
        '''
        Returns two children by crossovering with another individual.
        It is based on indexes of common values between individuals.

        genes1 = [4, 9, 2, 0, 6, 3, 1, 8, 7, 5]
        genes2 = [3, 2, 8, 7, 5, 6, 0, 1, 9, 4]
        cut_point = 4
        child1 = [4, 2, 9, 0, 6, 3, 1, 8, 7, 5]
        child2 = [3, 2, 8, 7, 6, 4, 1, 0, 9, 5]
        '''
        genes1 = self.genes[1:-1]  # exclude start, stop points from crossover
        genes2 = other.genes[1:-1]

        # cut point to slice genes1 and genes2
        cut_point = random.randint(0, len(genes1) - 1)

        # common values in first slices
        common_values1 = intersection(genes1[:cut_point], genes2[:cut_point])

        # crossover first slices
        for value in common_values1:
            from_index = genes1.index(value)
            to_index = genes2.index(value)
            switch(from_index, to_index, genes1)

        # common values in second slices
        common_values2 = intersection(genes1[cut_point:], genes2[cut_point:])

        # crossover second slices
        for value in common_values2:
            from_index = genes2.index(value)
            to_index = genes1.index(value)
            switch(from_index, to_index, genes2)

        # merge start and stop points after crossover
        genes1 = [self.start()] + genes1 + [self.stop()]
        genes2 = [other.start()] + genes2 + [other.stop()]

        return Individual(genes1, self.graph), Individual(genes2, self.graph)

    def fitness(self):
        '''
        Returns the fitness (path cost) of individual
        '''
        fitness = 0
        chromosome_size = len(self.genes)
        for j in range(chromosome_size):
            if j < chromosome_size - 1:
                from_gene = self.genes[j]
                to_gene = self.genes[j + 1]
                cost = self.graph.cost(from_gene, to_gene)
                fitness += cost
        return fitness

    def mutation(self):
        '''
        Generates a mutation based on this individual
        '''
        genes = list(self.genes)
        a = random.randint(1, len(genes) - 2)  # exclude start and stop vertex
        b = random.randint(1, len(genes) - 2)
        switch(a, b, genes)
        return Individual(genes, self.graph)

    def start(self):
        '''
        Start gene of the individual
        '''
        return self.genes[0]

    def stop(self):
        '''
        Stop gene of the individual
        '''
        return self.genes[-1]


class Population:
    '''
    Group of individuals that represents possible solutions to the problem
    '''
    def __init__(self, graph):
        self.graph = graph
        self.individuals = []

    def __repr__(self):
        return str(self.individuals)

    def fitness(self):
        '''
        Sum of all individual fitness
        '''
        fitness = 0
        for individual in self.individuals:
            fitness += individual.fitness()
        return fitness

    def append(self, individual):
        '''
        Appends a new individual to the population
        '''
        if isinstance(individual, list):
            individual = Individual(individual, self.graph)
            self.individuals.append(individual)
        if isinstance(individual, Individual):
            self.individuals.append(individual)

    def best(self):
        '''
        Returns best individual of the population (with minimal fitness).
        '''
        return min(self.individuals)

    def get(self, index):
        '''
        Returns an individual by its index
        '''
        return self.individuals[index]

    def has(self, i):
        if isinstance(i, list):  # i is a list of genes of an individual
            for individual in self.individuals:
                if i == individual.genes:
                    return True
        if isinstance(i, Individual):  # i is an individual
            return i in self.individuals

    def roulette_wheel_selection(self):
        '''
        Select an individual based on roulette wheel selection strategy
        '''
        cumulative_fitness = 0.0
        total_fraction = self.fitness() * random.random()  # random [0.0, 1.0]
        for individual in self.individuals:
            cumulative_fitness += individual.fitness()
            if cumulative_fitness >= total_fraction:
                return individual

    def size(self):
        '''
        Returns number of individuals
        '''
        return len(self.individuals)


class Solution:
    '''
    Solution of shortest path problem using genetic algorithm
    '''
    def __init__(self, start, stop, graph, crossover_rate=0.7,
                 elitism_rate=0.1, max_population_size=100, max_stagnation=100,
                 mutation_rate=0.05):
        '''
        @start: start point for each individual in generation or population
        @stop: stop point for each individual in population
        @graph: graph of edge distances
        @crossover_rate: probability of two individuals crossing in population
        @elitism_rate: percentage of individual elitism in population
        @max_population_size: max number of individuals in population
        @max_stagnation: max stagnation in a population and its descendents
        @mutation_rate: probability of individual mutation in population
        '''
        self.start = start
        self.stop = stop
        self.graph = graph
        self.crossover_rate = crossover_rate
        self.elitism_rate = elitism_rate
        self.max_population_size = max_population_size
        self.max_stagnation = max_stagnation
        self.mutation_rate = mutation_rate

    def random_population(self, max_population_size=None):
        '''
        Generates a random population with a predefined size
        '''
        max_population_size = max_population_size or self.max_population_size
        population = Population(self.graph)

        while population.size() < max_population_size:
            genes = self.random_genes()
            if(not population.has(genes)):  # preventing twins
                population.append(genes)

        return population

    def random_genes(self):
        '''
        Generate random genes (without repetions) for an individual.
        '''
        genes = []

        vertices = self.graph.vertices()
        missing_genes = list(vertices)  # copy
        missing_genes.remove(self.start)
        missing_genes.remove(self.stop)

        genes.append(self.start)

        for i in range(len(missing_genes)):
            gene = random.choice(missing_genes)  # choosing a distinct gene
            genes.append(gene)
            missing_genes.remove(gene)  # removing already choosed gene

        genes.append(self.stop)

        return genes

    def solve(self):
        '''
        Creates lazy generations (genetic algorithm) and returns the last one
        '''

        population = self.random_population(self.max_population_size)

        # number of times there is no improvement
        stagnation_count = 0

        # number of generations created
        generations_count = 0

        while stagnation_count < self.max_stagnation:
            new_population = Population(self.graph)

            # elitism
            individuals = list(population.individuals)
            elitism_size = int(self.max_population_size * self.elitism_rate)
            while new_population.size() < elitism_size:
                best_individual = min(individuals)  # with min fitness
                new_population.append(best_individual)
                individuals.remove(best_individual)  # remove already computed

            while new_population.size() < self.max_population_size:
                father = population.roulette_wheel_selection()
                mother = population.roulette_wheel_selection()

                son = daugther = None

                # crossover
                if (random.random() < self.crossover_rate):
                    son, daugther = mother.crossover(father)

                # mutation
                if (random.random() < self.mutation_rate):
                    son = father.mutation()

                if (random.random() < self.mutation_rate):
                    daugther = mother.mutation()

                # preventing None values
                son = son or father.copy()
                daugther = daugther or mother.copy()

                # preventing duplicated individuals
                if new_population.has(son) or new_population.has(daugther):
                    continue

                new_population.append(son)
                new_population.append(daugther)

            # if there was no improvement with new population
            if population.best().fitness() <= new_population.best().fitness():
                stagnation_count += 1
            else:
                stagnation_count = 0  # reset count

            # print('stagnation.count', 'old.pop', 'new.pop')
            # print(
            #     stagnation_count,
            #     population.best().fitness(),
            #     new_population.best().fitness())

            population = new_population
            generations_count += 1

        self.generations_count = generations_count
        self.population = population

        return population


def test(max_runs=5, max_stagnation=100):
    from datetime import datetime

    results = []

    for run in range(max_runs):
        print('Run:', run)
        graph = read_graph('data/brazil58.json')
        graph = Graph(graph)
        solution = Solution('0', '57', graph, max_stagnation=max_stagnation)
        start_time = datetime.now()
        population = solution.solve()
        end_time = datetime.now()
        elapsed_time = end_time - start_time
        print("Elapsed time:", str(elapsed_time), "ms")
        print('Generations created:', solution.generations_count)
        print('Fitness:', population.best().fitness())
        print('Path:', population.best())
        results.append([elapsed_time, solution])

    return results
