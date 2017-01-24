import numpy as np
from math import factorial, sqrt, ceil
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as pl	
from matplotlib.pyplot import FormatStrFormatter
import random as rnd
import sys, os, glob
import scipy.stats as sistat
import collections
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata	
from matplotlib import cm
from scipy import stats

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

# Bhattacharyya method to compare two normalized histograms
def bhatta_hists(HA, HB):
	N  = len(HA)
	HA_bar  = sum(HA) / float(N)
	HB_bar  = sum(HB) / float(N)
	S1      = 1./ sqrt(HA_bar*HB_bar*N*N)
	S2      = 0
	for i in range(0, N) :
		S2 = S2 + sqrt(HA[i]*HB[i])
	
	S3  = sqrt(1 - S1*S2)	
	return S3
	
# comparing histograms with two different tests
def compare_hist(name_A, name_B, THR, SIG):
	R_thr = {}
	K_thr = {}
	for THR in thr_array :
		R_temp = []
		K_temp = []
		for SIG in sig_array :
			input_A = name_A % (THR, SIG)
			input_B = name_B % (THR, SIG)
			
			
			mtx_A = load_matrix(input_A)
			HistA = corr_histo(mtx_A)
			
			mtx_B = load_matrix(input_B)
			HistB = corr_histo(mtx_B)			
			
			# Bhattacharyya test
			R_val = bhatta_hists(HistA, HistB)
			R_temp = np.append(R_temp, R_val)
			
			# Kolmogorov-Smirnoff test
			K_val, p = stats.ks_2samp(HistA, HistB)
			K_temp   = np.append(K_temp, K_val)
		
		R_thr[THR] 	   = np.array(R_temp)
		K_thr[THR]     = np.array(K_temp)
		
	Ordered_R = collections.OrderedDict(sorted(R_thr.items()))	
	Bhat = np.array(Ordered_R.values())
	
	Ordered_K = collections.OrderedDict(sorted(K_thr.items()))
	Kolm = np.array(Ordered_K.values())
	
	return Bhat, Kolm

## FHN
#data_brain  = '/run/media/sheyma/0a5437d3-d51c-4c40-8c7a-06738fd0c83a/sheyma_bayrak_2015/jobs_corr/'
#name_brain  = data_brain + 'acp_w_0_ADJ_thr_0.%02d_sigma=%g_D=0.05_v=30.0_tmax=45000_FHN_corr.dat'
#data_random = '/var/tmp/fitzefatze-hydra/jobs_erdos%02d/'
#name_random = 'acp_w_thr_0.%02d_erdos_sigma=%.3f_D=0.05_v=30.0_tmax=45000_pearson.dat'

# BOLD
data_brain  = '/run/media/sheyma/0a5437d3-d51c-4c40-8c7a-06738fd0c83a/sheyma_bayrak_2015/jobs_corr_bold/'
name_brain  = data_brain + 'acp_w_0_ADJ_thr_0.%02d_sigma=%g_D=0.05_v=30.0_tmax=45000_NORM_BOLD_signal_corr.dat'

data_random = '/var/tmp/fitzefatze-hydra/jobs_erdos%02d/'
name_random = 'acp_w_thr_0.%02d_erdos_sigma=%g_D=0.05_v=30.0_tmax=45000_NORM_BOLD_signal_corr.dat'

thr_array = np.arange(34, 86, 4)
sig_array = np.array([0.050, 0.045, 0.040, 0.035, 0.030, 0.025, 0.020,  0.015, 0.010, 0.005 ])

#erdos_nums = np.arange(37)
erdos_nums = [0]

B = np.zeros((len(thr_array), len(sig_array)))
K = np.zeros((len(thr_array), len(sig_array)))

for erdos_num in erdos_nums:
    print erdos_num
    name_random_x = (data_random % erdos_num) + name_random
    Bhat, Kolm = compare_hist(name_brain, name_random_x, thr_array, sig_array)
    
    B += Bhat
    K += Kolm

B = B /float(len(erdos_nums))
K = K /float(len(erdos_nums))

#Parameter Space Plot 
fig, ax = pl.subplots(figsize=(15,12))
pl.subplots_adjust(left=0.15, right=0.95, top=0.93, bottom=0.13)
pl.subplot(1,1,1)

pl.imshow(np.transpose(B), interpolation='nearest', 
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

#Parameter Space Plot 
fig, ax = pl.subplots(figsize=(15,12))
pl.subplots_adjust(left=0.15, right=0.95, top=0.93, bottom=0.13)
pl.subplot(1,1,1)

pl.imshow(np.transpose(K), interpolation='nearest', 
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
#pl.show()

# compare two results 
#A = np.ndarray.flatten(B)
#B = np.ndarray.flatten(K)
#from scipy.stats.stats import pearsonr
#print "pearsonr correlation between kolmo and bhatta: ", pearsonr(A, B)
##get linear regression 
#m, n = np.polyfit(A, B, 1)
#pl.figure(2)
#pl.plot(A, B, 'yo', A, m*A+n, 'k')
#pl.show()

