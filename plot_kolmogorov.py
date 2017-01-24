import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as pl	
import sys, glob, os 
from scipy import stats
import collections
from math import factorial, sqrt, ceil

# check the loaded matrix if it is symmetric
def load_matrix(file):
	A  = np.loadtxt(file, unpack=True)
	AT = np.transpose(A)
	# check the symmetry				
	if A.shape[0] != A.shape[1] or not (A == AT).all():
		print "error: loaded matrix is not symmetric"
		raise ValueError
	return AT

def corr_histo(corr_matrix):
    corr_flat = np.ndarray.flatten(corr_matrix) 
    corr_max  = 1.0
    corr_min  = -1.0
    bin_nu    = 100
    # get a normalized histogram
    hist, bin_edges = np.histogram(corr_flat, bins=bin_nu, 
                                   range=[corr_min, corr_max], normed =True)
    return hist

def compare_kolmo(name_A, name_B, THR, SIG):
    R_thr = {}

    for THR in thr_array :
        R_temp = []

        for SIG in sig_array :
            input_A = name_A % (THR, SIG)
            input_B = name_B % (THR, SIG)

            mtx_A = load_matrix(input_A)
            HistA = corr_histo(mtx_A)

            mtx_B = load_matrix(input_B)
            HistB = corr_histo(mtx_B)                       

            diff, p = stats.ks_2samp(HistA, HistB)
            R_val = diff

            R_temp = np.append(R_temp, R_val)               

        R_thr[THR]         = np.array(R_temp)
        Ordered_R = collections.OrderedDict(sorted(R_thr.items()))      
        datam = np.array(Ordered_R.values())

    return datam
   
data_brain  = '/run/media/sheyma/0a5437d3-d51c-4c40-8c7a-06738fd0c83a/sheyma_bayrak_2015/jobs_corr/'
name_brain  = data_brain + 'acp_w_0_ADJ_thr_0.%02d_sigma=%g_D=0.05_v=30.0_tmax=45000_FHN_corr.dat'

data_random = '/var/tmp/fitzefatze-hydra/jobs_erdos01/'
name_random = data_random + 'acp_w_thr_0.%02d_erdos_sigma=%.3f_D=0.05_v=30.0_tmax=45000_pearson.dat'

thr_array = np.arange(34, 86, 4)
sig_array = np.array([0.050, 0.045, 0.040, 0.035, 0.030, 0.025, 0.020,  0.015, 0.010, 0.005 ])

KS = compare_kolmo(name_brain, name_random, thr_array, sig_array)

#Parameter Space Plot 
fig, ax = pl.subplots(figsize=(15,12))
pl.subplots_adjust(left=0.15, right=0.95, top=0.93, bottom=0.13)
pl.subplot(1,1,1)

pl.imshow(np.transpose(KS), interpolation='nearest', 
          cmap='jet', aspect='auto')

a = np.array([0.38, 0.50, 0.62, 0.74])	
b = np.array([0.05, 0.04, 0.03, 0.02, 0.01])

separ_xthick = ceil(float(len(thr_array))/len(a)) -1

pl.xticks(np.arange(1,len(thr_array), separ_xthick), a, fontsize = 50)
pl.yticks([0, 2, 4, 6, 8], b, fontsize = 50)
pl.tick_params(which='major', length=12, width=5)

pl.ylabel('$c$', fontsize = 50)
pl.xlabel('$p$', fontsize = 50)

cbar = pl.colorbar()
cbar.ax.set_title('d', fontsize = 50)
for t in cbar.ax.get_yticklabels():
	t.set_fontsize(50)

pl.show()


