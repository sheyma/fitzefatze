import numpy as np
import networkx as nx
import re
import subprocess as sp
import math

params = { # Fitzhugh-Nagumo simulation parameters...
        'dt': 0.001, 
			}

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

def load_simfile(infile, unpack=False):
	print "reading data ..."
	
	# handle xz files transparently
	if re.search(r'\.xz$', infile, flags=re.IGNORECASE):
		# non-portable but we don't want to depend on pyliblzma module
		xzpipe = sp.Popen(["xzcat", infile], stdout=sp.PIPE)
		x_infile = xzpipe.stdout
	else:
		# in non-xz case we just use the file name instead of a file
		# object, numpy's loadtxt() can deal with this
		x_infile = infile
	
	A  = np.loadtxt(x_infile, unpack=unpack)
	print "shape of input matrix : " , np.shape(A)
	return A

# return file name without extensions like ".dat", ".dat.xz", etc.
def get_data_basename(infile):
	basename = re.sub(r'\.dat(|\.xz|\.gz|\.bz2)$', '', infile, flags=re.IGNORECASE)
	return basename

# obtain u_i time series from loaded matrix
def get_timeseries(simfile):
	print "subtracting u-time series as numpy matrix..."
	# extract first column of simout as time vector
	tvec = simfile[:,0]
	dt   = tvec[1] - tvec[0]
	# calculate total time of simulation 
	T    = int(math.ceil( (tvec[-1])  / dt * params['dt'] ))
	print "T = " , T , "[seconds]", "dt = " , dt/100 ,"[seconds]"
	# extract u-columns
	u_indices  = np.arange(1, simfile.shape[1] ,1)
	u_series   = simfile[:, u_indices]
	return u_series , T, dt, tvec
