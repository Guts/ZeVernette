# -*- coding: UTF-8 -*-
#!/usr/bin/env python

##from Tkinter import Tk
##from tkFileDialog import askdirectory
import os
import sys
import glob
import hashlib
from xlwt import Workbook, easyxf, Font, XFStyle, Formula  # écriture excel 2003
from expexcel import *


#### Fonctions

def compfichiers(nfc1, nfc2, lgbuf=32*1024):
    u""" Compare les 2 fichiers et renvoie True seulement s'ils ont un \
    contenu identique """
    f1 = f2 = None
    result = False
    try:
        if os.path.getsize(nfc1) == os.path.getsize(nfc2):
            f1 = open(nfc1, "rb")
            f2 = open(nfc2, "rb")
            while True:
                buf1 = f1.read(lgbuf)
                if len(buf1) == 0:
                    result = True
                    break
                buf2 = f2.read(lgbuf)
                if buf1 != buf2:
                    break
            f1.close()
            f2.close()
    except:
        if f1 != None: f1.close()
        if f2 != None: f2.close()
        raise IOError
    return result

def md5_fichier(fichier, block_size=2**20):
    u""" Calcule la signature numérique md5 d'un fichier """
    md5 = hashlib.md5() # instance md5
    # boucle de test de calculs pour éviter les erreurs
    with open(fichier, 'r') as fd:
        try:
            while True:
                data = fd.read(block_size)
                if not data:
                    break
                md5.update(data)
        except Exception, why:
            print u"Erreur dans le fichier {0}. Raison : {1}".format(f, why)
            return None

    return md5.hexdigest()

def listrepertoire(path, extension='*'):
    u""" liste les fichiers de l'extension spécifiée
    d'un répertoire et sous-répertoires """
    fichiers = []   # liste des tuples de fichiers
    dossiers = []   # liste des tuples de dossiers
    l = glob.glob(os.path.join(path, '*'))  # liste des dossiers et fichiers
    for i in l:
        if os.path.isdir(i):
            u""" si c'est un dossier... """
##            dossiers += 1   # incrémente le compteur des dossiers...
            # calcule la taille totale des fichiers contenus dans le dossier
            dossize_ = sum([os.path.getsize(f) for f in os.listdir('.') if os.path.isfile(f)])
            dossiers.append((os.path.basename(i), i, dossize_))
            # et ajoute à la liste les fichiers selon l'extension donnée
            l.extend(glob.glob(os.path.join(i, extension)))
        else:
            u""" si c'est un fichier... """
            name_ = os.path.basename(i)     # nom
            size_ = os.path.getsize(i)      # taille
            cdate_ = os.path.getctime(i)    # date de création
            mdate_ = os.path.getmtime(i)    # date de dernière modification
            hash_ =  md5_fichier(i)         # calcule son md5
            if hash_ is not None:           # si le calcul du md5 réussit ...
                # ... => ajoute fichier et métadonnées à liste globale
                fichiers.append((name_, i, size_, cdate_, mdate_, hash_))
    # Information des éléments traités
    print u"Vérification de {0} fichiers dans {1} dossiers".format(len(fichiers),
                                                                   len(dossiers))
    return fichiers, dossiers

def control_arg():
    if len(sys.argv) != 2 :
        print u"Argument ou paramètre manquant ou incorrect"
        sys.exit ()
    if not (os.path.isdir(sys.argv[1])):
        print sys.argv[1], u" n'est pas un dossier."
        sys.exit ()




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

chemin = os.getcwd() + r'/test_doublons'

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

