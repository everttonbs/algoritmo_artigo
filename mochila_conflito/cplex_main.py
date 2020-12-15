
from docplex.cp.model import CpoModel
from docplex.cp.config import context


def run_CPLEX(X, W, P, b, F, D):
    context.solver.trace_log = False

    # Create CPO Model
    mdl = CpoModel()

    # Create model variables
    # X -> itens disponíveis
    # W -> peso de cada item
    # P (Profit) -> lucro, ganho, valor de cada item
    # b -> capacidade da mochila
    # F (Forfeits) -> conflito, penalidade
    # D (Forfeits Cost) -> custo de cada conflito, penalidade

    n_items = len(X) # 500, 700, 800 e 1000
    n_forfeits = len(F)


    x_i = mdl.binary_var_list(n_items, name='X')
    x_j = mdl.binary_var_list(n_items, name='Xj')
    v = mdl.binary_var_list(n_forfeits, name='v')

    profit_sum = 0
    for i in range(n_items):
        profit_sum += x_i[i] * P[i]

    forfeit_sum = 0
    for k in range(n_forfeits):
        forfeit_sum += D[k] * v[k]

    mdl.add(mdl.maximize(profit_sum - forfeit_sum))

    # restrições
    b_res_sum = 0
    for i in range(n_items):
        b_res_sum += W[i] * x_i[i]
    mdl.add(b_res_sum <= b)

    cost_sum = 0    
    for i in range(n_items):
        j = 0       
        for f in range(n_forfeits):
            cost_sum += x_i[i] + x_j[j] - v[f]
        j += 1

    mdl.add(cost_sum <= 1)  


    # Executando model
    print("\nSolving model ....")
    try:
        msol = mdl.solve(TimeLimit=10)
    except:
        return list()

    if msol:        
        list_itens = list()
        for i in range(len(x_i)):
            # print('X ', msol[x_i[i]])
            if msol[x_i[i]] == 1:
                list_itens.append(X[i])

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
