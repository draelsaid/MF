#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------------------------
# 

import matplotlib.pyplot as plt
import numpy 
import os
import datetime




# EXptrace.py
#----

exp = ['B482_WMED'] #, '6ANA']
nbfc= ['180','96','100']
nbxplev =[60,60,90]

param = ['q','t', 'd']
listlabel = ['MOY38','MOY13']
couleur = ["b--","k--","g","r"]

lev=21
chainetitre='varexpl_moy_clim'

# Choix de la date
#-------------------

#mois = raw_input("Nous vous laissons le choix dans la date : SEP, OCT, NOV \n ")
#mois = 'SEP'

#if mois == 'SEP':
#	periode = ['0916H03','0920H00']
#if mois == 'OCT':
#	periode = ['1006H03','1013H00']
#if mois == 'NOV':
#	periode = ['1124H03','1130H00']
# periode = [date debut periode , date fin periode]


# Création d'un tableau contenant le temps
#-----------------------------------------
# Il y a toujours 241 pas de temps
# données toute les 45 sec.
pas_de_temps = 45


#temps = range(0, (241*pas_de_temps), pas_de_temps)
	
# convertie en tableau de float (divisions possibles)
#map(float, temps)	
# Tout en heure
#temps = [x/3600. for x in temps]



# Correspondance pression / niveau
#------------------------------------
nom_fic = "pressure_lev90.txt"
# niveau_P contient les niveaux de P en fonction du niveau 90 = sol
with open(nom_fic, 'r') as f:
	niveau_P = f.readlines()
niveau_P = [t[:-1] for t in niveau_P]
# niveau_P[1] = 13hpa
tous_les_niveaux = range(1,90,1)
# restriction de niveau_P à tous_les_niveaux 
#niveau_P = niveau_P[ [k-1 for k in tous_les_niveaux],1]
# on ne garde que la col (2°) contenant les
#niveau_P = niveau_P[...,1]


plt.figure(figsize=(20,20))

datedeb = datetime.datetime(2015,10,20,00)
incr = datetime.timedelta(seconds=10800)

NMAXRES=0
nres=0

# Parcour des exp
#-----------------
for p in range(0,len(param)):
	laboite= p+1
	valeur_max=0
	valeur_min=100
       


	for i in range(0,len(exp)):
                print("traitement de l'exp : " + exp[i])
		monstyle=couleur[i]
		temps = range(0, NMAXRES+1)
		norme = range(0, NMAXRES+1)
		nres=0
		mydate=datedeb
         	nom_fic = "pressure_lev" + str(nbxplev[i]) + ".txt"
                # niveau_P contient les niveaux de P en fonction du niveau 90 = sol
                with open(nom_fic, 'r') as f:
	            niveau_P = f.readlines()
                niveau_P = [t[:-1] for t in niveau_P]

		while nres <= NMAXRES:
			yyyy='{:0>4}'.format(mydate.year)
			mm='{:0>2}'.format(mydate.month)
			dd='{:0>2}'.format(mydate.day)
			hh='{:0>2}'.format(mydate.hour)
			DATE=''.join([yyyy,mm,dd,hh])
			print("traitement de la date : " + DATE)
		        nom_fic = ("/home/broussea/Jbens/JB_" + exp[i] + "_" + DATE + hh + "_" + nbfc[i] + "/expl" + param[p] + "lev.y" )
		        with open(nom_fic, 'r') as f:
				tab = f.readlines()
                        tab = [t[:-1] for t in tab]
                      #  tab = tab[-90:]
			profil = [float(t.split()[1].strip()) for t in tab]
		#	print("debug : ")
		#	print(norme[70])
			nres=nres+1
			mydate=mydate + incr
			valeur_max = max (valeur_max, max(profil))
         		valeur_min = min (valeur_min, min(profil))
		# tracés fenetre de gauche
		#-------------------------- 
		# Couleurs possibles: b g r c m y k w
		# blue, green, red, cyan, magenta, magenta, black, white
			plt.subplot(2,2,laboite)
			plt.plot(profil,niveau_P,couleur[i],linestyle='-',linewidth=2.0, label= listlabel[i])

		

               
	valeur_max = max (valeur_max, max(profil))
        valeur_min = min (valeur_min, min(profil))
	plt.subplot(2,2,laboite)
#	plt.plot(profil,niveau_P,label= 'clim hiv',linewidth=2.0  )






	plt.suptitle(chainetitre) # pas d'accents!

# Fenetre de gauche
	plt.subplot(2,2,laboite)
	plt.title(param[p] )
#ex : periode[0] = 0916H03
	plt.ylabel('')
# ylim(ymin, ymax)
        ax = plt.gca()
	plt.xlim(valeur_min,valeur_max)
	plt.xlabel('ratio')
# Joli axe des ordonnées
#plt.xticks([0,1,2,3])
	plt.legend()
        plt.ylim(0,1030)
	ax.invert_yaxis()


# Sauvegarde 
#-----------------
nom_fig = './multiprof_' + chainetitre + '.png'
print("titre trouvé : " + nom_fig +'\n')
plt.savefig(nom_fig)
print("Figure sauvée !\n" )
plt.close()



#os.system("killall totem")
print('\n')
print("Merci de votre visite, et à bientôt dans votre intermarché le plus proche !\n")
