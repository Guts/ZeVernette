#!/usr/bin/python
# -*- coding: utf-8 -*-

### Import librairies tierces

from xlwt import Workbook, easyxf, Font, XFStyle, Formula  # écriture excel 2003


class DoblExcel:
    u""" crée un onglet dans un fichier excel listant les doublons """
    def __init__(self, workbook, fichier, doublon):
        self.onglet = workbook.add_sheet(fichier, True)
        # Styles excel
        self.hyperlien = easyxf(u'font: underline single')   # pour les URL
        self.font1 = Font()             # création police 1
        self.font1.name = 'Times New Roman'
        self.bold = True
        self.entete = XFStyle()         # création style des en-têtes
        self.entete.font = self.font1        # application de la police 1 au style entete
        # en première ligne
        self.premiere_ligne(self.onglet)
        # fichier référence
        self.genuine(self.onglet, fichier)
        # doublons
        self.doublures(self.onglet, doublon)

    def premiere_ligne(self, onglet):
        u""" crée la première ligne de l'onglet """
        self.onglet.write(0, 0, 'Nom', self.entete)
        self.onglet.write(0, 1, 'Chemin', self.entete)
        self.onglet.write(0, 2, 'Taille', self.entete)
        self.onglet.write(0, 3, 'Création', self.entete)
        self.onglet.write(0, 4, 'Dernière modification', self.entete)
        self.onglet.write(0, 5, 'Signature md5', self.entete)
        self.onglet.write(0 ,6, 'Probabilité', self.entete)
        # fin fonction
        return onglet

    def genuine(self, onglet, fichier):
        u""" écrit les infos du 'vrai' fichier qui fait référence """
        self.onglet.write(0, 1, fichier)
        return onglet, fichier


    def doublures(self, onglet, doublon):
        u""" écrit les infos des fichiers similaires au 'vrai' fichier """
        for elt in doublon:
            self.onglet.write(0, doublon.index(elt), elt[0])
            self.onglet.write(1, doublon.index(elt), elt[1])
        return onglet, doublon


if __name__ == '__main__':
    wb = Workbook(encoding='utf8')
    DoblExcel(wb, 'youpi', 1)
