
from mochila_conflito import GreedyForfeits
from mochila_conflito import carousel_forfeits

def run_ils(X, W, P, b, F, D):
    # Solução Inicial
    S0 = GreedyForfeits.GreedyForfeits(X, W, P, b, F, D)
    hash_forfeits = get_hash(X, F) # retorna dicionario

    # S = local_search_old(S0, X, W, P, b, F, D)
    Si = local_search(S0, X, W, b, hash_forfeits)

    Sii = GreedyForfeits.GreedyForfeitsInit(X, W, P, b, F, D, Si)
    # print('Solução inical: ', len(S0))
    # print('Solução ILS: ', len(Si))
    # print('Solução final -> ', len(Sii))
    # print('Verificação de conjunto -> ', len(set(Sii)))

    # count = 1
    # i = 1

    # while count <= i:
    #     S1 = perturb_solution()
    #     S1 = local_search(S1, X, W, P, b, F, D)
    #     accept_solution()
        
    #     count += 1        

    return Sii
    # return list()

def get_hash(X, F):

    hash_forfeits = dict()
    list_forfeits = list()

    for x in X:
        for f in F:
            if x in f:
                list_forfeits.append(f)

        hash_forfeits[x] = list_forfeits
        list_forfeits = list()    


    return hash_forfeits

def local_search(S0, X, W, b, hash_forfeits):

    sum_forfeits = 0
    
    # Soma a quantidade de conflitos existentes na mochila
    for key, value in hash_forfeits.items():
        if key in S0:
            # print(value)            
            for v in value:
                if v[0] in S0 and v[1] in S0:                    
                    sum_forfeits += 1
            # print(sum_forfeits)

    best_solution = sum_forfeits
    hash_changes = dict()

    for s in S0:
        sum_forfeits_s = 0
        hash_changes[s] = list()

        forfeit_i = hash_forfeits[s]
        for f in forfeit_i:
            if f[0] != s and f[0] in S0:
                sum_forfeits_s += 1
            elif f[1] != s and f[1] in S0:
                sum_forfeits_s += 1

        for x in S0:
            best_local = 0
            
            if x != s:
                sum_forfeits_x = calcule_sum_forfeits(S0, hash_forfeits, x)
            else:
                sum_forfeits_x = len(S0) + 1 

            # Só adiciona itens com menores conflitos
            if sum_forfeits_x < sum_forfeits_s:               
                hash_changes[s].append(x)                


    S1 = swap_itens(S0, X, W, b, hash_changes)
    return S1   
            
           
                
def calcule_sum_forfeits(S0, hash_forfeits, j):
    
    forfeit_j = hash_forfeits[j]    
    sum_forfeits_j = 0
    
    for f in forfeit_j: 

        if f[0] != j and f[0] in S0:
            sum_forfeits_j += 1
        elif f[1] != j and f[1] in S0:
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

            if s not in S0:
                Wi = W[index]

                if Wi <= b_res:
                    S1.append(s)
                    b_res -= Wi
   
    # print('Len -> ', len(S1))
    # print('Conjunto -> ', len(set(S1)))
    
    return S1



def local_search_old(S0, X, W, P, b, F, D):

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


