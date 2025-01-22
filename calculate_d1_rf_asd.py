import skbio
import ete3
from itertools import combinations
import numpy as np
import networkx as nx
from collections import deque
def adjacency_spectral_distance(G1, G2):
    # Compute eigenvalues of adjacency matrices
    A1, A2 = nx.adjacency_matrix(G1).toarray(), nx.adjacency_matrix(G2).toarray()
    eigs1, eigs2 = np.linalg.eigvalsh(A1), np.linalg.eigvalsh(A2)
    
    # Ensure the eigenvalues are sorted
    eigs1.sort()
    eigs2.sort()

    # Compute spectral distance (Euclidean distance between spectra)
    min_len = min(len(eigs1), len(eigs2))
    distance = np.linalg.norm(eigs1[:min_len] - eigs2[:min_len])
    
    return distance
def assign_names_to_unnamed_nodes(tree):
    unnamed_count = 1  
    queue = deque([tree])  
    while queue:
        node = queue.popleft()  
        if not node.name: 
            if node.is_root():
                node.name = 'root'
            else:
                node.name = f"N{unnamed_count}"  
            unnamed_count += 1
        queue.extend(node.children) 
    return tree
def newick_to_graph(tree,graph):
    if tree.is_leaf():
        return 
    for nodo in tree.children:
        graph.add_edge(tree.name,nodo.name,weight=tree.get_distance(nodo))
        newick_to_graph(nodo,graph)
def preprocess(distance):
    if distance == 'spectral':
        with open('g1.data','r') as f:
            grafosg1 = f.readlines()
        with open('g2.data','r') as f:
            grafosg2 = f.readlines()
        gg1 = [nx.Graph() for i in range(len(grafosg1))]
        gg2 = [nx.Graph() for i in range(len(grafosg2))]
        for i,graph in enumerate(gg1):
            tree = ete3.Tree(grafosg1[i],format=1)
            assign_names_to_unnamed_nodes(tree)
            newick_to_graph(tree,graph)
        for i,graph in enumerate(gg2):
            tree = ete3.Tree(grafosg2[i],format=1)
            assign_names_to_unnamed_nodes(tree)
            newick_to_graph(tree,graph)
        return gg1,gg2
    if distance == 'RF':
        with open('g1.data','r') as f:
            grafosg1 = f.readlines()
        with open('g2.data','r') as f:
            grafosg2 = f.readlines()
        return [ete3.Tree(newick,format=1) for newick in grafosg1],[ete3.Tree(newick,format=1) for newick in grafosg2]
def calculateD1(distance):
    g1,g2 = preprocess(distance)
    d0 = []
    for gg1,gg2 in combinations(g1,2):
        if distance == 'spectral':
            dist = adjacency_spectral_distance(gg1,gg2)
        if distance == 'RF':
            dist,*_ = gg1.robinson_foulds(gg2,unrooted_trees=True)
        d0.append(dist)
    d1 = []
    for gg1 in g1:
        for gg2 in g2:
            if distance == 'spectral':
                dist = adjacency_spectral_distance(gg1,gg2)
            if distance == 'RF':
                dist,*_ = gg1.robinson_foulds(gg2,unrooted_trees=True)
            d1.append(dist)
    mu_0 = np.mean(d0)
    sigma_0 = np.std(d0)
    d1_hat = [(d-mu_0)/sigma_0 for d in d1]
    return d1_hat
d1_hat = calculateD1('spectral')
with open('ASD_values.txt','w') as f:
    for line in d1_hat:
        f.write(str(line)+"\n")
d1_hat = calculateD1('RF')
with open('RF_values.txt','w') as f:
    for line in d1_hat:
        f.write(str(line)+"\n")