import sys, os
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np




direc = '/home/sheyma/HD/sheyma_bayrak_2015/jobs_adj'
#file_orig = os.path.join(direc, 'acp_w_R0_single_network_measures.dat')
#file_rand = os.path.join(direc, 'acp_w_Ra_single_network_measures.dat')

#file_orig = '/home/sheyma/devel/tmp/data/jobs_network/acp_w_single_network_measures.dat'
#file_rand = '/home/sheyma/devel/tmp/data/jobs_network/acp_w_erdos_single_network_measures.dat'

#G_orig = np.loadtxt(file_orig, unpack=True).T
#G_rand = np.loadtxt(file_rand, unpack=True).T

#file_orig_sw = os.path.join(direc, 'acp_w_R0_small_worldness.dat')

file_orig_sw = '/home/sheyma/devel/fitzefatze/data/jobs_adj/small_worldness.dat'
sw           = np.loadtxt(file_orig_sw, unpack=True).T


file_orig = '/home/sheyma/devel/fitzefatze/data/jobs_adj/single_network_measures.dat'
G_orig    = np.loadtxt(file_orig, unpack=True).T

# number of num_realization at each threshold

density_rand = []
cluster_rand = []

num_realization = 100
for i in range(0, num_realization):
    
    file_rand = 'data/jobs_erdos' + format(i, '02d') + '/single_network_measures.dat'
    data_rand = np.loadtxt(file_rand, unpack=True).T
    #print file_rand
    # sum network densities (each at 3rd column)
    
    density_rand.append(data_rand[:,2])
    cluster_rand.append(data_rand[:,3])

density_rand = np.array(density_rand)
density_rand_mean = density_rand.mean(axis=0)
density_rand_std  = density_rand.std(axis=0)

cluster_rand = np.array(cluster_rand)
cluster_rand_mean = cluster_rand.mean(axis=0)
cluster_rand_std  = cluster_rand.std(axis=0)

print cluster_rand_std

thr_steps = 101

# just a safety check
sw_values = []
if num_realization * thr_steps != sw.shape[0]:
    print "error:", num_realization * thr_steps, "!=", sw.shape[0]
    sys.exit(-1)
    
for i in range(0, num_realization):
    a = i * thr_steps
    b = a + thr_steps
    
    #print sw[a:b,0]
    sw_values.append(sw[a:b,7])
    #if i == 0:
    #    sw_sum = sw[a:b,7]
    #else:
    #    sw_sum += sw[a:b,7]
    
    
    #print sw[0:101,0]
    #print sw[101:202, 0]
    #print sw[202:303, 0]

#sw_ave = sw_sum / num_realization
sw_values = np.array(sw_values)
sw_values_mean = sw_values.mean(axis=0)
sw_values_std  = sw_values.std(axis=0)

#density_rand = density_rand / float(num_realization)
#cluster_rand = cluster_rand / float(num_realization)

############### plotting #############################################

first_threshold  = 0.34
second_threshold = 0.82

# network density ####################################################
fig, ax  = plt.subplots(figsize=(22, 6))
plt.subplots_adjust(left=0.06, right=0.99, top=0.93, bottom=0.18)
ax = plt.subplot(131)
plt.plot(G_orig[:,0], G_orig[:,2], 'k', linewidth=3, label='R$_{BG}$')
plt.errorbar(data_rand[:,0], density_rand_mean, yerr=density_rand_std,
             fmt='or', linewidth=2, markersize=8, label='R$_{ER}$')
plt.ylim(0, 1.02)

plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0],
           ['0', '0.2', '0.4', '0.6', '0.8', '1'], fontsize = 30)
plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0],
           ['0', '0.2', '0.4', '0.6', '0.8', '1'], fontsize = 30)

plt.xlabel('p', fontsize = 30)
plt.ylabel('$\kappa$', fontsize = 45)
plt.legend(frameon=False, fontsize = 30)

# plot lines
thr_ax = first_threshold
thr_ay = density_rand_mean[np.where(data_rand[:,0]==thr_ax)]
thr_bx = second_threshold
thr_by = density_rand_mean[np.where(data_rand[:,0]==thr_bx)]
thr_cx = first_threshold
thr_cy = G_orig[:,2][np.where(G_orig[:,0]==thr_cx)]
thr_dx = second_threshold
thr_dy = G_orig[:,2][np.where(G_orig[:,0]==thr_dx)]

points = [(thr_ax, thr_ay), (thr_bx, thr_by),
          (thr_cx, thr_cy), (thr_dx, thr_dy)] # (a1,b1), (a2,b2), ...

for pt in points:
    # plot (x,y) pairs.
    # vertical line: 2 x,y pairs: (a,0) and (a,b)
    plt.plot( [pt[0],pt[0]], [0,pt[1]], 'g', linewidth=2.5)
    plt.plot( [0,pt[0]], [pt[1],pt[1]], 'g', linewidth=2.5)
    print pt[0],pt[0],0,pt[1]

plt.legend(frameon=False, fontsize = 30, numpoints=1)


# clustering coefficient #############################################
plt.subplot(132)

plt.plot(G_orig[:,0], G_orig[:,3], 'k' , linewidth=3, label='R$_{BG}$')
plt.errorbar(data_rand[:,0], cluster_rand_mean, yerr=cluster_rand_std,
             fmt='or', linewidth=2, markersize=8, label='R$_{ER}$')
plt.ylim(0, 1.02)

plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0],
           ['0', '0.2', '0.4', '0.6', '0.8', '1'], fontsize = 30)
plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0],
           ['0', '0.2', '0.4', '0.6', '0.8', '1'], fontsize = 30)

plt.xlabel('p', fontsize = 30)
plt.ylabel('C', fontsize = 30)


# plot lines
thr_ax = first_threshold
thr_ay = cluster_rand_mean[np.where(data_rand[:,0]==thr_ax)]
thr_bx = second_threshold
thr_by = cluster_rand_mean[np.where(data_rand[:,0]==thr_bx)]
thr_cx = first_threshold
thr_cy = G_orig[:,3][np.where(G_orig[:,0]==thr_cx)]
thr_dx = second_threshold
thr_dy = G_orig[:,3][np.where(G_orig[:,0]==thr_dx)]

points = [(thr_ax, thr_ay), (thr_bx, thr_by),
          (thr_cx, thr_cy), (thr_dx, thr_dy)] # (a1,b1), (a2,b2), ...

for pt in points:
    # plot (x,y) pairs.
    # vertical line: 2 x,y pairs: (a,0) and (a,b)
    plt.plot( [pt[0],pt[0]], [0,pt[1]], 'g', linewidth=2.5)
    plt.plot( [0,pt[0]], [pt[1],pt[1]], 'g', linewidth=2.5)
    print pt[0],pt[0],0,pt[1]

plt.legend(frameon=False, fontsize = 30, numpoints=1)


# small-Worldness (a relative measure) ##################################
plt.subplot(133)
plt.errorbar(sw[0:83, 0], sw_values_mean[0:83], yerr=sw_values_std[0:83],
             fmt='ok', linewidth=2, markersize=8, label='R$_{BG}$')

plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0],
           ['0', '0.2', '0.4', '0.6', '0.8', '1'], fontsize = 30)
plt.yticks(fontsize = 30)

plt.xlabel('p', fontsize = 30)
plt.ylabel('S', fontsize = 30)
plt.xlim(0, 1.0)

# plot lines
thr_ax = first_threshold
thr_ay = sw_values_mean[0:83][np.where(sw[0:83, 0]==thr_ax)]
thr_bx = second_threshold
thr_by = sw_values_mean[0:83][np.where(sw[0:83, 0]==thr_bx)]


points = [(thr_ax, thr_ay), (thr_bx, thr_by)] # (a1,b1), (a2,b2), ...

for pt in points:
    # plot (x,y) pairs.
    # vertical line: 2 x,y pairs: (a,0) and (a,b)
    plt.plot( [pt[0],pt[0]], [0,pt[1]], 'g', linewidth=2.5)
    plt.plot( [0,pt[0]], [pt[1],pt[1]], 'g', linewidth=2.5)
    print pt[0],pt[0],0,pt[1]

plt.legend(frameon=False,  loc='best', fontsize = 28,  numpoints=1 )

plt.show()

