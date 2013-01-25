# -*- coding: UTF-8 -*-
#!/usr/bin/env python

##from Tkinter import Tk
##from tkFileDialog import askdirectory
import sys
from checkdobles import *
from xlwt import Workbook, easyxf, Font, XFStyle, Formula  # écriture excel 2003
from expexcel import *

##### Programme principal #######


# répertoire cible
##cibler = Tk()
##cibler.withdraw()
##chemin = askdirectory(initialdir = sys.argv[0],
##                      mustexist = True)         # explorateur windows
##
##if chemin == "":          # si aucun dossier n'est choisi, le programme s'arrête
##    cibler.destroy()
##    exit()

chemin = r'D:\A_Ordenar\Julien\python\Zevernette\test_doublons'

# Extension
extension = '*'

# Liste les dossiers et taille cumulée
dossiers = listrepertoire(chemin, extension)[1]
dossiers.sort() # ordonne la liste

# Liste les fichiers et métadonnées
fichiers = listrepertoire(chemin, extension)[0]
fichiers.sort() # ordonne la liste

# Extrait les numéros de hash md5
hashs = [h[5] for h in fichiers]
hashs.sort()    # ordonne la liste des numéros de hash

# Crée une liste de hashs unique
unikhashs = set(hashs)  # supprime les doublons de la liste des hashs

# Compare la longueur des deux listes précédentes
if len(unikhashs) == len(hashs):
    u""" si elles sont égales alors c'est qu'il n'y a aucun doublon """
    print u"Aucun doublon dans le dossier {0}".format(sys.argv[1])
    sys.exit () # => au revoir !

# si différentes, on crée une liste des doublons
doublons = []
for idx, elt in enumerate(hashs):
    u""" boucle sur la liste des hashs indexée numériquement (enumerate) """
    try:
        # on compare les hashs des fichiers un par un
        if elt == hashs[idx + 1]:
            # si les deux hashs sont égaux, on ajoute les fichiers à liste
            doublons.append((fichiers[idx][1], fichiers[idx + 1][1]))
    except:
        # fin de la liste
        pass

# si la liste des doublons contient quelque-chose, on publie la liste paire par paire
if len(doublons):
    print u"Ces fichiers sont identiques:",
    for d in doublons:
        print "\n  {0}\n  {1}".format(d[0], d[1])
else:
    print u"Aucun doublon dans le dossier {0}".format(sys.argv[1])
    sys.exit ()


####### Export en onglets Excel

wb = Workbook(encoding='utf8')

DoblExcel(wb, fichiers[idx][0], doublons)

# sauvegarde de la fiche excel
wb.save("bubbles.xls")

####### Import des librairies #######
##
##from tkFileDialog import askdirectory as doss_cible
##from os import walk, path
##
####### Définition fonctions #######
##
##def ubiquite(dossier):
##    u"""Liste les shapes contenus dans un répertoire et
##    ses sous-répertoires"""
##    global liste_shapes
##    for root, dirs, files in walk(chemin_dossier):
##        for i in files:
##            if path.splitext(path.join(root, i))[1] == u'.shp' and \
##            path.isfile(path.join(root, i)[:-4] + u'.dbf') and \
##            path.isfile(path.join(root, i)[:-4] + u'.shx') and \
##            path.isfile(path.join(root, i)[:-4] + u'.prj'):
##                liste_shapes.append(path.join(root, i))
##    return liste_shapes
##
##
####### Variables #######
##
##
##




