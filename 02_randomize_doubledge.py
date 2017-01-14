import networkx as nx
import numpy as np
import sys  
from utils import load_adjacency
from utils import export_random_adjacency

# increase recursion limit for our recursive random_graph function
sys.setrecursionlimit(10000)
# global debug variable
deep = 0

# networkx.double_edge_swap : random graph by swaping two edges 
def get_random_graph(B):
	G = nx.from_numpy_matrix(B)
	L = nx.number_of_edges(G)	
	trial = L*(L-1.)/2
	swap_num = L;
	if L >2:
		RG = nx.double_edge_swap(G,nswap=swap_num,max_tries=trial)
		return RG
	else:
		print "No swap possible for number of edges", L
		return G
	
file_in    = '/home/sheyma/devel/tmp/data/acp_w_thr_0.54.dat'
binary_mtx = load_adjacency(file_in)
Random_G   = get_random_graph(binary_mtx)
export_random_adjacency(Random_G, file_in, 'doubedge')
