
from mochila_conflito import GreedyForfeits
from mochila_conflito import carousel_forfeits
import random

def run_ils(X, W, P, b, F, D):
    # Solução Inicial
    S0 = GreedyForfeits.GreedyForfeits(X, W, P, b, F, D)
    
    hash_forfeits = get_hash(X, F) # retorna dicionario
    # hash_cost = get_cost(X, F, D)
    # hash_profit = get_profit(X, W, P)
    
    Si = local(S0, X, W, b, hash_forfeits, S0[0])
    # Si = local_search(S0, X, W, b, hash_forfeits)
    
    history = list()

    # NumeroItens // 2
    while len(history) != 50:

        S1 = perturb_solution(Si, history)

        S2 = local(S1, X, W, b, hash_forfeits, S1[0])
        # S2 = local_search(S0, X, W, b, hash_forfeits)
        
        Si = accept_solution(Si, S2, hash_forfeits)


    Sii = GreedyForfeits.GreedyForfeitsInit(X, W, P, b, F, D, Si)

    print('Solução inical: ', len(S0))
    print('Solução ILS: ', len(Si))
    print('Solução final -> ', len(Sii))
    print('Verificação de conjunto -> ', len(set(Sii)))
    # print(calcule_sum_forfeits(Si, hash_forfeits))
    # print(calcule_sum_forfeits(Sii, hash_forfeits))
    
    return Sii

def get_hash(X, F):

    hash_forfeits = dict()
    list_forfeits = list()

    for x in X:
        for f in F:
            if x in f:
                # list_forfeits.append(f)
                if x == f[0]:
                    list_forfeits += [f[1]]
                else:
                    list_forfeits += [f[0]]

        hash_forfeits[x] = list_forfeits
        list_forfeits = list()

    return hash_forfeits

def get_cost(X, F, D):
    hash_cost = dict()
    list_forfeits = list() 

    for x in X:
        i = 0
        for f in F:            
            if x in f:
                # list_forfeits.append(f)
                if x == f[0]:
                    list_forfeits.append([f[1], D[i]])
                else:
                    list_forfeits.append([f[0], D[i]])

            i += 1

        hash_cost[x] = list_forfeits
        list_forfeits = list()

    return hash_cost

def get_profit(X, W, P):

    hash_profit = dict()
    list_profit = list()
    
    for x in range(len(X)):
        hash_profit[X[x]] = P[x] / W[x]

    return hash_profit

def local(S0, X, W, b, hash_forfeits, i):
    
    hash_changes = dict()
    hash_changes[i] = list()

    sum_forfeits_s = calcule_sum_forfeits(S0, hash_forfeits[i])

    if sum_forfeits_s == 0:
        return S0

    for x in hash_forfeits[i]:
        
        sum_forfeits_x = calcule_sum_forfeits(S0, hash_forfeits[x])        
        
        # Só adiciona itens com menores conflitos
        if sum_forfeits_x <= sum_forfeits_s :                      
            hash_changes[i].append(x)

    S1 = swap_itens(S0, X, W, b, hash_changes)
    # print(S1)
    return S1

    # return S0  


def local_search(S0, X, W, b, hash_forfeits):

    sum_forfeits = 0
    
    # Soma a quantidade de conflitos existentes na mochila
    for key, value in hash_forfeits.items():
        if key in S0:
            # print(value)            
            for v in value:
                if v in S0:                    
                    sum_forfeits += 1            

    best_solution = sum_forfeits

    hash_changes = dict()

    for s in S0:
        hash_changes[s] = list()

        sum_forfeits_s = calcule_sum_forfeits(S0, hash_forfeits[s])

        for x in hash_forfeits[s]:            
            
            if x != s:
                sum_forfeits_x = calcule_sum_forfeits(S0, hash_forfeits[x])
            else:
                sum_forfeits_x = len(S0) + 1 

            # Só adiciona itens com menores conflitos
            if sum_forfeits_x < sum_forfeits_s:               
                hash_changes[s].append(x)                


    S1 = swap_itens(S0, X, W, b, hash_changes)
    return S1   
            
           
                
def calcule_sum_forfeits(S0, hash_forfeits):    
      
    sum_forfeits_j = 0
    
    for f in hash_forfeits:

        if f in S0:
            sum_forfeits_j += 1            

    return sum_forfeits_j

def get_item(list_change):
        return list_change[-1]

def swap_itens(S0, X, W, b, hash_changes):
    b_res = b
    S1 = list()
    for s in S0:
        try:
            aux_item = get_item(hash_changes[s])            

            while aux_item in S1:
                hash_changes[s].pop()
                aux_item = get_item(hash_changes[s])

            index = X.index(aux_item)
            Wi = W[index]

            if Wi <= b_res:
                S1.append(aux_item)
                b_res -= Wi

        # KeyError or IndexError
        except:
            index = X.index(s)

            if s not in S1:
                Wi = W[index]

                if Wi <= b_res:
                    S1.append(s)
                    b_res -= Wi
   
    # print('Len -> ', len(S1))
    # print('Conjunto -> ', len(set(S1)))
    
    return S1

    
def perturb_solution(S, history):

    S_aux = S[1:] + S[:1]
    history.append(S_aux)
    # b_res = b

    # for s in S_aux:
    #     index = X.index(s)
    #     if s in S_aux:
    #         b_res -= W[index]

    # while b_res > 0:
    #     index = random.randint(0, len(X) -1)
    #     if X[index] not in S_aux:
    #         if b_res > W[index]:
    #             S_aux.append(X[index])
    #             b_res -= W[index]
    #         else:
    #             return S_aux

    return S_aux

def accept_solution(Sii, S, hash_forfeits):
    
    best_local = 0
    for s in Sii:
        best_local += calcule_sum_forfeits(Sii, hash_forfeits[s])
    
    aux_local = 0
    for s in S:
        aux_local += calcule_sum_forfeits(S, hash_forfeits[s])    

    # print('Sii ', best_local, 'S', aux_local)
    # print(len(Sii), len(S))   

    if best_local < aux_local: 
        # print('aux')       
        return Sii

    else:        
        return S   

