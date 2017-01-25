import numpy as np
import sys
from utils import load_simfile, get_data_basename


# Pearson's correlation coefficients among the columns of a given matrix
def pearson_corr(matrix , file_out):
	print "obtaining Pearson correlation coefficients among time series..."
	# numpy array must be transposed to get the right corrcoef
	tr_matrix = np.transpose(matrix)
	cr_matrix = np.corrcoef(tr_matrix)
	np.savetxt(file_out, cr_matrix, '%.6f',delimiter='\t')
	return cr_matrix

# Spearman correlation coefficients among the columns of a given matrix
def spearma_corr(matrix , file_out):
	print "obtaining Spearman correlation coefficients among time series..."
	from scipy.stats import spearmanr
	# numpy array must be transposed to get the right corrcoef
	tr_matrix = np.transpose(matrix)
	results   = spearmanr(matrix)
	cr_matrix = results.correlation
	np.savetxt(file_out, cr_matrix, '%.6f',delimiter='\t')
	return cr_matrix


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print "%s: no input files given" % sys.argv[0]
        print "usage: %s FILE_NAMES..." % sys.argv[0]

    for file_in in sys.argv[1:]:
        print "load file", file_in

	# skip first time column!
        data_matrix   = load_simfile(file_in)[:,1:]

        ## calculate correlation with two different methods
        basename = get_data_basename(file_in)
        pearson_matrix = pearson_corr(data_matrix, basename + "_pearson.dat")
        spearma_matrix = spearma_corr(data_matrix, basename + "_spearm.dat")
