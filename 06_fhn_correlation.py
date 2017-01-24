import numpy as np
import sys, math 
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as pl
import scipy.stats as sistat
from utils import load_simfile, get_data_basename

params = { # Fitzhugh-Nagumo simulation parameters...
        'dt': 0.001, 
			}

# obtain u_i time series from loaded matrix
def fhn_timeseries(simfile):
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

# Pearson's correlation coefficients among the columns of a given matrix
def pearson_corr(matrix , out_basename):
	print "obtaining Pearson correlation coefficients among time series..."
	# numpy array must be transposed to get the right corrcoef
	tr_matrix = np.transpose(matrix)
	cr_matrix = np.corrcoef(tr_matrix)
	file_name = str(out_basename + '_FHN_corr.dat')
	np.savetxt(file_name, cr_matrix, '%.6f',delimiter='\t')
	return cr_matrix

# Spearman correlation coefficients among the columns of a given matrix
def spearma_corr(matrix , out_basename):
	print "obtaining Spearman correlation coefficients among time series..."
	from scipy.stats import spearmanr
	# numpy array must be transposed to get the right corrcoef
	tr_matrix = np.transpose(matrix)
	results   = spearmanr(matrix)
	cr_matrix = results.correlation
	
	file_name = str(out_basename + '_FHN_spearm.dat')
	np.savetxt(file_name, cr_matrix, '%.6f',delimiter='\t')
	return cr_matrix


data_dir = '/home/sheyma/devel/fitzefatze/data/jobs_adj/'
file_in  =  data_dir + 'acp_w_thr_0.98_sigma=0.05_D=0.05_v=30.0_tmax=45000.dat'

print file_in

data_matrix   = load_simfile(file_in)
out_basename  = get_data_basename(file_in)

[u_matrix , T, dt, tvec] =	fhn_timeseries(data_matrix)
#pearson_matrix           =   pearson_corr(u_matrix, out_basename)
#spearma_matrix           =   spearma_corr(u_matrix, out_basename)

#print pearson_matrix.shape  
#print spearma_matrix.shape

from sklearn.covariance import GraphLassoCV
estimator = GraphLassoCV()

A = estimator.fit(u_matrix)

from matplotlib import pyplot as plt

# Display the covariance
plt.figure(figsize=(10, 10))

# The covariance can be found at estimator.covariance_
plt.imshow(estimator.covariance_, interpolation="nearest",
           vmax=1, vmin=-1, cmap=plt.cm.RdBu_r)
#thr_array = np.arange(34, 86, 4)
#sig_array = np.array([0.050, 0.045, 0.040, 0.035, 0.030, 0.025, 0.020,  0.015, 0.010, 0.005 ])

#DIR_FHN = '/run/media/sheyma/0a5437d3-d51c-4c40-8c7a-06738fd0c83a/sheyma_bayrak_2015/jobs/'
#name_fhn  = 'acp_w_0_ADJ_thr_0.54_sigma=0.3_D=0.05_v=30.0_tmax=45000.dat.xz'

#for THR in thr_array :
#    for SIG in sig_array :
#        input_A = name_fhn[0:18] + str(THR) + name_fhn[20:27] + str(SIG) + name_fhn[30:]
#        out_basename  = 'data/spearman/' + input_A[:-7]
#        input_A = DIR_FHN + input_A
#        data_matrix   = load_simfile(input_A)
        
#        # calculate correlation with two different methods
#        spearma_matrix = spearma_corr(data_matrix, out_basename)
#        pearson_matrix = pearson_corr(data_matrix, out_basename)
        
