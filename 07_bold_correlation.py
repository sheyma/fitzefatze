import numpy as np
import sys, math 
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as pl
import subprocess as sp
import scipy.stats as sistat
from utils import load_simfile, get_data_basename

def corr_matrix(matrix, out_basename):
	print "obtaining correlation coefficients among BOLD time series..."
	# numpy array must be transposed to get the right corrcoef
	tr_matrix = np.transpose(matrix)
	cr_matrix = np.corrcoef(tr_matrix)
	file_name = str(out_basename + '_corr.dat')
	#np.savetxt(file_name, cr_matrix, '%.6f',delimiter='\t')
	return cr_matrix

data_dir = '/home/sheyma/devel/fitzefatze/data/jobs_adj/'
file_in  = data_dir + 'acp_w_thr_0.98_sigma=0.05_D=0.05_v=30.0_tmax=45000_NORM_BOLD_signal.dat'

data_matrix = load_simfile(file_in)
out_prfx    = get_data_basename(file_in)

corr_mtx    = corr_matrix(data_matrix, out_prfx)
print corr_mtx.shape
