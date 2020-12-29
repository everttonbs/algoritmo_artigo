
from mochila_conflito import GreedyForfeits

def run_ils(X, W, P, b, F, D):
    # Solução Inicial
    S0 = GreedyForfeits.GreedyForfeits(X, W, P, b, F, D)

    S = LocalSearch(S0, X, W, P, b, F, D)

    return S


def LocalSearch(S0, X, W, P, b, F, D):

    X_iter = X.copy()
    best_profit = calcule_profit(S0, X, P)
    
    # Elementos que não estão na mochila
    for i in S0:
        X_iter.remove(i)

    S1 = S0.copy()
    list_change = list()
    for i in S0:
        for j in X_iter:
            S1.remove(i)
            S1.append(j)

            profit = calcule_profit(S1, X, P)
            if profit > best_profit:
                best_profit = profit
                list_change = [i, j]

            S1.remove(j)
            S1.append(i)

    if len(list_change) > 1:
        S1 = move_swap(S1, list_change)
  

    return S1            


def calcule_profit(S0, X, P):
    sum_profit = 0

    for s in S0:
        index = X.index(s)
        sum_profit += P[index]

    return sum_profit

def move_swap(S1, swap):
    S1.remove(swap[0])
    S1.append(swap[1])

    return S1


    
def Perturb():
    ...

