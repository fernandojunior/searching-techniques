'''
Genetic algorithm implementation to find shortest path.
Under development.
@author Fernando Felix do Nascimento Junior
'''
import random
import json


def open_distances(path):
    """
    Open a json file that contains the distances between vertices
    """
    with open(path) as f:  # open match
        return json.load(f)  # read match


def random_individual(vertices):
    '''
    Generate an individual randomly.
    Individual chromosome size is based on length of vertices.
    '''
    individual = []
    tmp = list(vertices)  # copy
    for i in range(len(vertices)):
        gene = random.choice(tmp)
        individual.append(gene)
        tmp.remove(gene)
    return individual

# distances of edges
distances = open_distances('data/brazil58.json')

# list of vertices
vertices = list(distances.keys())

# number of individuals in the population
POPULATION_SIZE = 1000

# number of genes of an individual
CHROMOSSOME_SIZE = len(vertices)

# stores initial population
population = []

# generates a random initial population with size = POPULATION_SIZE
while len(population) < POPULATION_SIZE:
    # random generation of an individual
    individual = random_individual(vertices)
    if(individual not in population):
        population.append(individual)
