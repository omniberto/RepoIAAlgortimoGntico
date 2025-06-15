import numpy as np

def eight_queens_heuristic(state):
    h = 0
    for i in range(8):
        for j in range(i + 1, 8):
            if state[i] == state[j]:
                h += 1
                continue
            if state[i] == state[j] + (j - i):
                h += 1
                continue
            if state[i] == state[j] - (j - i):
                h += 1
    return h

def genetic_algorithm(population, fitness, stepL = 100):

    def weighted_by(population, fitness):
        return [fitness(individual) for individual in population]

    def weighted_random_choices(population, weights, n):
        return [population[i] for i in np.random.choice(len(population), n, p = (weights)/np.sum(weights))]
    
    def reproduce_pick_better(parent1, parent2):
        n = len(parent1)
        c = np.random.randint(1, n)
        child_1 = np.array(list(parent1[:c]) + list(parent2[c:]))
        child_2 = np.array(list(parent2[:c]) + list(parent1[c:]))
        return child_1 if eight_queens_heuristic(child_1) <= eight_queens_heuristic(child_2) else child_2
    
    def random_genetic_mutation_plus(parent):
        n = len(parent)
        genes = np.random.choice(len(parent), n - 2)
        for i in genes:
            parent[i] = np.random.randint(1, 9)
        return parent

    step = 0
    while True:
        step += 1
        weights = weighted_by(population, fitness)
        population2 = []

        for i in range(len(population)):
            parent1, parent2 = weighted_random_choices(population, weights, 2)
            child = reproduce_pick_better(parent1, parent2)
            if np.random.random() < 0.15:
                child = random_genetic_mutation_plus(child)
            population2.append(child)
        population = sorted(population2, key = lambda x:fitness(x))

        if (fitness(population[-1]) == 28) or (step == stepL):
            return population[-1], step
        
        
population = []
for i in range(100):
    population.append(np.random.randint(1, 9, 8))  
solution, step = genetic_algorithm(population, lambda x:(28 - eight_queens_heuristic(x)), 100)
print("Heurística: ", eight_queens_heuristic(solution), " em ", step, " passos")
for _ in range (10):
    qRes = 0
    qFail = 0
    stepsRes = 0
    stepsFail = 0
    for i in range(100):
        population = []
        for i in range(100):
            population.append(np.random.randint(1, 9, 8)) 
        solution, steps = genetic_algorithm(population, lambda x:(28 - eight_queens_heuristic(x)), 1000)
        if eight_queens_heuristic(solution) == 0:
            qRes += 1
            stepsRes += steps
        else:
            qFail += 1
            stepsFail += steps
    if qRes > 0:
        print("Soluções encontradas: ", qRes, " em média em ", stepsRes/qRes, " passos")
    if qFail > 0:
        print("Falhas: ", qFail, " em média em ", stepsFail/qFail, " passos")