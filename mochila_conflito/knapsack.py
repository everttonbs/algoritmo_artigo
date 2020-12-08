
# X -> itens disponíveis
# W -> peso de cada item
# P (Profit) -> lucro, ganho, valor de cada item
# b -> capacidade da mochila
# F (Forfeits) -> conflito, penalidade
# D (Forfeits Cost) -> custo de cada conflito, penalidade

def knapsack(X, W, P, b, F, D):

    S = set() # itens na mochila
    b_res = b # peso possível de carregar

    while X != 0 or S != 0:
        X_iter = list() # itens fora da mochila

        for i in range(len(X)):
            if W[i] <= b_res and not(X[i] in S): # se existe espaço e não está na mochila
                X_iter.append(i)  # itens disponivéis
                # print(X[i])

        # print('Fora', X_iter)
        if len(X_iter) == 0:  
            print('X_iter == 0')          
            return S

        ratio = list()
        P_aux = list()
        for i in range(len(X_iter)):
            P_aux = P[:]

            # Análise de conflitos
            # for k in range(len(F)):
            #     #if j in S:
            #     if F[k][0] in S or F[k][1] in S:
            #         P_aux[X_iter[i]] = P_aux[X_iter[i]] - D[k]
            
            ratio.append(P_aux[X_iter[i]] / W[X_iter[i]])

        best_item = max(ratio)
        index = ratio.index(best_item)

        if ratio[index] < 0:
            print('Index < 0')    
            return S
        
        # S = S | set([X[index]])
        # X_iter[index] é um número. Indice de X
        if X[X_iter[index]] not in S:
            S = S | set([X[X_iter[index]]])
            b_res = b_res - W[X_iter[index]]

        print('Peso ', b_res)
        
    print('Fim do while')
    return S
