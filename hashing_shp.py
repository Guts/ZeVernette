# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import unicode_literals
#-------------------------------------------------------------------------------
# Name:         Hashing Shapefiles
# Purpose:      Calculate a numeric signature on a shapefiles (.shp + .dbf + .prj)
#
# Author:       Julien Moura (https://github.com/Guts/)
#
# Python:       2.7.x
# Created:      19/12/2012
# Updated:      20/02/2013
#
# Licence:      GPL 3
#-------------------------------------------------------------------------------

################################################################################
########### Libraries #############
###################################
# Standard library
import hashlib
from multiprocessing import Process, Queue, TimeoutError
from os import path, walk
import sys

################################################################################
########### Functions #############
###################################

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
            print(u"Erreur dans le fichier {0}. Raison : {1}".format(f, why))
            return None
    # end of function
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
    print(u"Vérification de {0} fichiers dans {1} dossiers".format(len(fichiers), len(dossiers)))
    return fichiers, dossiers


def li_geofiles(foldertarget=".", shps_list=[], tabs_list=[], gdirs_list=[]):
    u""" List shapefiles and MapInfo files (.tab, not .mid/mif) contained
    in the folders structure """
    # reseting global variables
    num_folders = 0
    # Looping in folders structure
    for root, dirs, files in walk(unicode(foldertarget)):
        num_folders = num_folders + len(dirs)
        for f in files:
            try:
                unicode(path.join(root, f))
                full_path = path.join(root, f)
            except UnicodeDecodeError, e:
                full_path = path.join(root, f.decode('latin1'))
                print unicode(full_path), e
            # Looping on files contained
            if path.splitext(full_path.lower())[1].lower() == '.shp' and \
    (path.isfile('%s.dbf' % full_path[:-4]) or path.isfile('%s.DBF' % full_path[:-4])) and \
    (path.isfile('%s.shx' % full_path[:-4]) or path.isfile('%s.SHX' % full_path[:-4])) and \
    (path.isfile('%s.prj' % full_path[:-4]) or path.isfile('%s.PRJ' % full_path[:-4])):
                # add complete path of shapefile
                shps_list.append(full_path)
                # add complete path of folder
                gdirs_list.append(path.dirname(path.abspath(full_path)))
            elif path.splitext(full_path.lower())[1] == '.tab' and \
    (path.isfile(full_path[:-4] + '.dat') or path.isfile(full_path[:-4] + '.DAT')) and \
    (path.isfile(full_path[:-4] + '.map') or path.isfile(full_path[:-4] + '.MAP')) and \
    (path.isfile(full_path[:-4] + '.id') or path.isfile(full_path[:-4] + '.ID')):
                # add complete path of MapInfo file
                tabs_list.append(full_path)
                # add complete path of folder
                gdirs_list.append(path.dirname(path.abspath(full_path)))
            else:
                pass

    # End of function
    return foldertarget, shps_list, tabs_list, gdirs_list


def sign_shp(shapefile, block_size=2**20):
    u""" Calcule la signature numérique md5 d'un fichier """
    # local variables
    shps_files = (shapefile, shapefile[:-4] + '.dbf', shapefile[:-4] + '.prj')
    shps_signs = []
    # instance de hashing en 256 bits
    sha_glob = hashlib.sha256()
    # updating with the filename
    sha_glob.update(path.splitext(path.basename(shapefile))[0])
    # boucle de test de calculs pour éviter les erreurs
    for shp in shps_files:
        sha_local = hashlib.sha256()
        with open(shp, 'r') as fd:
            try:
                while True:
                    data = fd.read(block_size)
                    if not data:
                        break
                    sha_local.update(data)
                    sha_glob.update(data)
            except Exception, why:
                print(u"Erreur dans le fichier {0}. Raison : {1}".format(f, why))
                return None
        shps_signs.append(sha_local.hexdigest())
        print("{0} == {1}".format(shp, sha_local.hexdigest()))
        del sha_local
    # total sum
    print("Total: {}\n".format(sha_glob.hexdigest()))
    shps_signs.append(sha_glob.hexdigest())
    # end of function
    return shps_signs


def sign_tab(tab, block_size=2**20):
    u""" Calcule la signature numérique md5 d'un fichier """
    # local variables
    tabs_files = (tab, tab[:-4] + '.DAT', tab[:-4] + '.MAP')
    tabs_signs = []
    # instance de hashing en 256 bits
    sha_glob = hashlib.sha256()
    # updating with the filename
    sha_glob.update(path.splitext(path.basename(tab))[0])
    # boucle de test de calculs pour éviter les erreurs
    for tab in tabs_files:
        sha_local = hashlib.sha256()
        with open(tab, 'r') as fd:
            try:
                while True:
                    data = fd.read(block_size)
                    if not data:
                        break
                    sha_local.update(data)
                    sha_glob.update(data)
            except Exception, why:
                print(u"Erreur dans le fichier {0}. Raison : {1}".format(f, why))
                return None
        tabs_signs.append(sha_local.hexdigest())
        print("{0} == {1}".format(tab, sha_local.hexdigest()))
        del sha_local
    # total sum
    print("Total: {}\n".format(sha_glob.hexdigest()))
    tabs_signs.append(sha_glob.hexdigest())
    # end of function
    return tabs_signs


################################################################################
###### Stand alone program ########
###################################

if __name__ == '__main__':
    """ testing the script """
    # variables
    mainfolder = r"data"
    li_shp = []
    li_tab = []
    li_geofolders = []
    # listing geofiles among folders
    li_geofiles(foldertarget= mainfolder, shps_list=li_shp, tabs_list=li_tab, gdirs_list=li_geofolders)
    print("In {0}, it found : \n\t{1} shapefiles\n\t{2} tables MapInfo\ndistributed in {3} folders.\n".format(mainfolder,len(li_shp), len(li_tab), len(li_geofolders)))

    # signing shapefiles
    for shp in li_shp:
        sign_shp(shp)

    # signing tables MapInfo
    for tab in li_tab:
        sign_tab(tab)

    # liste.sort()
    # hashs = [h[0] for h in liste]
    # s = set(hashs)

    # if len(s) == len(hashs):
    #     print u"Aucun doublon dans le dossier {0}".format(sys.argv[1])
    #     sys.exit ()

    # doublons = []
    # for idx, elt in enumerate(hashs):
    #     try:
    #         if elt == hashs[idx + 1]:
    #             doublons.append((liste[idx][1], liste[idx + 1][1]))
    #     except:
    #         # end of list
    #         pass

    # if len(doublons):
    #     print u"Ces fichiers sont identiques:",
    #     for d in doublons:
    #         print "\n  {0}\n  {1}".format(d[0], d[1])
    # else:
    #     print u"Aucun doublon dans le dossier {0}".format(sys.argv[1])
    #     sys.exit ()




# chercher données géographiques
# retenir répertoires en contenant : signer répertoires
# lister données géographiques :
# dict / répertoire: chemin shp, chemin dbf, chemin prj
# signer les dépendances
# foutre dans la BDD


# tables needed :
#     - répertoires : UID, nom, chemin complet, détails, score
#     - 1 table par répertoire : UID_répertoire (clé étrangère), UID donnée (primary key), nom, type, dépendances, détails, score