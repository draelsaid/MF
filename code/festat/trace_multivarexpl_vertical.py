#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------------------------
# 

import matplotlib.pyplot as plt
import numpy 
import os
import datetime
from scipy import *

# EXptrace.py
#----
'exp1'
path = "/home/elsaida/hendrix/xp/"
exp = ['6BZW', '6BXF']
loc2 = ["/20170701H00", "/20170701H00"]
lbl = ['6BZW Jul-17 ENS SU 6H', '6BXF Jul-17 ENS DA 6H']

'exp2'
#path = "/home/elsaida/hendrix/xp/"
#exp = ['6BYL', '6BXF', '6BYM', '6BZW']
#loc2= ["/20170701H00", "/20170701H00", "/20180101H00", "/20170701H00"]
#lbl = ['6BYL Jul-17 ENS DA 3H', '6BXF Jul-17 ENS DA 6H', '6BYM Jul-17 ENS SU 3H', '6BZW Jul-17 ENS SU 6H']

'exp3'
#path = "/home/elsaida/hendrix/xp/"
#exp = ['6BYB', '6BZJ']
#loc2= ["/20180101H00", "/20180101H00"]
#lbl = ['6BYB Jan-18 ENS DA 6H', '6BYM Jan-18 ENS DA 3H']

'exp4'
#path = "/home/elsaida/hendrix/xp/"
#exp = ['6BXF', '6BY8', '6BYB']
#loc2= ["/20170701H00", "/20170701H00", "/20180101H00"]
#lbl = ['6BXF Jul-17 ENS DA 6H', '6BY8 Jul-17 ENS DA 6H (90`s obs)', '6BYB Jan-18 ENS DA 6H']

plt_ltr = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)', '(g)', '(h)', '(i)', '(j)']
lev = '106'
nbxplev =[int(lev)]*len(exp)
listlabel =['Total', 'Pb', 'Divergence\_u', '(T,Ps)\_u']
couleur = ["r", "c--", "y--", "b--"]

chainetitre='Background forecast errors \n explained by other variables (ratios)'

plt.figure(figsize=(25,25))

# Parcour des exp
#-----------------
valeur_max=0
valeur_min=100
nb_exp=len(exp)       

laboite=0

for i in range(0,len(exp)):
        print("traitement de l'exp : " + exp[i])
        nom_fic = "pressure_lev" + str(nbxplev[i]) + ".txt"
        # niveau_P contient les niveaux de P en fonction du niveau 90 = sol
        with open(nom_fic, 'r') as f:
		niveau_P = f.readlines()
	niveau_P = [t[:-1] for t in niveau_P]	                       

        # Traitement de la température
        print("traitement de la température\n")
        nom_fic = (path + exp[i] + loc2[i] + "A/stat/explt_lev.y" )
	with open(nom_fic, 'r') as f:
		tab = f.readlines()
        tab = [t[:-1] for t in tab]
        k=1
        ratio_total=zeros(nbxplev[i])
        ratio_Pb=zeros(nbxplev[i])
        ratio_divu=zeros(nbxplev[i])
        for j in range(0,nbxplev[i]):
                k=k+1
    		ratio_total[j] = float(tab[k].split()[1].strip())
                ratio_Pb[j] = float(tab[k].split()[2].strip())
                k=k+1
                ratio_divu[j] = float(tab[k].split()[0].strip())
  
	valeur_max = max (valeur_max, max(ratio_total))
        valeur_min = min (valeur_min, min(ratio_Pb),min(ratio_divu))
        
        laboite=laboite+1
	plt.subplot(nb_exp,2,laboite)
	plt.plot(ratio_total,niveau_P,couleur[0],linestyle='-',linewidth=2.0, label= listlabel[0])
        plt.plot(ratio_Pb,niveau_P,couleur[1],linestyle='--',linewidth=2.0, label= listlabel[1])
        plt.plot(ratio_divu,niveau_P,couleur[2],linestyle='--',linewidth=2.0, label= listlabel[2])
        valeur_max = max (valeur_max, max(ratio_total))
        valeur_min = min (valeur_min, min(ratio_Pb),min(ratio_divu))
        plt.suptitle(chainetitre, fontsize=25) 
        plt.ylabel('Pressure (hPa)', fontsize=25)
	plt.tick_params(axis='both', labelsize=25)
        plt.xlabel('Ratio', fontsize=25)
        plt.title(plt_ltr[laboite-1] + '\n Temperature '+lbl[i], fontsize=25)
        # ylim(ymin, ymax)
        ax = plt.gca()
        plt.xlim(valeur_min,valeur_max)

        plt.ylim(0,1030)
	plt.xlim(0,0.7)
	ax.invert_yaxis()
        			                        
         # Traitement de l'humidité spécifique
        print("traitement de l'humidité spécifique\n")
        nom_fic = (path + exp[i] + loc2[i] + "A/stat/explq_lev.y" )
	with open(nom_fic, 'r') as f:
		    tab = f.readlines()
        tab = [t[:-1] for t in tab]
        k=1
        ratio_total=zeros(nbxplev[i])
        ratio_Pb=zeros(nbxplev[i])
        ratio_divu=zeros(nbxplev[i])
        ratio_TPsu=zeros(nbxplev[i])
        for j in range(0,nbxplev[i]):
                k=k+1
                ratio_total[j] = float(tab[k].split()[1].strip())
                ratio_Pb[j] = float(tab[k].split()[2].strip())
                k=k+1
                ratio_divu[j] = float(tab[k].split()[0].strip())
                ratio_TPsu[j] = float(tab[k].split()[1].strip())

	valeur_max = max (valeur_max, max(ratio_total))
        valeur_min = min (valeur_min, min(ratio_Pb),min(ratio_divu),min(ratio_TPsu))
        laboite=laboite+1
	plt.subplot(nb_exp,2,laboite)
 	plt.plot(ratio_total,niveau_P,couleur[0],linestyle='-',linewidth=2.0, label= listlabel[0])
        plt.plot(ratio_Pb,niveau_P,couleur[1],linestyle='--',linewidth=2.0, label= listlabel[1])
        plt.plot(ratio_divu,niveau_P,couleur[2],linestyle='--',linewidth=2.0, label= listlabel[2])
        plt.plot(ratio_TPsu,niveau_P,couleur[3],linestyle='--',linewidth=2.0, label= listlabel[3])
        valeur_max = max (valeur_max, max(ratio_total))
        valeur_min = min (valeur_min, min(ratio_Pb),min(ratio_divu),min(ratio_TPsu))
        plt.suptitle(chainetitre, fontsize=25) 
        plt.ylabel('Pressure (hPa)', fontsize=25)
        plt.xlabel('Ratio', fontsize=25)
	plt.tick_params(axis='both', labelsize=25)
        plt.title(plt_ltr[laboite-1] + '\n Specific Humidity ' + lbl[i], fontsize=25)
        # ylim(ymin, ymax)
        ax = plt.gca()
        plt.xlim(valeur_min,valeur_max)
        plt.ylim(0,1030)
	plt.xlim(0,0.7)
	ax.invert_yaxis()

# Sauvegarde 
#-----------------
plt.legend(loc="lower center", bbox_to_anchor=(-0.2,-0.2), fontsize=30, ncol=4)
plt.tight_layout(pad=10, w_pad=5, h_pad=5)
nom_fig = 'varxpl_verscale.png'
print(nom_fig)
plt.savefig(nom_fig)
plt.close()

#os.system("killall totem")
print('\n')
print("Merci de votre visite, et à bientôt dans votre intermarché le plus proche !\n")
