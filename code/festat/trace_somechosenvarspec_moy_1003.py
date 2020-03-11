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

exp = ['6B4L', '6B1G','6B33'] #, '6ANA']
listlabel = ['MOY38','MOY13','MOY13_ni_ns']
listlocleg =[1,1,2,2,2]
nbfc= ['96','96','96'] #,'100','100']
param = ['q','t', 'v', 'd' ]
couleur = ["r--","k--","g--","r"]
couleur = ["b","k","g","m"]
typedeligne = ["-","--",":"]
lev=65
chainetitre='varspec_lev65_1003_moy'

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


datedeb = datetime.datetime(2015,10,02,00)
incr = datetime.timedelta(seconds=10800)

NMAXRES=12
nres=0

listedate=['201510200000']

# Parcour des paramètres
#-----------------
for lev in [49,57,65,73,81,90]:
  plt.figure(figsize=(20,10))
  
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
                lenght=2160
		#parcour des dates
		#-----------------
		#while nres <= NMAXRES:
                for dat in range(0,len(listedate)):
                        
			#yyyy='{:0>4}'.format(mydate.year)
			#mm='{:0>2}'.format(mydate.month)
			#dd='{:0>2}'.format(mydate.day)
			#hh='{:0>2}'.format(mydate.hour)
			#DATE=''.join([yyyy,mm,dd,hh])
                        DATE=listedate[dat]

			print("traitement de la date : " + DATE)
		        
			#lecture
			nom_fic = ("/home/broussea/ASSIM/jbens/JB_" + exp[i] + "_" + DATE + "_" + nbfc[i] + "/varsp" + param[p] + str(lev) + ".y" )
			with open(nom_fic, 'r') as f:
				tab = f.readlines()
                        #on enleve le caractère \n
			tab = [t[:-1] for t in tab]
			#on garde la deuxième colone
			spectre = [float(t.split()[1].strip()) for t in tab]
		        lenghtscale = [float(lenght/(float(t.split()[0].strip()) + 1)) for t in tab]

					
			#incrementation	
			nres=nres+1
			mydate=mydate + incr
			valeur_max = max (valeur_max, max(spectre))
         		valeur_min = min (valeur_min, min(spectre))
		
		
			# tracés 
			plt.subplot(2,2,laboite)
			plt.loglog(lenghtscale,spectre,couleur[i],linestyle=typedeligne[dat],linewidth=2.0, label= listlabel[i])

		

        #lecture clim 
#        nom_fic = ("/home/broussea/ASSIM/jbens/JB_68NQ_20130716_96/stdav" + param[p] + ".y" )
#	with open(nom_fic, 'r') as f:
#		tab = f.readlines()
#	
#        tab = [t[:-1] for t in tab]
#	tab = tab[-90:]
#	profil = [float(t.split()[1].strip()) for t in tab]
#
#	# tracés
#	valeur_max = max (valeur_max, max(profil))
#        valeur_min = min (valeur_min, min(profil))
#	plt.subplot(2,2,laboite)
#	plt.plot(profil,niveau_P,label= 'clim',linewidth=2.0  )

       #lecture clim hiv 
	nom_fic = ("/home/broussea/ASSIM/jbens/JB_68NQ_20130716_96/varsp" + param[p] + str(lev) + ".y" )
	lenght=2160
	with open(nom_fic, 'r') as f:
		tab = f.readlines()
	
        tab = [t[:-1] for t in tab]
	spectre = [float(t.split()[1].strip()) for t in tab]
	lenghtscale = [float(lenght/(float(t.split()[0].strip()) + 1)) for t in tab]

	# tracés
	valeur_max = max (valeur_max, max(spectre))
        valeur_min = min (valeur_min, min(spectre))
	plt.subplot(2,2,laboite)
	plt.loglog(lenghtscale,spectre,label= 'OPER13',linewidth=2.0,color='r',linestyle='--'  )
 

        #option de tracé 
	plt.suptitle(chainetitre) # pas d'accents!
	plt.subplot(2,2,laboite)
	plt.title(param[p])
	plt.ylabel('')
        ax = plt.gca()
        #plt.ylim(0.000004,0.2)
	#plt.xlim(0,2500)
	plt.xlabel('lenghtscale')
	plt.legend(loc=listlocleg[p])
        #plt.ylim(valeur_min,valeur_max)
	ax.invert_xaxis()


# Sauvegarde 
#-----------------
  nom_fig = './DATA/moyenne_' + str(lev) + '_' + chainetitre + '.png'
  print("titre trouvé : " + nom_fig +'\n')
  plt.savefig(nom_fig)
  print("Figure sauvée !\n" )
  plt.close()



#os.system("killall totem")
print('\n')
print("Merci de votre visite, et à bientôt dans votre intermarché le plus proche !\n")
