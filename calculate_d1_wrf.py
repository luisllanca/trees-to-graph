import skbio
from itertools import combinations
import numpy as np
def preprocess():
    with open('g1.data','r') as f:
        grafosg1 = f.readlines()
    with open('g2.data','r') as f:
        grafosg2 = f.readlines()
    return [skbio.TreeNode.read([newick]) for newick in grafosg1],[skbio.TreeNode.read([newick]) for newick in grafosg2]
def calculateD1(distance):
    g1,g2 = preprocess()
    d0 = []
    for gg1,gg2 in combinations(g1,2):
        if distance == 'WRF':
            dist = gg1.compare_wrfd(gg2)
        d0.append(dist)
    d1 = []
    for gg1 in g1:
        for gg2 in g2:
            if distance == 'WRF':
                dist = gg1.compare_wrfd(gg2)
            d1.append(dist)
    mu_0 = np.mean(d0)
    sigma_0 = np.std(d0)
    d1_hat = [(d-mu_0)/sigma_0 for d in d1]
    return d1_hat
d1_hat = calculateD1('WRF')
with open('WRF_values.txt','w') as f:
    for line in d1_hat:
        f.write(str(line)+"\n")
    