# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import unicode_literals
#-------------------------------------------------------------------------------
# Name:         Hashing Shapefiles
# Purpose:      Calculate a numeric print on :
#                   - shapefiles (.shp + .dbf + .prj)
#                   - tables MapInfo (.tab + .dat + .map)
#                   - folders
#
# Author:       Julien Moura (https://github.com/Guts/)
#
# Python:       2.7.x
# Created:      19/12/2012
# Updated:      03/06/2014
#
# Licence:      GPL 3
#-------------------------------------------------------------------------------

################################################################################
########### Libraries #############
###################################
# Standard library
import hashlib
from multiprocessing import Process, Queue, TimeoutError
from os import path, walk, listdir
from datetime import datetime
import sys

################################################################################
########### Functions #############
###################################

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
    u""" compute a tuple of shapefiles hashs. Tuple structure:
    [0] = hash of *.shp data (sha256)
    [1] = hash of *.dbf data (sha256)
    [2] = hash of *.prj data (sha256)
    [3] = global hash (sha256) : filename (without extension) + [0],[1],[2]
    """
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
                print(u"Error in the file {0}. Reason: {1}".format(f, why))
                return None
        shps_signs.append(sha_local.hexdigest())
        print("{0} == {1}".format(shp, sha_local.hexdigest()))
        del sha_local
    # total sum
    print("Total: {}\n".format(sha_glob.hexdigest()))
    shps_signs.append(sha_glob.hexdigest())
    # end of function
    return tuple(shps_signs)


def sign_tab(tab, block_size=2**20):
    u""" compute a tuple of MapInfo table hashs. Tuple structure:
    [0] = hash of *.tab data (sha256)
    [1] = hash of *.dat data (sha256)
    [2] = hash of *.map data (sha256)
    [3] = global hash (sha256) : filename (without extension) + [0],[1],[2]
    """
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
                print(u"Error in the file {0}. Reason: {1}".format(f, why))
                return None
        tabs_signs.append(sha_local.hexdigest())
        print("{0} == {1}".format(tab, sha_local.hexdigest()))
        del sha_local
    # total sum
    print("Total: {}\n".format(sha_glob.hexdigest()))
    tabs_signs.append(sha_glob.hexdigest())
    # end of function
    return tuple(tabs_signs)


def sign_dir(folderpath):
    u""" compute a tuple of a directory hash and specifications. Tuple structure:
    [0] = hash of folder name (sha256)
    [1] = hash of folder path (without name) (sha256)
    [2] = folder size (cumulated)
    [3] = folder creation date
    [4] = folder last update date
    [5] = global hash (sha256) : [0],[1],[2] hashed,[3] hashed,[4] hashed
    """
    # variables
    gdirs_signs = []
    # instance de hashing en 256 bits

    # updating with the directory name
    sha_loc_name = hashlib.sha256()
    sha_loc_name.update(path.basename(folderpath))
    gdirs_signs.append(sha_loc_name.hexdigest())

    # updating with the directory path
    sha_loc_path = hashlib.sha256()
    sha_loc_path.update(folderpath[:-len(path.basename(folderpath))])
    gdirs_signs.append(sha_loc_path.hexdigest())

    # getting folder specifications
    dossize = sum([path.getsize(path.join(folderpath, f)) for f in listdir(folderpath) if path.isfile(path.join(folderpath, f))])
    date_crea = path.getctime(folderpath)
    date_updt = path.getmtime(folderpath)

    # adding to the final tuple
    gdirs_signs.append(dossize)
    gdirs_signs.append(date_crea)
    gdirs_signs.append(date_updt)

    # pretty print
    print("\n{0} = {1}. It's been created on {2} and lately updated on {3}.".format(folderpath, \
                                                                           sizeof_fmt(dossize),
                                                                           datetime.fromtimestamp(int(date_crea)).strftime('%Y-%m-%d %H:%M:%S'), 
                                                                           datetime.fromtimestamp(int(date_updt)).strftime('%Y-%m-%d %H:%M:%S')))

    # global hash
    sha_glob = hashlib.sha256()
    sha_glob.update(path.basename(folderpath))
    sha_glob.update(folderpath[:-len(path.basename(folderpath))])
    sha_glob.update(unicode(dossize))
    sha_glob.update(unicode(date_crea))
    sha_glob.update(unicode(date_updt))
    gdirs_signs.append(sha_glob.hexdigest())
    # end of function
    return tuple(gdirs_signs)


def sizeof_fmt(num):
    u""" one of the various snippets found ont the Web to get
    human readable version of files sizes.
    see: http://stackoverflow.com/a/1094933"""
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f %s" % (num, 'TB')

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

    # signing folders containing geo datas
    for folder in li_geofolders:
        sign_dir(folder)


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