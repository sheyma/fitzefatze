import numpy as np
from math import factorial 
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import colors

# load *txt or *dat as numpy array
def load_matrix(file):
    A  = np.loadtxt(file, unpack=True)
    AT = np.transpose(A)
    return AT
	

# plotting binary matrix as black and white
def plot_adj(adjacency_matrix):

    N_col  = np.shape(adjacency_matrix)[1]
    
    for i in range(0,N_col):
        for j in range(0, N_col):
            if i==j:
                adjacency_matrix[i,j] = 1
                #print i,j 
    extend = (0.5 , N_col+0.5 , N_col+0.5, 0.5 )
    fig , ax = plt.subplots(figsize=(15, 12))
    #ax.tick_params('both', length=15, width=8, which='major', color='red')
    plt.subplots_adjust(left=0.10, right=0.95, top=0.93, bottom=0.12)				
    cmap = colors.ListedColormap(['white', 'black'])
    bounds=[0, 0.5, 1]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    img = plt.imshow(adjacency_matrix, interpolation='nearest', vmin=0, vmax=1.0, 
                     extent=extend, cmap=cmap, norm=norm)

    cbar = plt.colorbar(img, cmap=cmap, norm=norm, boundaries=bounds, ticks=[0, 1])
    cbar.ax.set_title('a$_{ij}$', fontsize = 50, x=0, y=1.03)
    for t in cbar.ax.get_yticklabels():
        t.set_fontsize(50)
    plt.xticks(fontsize = 50)
    plt.yticks(fontsize = 50)
    plt.xlabel('Nodes', fontsize = 50)
    plt.ylabel('Nodes', fontsize = 50)

    return

#file_in    = '/home/sheyma/devel/tmp/data/acp_w_thr_0.54.dat'
#file_in    = '/home/sheyma/devel/tmp/data/acp_w_thr_0.54_erdos.dat'
#file_in    = '/home/sheyma/devel/tmp/data/acp_w_thr_0.54_doubedge.dat'
#file_in    = '/home/sheyma/devel/tmp/data/acp_w_thr_0.54_presdist.dat'
#file_in    = '/home/sheyma/devel/tmp/data/acp_w_thr_0.54_partial.dat'
file_in    = '/home/sheyma/devel/tmp/data/acp_w_thr_0.54_config.dat'


adj_matrix = load_matrix(file_in)
plot_adj(adj_matrix)
plt.show()
