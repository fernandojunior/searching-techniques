'''
Genetic algorithm implementation to find shortest path.
Under development.
@author Fernando Felix do Nascimento Junior
'''
import random
import json


def read_costs(path):
    """
    Open a json file that contains the edge costs
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
costs = read_costs('data/brazil58.json')

# list of vertices
vertices = list(costs.keys())

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

# stores fitness for each individual in population
fitness = [0] * POPULATION_SIZE

# sum of all individual fitness
total_fitness = 0

# computing individual fitness based on distances of edges
for i in range(POPULATION_SIZE):
    individual = population[i]
    for j in range(CHROMOSSOME_SIZE):
        if j < CHROMOSSOME_SIZE - 1:
            gene = individual[j]
            next_gene = individual[j + 1]
            cost = costs[gene][next_gene]
            fitness[i] += cost  # fitness of individual with index i
            total_fitness += cost
