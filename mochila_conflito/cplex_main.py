
from docplex.mp.model import Model


def run_CPLEX(X, W, P, b, F, D):
    #context.solver.trace_log = False

    # Create CPO Model
    mdl = Model('knapsack_problem')

    # Create model variables
    # X -> itens disponíveis
    # W -> peso de cada item
    # P (Profit) -> lucro, ganho, valor de cada item
    # b -> capacidade da mochila
    # F (Forfeits) -> conflito, penalidade
    # D (Forfeits Cost) -> custo de cada conflito, penalidade

    n_items = len(X) # 500, 700, 800 e 1000
    n_forfeits = len(F)

    xi = mdl.binary_var_list(n_items, name='X')   
    v = mdl.binary_var_list(n_forfeits, name='v')


    profit_sum = 0
    for i in range(n_items):
        profit_sum += xi[i] * P[i]

    forfeit_sum = 0
    for k in range(n_forfeits):
        forfeit_sum += D[k] * v[k]

    mdl.maximize(profit_sum - forfeit_sum)

    # restrições
    b_res_sum = 0
    for i in range(n_items):
        b_res_sum += W[i] * xi[i]
    mdl.add_constraint(b_res_sum <= b)


    for f in range(n_forfeits):
        for i in range(n_items):
            for j in range(n_items):
                if X[i] in F[f] and X[j] in F[f] and i != j:
                    mdl.add_constraint(xi[i] + xi[j] - v[f] <= 1)

    # print(mdl.export_to_string())

    # Executando model
    # print("\nSolving model ....")

    try:
        msol = mdl.solve()
    except:
        return list()

    if msol:        
        list_itens = list()

        for i in range(len(xi)):
            # print('X ', msol[x_i[i]])
            if msol[xi[i]] == 1:
                list_itens.append(X[i])

        # msol.display()
        # print(list_itens)
        return list_itens
        

    else:
        print("No solution found")
        return list()


# X = ['laranja', 'melancia', 'abacate', 'pera', 'goiaba', 'pessego', 'jaca']
# W = [7, 5, 3, 8, 12, 15,11]
# P = [5, 24, 10, 12, 6, 6, 21]
# b = 30.0
# F = [('laranja', 'pera'), ('abacate', 'melancia'), ('goiaba', 'jaca')]
# D = [3, 14, 12]

# run_CPLEX(X, W, P, b, F, D)      
