import numpy as np
import random
from timeit import default_timer as timer

# implement a union-find data structure
# thru union-by-rank and path-compression

class DisjointSet():
    def __init__(self, num_of_objs):
        """
            initialize the disjoint set using indexes instead of values
        """
        assert isinstance(num_of_objs, int)
        self.num_of_objs = num_of_objs
        self.num_of_sets = num_of_objs
        self.parents = list(range(num_of_objs))
        self.ranks   = [0] * num_of_objs

        return

    def find(self, x):

        p = self.parents[x]
        if(p == x): return p

        while (p != self.parents[p]):
            p = self.parents[p]

        # path compression
        if(p != self.parents[x]): self.parents[x] = p

        return p

    def union(self, x, y):
        s1 = self.find(x)
        s2 = self.find(y)

        if(s1 == s2): return

        r1 = self.ranks[s1]
        r2 = self.ranks[s2]

        if(r1 > r2):
            self.parents[s2] = s1
        else:
            self.parents[s1] = s2
            # rank goes up when equal
            if (r1 == r2): self.ranks[s2] +=1

        self.num_of_sets -= 1

        return

def hammimng_distance(x, y, nbits):
    result = x ^ y
    return (sum([(result >> i) & 1 for i in range(nbits)]))

def gen_bit_masks(n_bits, n_diff_bits, 
                 passed_bit=None,
                 cur_bit=None,
                 cur_start=None,
                 cur_end=None):
    
    assert n_diff_bits >= 1
    assert n_bits >= n_diff_bits
    
    if passed_bit is None:
        cur_bit    = 1
        passed_bit = 0
        cur_start  = 0
        cur_end    = n_bits - n_diff_bits + 1
    
    masks = []
    if(cur_bit == n_diff_bits):
        masks += [passed_bit | 1 << i for i in range(cur_start,cur_end)]
    else:
        for i in range(cur_start,cur_end):
            passing_bit = passed_bit | 1 << i 
            masks += gen_bit_masks(n_bits, n_diff_bits, passed_bit=passing_bit,
                                   cur_bit=cur_bit+1, cur_start=i+1,cur_end=cur_end+1)      
    return masks


if __name__ == '__main__':

    with open('cluster2.txt', 'r') as f:
        lines = f.readlines()

    n_nodes, n_bits = list(map(int, lines[0].split()))
    nodes = list(map(lambda x: int(x.replace(' ', ''),2), lines[1:]))
    nodes = list(set(nodes))
    n_nodes = len(nodes)
    print('There are %i distinct nodes, each nodes have %i bits' %(n_nodes, n_bits))
    
    # make dictionary for each nodes:
    nodes_map = {}
    for i in range(n_nodes):
        nodes_map[nodes[i]] = i

    bit_masks = [0]
    bit_masks += gen_bit_masks(n_bits, 1)
    bit_masks += gen_bit_masks(n_bits, 2)   
    
    start = timer()
    dj_set = DisjointSet(n_nodes)
    
    for i in range(n_nodes):
        target_nodes = [ nodes[i] ^ mask for mask in bit_masks]
        for nodes_j in target_nodes:
            if nodes_j in nodes_map.keys():
                dj_set.union(i,nodes_map[nodes_j])
    
    end = timer()
    print('finished in '+str(end-start) +' seconds!')
    print('there is ' + str(dj_set.num_of_sets) + ' clusters')
    # do stochastic pick on some number of pair to build a inital connection between clusters
#    print('start to do a stochastic process')
#    sto_picking = 100 * n_nodes
#    for k in range(sto_picking):
#        i = random.randint(0,n_nodes-1)
#        j = random.randint(0,n_nodes-1)
#        if(i!=j and dj_set.find(i) != dj_set.find(j)):
#            if(sum(nodes[i] == nodes[j]) < 3):
#                dj_set.union(i,j)
#
#        if(k%n_nodes == 0): print(' step %i : there are %i clusters now' %(k,dj_set.num_of_sets))  
    
#    # do a sweep on all nodes
#    for i in range(n_nodes):
#        for j in range(i+1, n_nodes):
#            ci = dj_set.find(i)
#            cj = dj_set.find(j)
#            if (ci != cj):
#                # hammimng_distance
#                if(hammimng_distance(nodes[i],nodes[j],n_bits) < 3):
#                    dj_set.union(i,j)
#        print('finish node %i now,  there are %i clusters' %(i,dj_set.num_of_sets))
    
    
    
