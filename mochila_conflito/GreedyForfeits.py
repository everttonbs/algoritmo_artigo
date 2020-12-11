
# X -> itens disponíveis
# W -> peso de cada item
# P (Profit) -> lucro, ganho, valor de cada item
# b -> capacidade da mochila
# F (Forfeits) -> conflito, penalidade
# D (Forfeits Cost) -> custo de cada conflito, penalidade

def GreedyForfeits(X, W, P, b, F, D):

    S = list() # itens na mochila
    b_res = b # peso possível de carregar
    sum_profit = 0
    sum_forfeits = 0

    while len(X) - len(S) != 0:
        
        X_iter = list() # itens fora da mochila

        for i in range(len(X)):
            if W[i] <= b_res and not(X[i] in S): # se existe espaço e não está na mochila
                X_iter.append(i)  # itens disponivéis
                # print(X[i])
        
        if len(X_iter) == 0:  
            # print('Nenhum item fora da mochila')          
            return S

        ratio = list()
        P_aux = list()
        for i in range(len(X_iter)):
            P_aux = P[:]

            # Análise de conflitos
            for k in range(len(F)):
                # F = [(i, j), ...]
                if F[k][0] == X[X_iter[i]] and F[k][1] in S:
                    P_aux[X_iter[i]] = P_aux[X_iter[i]] - D[k]
                    break
            
            ratio.append(P_aux[X_iter[i]] / W[X_iter[i]])

        best_item = max(ratio)
        index = ratio.index(best_item)

        if ratio[index] < 0:
            # print('Index < 0', ratio[index])    
            return S            
        
        
        if X[X_iter[index]] not in S:
            #S = S | set([X[X_iter[index]]])
            S.append(X[X_iter[index]])
            b_res = b_res - W[X_iter[index]]
            sum_profit += P[X_iter[index]]
            sum_forfeits += D[X_iter[index]]
            
        # print('Peso ', b_res) 

    return S


def GreedyForfeitsSingle(X, W, P, b, F, D, Si):
    S = Si.copy()
    b_res = b
    # peso possível de carregar
    for item in Si:
        index = X.index(item)
        b_res = b_res - W[index]

    while len(X) - len(S) != 0:
        X_iter = list() # itens fora da mochila

        for i in range(len(X)):
            if W[i] <= b_res and not(X[i] in S): # se existe espaço e não está na mochila
                X_iter.append(i)  # itens disponivéis
                # print(X[i])        

        ratio = list()
        P_aux = list()
        for i in range(len(X_iter)):
            P_aux = P[:]

            # Análise de conflitos
            for k in range(len(F)):
                # F = [(i, j), ...]
                if F[k][0] == X[X_iter[i]] and F[k][1] in S:
                    P_aux[X_iter[i]] = P_aux[X_iter[i]] - D[k]
                    break
            
            ratio.append(P_aux[X_iter[i]] / W[X_iter[i]])

        best_item = max(ratio)
        index = ratio.index(best_item)

        if X[X_iter[index]] not in S:               
            return X[X_iter[index]] 


def GreedyForfeitsInit(X, W, P, b, F, D, Sii):
    S = Sii.copy()
    b_res = b
    # peso possível de carregar
    for item in Sii:
        index = X.index(item)
        b_res = b_res - W[index]



    while len(X) - len(S) != 0:
        X_iter = list() # itens fora da mochila

        for i in range(len(X)):
            if W[i] <= b_res and not(X[i] in S): # se existe espaço e não está na mochila
                X_iter.append(i)  # itens disponivéis
                # print(X[i])
       
        if len(X_iter) == 0:  
            # print('X_iter == 0')          
            return S

        ratio = list()
        P_aux = list()
        for i in range(len(X_iter)):
            P_aux = P[:]

            # Análise de conflitos
            for k in range(len(F)):
                # F = [(i, j), ...]
                if F[k][0] == X[X_iter[i]] and F[k][1] in S:
                    P_aux[X_iter[i]] = P_aux[X_iter[i]] - D[k]
                    break
            
            ratio.append(P_aux[X_iter[i]] / W[X_iter[i]])

        best_item = max(ratio)
        index = ratio.index(best_item)

        if ratio[index] < 0:
            # print('Index < 0', ratio[index])    
            return S   
        
        
        if X[X_iter[index]] not in S:
            # S = S | set([X[X_iter[index]]])
            S.append(X[X_iter[index]])
            b_res = b_res - W[X_iter[index]]

        
    return S


        