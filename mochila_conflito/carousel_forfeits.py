
from mochila_conflito import GreedyForfeits

def carousel_forteits(X, W, P, b, F, D, alfa, beta):

    S = GreedyForfeits.GreedyForfeits(X, W, P, b, F, D)

    # S2 = RemoveLastChoices(S1, beta)
    number_drops = round(len(S) * beta)
    S_aux = list(S.copy())
    for x in range(number_drops):
        try:
            S_aux.pop(-1) # remove o último elemento da lista
        except:
            pass
    Si = S_aux.copy()
    
    size = len(Si)    

    number_iteration = alfa * size
    for i in range(alfa * size):
        # remove o elemento mais antigo da lista
        #S2 = RemoveOldestChoices(S2)
        try:
            Si.pop(0) # remove o primeiro elemento
        except:
            pass

        j = GreedyForfeits.GreedyForfeitsSingle(X, W, P, b, F, D, Si)
        Si.append(j)
        

    Sii = GreedyForfeits.GreedyForfeitsInit(X, W, P, b, F, D, Si)

    return Sii

    

