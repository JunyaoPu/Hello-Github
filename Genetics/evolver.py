import random


parent_fraction = 0.1
mutation_probability = 0.1
k = 0.01 # amount to mutate


def evolve(population):
    parent_num  = int(parent_fraction * len(population))
    population  = population_sort(population) # Ordering population
    parents     = population[:parent_num] # Selecting top performers
    children    = population[parent_num:] # Selecting worst performers

    children    = population_breed(parents, children)

    new_generation = parents + children

    return new_generation

def population_breed(parents, children):
    for child in children:
        mother_ID   = random.randint(0, len(parents)-1)
        father_ID   = random.randint(0, len(parents)-1)

        mother      = parents[mother_ID]
        father      = parents[father_ID]

        child       = crossover(mother, father, child)
        child.distance = 0
        child.score    = 0

        if (random.uniform(0, 1) < mutation_probability):
            mutate(child)

    return children



def mutate(child):
    child.w1  += random.uniform(-k,+k)
    child.w2  += random.uniform(-k,+k)

def crossover(mother, father, child):
    if (random.uniform(0,1) < 0.5):
        new1 = mother.w1
    else:
        new1 = father.w1

    if (random.uniform(0,1) < 0.5):
        new2 = mother.w2
    else:
        new2 = father.w2


    sum = new1 + new2
    new1 = new1 / sum
    new2 = new2 / sum



    child.w1 = new1
    child.w2 = new2



    return child

def population_sort(population):
    """
    Should sort based on distance, from high to low.
    """
    new_population = sorted(population, key=lambda x:x.distance, reverse=True)
    return new_population
