import networkx as nx
import numpy as np
import sys  
from utils import load_adjacency
from utils import export_random_adjacency

# increase recursion limit for our recursive random_graph function
sys.setrecursionlimit(10000)
# global debug variable
deep = 0

# networkx.expected_degree_graph : 
# random graph with given degree sequence - a probabilistic approach
def get_random_graph(B):
	G = nx.from_numpy_matrix(B)
	degree_seq = nx.degree(G).values()
	RG = nx.expected_degree_graph(degree_seq, seed=None, selfloops=False)
	return RG

file_in    = '/home/sheyma/devel/tmp/data/acp_w_thr_0.54.dat'
binary_mtx = load_adjacency(file_in)
Random_G   = get_random_graph(binary_mtx)
export_random_adjacency(Random_G, file_in, 'config')
