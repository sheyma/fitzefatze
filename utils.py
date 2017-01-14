import numpy as np
import networkx as nx

# loading binary matrix 
def load_adjacency(file):
	A = np.loadtxt(file, unpack=True)
	AT = np.transpose(A)
	return AT
	

# save adjacency matrix
def export_random_adjacency(graph, file_name, method):		
	#print graph
	hiwi = nx.adjacency_matrix(graph)
	f = open(file_name[:-4] + '_' + method + '.dat','w')
	for i in range(len(hiwi)):
		for j in range(len(hiwi)):
			f.write("%d\t" % (hiwi[i,j]))
		f.write("\n")
	f.close()	
