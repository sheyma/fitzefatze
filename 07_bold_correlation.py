import numpy as np
import sys
from utils import load_simfile, get_data_basename

def corr_matrix(matrix, out_basename):
	print "obtaining correlation coefficients among BOLD time series..."
	# numpy array must be transposed to get the right corrcoef
	tr_matrix = np.transpose(matrix)
	cr_matrix = np.corrcoef(tr_matrix)
	file_name = str(out_basename + '_corr.dat')
	np.savetxt(file_name, cr_matrix, '%.6f',delimiter='\t')
	return cr_matrix

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print "%s: no input files given" % sys.argv[0]
        print "usage: %s FILE_NAMES..." % sys.argv[0]


    for file_in in sys.argv[1:]:
        data_matrix = load_simfile(file_in)
        out_prfx    = get_data_basename(file_in)

        corr_mtx    = corr_matrix(data_matrix, out_prfx)
        print corr_mtx.shape
