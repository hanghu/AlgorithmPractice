import numpy as np
from timeit import default_timer as timer

with open('2Sum.txt','r') as f:
    lines = f.readlines()

a_set = set(list(map(lambda x: int(x[:-1]), lines)))
x_list = np.array(list(a_set))

count = 0
for t in range(-2001,10001):
    y_list = t - x_list
    y_in_a = list(map(lambda y: int(y in a_set), y_list))
    if (sum(y_in_a)/2 >= 1): count+=1
    if(t%1000 == 0):
        print('t='+str(t))
        print('counts='+str(count))

print('final counts=' +str(count))
