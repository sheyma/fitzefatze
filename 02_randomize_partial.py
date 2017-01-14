import networkx as nx
import numpy as np
import sys  
from utils import load_adjacency
from utils import export_random_adjacency

# increase recursion limit for our recursive random_graph function
sys.setrecursionlimit(10000)
# global debug variable
deep = 0

# check the loaded matrix if it is symmetric
def load_matrix(file):
	A  = np.loadtxt(file, unpack=True)
	AT = np.transpose(A)
	# check the symmetry				
	if A.shape[0] != A.shape[1] or not (A == AT).all():
		print "error: loaded matrix is not symmetric"
		raise ValueError
	return AT

def get_random_graph(A,B,maxswap):
    '''
A = RANDOMIZE_GRAPH_PARTIAL_UND(A,B,MAXSWAP) takes adjacency matrices A 
and B and attempts to randomize matrix A by performing MAXSWAP 
rewirings. The rewirings will avoid any spots where matrix B is 
nonzero.
Inputs:       A,      adjacency matrix to randomize
              B,      edges to avoid
        MAXSWAP,      number of rewirings
Outputs:      A,      randomized matrix
Notes:
1. Graph may become disconnected as a result of rewiring. Always
  important to check.
2. A can be weighted, though the weighted degree sequence will not be
  preserved.
3. A must be undirected.
    '''
    A=A.copy()
    i,j=np.where(np.triu(A,1))
    i.setflags(write=True); j.setflags(write=True)
    m=len(i)

    nswap=0
    while nswap < maxswap: 
        while True:
            e1,e2=np.random.randint(m,size=(2,));
            while e1==e2: e2=np.random.randint(m)
            a=i[e1]; b=j[e1]
            c=i[e2]; d=j[e2]
        
            if a!=c and a!=d and b!=c and b!=d:
                break					#all 4 vertices must be different

        if np.random.random()>.5:
            i[e2]=d; j[e2]=c			#flip edge c-d with 50% probability
            c=i[e2]; d=j[e2]			#to explore all potential rewirings
            
        #rewiring condition
        if not (A[a,d] or A[c,b] or B[a,d] or B[c,b]): #avoid specified ixes
            A[a,d]=A[a,b]; A[a,b]=0
            A[d,a]=A[b,a]; A[b,a]=0
            A[c,b]=A[c,d]; A[c,d]=0
            A[b,c]=A[d,c]; A[d,c]=0

            j[e1]=d; j[e2]=b			#reassign edge indices
            nswap+=1
            
    print A        
    return nx.from_numpy_matrix(A)

file_in    = '/home/sheyma/devel/tmp/data/acp_w_thr_0.54.dat'
binary_mtx = load_adjacency(file_in)
B          = load_matrix('/home/sheyma/devel/tmp/data/acp_w.txt')
Random_G   = get_random_graph(binary_mtx, B, maxswap=100)
export_random_adjacency(Random_G, file_in, 'partial')
