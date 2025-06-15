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

def genetic_algorithm(population, fitness, stepL = 100, rho = 2):

    def weighted_by(population, fitness):
        return [fitness(individual) for individual in population]

    def weighted_random_choices(population, weights, n):
        return [population[i] for i in np.random.choice(len(population), n, p = (weights)/np.sum(weights))]
    
    def reproduce_pick_better(parents : list, rho):
        n = len(parents[0])
        children:list
        if rho == 1:
            children = [single_mutation_front(parents[0]), 
                          single_mutation_end(parents[0]), 
                          random_genetic_mutation(parents[0])]
        elif rho == 3: 
            c_1 = np.random.randint(1, 6)
            c_2 = np.random.randint(1, n - c_1)
            children = [np.array(list(parents[0][:c_1]) + list(parents[1][c_1: c_1 + c_2]) + list(parents[2][c_1 + c_2:])),
                        np.array(list(parents[0][:c_1]) + list(parents[2][c_1: c_1 + c_2]) + list(parents[1][c_1 + c_2:])),
                        np.array(list(parents[1][:c_1]) + list(parents[0][c_1: c_1 + c_2]) + list(parents[2][c_1 + c_2:])),
                        np.array(list(parents[1][:c_1]) + list(parents[2][c_1: c_1 + c_2]) + list(parents[0][c_1 + c_2:])),
                        np.array(list(parents[2][:c_1]) + list(parents[1][c_1: c_1 + c_2]) + list(parents[0][c_1 + c_2:])),
                        np.array(list(parents[2][:c_1]) + list(parents[0][c_1: c_1 + c_2]) + list(parents[1][c_1 + c_2:]))]
        else:
            c = np.random.randint(1, n)
            children = [np.array(list(parents[0][:c]) + list(parents[1][c:])),
                        np.array(list(parents[1][:c]) + list(parents[0][c:])),
                        np.array(list(parents[0][:n//2]) + list(parents[1][n//2:])),
                        np.array(list(parents[1][:n//2]) + list(parents[0][n//2:]))]
        children.sort(key=lambda x: eight_queens_heuristic(x))
        return children[0]

    # Mutação aleatória de um gene
    def mutate(child):
        n = len(child)
        c = np.random.randint(0, n)  # Escolhe posição
        child[c] = np.random.randint(1, 9)  # Novo valor entre 1 e 8
        return child
    
    def random_genetic_mutation_plus(parent): # Altera 6 posições de forma aleatória
        n = len(parent)
        genes = np.random.choice(len(parent), n - 2)
        for i in genes:
            child[i] = np.random.randint(1, 9)
        return child
    
    def random_genetic_mutation(parent): # Altera 4 posições de forma aleatória
        n = len(parent)//2
        genes = np.random.choice(len(parent), n)
        child = parent
        for i in genes:
            child[i] = np.random.randint(1, 9)
        return child
    
    def single_mutation_front(parent: np.array): # Altera as primeiras 4 posições de forma aleatória
        n = len(parent)//2
        child = np.array(parent)
        for i in range(n):
            child[i] = np.random.randint(1, 9)
        return child

    def single_mutation_end(parent): # Altera as últimas 4 posições de forma aleatória
        n = len(parent)//2
        child = parent
        for i in range(n):
            child[n + i] = np.random.randint(1, 9)
        return child
    
    step = 0
    while True:
        step += 1
        weights = weighted_by(population, fitness)
        population2 = []

        for i in range(len(population)):
            parents = weighted_random_choices(population, weights, rho)
            child = reproduce_pick_better(parents, 2)
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
        solution, steps = genetic_algorithm(population, lambda x:(28 - eight_queens_heuristic(x)), 250)
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