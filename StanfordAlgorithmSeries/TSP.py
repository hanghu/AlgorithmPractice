import numpy as np

with open('tsp.txt','r') as f:
    lines = f.readlines()

NC = int(lines[0])
City = list(map(lambda x: tuple(map(float,x.split())), lines[1:]))

def eucliean_distance(x,y):
    return np.sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)

#initialize
City_code = [0b1 << i for i in range(NC)] 

A_new = {}
A_new_set = set([0b1])
A_new[0b1] = np.zeros(NC)

# main loop
for m in range(2,NC+1):
    print('Subproblem size: ', m)
    A_old_set = A_new_set.copy()
    A_old = A_new.copy()
    #print(A_old.keys())

    #making new subsets containing m elements:
    A_new_set_list = list(filter(lambda x: x & 0b1, A_old_set))
    A_new_set_temp = list(map(lambda x: set(map(lambda y: x | y, City_code)), A_new_set_list))
    A_new_set = set.union(*A_new_set_temp)
    A_new_set = A_new_set - A_old_set

    print(' total number of subsets: ',len(A_new_set))

     # initialize A_new
    A_new = {}
    for S in A_new_set:
         A_new[S] = np.full(NC,np.inf)

    #A_new_set = list(filter(lambda x: x & 0b1, A_new_set))
    #print(' total number of subsets containing 1: ',len(A_new_set))

    # update A_new
    for code_j in City_code:
        j = City_code.index(code_j)
        print(j)
        for S in A_new_set:
            #print(bin(S),bin(S^code_j))
            if code_j & S and S^code_j in A_old.keys():
                subp_sols = []
                code_k_list = list(filter(lambda x: x & S, City_code))
                code_k_list.remove(code_j)
                for code_k in code_k_list:
                    k = City_code.index(code_k)
                    #print(k, j, bin(S^code_j), A_old[S^code_j][k])
                    subp_sols.append(A_old[S^code_j][k] + eucliean_distance(City[k], City[j]))
                A_new[S][j] = min(subp_sols)


A_last = list(A_new.values())[0]
for j in range(1,NC):
    A_last[j] += eucliean_distance(City[0],City[j])
print('Solution of TSP problem:', min(A_last))

