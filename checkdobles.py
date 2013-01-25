#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import glob
import hashlib

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



####### lancement autonome

if __name__ == '__main__':
    control_arg()
    liste = listrepertoire(sys.argv[1])
    liste.sort()
    hashs = [h[0] for h in liste]
    s = set(hashs)

    if len(s) == len(hashs):
        print u"Aucun doublon dans le dossier {0}".format(sys.argv[1])
        sys.exit ()

    doublons = []
    for idx, elt in enumerate(hashs):
        try:
            if elt == hashs[idx + 1]:
                doublons.append((liste[idx][1], liste[idx + 1][1]))
        except:
            # end of list
            pass

    if len(doublons):
        print u"Ces fichiers sont identiques:",
        for d in doublons:
            print "\n  {0}\n  {1}".format(d[0], d[1])
    else:
        print u"Aucun doublon dans le dossier {0}".format(sys.argv[1])
        sys.exit ()