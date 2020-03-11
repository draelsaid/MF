#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------------------------
# 

import matplotlib.pyplot as plt
from matplotlib import rc
import numpy 
import os
import datetime
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)



# EXptrace.py
#----

exp = ['68NQ_20130716','B482_WMED','6BRZ_PRECISE_AD']
nbfc= ['96','180','120']
listlabel = ['AROME-FR','WMED','PRECISE']
nbxplev =[90,60,106]
param = ['q','t', 'v', 'd' ]
listtitle =['Specific humidity','Temperature','Vorticity','Vorticity']
listxlabel =  [r"g.kg$^{-1}$",r"K",r"10$^{-4}$.s$^{-1}$",r"10$^{-4}$.s$^{-1}$"]
listxmax =[1.5,2.0,4.5,5.5]
rednmc = [1000,1,10000,10000]
couleur = ["k--","b-","g--","r"]
lev=52
chainetitre='sigmab_pre_moy'

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


plt.figure(figsize=(11,11))

datedeb = datetime.datetime(2015,10,20,00)
incr = datetime.timedelta(seconds=10800)

NMAXRES=0
nres=0

# Parcour des paramètres
#-----------------
for p in range(0,len(param)):
	laboite= p+1
	valeur_max=0
	valeur_min=100
    
        #parcour des xp
	#---------------
	for i in range(0,len(exp)):
                print("traitement de l'exp : " + exp[i])
		temps = range(0, NMAXRES+1)
		norme = range(0, NMAXRES+1)
		nres=0
		mydate=datedeb
                
                nom_fic = "pressure_lev" + str(nbxplev[i]) + ".txt"
                # niveau_P contient les niveaux de P en fonction du niveau 90 = sol
                with open(nom_fic, 'r') as f:
	            niveau_P = f.readlines()
                niveau_P = [t[:-1] for t in niveau_P]

		#parcour des dates
		#-----------------
		while nres <= NMAXRES:
			yyyy='{:0>4}'.format(mydate.year)
			mm='{:0>2}'.format(mydate.month)
			dd='{:0>2}'.format(mydate.day)
			hh='{:0>2}'.format(mydate.hour)
			DATE=''.join([yyyy,mm,dd,hh])
			print("traitement de la date : " + DATE)
		        
			#lecture
			nom_fic = ("/home/broussea/ASSIM/jbens/JB_" + exp[i] + "_" + nbfc[i] + "/stdav" + param[p] + ".y" )
			with open(nom_fic, 'r') as f:
				tab = f.readlines()
                        #on enleve le caractère \n
			tab = [t[:-1] for t in tab]
                        #on garde les 90 dernières lignes
			tab = tab[-nbxplev[i]:]
			#on garde la deuxième colone
			profil = [float(t.split()[1].strip())*rednmc[p] for t in tab]
		
			#incrementation	
			nres=nres+1
			mydate=mydate + incr
			valeur_max = max (valeur_max, max(profil))
         		valeur_min = min (valeur_min, min(profil))
		
		
			# tracés 
			plt.subplot(2,2,laboite)
			plt.plot(profil,niveau_P,couleur[i],linewidth=2.0, label= listlabel[i]) # pas d'accents!
	plt.subplot(2,2,laboite)
	plt.title(listtitle[p])
	plt.ylabel(r"pressure (hPa)")
        ax = plt.gca()
	plt.xlim(0,listxmax[p])
	plt.xlabel(listxlabel[p])
        if p==3 :
	   plt.legend()
        plt.ylim(0,1030)
	ax.invert_yaxis()
# Sauvegarde 
#-----------------
nom_fig = './multiprof_' + chainetitre + '.eps'
print("titre trouvé : " + nom_fig +'\n')
plt.savefig(nom_fig,bbox_inches='tight',format='eps')
print("Figure sauvée !\n" )
plt.close()



#os.system("killall totem")
print('\n')
print("Merci de votre visite, et à bientôt dans votre intermarché le plus proche !\n")
