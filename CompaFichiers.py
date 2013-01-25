#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

def compfichiers(nfc1, nfc2, lgbuf=32*1024):
    """Compare les 2 fichiers et renvoie True seulement s'ils ont un contenu identique"""
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

if __name__ == "__main__":

    import time

    # 1er cas: les 2 fichiers sont identiques
    nf1 = r"D:\A_Ordenar\Julien\python\Zevernette\test_doublons\Historiadistritos_2.xls"
    nf2 = r"D:\A_Ordenar\Julien\python\Zevernette\test_doublons\Mapa_historia_formacion_distritos\Historiadistritos_2.xls"

    try:
        t = time.clock()
        result = compfichiers(nf1, nf2)
        t = time.clock()-t
        print u"Résultat:", result, "%.3f s" % t
    except:
        t = time.clock()-t
        print u"Résultat: Erreur", "%.3f s" % t


    # 2ème cas: les 2 fichiers sont différents
    nf1 = r"C:\Python25\DLLs\tk84.dll"
    nf2 = r"C:\Python25\DLLs\unicodedata.pyd"
    try:
        t = time.clock()
        result = compfichiers(nf1, nf2)
        t = time.clock()-t
        print u"Résultat:", result, "%.3f s" % t
    except:
        t = time.clock()-t
        print u"Résultat: Erreur", "%.3f s" % t

    # 3ème cas: le second fichier n'existe pas
    nf1 = r"C:\Python25\DLLs\tk84.dll"
    nf2 = r"C:\Python25\DLLs\cefichiernexistepas.$$$"
    try:
        t = time.clock()
        result = compfichiers(nf1, nf2)
        t = time.clock()-t
        print u"Résultat:", result, "%.3f s" % t
    except:
        t = time.clock()-t
        print u"Résultat: Erreur", "%.3f s" % t