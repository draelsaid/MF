#!/usr/bin/python
# Adam El-Said 2019
# Plotting sigmab values from festat experiment
# Run this INSIDE experiment folder

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

import os
import glob

exp1 = sorted(list(glob.glob(os.path.join('.','*6C6F*'))))
exp2 = sorted(list(glob.glob(os.path.join('.','*6C5H*'))))
var_list=['Divergence', 'Kinetic energy', 'Specific humidity', 'Temperature', 'Vorticity', 'Surface Pressure']

with open("6BXF_stdav.tot") as r:
 datat=r.read()
datat=datat.split('\n')
datat.remove('')

with open("6BYB_stdav.tot") as rr:
 datat2=rr.read()
datat2=datat2.split('\n')
datat2.remove('')

# If you want to print certain parts of list matching a pattern
#matching = [s for s in fname if std in s]

for l in xrange(len(exp1)):

 with open(exp1[l]) as f:
    data = f.read()
 data = data.split('\n')
 data.remove('')

 with open(exp2[l]) as ff:
    data2 = ff.read()
 data2 = data2.split('\n')
 data2.remove('')

 x = [row.split(',')[0] for row in data]
 y = [row.split(' ')[1] for row in data]
 y2 = [row.split(' ')[1] for row in data2]

 if len(x)!=72:
  print "There may be missing data in: %s" % (exp1[l])
 xh=np.arange(0,len(x)*6,6)/24.

 fig = plt.figure(figsize=(20,10))

 ax1 = fig.add_subplot(111)

 ax1.set_title(exp1[l][7:-11])    
 ax1.set_xlabel('Days', fontsize=20)
 ax1.set_ylabel(r'$\sigma_{b}$ of ' + exp1[l][12:-11], fontsize=20)
 ax1.tick_params(labelsize=18)
 
 if datat[l][:6]==exp1[l][7:13] and datat2[l][:6]==exp1[l][7:13]:
  ind1 = datat[l].replace("\t","\\", 2).replace("\\", "\t",1).find("\\")
  ind2 = datat2[l].replace("\t","\\", 2).replace("\\", "\t",1).find("\\")
  yt = float(datat[l][ind1+1:])
  yt2 = float(datat2[l][ind2+1:])

  ax1.plot(xh, y, c='r', label='Summer \'17 3d avg', lw=3)
  ax1.plot(xh, y2, c='b', label='Winter \'18 3d avg', lw=3)
 
 ax1.axhline(y=yt, c='r', ls='dashed', label='Summer 17 20d avg (lvl100)', lw=3)
 ax1.axhline(y=yt2, c='b', ls='dashed', label='Winter 17 20d avg (lvl100)', lw=3)

 # Shrink current axis's height by 10% on the bottom
 box = ax1.get_position()
 ax1.set_position([box.x0, box.y0 + box.height * 0.1,box.width, box.height * 0.9]) 

 # Put a legend below current axis
 leg = ax1.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25), fancybox=True, shadow=True, ncol=2, fontsize=20)
 #leg = ax1.legend(loc='upper left',fontsize=20)

 nom_fig = exp1[l][7:13] + '_sigb.png'
 plt.savefig('results/'+nom_fig)

