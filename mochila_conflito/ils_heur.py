
from mochila_conflito import GreedyForfeits

def run_ils(X, W, P, b, F, D):
    # Solução Inicial
    S0 = GreedyForfeits.GreedyForfeits(X, W, P, b, F, D)

    S = LocalSearch(S0, X, W, P, b, F, D)





def LocalSearch(S0, X, W, P, b, F, D):
    ...

def Perturb():
    ...

