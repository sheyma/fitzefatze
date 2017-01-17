import numpy as np
from math import factorial 
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

# load input data *txt
def load_matrix(file):
	A  = np.loadtxt(file, unpack=True)
	AT = np.transpose(A)
	return AT
	
# plotting color coded distance matrix
def plot_corr(distance_matrix, distance_unit):	
	# distance_matrix : 2D array
	# distance_unit : string
	
	N_col  = np.shape(distance_matrix)[1]
	extend = (0.5 , N_col+0.5 , N_col+0.5, 0.5 )
	
	fig , ax = plt.subplots(figsize=(15, 12))
	ax.tick_params('both', length=15, width=8, which='major')
	plt.subplots_adjust(left=0.10, right=0.95, top=0.95, bottom=0.12)
	
	# for the original fiber length...
	cmin = distance_matrix.min()
	cmax = distance_matrix.max()
	
	cmin = 0
	cmax =332.71967
	print cmin, cmax
	
	plt.imshow(distance_matrix, vmin=cmin, vmax=cmax, extent=extend)
	
	cbar = plt.colorbar()
	#cbar.set_label('Some Units', labelpad=-40, y=0.45)
	cbar.ax.set_title(distance_unit, fontsize = 50)
	for t in cbar.ax.get_yticklabels():
		t.set_fontsize(50)
	plt.xticks(fontsize = 50)
	plt.yticks(fontsize = 50)
	plt.xlabel('Nodes', fontsize = 50)
	plt.ylabel('Nodes', fontsize = 50)
	return fig 	

def distance_masking(distance_matrix, mask_file):
    mask     = load_matrix(mask_file)
    d_masked = np.copy(distance_matrix)
    d_masked[np.where(mask==0)] = 0
    return d_masked


file_in  = '/home/sheyma/devel/fitzefatze/data/fib_length.dat'
d_matrix = load_matrix(file_in)

file_orig = '/home/sheyma/devel/fitzefatze/data/jobs_adj/acp_w_thr_0.54.dat'
file_rand = '/home/sheyma/devel/fitzefatze/data/jobs_erdos00/acp_w_thr_0.54_erdos.dat'

d_orig = distance_masking(d_matrix, file_orig)
d_rand = distance_masking(d_matrix, file_rand)


#flat_orig = np.ndarray.flatten(d_orig)
#plt.figure(1)
#plt.hist(flat_orig)

#flat_rand = np.ndarray.flatten(d_rand)
#plt.figure(2)
#plt.hist(flat_rand)

#plt.show()

#figure   = plot_corr(d_orig, 'mm')
figure   = plot_corr(d_rand, 'mm')
#figure.savefig('/home/sheyma/devel/fitzefatze/figures/distance_matrix.png')
figure.savefig('/home/sheyma/devel/fitzefatze/figures/distance_matrix_random.png')
#figure.savefig('/home/sheyma/devel/fitzefatze/figures/distance_matrix_orig.png')
#plt.show()
