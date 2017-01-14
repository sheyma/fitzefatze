# python 01_adjacency.py data/acp_w.txt  data/jobs_adj/ 

import sys, os
import networkx as nx
import numpy as np 

def get_threshold_matrix(filename, threshold_value):
   
    A = np.transpose(np.loadtxt(filename, unpack=True))

    B = np.zeros((len(A),len(A)))

    for row in range(len(A)):
        for item in range(len(A)):
            #if row != item:
            if A[row,item] >= threshold_value:
                B[row,item] = 1
            else:
                B[row,item] = 0
    G=nx.from_numpy_matrix(B,create_using=nx.DiGraph())

    return G


def print_adjacency_matrix(G):
    print nx.adjacency_matrix(G)


def export_adjacency_matrix(G, filename, outdir, threshold_value):

    hiwi = nx.adjacency_matrix(G)
    threshold_value = format(threshold_value, '.2f')
    bname = os.path.basename(filename)[:-4]
   
    f = open(outdir + '/' + bname +'_thr_'+str(threshold_value)+'.dat','w')
    for i in range(len(hiwi)):
        for j in range(len(hiwi)):
            f.write("%d\t" % (hiwi[i,j]))
        f.write("\n")
    f.close()


if __name__ == '__main__':

    usage = 'Usage: %s correlation_matrix threshold' % sys.argv[0]
    try:
        infilename_data = sys.argv[1]
        if len(sys.argv) > 2 :
            outdir = sys.argv[2]
        else :
            outdir = "."
    except:
        print usage; sys.exit(1)

    for i in range(0, 101):
        thr = float(i) / 100
        print "loop", i, thr
        network = get_threshold_matrix(infilename_data, thr)
        #print_adjacency_matrix(network)
        export_adjacency_matrix(network, infilename_data, outdir, thr)
