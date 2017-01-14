#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

""" 
	input  : empirical matrix (e.g. fMRI-BOLD data), simulation outcome
	matrix (FHN or BOLD simulations)
	
	intermediate process : loading empirical and simulation matrices, 
	plotting color coded empirical mtx., calculating Pearson's correlat.
	coefficient between empirical and simulated matrices, parameter
	analysis plots for the Pearson coefficients over velocity-threshold 
	or sigma-threshold changing parameter regions 

	output : R_pearson, figures
"""
import numpy as np
from math import factorial 
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt	
from matplotlib import colors
from matplotlib.pyplot import FormatStrFormatter


# check the loaded matrix if it is symmetric
def load_matrix(file):
	A  = np.loadtxt(file, unpack=True)
	AT = np.transpose(A)
	# check the symmetry				
	if A.shape[0] != A.shape[1] or not (A == AT).all():
		print "error: loaded matrix is not symmetric"
		raise ValueError
	return AT
	
# plotting color coded empirical (structural) probability map
def plot_corr(corr_matrix):	
	N_col  = np.shape(corr_matrix)[1]
	extend = (0.5 , N_col+0.5 , N_col+0.5, 0.5 )

	fig , ax = plt.subplots(figsize=(15, 12))
	ax.tick_params('both', length=15, width=8, which='major')
	plt.subplots_adjust(left=0.10, right=0.95, top=0.93, bottom=0.12)	

	# vmin & vmax manually defined for the probability map
	plt.imshow(corr_matrix, interpolation='nearest', vmin=0.0, vmax=1.0, extent=extend)
	
	cbar = plt.colorbar()
	cbar.ax.set_title('p', fontsize = 50, y=1.02)
	for t in cbar.ax.get_yticklabels():
		t.set_fontsize(50)
	plt.xticks(fontsize = 50)
	plt.yticks(fontsize = 50)
	plt.xlabel('Nodes', fontsize = 50)
	plt.ylabel('Nodes', fontsize = 50)
	return fig 	

file_in = '/home/sheyma/devel/tmp/data/acp_w.txt'
empir_mtx = load_matrix(file_in)
figure   = plot_corr(empir_mtx)
figure.savefig('/home/sheyma/devel/tmp/figures/structural_map.png')
plt.show()
