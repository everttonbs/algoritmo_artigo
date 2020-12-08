
import random
import os.path

def get_input(n):
    """
    Retorna uma entrada para o problema da mochila com confitos
    n -> número de itens
    l = n x 6 -> número de conflitos
    b = n x 3 -> capacidade da mochila
    W -> [3, ..., 20] peso de cada item
    P -> [5, ..., 25]
    D -> [2, ..., 15]

    """
    itens_list = list()
    for i in range(n):
        if i < 10:
            itens_list.append('X00' + str(i))
        elif i >= 10 and i < 100:
            itens_list.append('X0' + str(i))

        else:
            itens_list.append('X' + str(i))

    #print(list_itens)   

    # Peso
    weight_list = list()
    for _ in range(n):
        weight_list.append(random.randint(3, 20))
    # print(weight_list)

    # Ganho
    profit_list = list()
    for _ in range(n):
        profit_list.append(random.randint(5, 25))
    # print(profit_list)

     # Capacidade da mochila
    b = n * 3

    # Conflitos
    l = n * 6
    pairs_forfeits_list = list()
    
    while len(pairs_forfeits_list) != l:
        i = random.choice(itens_list)
        j = random.choice(itens_list)

        if i != j:
            if [i, j] not in pairs_forfeits_list or [j, i] not in pairs_forfeits_list:
                pairs_forfeits_list.append([i, j])
        
    # print(len(pairs_forfeits_list))

    forfeits_list = list()
    for _ in range(len(pairs_forfeits_list)):
        forfeits_list.append(random.randint(2, 15))
    # print(forfeits_list)

    input_list = list()
    input_list.append(itens_list)
    input_list.append(weight_list)
    input_list.append(profit_list)
    input_list.append(b)
    input_list.append(pairs_forfeits_list)
    input_list.append(forfeits_list)

    # for i in input_list:
    #     print('\n', i, '\n')

    # criar arquivo .txt
    i = 1
    filename = str(n) + '_input_'+ str(i) + '.txt'
    while os.path.exists(filename):
        i += 1
        filename = str(n) + '_input_'+ str(i) + '.txt'    

    
    input_11 = open(filename, 'w')
    input_11.write(str(itens_list))
    input_11.write('\n')
    input_11.write(str(weight_list))
    input_11.write('\n')
    input_11.write(str(profit_list))
    input_11.write('\n')
    input_11.write(str(b))
    input_11.write('\n')
    input_11.write(str(pairs_forfeits_list))
    input_11.write('\n')
    input_11.write(str(forfeits_list))

    input_11.close()
    
    return (
        input_list[0], 
        input_list[1], 
        input_list[2], 
        input_list[3],
        input_list[4],
        input_list[5]
    ) 
    
    
get_input(700)
print('Sucess')


