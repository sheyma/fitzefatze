import numpy as np
import sys, math 
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as pl
import scipy.stats as sistat
from utils import load_simfile, get_data_basename
from utils import get_timeseries

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
def pearson_corr(matrix):
	print "obtaining correlation coefficients among time series..."
	# numpy array must be transposed to get the right corrcoef
	tr_matrix = np.transpose(matrix)
	cr_matrix = np.corrcoef(tr_matrix)
	return cr_matrix

a=[]
b=[]
def node_index(matrix):
	# ignore diagonal elements by assigning it to 0
	for i in range(0,np.shape(matrix)[0]):
		for j in range(0,np.shape(matrix)[1]):

			if matrix[i,j] >= 0.3 and matrix[i,j] < 0.90 and i<45 and j<45:
				nx = i
				ny = j
				print "cool correlations: ", i+1, j+1
				a.append(nx)
				b.append(ny)
			if i == j:
				matrix[i,j] = 0
				
	# nodes start from 1, not from 0, therefore not forget to add 1 to the index
	# assign diagonal elements back to 1 
	for i in range(0,np.shape(matrix)[0]):
		for j in range(0,np.shape(matrix)[1]):
			if i == j :
				matrix[i,j] = 1.0

	return nx, ny 

def plot_timeseries(t_start , t_final, dt, timeseries, tvec, x, y):
	
	# corresponding index of t_start and t_final in tvec
	i_s =  (t_start /dt)
	i_f =  (t_final /dt)
	
	# extracting the timeseries of the given nodes as separate vectors
	v1   = timeseries[:, x]
	v2   = timeseries[:, y]
	
	# Pearson correlation value between two timeseries
	[R_pearson , p_value] = sistat.pearsonr(v1 , v2)
	
	# plot the timeseries of two nodes in specific interval
	# tvec multiplied by 0.01 to make dimensiion equal to [ms]
	fig , ax = pl.subplots(figsize=(22, 5))
	pl.subplots_adjust(left=0.08, right=0.98, top=0.94, bottom=0.20)

	pl.plot(0.01*tvec[i_s:i_f], v1[i_s : i_f], linestyle='-',
         color='m', linewidth=2.5, label=('$u_{' + str(x+1) + '}(t)$'))
	pl.plot(0.01*tvec[i_s:i_f], v2[i_s : i_f], linestyle='-',
         color='g',linewidth=2.5, label=('$u_{' + str(y+1) + '}(t)$'))
    
	pl.setp(pl.gca().get_xticklabels(), fontsize = 25)
	pl.setp(pl.gca().get_yticklabels(), fontsize = 25)
	pl.locator_params(nbins=4)
	pl.legend(frameon=True, prop={'size':35})

	pl.xlabel('t [s]', fontsize=30)
	pl.ylabel('$u_{' + str(x+1) + '}(t)$ , ' + ' $u_{' + str(y+1) + '}(t)$' 
              ,fontsize=40)
	return	R_pearson, fig

data_dir = '/run/media/sheyma/0a5437d3-d51c-4c40-8c7a-06738fd0c83a/sheyma_bayrak_2015/jobs/'
file_in  =  data_dir + 'acp_w_0_ADJ_thr_0.54_sigma=0.03_D=0.05_v=30.0_tmax=45000.dat.xz'

data_matrix   = load_simfile(file_in)
out_basename  = get_data_basename(file_in)

[u_matrix , T, dt, tvec] =	get_timeseries(data_matrix)
corr_matrix  =   pearson_corr(u_matrix)

t_start = 1200
t_final = 1800

#[i, j ]      =   node_index(corr_matrix)
#plot_timeseries(t_start, t_final, dt, u_matrix, tvec, i, j)

# or plot manually
#R_pearson, fig = plot_timeseries(t_start, t_final, dt, u_matrix, tvec, 35, 36)
R_pearson, fig = plot_timeseries(t_start, t_final, dt, u_matrix, tvec, 57, 58)
print 'FHN: ', R_pearson
#pl.show()


data_dir = '/run/media/sheyma/0a5437d3-d51c-4c40-8c7a-06738fd0c83a/sheyma_bayrak_2015/jobs_bold/'
file_in  = data_dir + 'acp_w_0_ADJ_thr_0.54_sigma=0.03_D=0.05_v=30.0_tmax=45000_NORM_BOLD_signal.dat.xz'

data_matrix   = load_simfile(file_in)
# the best: x=57, y= 59, p=0.54, c=30
x=57
y=58
[R_pearson , p_value] = sistat.pearsonr(data_matrix[:,x] , data_matrix[:,y])
print data_matrix[:,x].shape, data_matrix[:,y].shape
print "BOLD", R_pearson 

fig , ax = pl.subplots(figsize=(22, 5))
# go from milisecond to minute
t_points = data_matrix.shape[0]
timing = np.arange(0, t_points,1) / float(60 * 1000)
pl.subplots_adjust(left=0.08, right=0.98, top=0.94, bottom=0.20)
pl.plot(timing, data_matrix[:,x], linestyle='-',color='m',
        linewidth=2.5, label=('$u_{' + str(x+1) + '}(t)$')); 
pl.plot(timing, data_matrix[:,y],linestyle='-',color='g',
        linewidth=2.5, label=('$u_{' + str(y+1) + '}(t)$')); 
pl.setp(pl.gca().get_xticklabels(), fontsize = 25)
pl.setp(pl.gca().get_yticklabels(), fontsize = 25)	
pl.setp(pl.gca().get_xticklabels(), fontsize = 25)
pl.setp(pl.gca().get_yticklabels(), fontsize = 25)
pl.locator_params(nbins=4)
pl.legend(frameon=True, prop={'size':35})
pl.ylim(-0.3, 0.3)
pl.xlabel('t [min]', fontsize=30)
pl.ylabel('$u_{' + str(x+1) + '}(t)$ , ' + ' $u_{' + str(y+1) + '}(t)$' ,fontsize=40)
pl.show()


