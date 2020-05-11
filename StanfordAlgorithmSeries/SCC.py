import numpy as np 
import sys, threading
import queue as q

def read_test(filename, len_G):
    with open(filename,'r') as f:
        lines = f.readlines()
    graph = np.ndarray(len_G+1,dtype=list)
    graph = list(map(lambda x: [], graph))
    graph_rev = list(map(lambda x: [], graph))
    lines = list(map(lambda x: x[:-1].split(),lines))
    
    any(map(lambda x: graph[int(x[0])].append(int(x[1])), lines))
    any(map(lambda x: graph_rev[int(x[1])].append(int(x[0])), lines))
    
    return graph, graph_rev

def DFS_1st(G, i):
    global t, f, G_visited
    G_visited[i] = True
    for j in G[i]:
        if(not G_visited[j]):
            DFS_1st(G, j)
    t += 1
    f[i] = t

    return 

def DFS_2nd(G, i):
    global G_visited
    G_visited[i] = True
    scc.append(i)
    for j in G[i]:
        if (not G_visited[j]):
            DFS_2nd(G, j)
    return
        
def kosrajus_two_pass(G, G_rev):
    if G_rev == None: G_rev = get_G_rev(G)
    # two pass varibles
    global t, f, f_rev, G_visited, G_visited, scc
    t = 0 # finishing time 
    #global s = [] # current source vertex
    f = np.zeros(len(G), dtype=int) # finishing time for n variables
    
    # 1st pass, recursion thru G_rev
    G_visited = np.zeros(len(G_rev), dtype=bool)
    for i in range(len(G)-1,0,-1):
        if(not G_visited[i]):
            DFS_1st(G_rev,i)
    
    f_rev = np.zeros(len(G), dtype=int)
    for i in range(len(f)):
        f_rev[f[i]] = i

    # 2nd pass, recursion thru G based on f
    SCCs = []
    G_visited = np.zeros(len(G), dtype=bool)
    for i in range(len(G)-1,0,-1):
        scc = []
        if(not G_visited[f_rev[i]]): DFS_2nd(G,f_rev[i])
        if(scc != []): SCCs.append(scc)
    
    return SCCs

def iterative_DFS_1st(G, i):
    global t, f, G_visited
    stack = q.LifoQueue()
    G_visited[i] = True
    stack.put(i)
    while not stack.empty():
        i_cur = stack.get()
        finished = True
        for j in G[i_cur]:
            if (not G_visited[j]):
                stack.put(i_cur)
                stack.put(j)
                G_visited[j] = True
                finished = False
                break
        if(finished):
            f[i_cur] = t
            t += 1

    return 

def iterative_DFS_2nd(G, i):
    global G_visited
    stack = q.LifoQueue()
    G_visited[i] = True
    scc.append(i)
    stack.put(i)
    
    while not stack.empty():
        i_cur = stack.get()
        for j in G[i_cur]:
            if (not G_visited[j]):
                stack.put(i_cur)
                stack.put(j)
                G_visited[j] = True
                scc.append(j)
                break

    return

def get_G_rev(G):
    # Graph format: adjacency list, edges i j are j in G[i]
    G_rev = [ []  for i in range(len(G)) ]
    for i in range(len(G)):
        for j in G[i]:
            G_rev[j].append(i)
     
    return G_rev

def iterative_kosrajus_two_pass(G, G_rev=None,print_info=False):
    """ """
    if G_rev == None: G_rev = get_G_rev(G)
    # two pass varibles  
    global t, f, f_rev, G_visited, G_visited, scc
    t = 0 # finishing time 
    #global s = [] # current source vertex
    f = np.zeros(len(G), dtype=int) # finishing time for n variables
    
    # 1st pass, iterate thru G_rev
    G_visited = np.zeros(len(G_rev), dtype=bool)
    for i in range(len(G)-1,-1,-1):
        if(not G_visited[i]):
            iterative_DFS_1st(G_rev,i)
    
    if(print_info): print('successfully calculated finishing time') 
    
    f_rev = np.zeros(len(G), dtype=int)
    for i in range(len(f)):
        f_rev[f[i]] = i
    # 2nd pass, iterate thru G based on f
    SCCs = []
    G_visited = np.zeros(len(G), dtype=bool)
    for i in range(len(G)-1,-1,-1):
        scc = []
        if(not G_visited[f_rev[i]]): iterative_DFS_2nd(G,f_rev[i])
        if(scc != []): 
            SCCs.append(scc)
            if(print_info): print('obtained a SCC with %i objects' %len(scc))
    
    return SCCs



if __name__ == '__main__':
    graph_len = 875714
    # load the data
    graph, graph_rev = read_test('SCC.txt', graph_len)
    print('successfully loaded the data')

    # compute SCCs using kosraju's two pass algorithm
    #sys.setrecursionlimit(800000)
    #threading.stack_size(67108864)
    SCCs = iterative_kosrajus_two_pass(graph, graph_rev,print_info=True)
    
    # counts the length of SCCs
    SCCs_len = list(map(len, SCCs))
    SCCs_len.sort(reverse=True)
    print('length of each SSCs in this graph in a desending order')
    print(SCCs_len[:min(10,len(SCCs_len))])







