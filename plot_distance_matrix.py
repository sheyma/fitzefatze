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
	
	N_col  = np.shape(distance_matrix)[1]
	extend = (0.5 , N_col+0.5 , N_col+0.5, 0.5 )
	
	fig , ax = plt.subplots(figsize=(15, 12))
	ax.tick_params('both', length=15, width=8, which='major')
	plt.subplots_adjust(left=0.10, right=0.95, top=0.95, bottom=0.12)
	
	cmin = distance_matrix.min()
	cmax = distance_matrix.max()
	
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

file_in  = '/home/sheyma/devel/tmp/data/fib_length.dat'
d_matrix = load_matrix(file_in)
figure   = plot_corr(d_matrix, 'mm')
figure.savefig('/home/sheyma/devel/tmp/figures/distance_matrix.png')
plt.show()
