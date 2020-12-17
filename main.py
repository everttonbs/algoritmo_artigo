
import os
import random
from datetime import datetime
import timeit
import time
from mochila_conflito import GreedyForfeits
from mochila_conflito import carousel_forfeits
from mochila_conflito import knapsack
from mochila_conflito import cplex_main
import numpy as np
# from mochila_conflito import create_inputs

# X, W, P, b, F, D

# X -> itens disponíveis
# W -> peso de cada item
# P (Profit) -> lucro, ganho, valor de cada item
# b -> capacidade da mochila
# F (Forfeits) -> conflito, penalidade
# D (Forfeits Cost) -> custo de cada conflito, penalidade

def main():
    # user_input()
    file_input()
    # random_input()

def user_input():
    X = ['laranja', 'melancia', 'abacate', 'pera', 'goiaba', 'pessego', 'jaca']
    W = [0.75, 2.5, 1.0, 1.75, 1.5, 1.2, 3.5]
    P = [1.9, 1.5, 1.6, 1.45, 0.7, 1.85, 1.65]
    b = 6.0
    F = [('laranja', 'melancia'), ('abacate', 'pera'), ('goiaba', 'pessego')]
    D = [0.75, 0.4, 0.4]

    itens = {
        'laranja' : [0.75, 0.9],
        'melancia' : [2.5, 0.5],
        'abacate' : [1.75, 0.6],
        'pera' : [1.5, 0.45],
        'goiaba' : [0.95, 0.7],
        'pessego' : [1.2, 0.85],
        'jaca' : [3.5, 0.65],
    }

    print(GreedyForfeits.GreedyForfeits(X, W, P, b, F, D))

def file_input():
    list_input = os.listdir('inputs')    
    
    for file in list_input:
        data = open('inputs\\' + file, 'r')
        print('inputs\\' + file)
        lines = data.readlines()

        X_aux = lines[0].strip()
        W_aux = lines[1].strip()
        P_aux = lines[2].strip()
        b = lines[3].strip()
        F_aux = lines[4].strip()
        D_aux = lines[5].strip()

        data.close()
        
        X = list()
        for i in range(2, len(X_aux), 8):
            X.append(X_aux[i:i+4])
        
        W = list()
        w = W_aux.split('[')
        w = w[1].split(']')
        W = w[0].split(', ')

        P = list()
        p = P_aux.split('[')
        p = p[1].split(']')
        P = p[0].split(', ')        

        F = list()
        f = F_aux.replace('[', '')
        f = f.replace(']', '')
        f = f.replace('\'', '')
        f = f.split(', ')

        for i in range(0, len(f), 2):
            F.append([f[i], f[i+1]])


        D = list()
        d = D_aux.split('[')
        d = d[1].split(']')
        D = d[0].split(', ')                

        W = [float(i) for i in W]
        P = [float(i) for i in P]
        b = float(b)
        D = [float(i) for i in D]

        start = time.time()

        alfa, beta = 2, 0.05
        out = carousel_forfeits.carousel_forteits(X, W, P, b, F, D, alfa, beta)

        # out = GreedyForfeits.GreedyForfeits(X, W, P, b, F, D)

        # CPLEX
        # cplex_main.run_CPLEX(X, W, P, b, list(), D)
        # out = cplex_main.run_CPLEX(X, W, P, b, F, D)        

        end = time.time()

        if len(out) == 0:
            print('TL')
        else:
            get_result(out, X, P, F, D, end, start)


def get_result(out, X, P, F, D, end, start):

    out_sorted = sorted(out)
    sum_profit = calcule_profit(out_sorted, X, P)
    sum_forfeits, forfeit_costs = calcule_forfeits(out_sorted, F, D)
    
    
    print('-------------------')
   #  print('itens ->', out_sorted)
    print('Profit ->', sum_profit)      
    print('Cost ->', forfeit_costs)      
    print('Forfeits ->', sum_forfeits) 
    print('Sol. ->', sum_profit - forfeit_costs)     
    print('Time:', (end - start))
    print('-------------------\n')


def calcule_profit(list_items, X, P):
    sum_profit = 0

    for i in list_items:
        index = X.index(i)
        sum_profit += P[index]

    return sum_profit

def calcule_forfeits(list_items, F, D):
    sum_forfeits = 0
    forfeit_costs = 0

    i = 0
    for pares in F:
        if pares[0] in list_items and pares[1] in list_items:
            sum_forfeits += 1
            forfeit_costs += D[i]
        i += 1

    return sum_forfeits, forfeit_costs



def random_input():
    for _ in range(10):
        start = time.time()
        num_itens = 10
        print('Relatório com ', num_itens, 'itens')        
        X, W, P, b, F, D = create_inputs.get_input(num_itens)
        # print('Itens: ', X)
        # print('Peso: ', W)
        # print('Ganho: ', P)
        # print('Capacidade da Mochila: ', b)
        # print('Pares de Conflitos: ', F)
        # print('Perda: ', D)

        # print(GreedyForfeits.GreedyForfeits(X, W, P, b, F, D))

        alfa, beta = 2, 0.05
        # print(carousel_forfeits.carousel_forteits(X, W, P, b, F, D, alfa, beta))
        
        end = time.time()
        print('Time: ', (end - start))
        print()
        
    
if __name__ == "__main__":
    main()


