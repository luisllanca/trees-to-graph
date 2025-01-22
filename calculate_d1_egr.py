import netcomp as nc
import numpy as np
from collections import deque
from ete3 import Tree
import networkx as nx
from itertools import combinations
def assign_names_to_unnamed_nodes(tree):
    unnamed_count = 1  
    queue = deque([tree])  
    while queue:
        node = queue.popleft()  
        if not node.name: 
            if node.is_root():
                node.name = 'root'
            else:
                node.name = "N"+str(unnamed_count)  
            unnamed_count += 1
        queue.extend(node.children) 
    return tree
def newick_to_graph(tree,graph):
    if tree.is_leaf():
        return 
    for nodo in tree.children:
        graph.add_edge(u=tree.name,v=nodo.name,weight=tree.get_distance(nodo))
        newick_to_graph(nodo,graph)
def preprocess():
    with open('g1.data','r') as f:
        grafosg1 = f.readlines()
    with open('g2.data','r') as f:
        grafosg2 = f.readlines()
    grupo1 = [nx.Graph() for i in range(len(grafosg1))]
    grupo2 = [nx.Graph() for i in range(len(grafosg2))]
    for t1,g1 in zip(grafosg1,grupo1):
        tree = Tree(str(t1),format=1)
        assign_names_to_unnamed_nodes(tree)
        newick_to_graph(tree,g1)
    for t2,g2 in zip(grafosg2,grupo2):
        tree = Tree(str(t2),format=1)
        assign_names_to_unnamed_nodes(tree)
        newick_to_graph(tree,g2)
    return grupo1,grupo2
def calculateD1(distance):
    g1,g2 = preprocess()
    d0 = []
    for gg1,gg2 in combinations(g1,2):
        if distance == 'EGR':
            A1,A2 = nx.adjacency_matrix(gg1).toarray(),nx.adjacency_matrix(gg2).toarray()
            dist = nc.resistance_distance(A1,A2)
        d0.append(dist)
    d1 = []
    for gg1 in g1:
        for gg2 in g2:
            if distance == 'EGR':
                A1,A2 = nx.adjacency_matrix(gg1).toarray(),nx.adjacency_matrix(gg2).toarray()
                dist = nc.resistance_distance(A1,A2)
            d1.append(dist)
    mu_0 = np.mean(d0)
    sigma_0 = np.std(d0)
    d1_hat = [(d-mu_0)/sigma_0 for d in d1]
    return d1_hat
d1_hat = calculateD1('EGR')
with open('EGR_values.txt','w') as f:
    for line in d1_hat:
        f.write(str(line)+"\n")