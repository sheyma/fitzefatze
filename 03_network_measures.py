import networkx as nx
import numpy as np
from math import factorial 
import math
import matplotlib.pyplot as pl	
import random as rnd
import sys, os, glob

# get L and D for full network for  different threshold values
# get average clustering coefficient of full network for dif.thre.val.
# get average degree of full network for different threshold values
# get number of connected components of full network for dif.thre.val.
# get shortest pathway of network
def get_single_network_measures(G, thr, out_prfx):
	f = open(out_prfx + 'single_network_measures.dat', 'a')
	N = nx.number_of_nodes(G)
	L = nx.number_of_edges(G)
	D = nx.density(G)
	cc = nx.average_clustering(G)
	compon = nx.number_connected_components(G)
	Con_sub = nx.connected_component_subgraphs(G)

	values = []
	values_2 =[]

	for node in G:
		values.append(G.degree(node))
	ave_deg = float(sum(values)) / float(N)
	
	f.write("%f\t%d\t%f\t%f\t%f\t%f\t" % (thr, L, D, cc, ave_deg, compon))
	#1. threshold, 2. edges, 3. density 4.clustering coefficient
	#5. average degree, 6. number of connected components
	
	for i in range(len(Con_sub)):
		if nx.number_of_nodes(Con_sub[i])>1:
			values_2.append(nx.average_shortest_path_length(Con_sub[i]))

	if len(values_2)==0:
		f.write("0.\n")
	else:
		f.write("%f\n" % (sum(values_2)/len(values_2)))
	#7. shortest pathway
	f.close()


def get_small_worldness(G, thr, out_prfx):
	f = open(out_prfx + 'small_worldness.dat', 'a')

	ER_graph   = nx.erdos_renyi_graph(nx.number_of_nodes(G), nx.density(G))
	cluster    = nx.average_clustering(G)   
	ER_cluster = nx.average_clustering(ER_graph)	
	
	transi     = nx.transitivity(G)
	ER_transi  = nx.transitivity(ER_graph)
	
	f.write("%f\t%f\t%f" % (thr, cluster, ER_cluster))

	components    = nx.connected_component_subgraphs(G)
	ER_components = nx.connected_component_subgraphs(ER_graph)

	values = []
	ER_values = []

	for i in range(len(components)):
		if nx.number_of_nodes(components[i]) > 1:
			values.append(nx.average_shortest_path_length(components[i]))
	for i in range(len(ER_components)):
		if nx.number_of_nodes(ER_components[i]) > 1:
			ER_values.append(nx.average_shortest_path_length(ER_components[i]))
	if len(values) == 0:
		f.write("\t0.")
	else:
		f.write("\t%f" % (sum(values)/len(values))) # pathlenght

	if len(ER_values) == 0:
		f.write("\t0.")
	else:
		f.write("\t%f" % (sum(ER_values)/len(ER_values)))

	f.write("\t%f\t%f" % (transi, ER_transi))  

	if (ER_cluster*sum(values)*len(values)*sum(ER_values)*len(ER_values)) >0 :
		S_WS = (cluster/ER_cluster) / ((sum(values)/len(values)) / (sum(ER_values)/len(ER_values)))  
	else:
		S_WS = 0.
	if (ER_transi*sum(values)*len(values)*sum(ER_values)*len(ER_values)) >0 :
		S_Delta = (transi/ER_transi) / ((sum(values)/len(values)) / (sum(ER_values)/len(ER_values)))
	else:
		S_Delta = 0.

	f.write("\t%f\t%f" % (S_WS, S_Delta)) # S_WS ~ small worldness 
	f.write("\n")

	f.close() 


data_dir = '/home/sheyma/devel/tmp/data/jobs_adj'
tmp_name = 'acp_w_thr_'
A = 'orig'
#A = 'erdos'

for i in range(0, 101):
        thr = float(i) / 100
        thr = format(thr, '.2f')

        if A == 'orig' :
            file_in  = tmp_name + thr + '.dat'
            out_prfx = '/home/sheyma/devel/tmp/data/jobs_network/acp_w_'
        elif A == 'erdos':
            file_in  = tmp_name + thr + '_erdos.dat'
            out_prfx = '/home/sheyma/devel/tmp/data/jobs_network/acp_w_erdos_'

        file_in  = os.path.join(data_dir, file_in)
        adj_mtx  =  np.loadtxt(file_in, unpack=True).T
        graph    = nx.from_numpy_matrix(adj_mtx)        
        get_single_network_measures(graph, float(thr), out_prfx)
        get_small_worldness(graph, float(thr), out_prfx)

        print file_in, (thr)



