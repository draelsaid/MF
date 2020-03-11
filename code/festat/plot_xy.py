#!/usr/bin/python
# Adam El-Said 2019
# Plotting sigmab values from festat experiment
# Run this INSIDE experiment folder

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

import os
import glob

fname=sorted(list(glob.glob(os.path.join('.','*.tot'))))

# If you want to print certain parts of list matching a pattern
matching = [s for s in fname if "stdavv" in s]

for fl in fname:

 with open(fl) as f:
    data = f.read()

 data = data.split('\n')
 data.remove('')

 x = [row.split(',')[0] for row in data]
 y = [row.split(' ')[1] for row in data]
 if len(x)!=72:
  print "There may be missing data in: %s" % (fl)
 xh=np.arange(0,len(x)*6,6)/24.

 fig = plt.figure(figsize=(20,10))

 ax1 = fig.add_subplot(111)

 ax1.set_title(fl)    
 ax1.set_xlabel('Days')
 ax1.set_ylabel(fl[7:-11])

 ax1.plot(xh, y, c='r', label='Summer')
 ax1.plot(xh, y, c='b', label='Winter')
 #leg = ax1.legend()

 chainetitre='sigmab_aearoyann'
 nom_fig = fl + chainetitre + '.png'
 plt.savefig(nom_fig)
