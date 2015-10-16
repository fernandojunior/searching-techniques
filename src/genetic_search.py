"""
https://code.google.com/p/tspag/source/browse/alggen.c
http://aimotion.blogspot.com.br/2009/03/resolvendo-o-problema-do-caixeiro.html
https://code.google.com/p/k-shortest-paths/source/checkout
https://code.google.com/p/mycodeplayground/source/browse/
http://lethain.com/genetic-algorithms-cool-name-damn-simple/

Individual - Any possible solution
Population - Group of all individuals
Search Space - All possible solutions to the problem
Chromosome - Blueprint for an individual
Trait - Possible aspect of an individual
Allele - Possible settings for a trait
Locus - The position of a gene on the chromosome
Genome - Collection of all chromosomes for an individual

https://code.google.com/p/spgenetic/
Example of 'graph': G = {'s':{'u':10, 'x':5}, 'u':{'v':1, 'x':2}, 'v':{'y':4},
                           'x':{'u':3, 'v':9, 'y':2}, 'y':{'s':7, 'v':6}}
"""

from random import choice, randint, random, randrange
from math import sqrt


class Graph:
    graph = {}

    def __init__(self, graph):
        self.graph = graph

    def findAllPaths(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if start not in self.graph:
            return []
        paths = []
        for node in self.graph[start]:
            if node not in path:
                newpaths = self.findAllPaths(node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def __len__(self):
        return len(self.graph)

    def getVertexes(self):
        return list(self.graph.keys())

    def pathExist(self, path):
        for i in range(len(path) - 1):
            if path[i + 1] not in self.graph[path[i]]:
                return False
        return True

    def pathCost(self, path):
        if not self.pathExist(path):
            return float('inf')
        return sum(self.graph[path[i]][path[i + 1]] for i in range(len(path) - 1))

    def findShortestPathDijkstra(self, start, end, path=[]):
        '''
        Simple implementation of Dijkstra algorithm.
        May be used for testing purpose.
        '''
        path = path + [start]
        if start == end:
            return path
        if start not in self.graph:
            return None
        shortest = None
        for node in self.graph[start].keys():
            if node not in path:
                newpath = self.findShortestPathDijkstra(node, end, path)
                if newpath:
                    if not shortest or self.pathCost(newpath) < self.pathCost(shortest):
                        shortest = newpath
        return shortest

    def __getitem__(self, n):
        return self.graph[n]


def generateRandomGraph(numVertex, maxLength=100, oriented=False, connectivity=0.5):
    '''
    Generates random graph
    '''
    gd = {}
    for i in range(numVertex):
        costs = {}
        for k in range(numVertex):
            if k != i:
                if random() > connectivity:
                    costs[k] = float('inf')
                if (not oriented) and (k in gd) and (i in gd[k]):
                    costs[k] = gd[k][i]
                else:
                    if k not in costs:
                        costs[k] = randint(1, maxLength)
            else:
                costs[k] = 0
        gd[i] = costs
    return Graph(gd)


class SPOrganismFactory:

    def __init__(self, graph):
        if isinstance(graph, Graph):
            self.graph = graph
        else:
            raise TypeError("Must be 'Graph' object")

    def newOrganism(self, genes):
        return SPOrganism(genes, self.graph)


class SPOrganism:
    '''
    Simple organism with simple sequence of genes
    '''
    genes = []

    crossoverRate = 0.5

    def __init__(self, genes, graph, **kw):
        if isinstance(genes, tuple) or isinstance(genes, list):
            self.genes = genes
            self.graph = graph
            self.kw = kw
        else:
            raise TypeError("Only list and tuple allowed")

    def __add__(self, partner):
        return self.cross(partner)

    def __eq__(self, other):
        return self.fitness() == other.fitness()

    def __lt__(self, other):
        return self.fitness() < other.fitness()

    def __getitem__(self, n):
        return self.genes[n]

    def __len__(self):
        return len(self.genes)

    def __repr__(self):
        return str(self.genes)

    def copy(self):
        return self.__class__(self.genes)

    def cross(self, partner):
        genes1 = []
        genes2 = []

        for i in range(len(self.genes)):
            ourGene = self.genes[i]
            partnerGene = partner[i]
            if random() < self.crossoverRate:
                genes1.append(ourGene)
                genes2.append(partnerGene)
            else:
                genes1.append(partnerGene)
                genes2.append(ourGene)

        child1 = self.makeChild(genes1)
        child2 = self.makeChild(genes2)
        return (child1, child2)

    def fitness(self):
        return self.graph.pathCost(self.genes)

    def makeChild(self, gens):
        return self.__class__(gens, self.graph)

    def mutate(self):
        mutant = self.copy()
        gene = choice(self.genes)
        mutant[randint(0, len(mutant) - 1)] = gene
        return mutant


class Population:
    '''
    Organisms population
    '''

    def __init__(self, childCull=200, childCount=1000, goodParents=10, mutants=0.1):
        self.sorted = False
        self.organisms = []
        self.childCull = childCull
        self.childCount = childCount
        self.goodParents = goodParents
        self.mutants = mutants

    def add(self, *args):
        for arg in args:
            if isinstance(arg, tuple) or isinstance(arg, list):
                self.add(*arg)
            if issubclass(arg.__class__, SPOrganism):
                self.organisms.append(arg)
            elif issubclass(arg.__class__, Population):
                self.organisms.extend(arg)
            else:
                raise TypeError("Only organisms and populations can be added")

    def __repr__(self):
        return str(self.organisms)

    def __getitem__(self, n):
        self.sort()
        return self.organisms[n]

    def __len__(self):
        return len(self.organisms)

    def fitness(self):
        fitnesses = map(lambda org: org.fitness(), self.organisms)
        return sum(fitnesses) / len(fitnesses)

    def best(self):
        self.sort()
        return self[0]

    def sort(self):
        if not self.sorted:
            self.organisms.sort()
            self.sorted = True

    def generate(self, nfittest=None, nchildren=None):
        if not nfittest:
            nfittest = self.childCull
        if not nchildren:
            nchildren = self.childCount

        children = []

        self.sort()
        nadults = len(self)
        n2adults = nadults * nadults

        for i in range(nchildren):
            # pick random parent
            i1 = i2 = int(sqrt(randrange(n2adults)))
            parent1 = self[-i1]

            while i2 == i1:
                i2 = int(sqrt(randrange(n2adults)))
            parent2 = self[-i2]

            # crossing
            child1, child2 = parent1 + parent2

            children.extend([child1, child2])

        if self.goodParents:
            children.extend(self[:self.goodParents])

        children.sort()

        # add a proportion of mutants
        nchildren = len(children)
        n2children = nchildren * nchildren
        mutants = []
        numMutants = int(nchildren * self.mutants)

        for i in range(numMutants):
            # pick one random child
            id = int(sqrt(randrange(n2children)))
            child = children[-id]
            mutants.append(child)

        children.extend(mutants)

        children.sort()

        # make new population
        self.organisms[:] = children[:nfittest]

        self.sorted = True


class SPSolution:
    '''
    Solution of shortest path problem
    '''
    def __init__(self, graph, start, stop, initPopulationLength=1000,
                 genesCount=10, populationCount=300,
                 childCull=200, childCount=1000, goodParents=10, mutants=0.1):
        self.orgFactory = SPOrganismFactory(graph)
        self.graph = graph
        self.start, self.stop = start, stop
        self.initPopulationLength = initPopulationLength
        self.genesCount = genesCount
        self.populationCount = populationCount
        self.childCull = 200
        self.childCount = childCount
        self.goodParents = goodParents
        self.mutants = mutants

    def generateRandomSPOrganism(self):
        genes = [self.start]
        for i in range(self.genesCount - 2):
            genes.append(choice(self.graph.getVertexes()))
        genes.append(self.stop)
        return self.orgFactory.newOrganism(genes)

    def generateInitPopulation(self):
        '''
        Generate random init population
        '''
        p = Population(childCull=self.childCull, childCount=self.childCount,
                       goodParents=self.goodParents, mutants=self.mutants)
        for i in range(self.initPopulationLength):
            p.add(self.generateRandomSPOrganism())
        return p

    def populationIterator(self):
        population = self.generateInitPopulation()
        for i in range(self.populationCount):
            population.generate()
            yield population

    def solve(self):
        '''
        Main method
        '''

        population = self.generateInitPopulation()
        for i in range(self.populationCount):
            population.generate()
        return population.best()
