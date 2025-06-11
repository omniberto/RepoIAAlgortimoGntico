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

def four_queens_heuristic(state):
    h = 0
    for i in range(4):
        for j in range(i + 1, 4):
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
    
    def reproduce(parent1, parent2):
        n = len(parent1)
        c = np.random.randint(1, n)
        return np.array(list(parent1[:c]) + list(parent2[c:]))
    
    def genetic_mutation(parent):
        if bool(np.random.randint(0, 2)):
            n = len(parent)
            for i in range(n):
                parent[i] = np.random.randint(1, 9)
        return parent
    
    def reproduce_in_vitro(parent1, parent2):
        if four_queens_heuristic(parent1[:4]) <= four_queens_heuristic(parent1[4:]):
            var = genetic_mutation(parent1[:4])
            if four_queens_heuristic(var) < four_queens_heuristic(parent1[:4]):
                embrio = np.array(list(var) + list(parent2[4:]))
            embrio = np.array(list(parent1[:4]) + list(parent2[4:]))
        else:
            embrio = np.array(list(parent2[:4]) + list(parent1[4:]))
        return embrio
    
    def reproduce_with_help(parent1, parent2, surrogate):
        if bool(np.random.randint(0, 2)):
            embrio = reproduce_in_vitro(parent1, parent2)
        else:
            embrio = reproduce(parent1, parent2)
        embrio[0] = surrogate[0]
        embrio[-1] = surrogate[-1]
        return embrio
    
    def reproduce_mamma_mia(parent1, parent2, parent3):
        n = len(parent1)//3 + 1
        c = np.random.randint(1, n)
        d = np.random.randint(1, n)
        return np.array(list(parent1[:c]) + list(parent2[c:d + c]) + list(parent3[d + c:]))
    
    def mutate(child):
        n = len(child)
        c = np.random.randint(0, n)
        child[c] = np.random.randint(1, np.random.randint(2, 9))
        #child[n - c - 1] = np.random.randint(np.random.randint(1, 8), 9)
        return child
    
    step = 0
    while True:
        step += 1
        weights = weighted_by(population, fitness)
        population2 = []

        for i in range(len(population)):
            parent1, parent2 = weighted_random_choices(population, weights, 2)
            choice = np.random.randint(0, 4)
            if choice == 0:
                surrogate = weighted_random_choices(population, weights, 1)
                child = reproduce_with_help(parent1, parent2, surrogate[0])
            elif choice == 1:
                child = reproduce_in_vitro(parent1, parent2)
            elif choice == 2:
                parent3 = weighted_random_choices(population, weights, 1)
                child = reproduce_mamma_mia(parent1, parent2, parent3[0])
            else:
                child = reproduce(parent1, parent2)
            if np.random.random() < 0.2:
                child = mutate(child)
            population2.append(child)
        population = sorted(population2, key = lambda x:fitness(x))

        if (fitness(population[-1]) == 28) or (step == stepL):
            return population[-1], step
        
        
population = []
for i in range(100):
    population.append(np.random.randint(1, 9, 8))  
solution, step = genetic_algorithm(population, lambda x:(28 - eight_queens_heuristic(x)), 1000)
print("Heurística: ", eight_queens_heuristic(solution), " em ", step, " passos")

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