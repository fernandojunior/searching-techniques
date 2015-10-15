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


class Population:
    def __init__(self, graph, population_size=1000):
        self.graph = graph
        self.population = self.random_population(population_size)

    def crossover(self, individual1, individual2):

        genes1 = individual1.genes
        genes2 = individual2.genes

        cut_point = random.randint(0, self.chromosome_size() - 1)

        child1 = genes1[:cut_point] + genes2[cut_point:]
        child2 = genes2[:cut_point] + genes1[cut_point:]

        return Individual(child1, self.graph), Individual(child2, self.graph)

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
