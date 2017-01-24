import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as pl	

# check the loaded matrix if it is symmetric
def load_matrix(file):
	A  = np.loadtxt(file, unpack=True)
	AT = np.transpose(A)
	# check the symmetry				
	if A.shape[0] != A.shape[1] or not (A == AT).all():
		print "error: loaded matrix is not symmetric"
		raise ValueError
	return AT

def plot_histog(corr_matrix, STRING):
	corr_flat = np.ndarray.flatten(corr_matrix) 
	corr_max  = float(1.0)
	corr_min  = float(-1.0)
	bin_nu    = 250
	# a normalized histogram is obtained
	pl.hist(corr_flat, bins=bin_nu, range=[corr_min, corr_max], 
            normed =True, histtype='bar', align='mid')
	pl.xlabel('$\\rho$', fontsize=25)
	pl.xlim(-0.3, 0.3)
	pl.ylim(0, 6.6)
	pl.xticks(fontsize=20)
	pl.yticks(fontsize=20)

	pl.text(0.2, 5, STRING,
				horizontalalignment='right',
				verticalalignment='center', fontsize=23)

	#pl.xlabel('$\\rho$', fontsize=25)



# Single Histogram Plot
#local_path    = '/home/sheyma/HD/sheyma_bayrak_2015/jobs_corr/'
#O = load_matrix(local_path + 'acp_w_0_ADJ_thr_0.54_sigma=0.03_D=0.05_v=30.0_tmax=45000_FHN_corr.dat')
#A = load_matrix(local_path + 'acp_w_a_ADJ_thr_0.54_sigma=0.03_D=0.05_v=30.0_tmax=45000_FHN_corr.dat')

local_path = '/home/sheyma/HD/sheyma_bayrak_2015/jobs_corr_bold/'
O = load_matrix(local_path + 'acp_w_0_ADJ_thr_0.54_sigma=0.01_D=0.05_v=30.0_tmax=45000_NORM_BOLD_signal_corr.dat')
A = load_matrix(local_path + 'acp_w_a_ADJ_thr_0.54_sigma=0.01_D=0.05_v=30.0_tmax=45000_NORM_BOLD_signal_corr.dat')


fig, ax = pl.subplots(nrows=1, ncols=2, sharex=True, 
                    sharey=True, figsize=(18, 6))
fig.text(0.04, 0.5, 'distribution of $\\rho$', va='center', 
         rotation='vertical', fontsize=22)


pl.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)

pl.subplot(1,2,1)
ax = fig.add_subplot(121)
ax.tick_params(axis='both', which='major', direction='in', length=4, width=3)
plot_histog(O, '$R_{BG}$')

pl.subplot(1,2,2)
ax = fig.add_subplot(122)
ax.tick_params(axis='both', which='major', direction='in', length=4, width=3)
plot_histog(A, '$R_{ER}$')


pl.show()

