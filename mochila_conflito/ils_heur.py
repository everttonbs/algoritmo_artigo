
from mochila_conflito import GreedyForfeits
from mochila_conflito import carousel_forfeits
import random

def run_ils(X, W, P, b, F, D):
    # Solução Inicial
    S0 = GreedyForfeits.GreedyForfeits(X, W, P, b, F, D)
    # S0 = list()

    hash_itens = get_hash_itens(X, W, P, F, D)
    # print(get_solution(S0, hash_itens))

    # hash_forfeits = get_hash(X, F) # retorna dicionario
   
    Si = get_local(S0, hash_itens)
    # hash_itens = put_itens_into_knapsack(S0, hash_itens)
    
    best_local = get_solution(Si, hash_itens)
    
    max_iter = 0

    while max_iter != 50:

        # S1 = perturb_solution(Si, history)
        S1 = get_perturbation(Si, hash_itens, b)

        # S2 = local(S1, X, W, b, hash_forfeits, S1[-1])
        S2 = get_local(S1, hash_itens)
        # S2 = local_search(S0, X, W, b, hash_forfeits)
        
        Si, best_local = get_accept(Si, S2, hash_itens, best_local, b)
        # Si = accept_solution(Si, S2, hash_forfeits)

        max_iter += 1

    #print('Solução inical: ', len(S0))
    print('Solução ILS: ', len(Si))
    print('Verificação do conjunto: ', len(set(Si)))
    # print('Solução final -> ', len(Sii))
    # print('Verificação de conjunto -> ', len(set(Sii)))
    # print(calcule_sum_forfeits(Si, hash_forfeits))
    # print(calcule_sum_forfeits(Sii, hash_forfeits))
    
    
    return Si

def get_hash_itens(X, W, P, F, D ):
    
    hash_item = dict()
    list_item = list()

    index = 0
    for x in X:
        hash_item[x] = [W[index], P[index], [], []]
        index += 1

    index_f = 0
    for f in F:
        dict_forfeits = dict()

        # dict_forfeits_1 = {f[0] : D[index_f]}
        # dict_forfeits_2 = {f[1] : D[index_f]}

        # hash_item[f[0]][2].append(dict_forfeits_2)
        # hash_item[f[1]][2].append(dict_forfeits_1)


        hash_item[f[0]][2].append(f[1])
        hash_item[f[0]][3].append(D[index_f])

        hash_item[f[1]][2].append(f[0])
        hash_item[f[1]][3].append(D[index_f])

        index_f += 1
    
    return hash_item

def put_itens_into_knapsack(S, hash_itens):

    for s in S:
        hash_itens[s][4] = 1

    return hash_itens

def get_solution(S, hash_itens):

    profit_sum = 0
    cost_sum = 0

    for i in S:
        profit_sum += hash_itens[i][1]

        index = 0
        for j in hash_itens[i][2]:
            if j in S:
                cost_sum += hash_itens[i][3][index]
            
            index += 1

    solution = profit_sum - cost_sum/2
    
    # print(solution)
    return solution

def get_accept(S0, S1, hash_itens, best_local, b):

    b_res = b    
    
    # Verificação de solução válida
    # if len(set(S1)) > len(S1):
    #     return S0, best_local
    
    for s in S1:
        b_res -= hash_itens[s][0]

    if b_res < 0:
        return S0, best_local

    sol_0 = best_local
    sol_1 = get_solution(S1, hash_itens)

    # print(sol_0, sol_1)

    if sol_1 >= sol_0:
        best_local = sol_1
        # hash_itens = put_itens_into_knapsack(S1, hash_itens)
        # print('** Melhorou! **', sol_1, sol_0)
        return S1, best_local

    else:
        best_local = sol_0
        return S0, best_local

def get_perturbation(S, hash_itens, b):    
    
    b_res = b
    # item = None

    min_ratio = 1000000
    for s in S:
        if hash_itens[s][1] / hash_itens[s][0] < min_ratio:
            min_ratio = hash_itens[s][1] / hash_itens[s][0]
            item = s


    S_aux = S.copy()
    S_aux.remove(item)

    for s in S_aux:
        b_res -= hash_itens[s][0]

    index = 0
    while b_res > 0 and index < len(S):
        item = random.choice(list(hash_itens.keys()))
        if hash_itens[item][0] <= b_res and item not in S_aux:
            if b_res - hash_itens[item][0] > 0:
                S_aux.append(item)
                b_res -= hash_itens[item][0]

        index += 1

    # print(b_res)
    return S_aux
   

def get_local(S0, hash_itens):

    S_aux = S0[:-1].copy()
    
    item = None
    # Lista da razão (Pi/Wi) dos itens fora da mochila
    
    best_ratio = hash_itens[S0[0]][1] / hash_itens[S0[0]][0]
    # best_sol = get_solution(S0, hash_itens)
    # sum_forfeits_s = calcule_sum_forfeits(S0, hash_forfeits[S0[0]])

    for s in hash_itens:
        if s not in S0:
            sol_aux = hash_itens[s][1] / hash_itens[s][0] 
            # sol_aux = get_solution(S_aux + [s], hash_itens)
            # forf_aux = sum_forfeits_s = calcule_sum_forfeits(S_aux, hash_forfeits[s])

            if sol_aux > best_ratio:
                best_ratio = sol_aux
                # sum_forfeits = forf_aux
                item = s

                # S_aux.append(item)

                # return list(set(S_aux))
                

    # Assim evita verficação dos vizinhos do mesmo item
    if item == None:
        S_aux.insert(0, S0[-1])

    else:
        S_aux.append(item)   
    
    return S_aux


def get_neighborhood(hash_itens):

    for i in hash_itens.keys():

        radio = hash_itens[i][1] / hash_itens[i][0]
    

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


