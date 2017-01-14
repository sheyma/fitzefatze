import sys, os
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

direc = '/home/sheyma/HD/sheyma_bayrak_2015/jobs_adj'
#file_orig = os.path.join(direc, 'acp_w_R0_single_network_measures.dat')
#file_rand = os.path.join(direc, 'acp_w_Ra_single_network_measures.dat')

file_orig = '/home/sheyma/devel/tmp/data/jobs_network/acp_w_single_network_measures.dat'
file_rand = '/home/sheyma/devel/tmp/data/jobs_network/acp_w_erdos_single_network_measures.dat'


file_orig_sw = os.path.join(direc, 'acp_w_R0_small_worldness.dat')

G_orig = np.loadtxt(file_orig, unpack=True).T
G_rand = np.loadtxt(file_rand, unpack=True).T

# network density
plt.figure(1)
plt.plot(G_orig[:,0], G_orig[:,2], 'k')
plt.plot(G_rand[:,0], G_rand[:,2], 'or')

# clustering Coefficient
plt.figure(2)
plt.plot(G_orig[:,0], G_orig[:,3], 'k')
plt.plot(G_rand[:,0], G_rand[:,3], 'or')

# small-Worldness (a relative measure)
sw_orig = np.loadtxt(file_orig_sw, unpack=True).T

plt.figure(3)
plt.plot(sw_orig[0:81, 0], sw_orig[0:81, 7], 'k')
plt.show()

