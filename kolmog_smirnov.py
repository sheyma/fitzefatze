import sys, os
import numpy as np
from math import ceil 
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from scipy import stats
from plot_distance_matrix import distance_masking, load_matrix


file_in  = '/home/sheyma/devel/fitzefatze/data/fib_length.dat'
d_matrix = load_matrix(file_in)

file_orig = '/home/sheyma/devel/fitzefatze/data/jobs_adj/acp_w_thr_0.54.dat'
file_rand = '/home/sheyma/devel/fitzefatze/data/jobs_erdos00/acp_w_thr_0.54_erdos.dat'

orig = distance_masking(d_matrix, file_orig)
rand = distance_masking(d_matrix, file_rand)

flat_orig = np.ndarray.flatten(orig)
flat_rand = np.ndarray.flatten(rand)

his_orig, bin_orig = np.histogram(flat_orig, bins=100, normed=True)
his_rand, bin_rand = np.histogram(flat_rand, bins=100, normed=True)

print stats.ks_2samp(his_orig, his_rand)
print orig.mean(), rand.mean()

# comparing distance distributions of two given graphs 
dir_adj = '/home/sheyma/devel/fitzefatze/data/jobs_adj'
dir_erdos = '/home/sheyma/devel/fitzefatze/data/jobs_erdos01'

ks_stats = []
ks_pval  = []

import csv

csvfile = open('outputFileName.csv', 'wb')
writer = csv.writer(csvfile)

for i in range(34, 83, 1):
    thr = float(i) / 100
    thr = format(thr, '.2f')
    
    name_orig = 'acp_w_thr_' + thr + '.dat'
    file_orig = os.path.join(dir_adj, name_orig)
    orig      = distance_masking(d_matrix, file_orig)
    flat_orig = np.ndarray.flatten(orig)
    his_orig, bin_orig = np.histogram(flat_orig, bins=100, normed=True)
    
    name_rand = 'acp_w_thr_' + thr + '_erdos.dat'
    file_rand = os.path.join(dir_erdos, name_rand)
    rand = distance_masking(d_matrix, file_rand)
    flat_rand = np.ndarray.flatten(rand)
    his_rand, bin_rand = np.histogram(flat_rand, bins=100, normed=True)
    
    diff, p = stats.ks_2samp(his_orig, his_rand)
    #print orig.mean() - rand.mean()
    #print thr, diff, p
    #writer.writerow([thr, diff, p])
    ks_stats.append(diff)
    ks_pval.append(p)

thr_array = np.arange(0.34, 0.83, 0.01)

ks_pval  = np.array(ks_pval)
ks_stats = np.array(ks_stats)

sig     = ks_stats[np.where(ks_pval < 0.01)]
sig_thr = thr_array[np.where(ks_pval < 0.01)]

fig, ax = plt.subplots(figsize=(15,12))
plt.subplots_adjust(left=0.14, right=0.95, top=0.93, bottom=0.12)
plt.subplot(1,1,1)
plt.plot(thr_array, ks_stats, 'o', markersize=15)
plt.plot(sig_thr, sig, 'or', markersize=15)
plt.xticks(thr_array[4:46:12], fontsize = 35)
plt.yticks(fontsize = 35)
plt.tick_params( length=10, width=4)
plt.xlabel('p', fontsize = 35)
plt.ylabel('KS distance', fontsize = 35)
plt.xlim(thr_array.min()-0.01, thr_array.max()+0.01)
plt.ylim(0, 0.4)
#plt.show()
