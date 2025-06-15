import numpy as np

# Calcula a heurística de conflitos entre rainhas (quantos pares se atacam)
def eight_queens_heuristic(state):
    h = 0
    for i in range(8):
        for j in range(i + 1, 8):
            if state[i] == state[j]:  # Rainhas na mesma linha
                h += 1
                continue
            if state[i] == state[j] + (j - i):  # Rainhas na mesma diagonal descendente
                h += 1
                continue
            if state[i] == state[j] - (j - i):  # Rainhas na mesma diagonal ascendente
                h += 1
    return h

# Algoritmo genético principal
def genetic_algorithm(population, 
                      fitness, 
                      stepL=100, 
                      selection_method='proportional',
                      taxa_mutacao = 0.15,
                      n_tournament=10, 
                      rho=3, 
                      elite_size=0, 
                      limite_abate=0,
                      tentativas_abate=100):
    
    # Calcula os pesos com base na função de fitness (aptidão), que mede o quão bom é um indivíduo (ou solução) da população
    def weighted_by(population, fitness):
        return [fitness(individual) for individual in population]

    # Seleção entre todos os indivíduos com probabilidade proporcional ao seu escore de aptidão (roleta)
    def weighted_random_choices(population, weights, n):
        return [population[i] for i in np.random.choice(len(population), n, replace = False, p = (weights) / np.sum(weights))]

    # Seleção aleatoria de n indivíduos (n > ρ), onde os ρ mais adequados são escolhidos como pais (torneio)
    def tournament_selection(population, fitness, n, rho):
        candidates = [population[i] for i in np.random.choice(len(population), n, replace = False)]  # sorteia n
        candidates.sort(key=fitness, reverse = True)  # ordena pelos melhores
        return list(candidates[:rho])  # escolhe os rho melhores

    # Cruzamento entre dois pais
    def reproduce(parent1, parent2):
        n = len(parent1)
        c = np.random.randint(1, n)  # Ponto de corte
        return np.array(list(parent1[:c]) + list(parent2[c:]))

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
        weights = weighted_by(population, fitness)  # Calcula pesos (fitness)

        # Número de tentativas para encontrar uma solução com o abate
        attempts = 0
        max_attempts = tentativas_abate # Limite de tentativas para evitar loops infinitos
        
        # Elitismo: preserva os melhores indivíduos
        if elite_size > 0:
            sorted_population = sorted(population, key = lambda x: fitness(x), reverse = True)
            elite = sorted_population[:elite_size]
        else:
            elite = []

        # Cria os descendentes
        population2 = []
    
        
        while len(population2) + elite_size < len(population):
            
            # Seleciona os pais de acordo com o método de seleção escolhido
            if selection_method == 'proportional':
                parents = weighted_random_choices(population, weights, rho)
            elif selection_method == 'tournament':
                parents = tournament_selection(population, fitness, n_tournament, rho)
            else:
                raise ValueError("Método inválido. Use 'proportional' ou 'tournament'.")

            # Geração do filho e possível mutação
            child = reproduce_pick_better(parents, rho)
            if np.random.random() < taxa_mutacao:
                child = random_genetic_mutation_plus(child)
            
            # Faz o abate de indivíduos com base no limite de abate
            if fitness(child) >= limite_abate or attempts >= max_attempts:
                population2.append(child)
            
            elif limite_abate > 0:
                    attempts += 1

        # Combina os descendentes com os elites
        population = elite + population2

        # Ordena nova população por fitness
        population = sorted(population, key=lambda x: fitness(x))

        # Critério de parada: encontrou solução ou atingiu limite de gerações
        if fitness(population[-1]) == 28 or step == stepL:
            return population[-1], step

# Avalia o desempenho de um método de seleção em 100 execuções
def testar_metodo(selection_method):
    qRes = 0       # Número de soluções encontradas
    qFail = 0      # Número de falhas
    stepsRes = 0   # Total de passos das soluções
    stepsFail = 0  # Total de passos das falhas

    for _ in range(100):
        # Geração inicial da população
        population = [np.random.randint(1, 9, 8) for _ in range(100)]

        # Executa algoritmo genético com o método escolhido
        solution, steps = genetic_algorithm(
            population,
            lambda x: 28 - eight_queens_heuristic(x),  # Fitness = 28 - número de conflitos
            stepL=1000,
            selection_method=selection_method,
            n_tournament=10,
            rho=3
        )

        # Avalia se foi uma solução válida
        if eight_queens_heuristic(solution) == 0:
            qRes += 1
            stepsRes += steps
        else:
            qFail += 1
            stepsFail += steps

    # Exibe estatísticas do método testado
    print(f"\n--- Método de Seleção: {selection_method} ---")
    if qRes > 0:
        print(f"Soluções encontradas: {qRes}, média de passos: {stepsRes / qRes:.2f}")
    if qFail > 0:
        print(f"Falhas: {qFail}, média de passos: {stepsFail / qFail:.2f}")

# Avalia o desempenho combinando métodos de seleção com elitismo e abate
def testar_metodo_completo(selection_method, elite_size=0, limite_abate=None, descricao=""):
    qRes = 0       # Número de soluções encontradas
    qFail = 0      # Número de falhas
    stepsRes = 0   # Total de passos das soluções
    stepsFail = 0  # Total de passos das falhas

    for _ in range(100):
        # Geração inicial da população
        population = [np.random.randint(1, 9, 8) for _ in range(100)]

        # Executa algoritmo genético com configuração escolhida
        solution, steps = genetic_algorithm(
            population,
            lambda x: 28 - eight_queens_heuristic(x),  # Fitness = 28 - número de conflitos
            stepL=1000,
            selection_method=selection_method,
            n_tournament=10,
            rho=3,
            elite_size=elite_size,
            limite_abate=limite_abate
        )

        # Avalia se foi uma solução válida
        if eight_queens_heuristic(solution) == 0:
            qRes += 1
            stepsRes += steps
        else:
            qFail += 1
            stepsFail += steps

    # Exibe estatísticas da configuração testada
    nome_config = f"{selection_method.capitalize()}"
    if elite_size > 0:
        nome_config += f" + Elite({elite_size})"
    if limite_abate is not None:
        nome_config += f" + Abate({limite_abate})"
    if descricao:
        nome_config += f" - {descricao}"
    
    print(f"\n--- {nome_config} ---")
    taxa_sucesso = (qRes / 100) * 100
    print(f"Taxa de sucesso: {taxa_sucesso:.1f}% ({qRes}/100)")
    
    if qRes > 0:
        print(f"Passos médios (sucesso): {stepsRes / qRes:.2f}")
    if qFail > 0:
        print(f"Passos médios (falha): {stepsFail / qFail:.2f}")
    
    return {
        'config': nome_config,
        'taxa_sucesso': taxa_sucesso,
        'sucessos': qRes,
        'falhas': qFail,
        'passos_sucesso': stepsRes / qRes if qRes > 0 else 0,
        'passos_falha': stepsFail / qFail if qFail > 0 else 0
    }

# Teste completo de todas as combinações
def teste_completo_estrategias():
    print("="*80)
    print("TESTE COMPARATIVO DE ESTRATÉGIAS - ALGORITMO GENÉTICO")
    print("="*80)
    
    resultados = []
    
    # Configurações base (sem elitismo/abate)
    print("\n" + "="*60)
    print("1. MÉTODOS BASE (sem elitismo, sem abate)")
    print("="*60)
    
    resultados.append(testar_metodo_completo('proportional', 0, None, "Base"))
    resultados.append(testar_metodo_completo('tournament', 0, None, "Base"))
    
    # Testando apenas elitismo
    print("\n" + "="*60)
    print("2. ADICIONANDO ELITISMO")
    print("="*60)
    
    for elite in [5, 10, 15]:
        resultados.append(testar_metodo_completo('proportional', elite, None, f"Elite {elite}"))
        resultados.append(testar_metodo_completo('tournament', elite, None, f"Elite {elite}"))
    
    # Testando apenas abate
    print("\n" + "="*60)
    print("3. ADICIONANDO ABATE")
    print("="*60)
    
    for abate in [10, 15, 20]:
        resultados.append(testar_metodo_completo('proportional', 0, abate, f"Abate {abate}"))
        resultados.append(testar_metodo_completo('tournament', 0, abate, f"Abate {abate}"))
    
    # Testando combinações elitismo + abate
    print("\n" + "="*60)
    print("4. COMBINANDO ELITISMO + ABATE")
    print("="*60)
    
    combinacoes = [
        (5, 15), (10, 15), (10, 20), (15, 20)
    ]
    
    for elite, abate in combinacoes:
        resultados.append(testar_metodo_completo('proportional', elite, abate, f"Elite {elite} + Abate {abate}"))
        resultados.append(testar_metodo_completo('tournament', elite, abate, f"Elite {elite} + Abate {abate}"))
    
    # Resumo final
    print("\n" + "*"*80)
    print("RESUMO DOS MELHORES RESULTADOS")
    print("*"*80)
    
    # Ordena por taxa de sucesso
    resultados_ordenados = sorted(resultados, key=lambda x: x['taxa_sucesso'], reverse=True)
    
    print("\nTOP 5 - MAIOR TAXA DE SUCESSO:")
    for i, resultado in enumerate(resultados_ordenados[:5], 1):
        print(f"{i}. {resultado['config']}: {resultado['taxa_sucesso']:.1f}%")
    
    # Filtra apenas sucessos para análise de eficiência
    com_sucessos = [r for r in resultados if r['sucessos'] > 0]
    mais_eficientes = sorted(com_sucessos, key=lambda x: x['passos_sucesso'])
    
    print("\nTOP 5 - MENOR NÚMERO DE PASSOS (entre os que tiveram sucesso):")
    for i, resultado in enumerate(mais_eficientes[:5], 1):
        print(f"{i}. {resultado['config']}: {resultado['passos_sucesso']:.2f} passos")

# Executar testes
if __name__ == "__main__":
    # Testes originais
    testar_metodo('proportional')
    testar_metodo('tournament')
    
    # Teste completo de estratégias
    teste_completo_estrategias()
