#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------------------------
# 

import matplotlib.pyplot as plt
import numpy as np
import os
import datetime




# EXptrace.py
#----

exp = ['6C5T', '6C5H']
nbfc= ['100','100','25','100','100']
param = ['q','t', 'd']
listlabel = ['6C5T','6C5H']
couleur = ["b--","k--","g","r"]

listlev= [10,68,80,85]
decal = [0,0,0,2,0]
chainetitre='evolvarxpl_1003_lev54'
pas_de_temps = 45

plt.figure(figsize=(20,10))

datedeb = datetime.datetime(2015,10,02,00)
incr = datetime.timedelta(seconds=10800)

NMAXRES=144
NMAXRES=144
nres=0

# Parcour des exp
#-----------------

for lev in listlev: 
   datedeb = datetime.datetime(2015,10,02,00)
   plt.figure(figsize=(20,10))
   chainetitre='evol_varexpl_1003_lev' + str(lev)
   for p in range(0,len(param)):
	laboite= p+1
	valeur_max=0
	valeur_min=100
	for i in range(0,len(exp)):
                print("traitement de l'exp : " + exp[i])
		temps = range(0, NMAXRES+1)
		norme = range(0, NMAXRES+1)
		nres=0
		mydate=datedeb
		while nres <= NMAXRES:
			yyyy='{:0>4}'.format(mydate.year)
			mm='{:0>2}'.format(mydate.month)
			dd='{:0>2}'.format(mydate.day)
			hh='{:0>2}'.format(mydate.hour)
			DATE=''.join([yyyy,mm,dd,hh])
			print("traitement de la date : " + DATE + " numero : " + str(nres) )
		        nom_fic = ("/home/broussea/ASSIM/jbens/JB_" + exp[i] + "_" + DATE + hh + "_" + nbfc[i] + "/expl" + param[p] + "lev.y" )
		        with open(nom_fic, 'r') as f:
				tab = f.readlines()
                        tab = [t[:-1] for t in tab]
                       	temps[nres] = nres - decal[i]
			norme[nres] = float(tab[lev].split()[1].strip())
		#	print("debug : ")
		#	print(norme[70])
			nres=nres+1
			mydate=mydate + incr

                valeur_max = max (valeur_max, max(norme))
         	valeur_min = min (valeur_min, min(norme))
		# tracés fenetre de gauche
		#-------------------------- 
		# Couleurs possibles: b g r c m y k w
		# blue, green, red, cyan, magenta, magenta, black, white
		plt.subplot(2,2,laboite)
		plt.plot(temps,norme, couleur[i],linestyle='-',linewidth=2.0, label= listlabel[i] )
		print("fenetre de gauche tracée !")
		print(exp[i]+" debut traité !")

	plt.suptitle(chainetitre) # pas d'accents!

# Fenetre de gauche
	plt.subplot(2,2,laboite)
	plt.title("stdav" + param[p] )
	plt.ylabel('')
	plt.ylim(valeur_min,valeur_max)
	plt.xlabel('reseaux')
# Joli axe des ordonnées
	plt.legend()

# Sauvegarde 
#-----------------
   nom_fig = './DATA/evolution_' + chainetitre + '.png'
   print("titre trouvé : " + nom_fig +'\n')
   plt.savefig(nom_fig)
   print("Figure sauvée !\n" )
   plt.close()

#os.system("killall totem")
print('\n')
print("Merci de votre visite, et à bientôt dans votre intermarché le plus proche !\n")
