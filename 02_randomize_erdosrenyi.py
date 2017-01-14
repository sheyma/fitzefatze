import networkx as nx
import numpy as np
import sys  
from utils import load_adjacency
from utils import export_random_adjacency

# increase recursion limit for our recursive random_graph function
sys.setrecursionlimit(10000)
# global debug variable
deep = 0

# create a random network with Erdos-Renyi method
# networkx.gnm_random_graph : random graph with given N and L
def get_random_graph(B):
	G = nx.from_numpy_matrix(B)
	L = nx.number_of_edges(G)
	N = nx.number_of_nodes(G)
	RG = nx.gnm_random_graph(N, L)
	print RG
	return RG


if __name__ == '__main__':

    for i in range(1, len(sys.argv)):
        file_in = sys.argv[i]
        binary_mtx = load_adjacency(file_in)
        Random_G   = get_random_graph(binary_mtx)
        export_random_adjacency(Random_G, file_in, 'erdos')
