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
labelxp = ['6C5T','6C5H']
nbfc= ['100','100','25','100','100','96']
#param = ['q','t', 'v', 'ke' ]
param = ['q','t','v','ke'] 
couleur = ["b","k","g","b--","r","k--"]
couleurmoy = ["b--","k--","g","b--","r","k--"]

listlev= [35,50,63,75,85,90]
decal = [0,0,0,0,0,0]
#listlevhpa = ["
chainetitre='sigmab_aearoyann'
lplotmoy=True
lplotclim=False
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

datedeb = datetime.datetime(2015,10,02,00)
incr = datetime.timedelta(seconds=10800)
NMAXRES=195
nres=0

# Parcour des exp
#-----------------

for lev in listlev: 
   datedeb = datetime.datetime(2017,8,13,00)
   
   
   chainetitre='evol_sigmab_aearoyann_lev' + str(lev)
   for p in range(0,len(param)):
        chainetitre='evol_sigmab_aearoyann_' + param[p] + '_lev_' + str(lev)

        fig=plt.figure(figsize=(20,20))
        ax = fig.gca()
 
	laboite= p+1
	valeur_max=0
	valeur_min=100
	for i in range(0,len(exp)):
                print("traitement de l'exp : " + exp[i])
		temps = range(0, NMAXRES+1)
		norme = range(0, NMAXRES+1)
                valmoy = range(0, NMAXRES+1)
		nres=0
		mydate=datedeb
		while nres <= NMAXRES:
			yyyy='{:0>4}'.format(mydate.year)
			mm='{:0>2}'.format(mydate.month)
			dd='{:0>2}'.format(mydate.day)
			hh='{:0>2}'.format(mydate.hour)
			DATE=''.join([yyyy,mm,dd,hh])
			print("traitement de la date : " + DATE + " numero : " + str(nres) )
		        nom_fic = ("/home/elsaida/Bdiag/stdav_with_time/hendrix/xp" + "/" + exp[i] + "/" + DATE + "H" + hh + "P" + "/stat/listing/" + param[p] + ".y" )
		        with open(nom_fic, 'r') as f:
				tab = f.readlines()
                        tab = [t[:-1] for t in tab]
                        #print(tab)
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
		plt.plot(temps,norme, couleur[i], linewidth=2.0, label= labelxp[i] )
                if lplotmoy==True :
                    avgval= float(sum(norme))/len(norme)
                    nres=0
                    while nres <= NMAXRES:
                        valmoy[nres]=avgval
                        nres=nres+1
  
                    plt.plot(temps,valmoy, couleurmoy[i], linewidth=2.0, label= 'moy ' + labelxp[i])  
                

		print("fenetre de gauche tracée !")
		print(exp[i]+" debut traité !")
                
        if lplotclim==True :
              norme=[] 
              nom_fic = ("/home/broussea/ASSIM/jbens/JB_68NQ_20130716_96/stdav" + param[p] + ".y" )
	      with open(nom_fic, 'r') as f:
	          tab = f.readlines()
                  
              tab = [t[:-1] for t in tab]

              #print(tab)
              for nres in temps :
                  norme.append(float(tab[lev].split()[1].strip()))
              plt.plot(temps,norme, 'r--', linewidth=2.0,label='OPER13' )             
        plt.suptitle(chainetitre) # pas d'accents!
	plt.title("stdav" + param[p] )
	plt.ylabel('')
	plt.ylim(valeur_min,valeur_max)
        plt.xlim(0,200)
        #ax.set_xticks(np.arange(0,144,8))
        plt.xticks(np.arange(0,200,8),np.arange(0,25,1))
        plt.grid()
	plt.xlabel('jours')
# Joli axe des ordonnées
#plt.xticks([0,1,2,3])
	plt.legend()
        nom_fig = './DATADEF/evolution_' + chainetitre + '.png'
        print("titre trouvé : " + nom_fig +'\n')
        plt.savefig(nom_fig)
        print("Figure sauvée !\n" )
        plt.close()



#os.system("killall totem")
print('\n')
print("Merci de votre visite, et à bientôt dans votre intermarché le plus proche !\n")
