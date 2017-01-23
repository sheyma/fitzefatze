import numpy as np
import sys, math
import scipy.stats as sta
from scipy.signal import  butter , filtfilt , correlate2d
from utils import load_simfile, get_data_basename

class Params(object):
	__slots__ = ['taus', 'tauf', 'tauo', 'alpha', 'dt', 'Eo', 'vo', 'k1', 'k2', 'k3']

def invert_params(params):
	params.taus = float(1/params.taus)
	params.tauf = float(1/params.tauf)
	params.tauo = float(1/params.tauo)
	params.alpha = float(1/params.alpha)
	return params

def bold_euler(T, r, iparams, x_init):
	# Baloon-Windkessel model with Euler's method
	# T : total simulation time [s]
	# r : neural time series to be simulated
	
	dt  = iparams.dt
	
	t = np.array(np.arange(0,(T+iparams.dt),iparams.dt))
	n_t = len(t)
	# cut BOLD signal from beginning bcs of transient behavior
	t_min = 20		# [s] CHECK FOR THE SIGNAL 

	n_min = round(t_min / iparams.dt)   
	r_max = np.amax(r)	
	x = np.zeros((n_t,4))
	
	x[0,:] = x_init
	
	for n in range(0,n_t-1):
		x[n+1 , 0] = x[n ,0] + dt * (r[n] - iparams.taus * x[n,0] - iparams.tauf * (x[n,1] -float(1.0)))
		x[n+1 , 1] = x[n, 1] + dt * x[n,0]
		x[n+1 , 2] = x[n, 2] + dt * iparams.tauo * (x[n, 1] - pow(x[n, 2] , iparams.alpha))
		x[n+1 , 3] = x[n, 3] + dt * iparams.tauo * ( x[n, 1] * (1.-pow((1- iparams.Eo),(1./x[n,1])))/iparams.Eo - pow(x[n,2],iparams.alpha) * x[n,3] / x[n,2])
	# discard first n_min points	
	t_new = t[n_min -1 :]
	s     = x[n_min -1 : , 0]
	fi    = x[n_min -1 : , 1]
	v     = x[n_min -1 : , 2]
	q     = x[n_min -1 : , 3]
	b= 100/iparams.Eo * iparams.vo * ( iparams.k1 * (1-q) + iparams.k2 * (1-q/v) + iparams.k3 * (1-v) )
			
	return b

def fhn_timeseries(simfile):
	# load simfile as numpy matrix
	# extract first column of simout as time vector
	# read u_i time series from simout
	
	simout = load_simfile(simfile)
	# extract time vector and dt
	tvec = simout[:,0]
	dt   = tvec[1] - tvec[0]
	T    = int(math.ceil( (tvec[-1])  / dt * params.dt ))

	# extract u-columns
	u_indices = np.arange(1, simout.shape[1] ,1)
	timeseries = simout[:, u_indices]
	return timeseries, T
		
# standart normalization of timeseries (MATLAB's zscore)			
def normalize_timeseries(timeseries):
	N_timeseries = sta.mstats.zscore(timeseries)
	return N_timeseries
			
def calc_bold(timeseries , T, out_basename):
	# applies Balloon Windkessel model to the timeseries
	# calculates the simulated bold signal
	# counts the number of NaN 's in simulated bold (error-check)

	N = np.shape(timeseries)[1] 	# total number of u columns		
	
	print "Bold-signalling of u-timeseries starts..."
	# type(Bold_signal) = <type 'dict'>
	Bold_signal = {}				
	for col in range(0, N):
		Bold_signal[col] = bold_euler(T, timeseries[:,[col]], iparams, x_init)
		#Bold_signal[col] = bold_ode(T, timeseries[:,[col]], iparams, x_init)
		count_nan = 0				
		for key,value in enumerate(Bold_signal[col]):
			if value == float('nan'):
				count_nan += 1
		if count_nan > 0:
			print "u_N, nu. of NaNs:", Bold_signal[key][col], count_nan
	# exporting BOLD signal 
	file_name = str(out_basename + '_NORM_BOLD_signal.dat')
	#file_name = str(out_basename + '_BOLD_signal.dat')
	print file_name
	f = open(file_name,'w')	
	for row in range( 0, len(Bold_signal[0]) ):
		for key in Bold_signal.iterkeys():
			f.write('%.6f\t' % ( Bold_signal[key][row] ))
		f.write('\n')
	f.close()
	return Bold_signal

		
def filter_bold(bold_input, out_basename):
	# Butterworth low pass filtering of the simulated bold signal		
	# type(bold_input) = <type 'dict'>
	# f_c : cut-off freq., f_s : sampling freq., f_n : Nyquist freq.
	# Or : order of filter, dtt : resolution of bold signal
	
	print "low pass filtering is applied..." 
	 
	n_T = len(np.array(bold_input[1]))
	N   = len(bold_input.keys())
	Or  = 5
	dtt = 0.001							# [second]	
	f_c = 0.25					 		# [Hz]	
	f_s = 1/dtt							# [Hz]
	f_n = f_s /2						# [Hz]
	
	# calculate butterworth coefficients with Python's butter function
	#b , a = butter(Or,float(f_c)/f_n, btype='low',analog=False, output='ba')
	
	# import butterworth coefficients from MATLAB results
	b   = np.loadtxt('data/Bs_matlab.dat')
	a   = np.loadtxt('data/As_matlab.dat')

	Bold_filt = np.zeros((n_T , N))
	for col in range(0,N):			
		Bold_filt[: , col] = filtfilt(b, a, bold_input[col])
			
	file_name = str(out_basename + '_BOLD_filtered.dat')
	print "file_name : " , file_name
	np.savetxt(file_name, Bold_filt,'%.6f',delimiter='\t')
	return Bold_filt


# here we go

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print "%s: no input files given" % sys.argv[0]
        print "usage: %s FILE_NAMES..." % sys.argv[0]

    params = Params()
    params.taus = 0.65
    params.tauf = 0.41
    params.tauo = 0.98
    params.alpha  = 0.32
    params.dt = 0.001
    params.Eo = 0.34
    params.vo = 0.02;
    params.k1 = 7.0 * params.Eo
    params.k2 = 2.0
    params.k3 = 2.0 * params.Eo - 0.2

    iparams = invert_params(params)
    # initial conditions for the bold differential equations
    x_init = np.array([0 , 1, 1, 1])

    for file_in in sys.argv[1:]:
        out_basename    = get_data_basename(file_in)
        [timeseries, T] = fhn_timeseries(file_in)
        print timeseries.shape

        N_timeseries  = normalize_timeseries(timeseries)

        N_bold_signal = calc_bold(N_timeseries, T, out_basename)

        N_bold_filt   = filter_bold(N_bold_signal, out_basename)
