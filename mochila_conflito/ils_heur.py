
from mochila_conflito import GreedyForfeits

def run_ils(X, W, P, b, F, D):
    # Solução Inicial
    S0 = GreedyForfeits.GreedyForfeits(X, W, P, b, F, D) 
    S = local_search(S0, X, W, P, b, F, D)

    # count = 1
    # i = 1

    # while count <= i:
    #     S1 = perturb_solution()
    #     S1 = local_search(S1, X, W, P, b, F, D)
    #     accept_solution()
        
    #     count += 1        

    return S


def local_search(S0, X, W, P, b, F, D):

    X_iter = X.copy()
    #best_solution = calcule_profit(S0, X, P) - calcule_forfeits(S0, F, D)    
    best_solution = calcule_solution(S0, X, W, P, b, F, D)

    # Elementos que não estão na mochila
    for i in S0:
        X_iter.remove(i)

    S1 = S0.copy()
    list_change = list()
    for i in S0:
        for j in X_iter:
            S1.remove(i)
            S1.append(j)

            # solution = calcule_profit(S1, X, P) - calcule_forfeits(S1, F, D)
            solution = calcule_solution(S1, X, W, P, b, F, D)
            if solution > best_solution:
                best_solution = solution
                list_change = [i, j]                

                # retorna a primeira melhor solução                
                return S1

            S1.remove(j)
            S1.append(i)

    if len(list_change) > 1:
        S1 = move_swap(S1, list_change)

    return S1          


def calcule_solution(S0, X, W, P, b, F, D):
    sum_profit = 0
    # sum_forfeits = 0
    forfeit_costs = 0
    b_res = b

    for s in S0:
        index = X.index(s)
        sum_profit += P[index]
        b_res -= W[index]

    i = 0
    for pares in F:
        if pares[0] in S0 and pares[1] in S0:
            # sum_forfeits += 1
            forfeit_costs += D[i]
        i += 1

    sol = sum_profit - forfeit_costs

    if b_res >= 0:
        return sol

    else:
        return -1


def calcule_profit(S0, X, P):
    sum_profit = 0

    for s in S0:
        index = X.index(s)
        sum_profit += P[index]

    return sum_profit

def calcule_forfeits(S0, F, D):
    # sum_forfeits = 0
    forfeit_costs = 0

    i = 0
    for pares in F:
        if pares[0] in S0 and pares[1] in S0:
            # sum_forfeits += 1
            forfeit_costs += D[i]
        i += 1

    return forfeit_costs

def move_swap(S1, swap):
    S1.remove(swap[0])
    S1.append(swap[1])

    return S1

    
def perturb_solution():
    ...

def accept_solution():
    ...


