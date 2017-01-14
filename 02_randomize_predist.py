import networkx as nx
import numpy as np
import sys  
import math
import random as rnd
from utils import load_adjacency
from utils import export_random_adjacency

# increase recursion limit for our recursive random_graph function
sys.setrecursionlimit(10000)
# global debug variable
deep = 0

# create a random network with method h
# generating a random network by preserving degree distribution
# reference : Brain Connectivity Toolbox, Rubinov & Sporns, 2009
# ported script : "randmio_und_connected.m"
def get_random_graph(B):
	ITER = 200						# ITERATION CAN BE CHANGED!
	n_col   = np.shape(B)[1]		# number of columns in array
	new_B   = np.triu(B)			# upper triangle of array	
	(j , i) = new_B.nonzero()		# (row,col) index of non-zero elem.
	i.setflags(write=True)
	j.setflags(write=True)	
	K       = len(i)				# total number of non-zero elements
	ITER    = K*ITER				# total iteration number 
	maxAttempts = int(K/(n_col-1))  # max attempts per iteration
	eff     = 0  
	for iter in range(1 , ITER+1 ):
		att = 0
		while att<=maxAttempts:
			rewire = 1
			while 1:
				e1 = int(math.floor(K*rnd.random()))
				e2 = int(math.floor(K*rnd.random()))
				while e1==e2:
					e2 = int(math.floor(K*rnd.random()))
				
				a = i[e1]          # chose a col number from i
				b = j[e1]		   # chose a row number from j		
				c = i[e2]		   # chose another col number from i	
				d = j[e2]		   # chose another row number from j		
								
				if ( ( (a!=c) & (a!=d) ) & ( (b!=c) & (b!=d)) ) :
					break          # make sure that a,b,c,d differ
			
			# flipping edge c-d with 50% probability	
			if rnd.random() > 0.5 :
				i[e2]  = d
				j[e2]  = c
				c      = i[e2]
				d      = j[e2]		
			
			# rewiring condition
			if int(not(bool( B[a,d] or B[c,b] ))) : 
				
				# connectedness condition	
				if int(not(bool( B[a,c] or B[b,d] ))) :
					
					P = B[(a, d) , : ]
					P[0,b] = 0
					P[1,c] = 0
					PN     = P
					PN[:,d]= 1
					PN[:,a]= 1
			
					while 1:
						
						P[0,:] = (B[(P[0,:]!=0), :]).any(0).astype(int) 
						P[1,:] = (B[(P[1,:]!=0), :]).any(0).astype(int)
						
						P = P* (np.logical_not(PN).astype(int))
							
						if int(not((P.any(1)).all())):
							rewire = 0
							break
						
						elif  (P[:,[b, c]].any(0)).any(0):
							break
							
						PN = PN +1
				
				# reassigning edges
				if rewire :
					B[a,d] = B[a,b]
					B[a,b] = 0			
					B[d,a] = B[b,a]
					B[b,a] = 0		
					B[c,b] = B[c,d]
					B[c,d] = 0		
					B[b,c] = B[d,c]
					B[d,c] = 0
				
					# reassigning edge indices
					j[e1]  = d
					j[e2]  = b
					
					eff = eff+1;
					break
		
			att = att +1
	RG = nx.from_numpy_matrix(B)
	return RG

file_in    = '/home/sheyma/devel/tmp/data/acp_w_thr_0.54.dat'
binary_mtx = load_adjacency(file_in)
Random_G   = get_random_graph(binary_mtx)
export_random_adjacency(Random_G, file_in, 'presdist')
