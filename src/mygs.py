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
        print(from_node, to_node)
        return self.graph[from_node][to_node]

    def vertex(self, position):
        return self.vertices()[position]

    def vertices(self):
        return list(self.graph.keys())


class Individual:

    def __init__(self, genes, graph):
        self.genes = genes
        self.graph = graph

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


def replace(a, b, l):
    '''
    In a list l, find all elements equals to a and replace with b
    '''
    for n, i in enumerate(l):
        if i == a:
            l[n] = b


class Population:
    def __init__(self, graph, population_size=1000):
        self.graph = graph
        self.population = self.random_population(population_size)

    def crossover(self, individual1, individual2):

        # genes1 = [4, 9, 2, 0, 6, 3, 1, 8, 7, 5]
        genes1 = list(individual1.genes)
        # genes2 = [3, 2, 8, 7, 5, 6, 0, 1, 9, 4]
        genes2 = list(individual2.genes)

        # cut_point = 4
        cut_point = random.randint(0, self.chromosome_size() - 1)

        # finding all uncommons genes from first slice of genes1 and genes2
        diff_slice1 = [
            # genes1[:cut_point] - genes2[:cut_point] = [4, 9, 0]
            difference(genes1[:cut_point], genes2[:cut_point]),
            # genes2[:cut_point] - genes1[:cut_point] = [3, 8, 7]
            difference(genes2[:cut_point], genes1[:cut_point])]

        # crossover first slice
        # result = [3, 8, 2, 7] + [6, 3, 1, 8, 7, 5]
        for n, el in enumerate(diff_slice1[0]):
            replace(el, diff_slice1[1][n], genes1)

        diff_slice2 = [
            # [3, 8, 7]
            difference(genes1[cut_point:], genes2[cut_point:]),
            # [0, 9, 4]
            difference(genes2[cut_point:], genes1[cut_point:])]

        # crossover second slice
        # result = [0, 2, 9, 4] + [6, 0, 1, 9, 4, 5]
        for n, el in enumerate(diff_slice2[0]):
            replace(el, diff_slice2[1][n], genes2)

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

    def __repr__(self):
        return str(self.population)

# distances of edges
graph = read_graph('data/brazil58.json')
graph = Graph(graph)
population = Population(graph)
print(population.population[0].fitness())

# TODO: linkar individuals e population
