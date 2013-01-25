#!/usr/bin/python
# -*- coding: utf-8 -*-

# attention: pour les accents, ce fichier doit être impérativement
#      lu et modifié sous éditeur avec encodage UTF-8

################################################################
######                                                    ######
######                    HASHSOMME                       ######
######                                                    ######
###### ==> Calculatrice de MD5 et SHA-1 sur fichiers <=== ######
######                                                    ######
######                   Version 1.10                     ######
######                                                    ######
################################################################

# Copyright (C) 2008 Jean-Paul Vidal dit "Tyrtamos" — Tous droits réservés.
#   Logiciel distribué gratuitement sur le site <http://python.jpvweb.com>
#
#   Ce programme est un logiciel libre. Vous pouvez le redistribuer ou le
#   modifier suivant les termes de la "GNU General Public License" version 3,
#   telle que publiée par la Free Software Foundation.
#
#   Ce programme est distribué dans l’espoir qu’il vous sera utile, mais SANS
#   AUCUNE GARANTIE : sans même la garantie implicite de COMMERCIALISABILITÉ
#   ni d’ADÉQUATION À UN OBJECTIF PARTICULIER. Consultez la Licence Générale
#   Publique GNU pour plus de détails.
#
#   Pour avoir une copie de la License Générale Publique GNU,
#   consultez: <http://www.gnu.org/licenses/gpl.html>.

# pour que les divisions entre 2 entiers soient décimales
from __future__ import division

# si l'accélérateur psyco est installé, il est utilisé:
try:
    import psyco
    psyco.full()
except ImportError:
    pass

# importations système
import os
import sys
import Tkinter, tkFont, tkFileDialog
import md5
import sha

# variables globales
repcourant = os.getcwd()
selectcode = ""

##############################################################################
def md5somme(fichier):
    """Calcul du MD5 du fichier 'fichier' """
    try:
        f = file(fichier, 'rb')  # ouverture en mode binaire
    except:
        return "erreur d'ouverture en lecture du fichier"
    cle = md5.new()
    try:
        while True:
            t = f.read(1024)
            if len(t) == 0:
                break # fin du fichier
            cle.update(t)
    except:
        f.close()
        return "erreur de lecture du fichier"
    f.close()
    return cle.hexdigest()

##############################################################################
def shasomme(fichier):
    """Calcul du SHA-1 du fichier 'fichier' """
    try:
        f = file(fichier, 'rb')  # ouverture en mode binaire
    except:
        return "erreur d'ouverture en lecture du fichier"
    cle = sha.new()
    try:
        while True:
            t = f.read(1024)
            if len(t) == 0:
                break # fin du fichier
            cle.update(t)
    except:
        f.close()
        return "erreur de lecture du fichier"
    f.close()
    return cle.hexdigest()

##################################################################
def centrefenetre(fen):
    """place la fenêtre au centre de l'écran"""
    def geoliste(g):
        r = [i for i in range(0,len(g)) if not g[i].isdigit()]
        return [int(g[0:r[0]]), int(g[r[0]+1:r[1]]), int(g[r[1]+1:r[2]]), int(g[r[2]+1:])]
    fen.update_idletasks()
    l,h,x,y = geoliste(fen.geometry())
    fen.geometry("%dx%d%+d%+d" % (l, h, (fen.winfo_screenwidth()-l)//2, (fen.winfo_screenheight()-h)//2))

##############################################################################
class Apropos(Tkinter.Toplevel):
    """fenêtre 'A propos'"""

    def __init__(self, master=None):
        Tkinter.Toplevel.__init__(self, master)
        self.title("A propos")
        self.mes="""
HashSomme version 1.10
Calculatrice de MD5 et de SHA-1 sur fichiers

Copyright 2008 Jean-Paul Vidal dit "Tyrtamos"
Distribution sous license GPL v3
Site http://python.jpvweb.com
            """
        police = tkFont.Font(self, size=12, family='Arial')
        self.L = Tkinter.Label(self, text=self.mes, bg='yellow', font=police).grid()
        self.bind_all("<Button-1>", self.quitter)
        centrefenetre(self)

    def quitter(self, event=None):
        self.destroy()

##############################################################################
class SelectCode(Tkinter.Toplevel):
    """sélection d'une ligne dans une liste de lignes (=listbox dans une fenêtre)"""

    def __init__(self, master, listecodes):
        """initialise la fenêtre lors de l'instanciation de la classe"""

        # initialise la classe parent
        Tkinter.Toplevel.__init__(self, master)

        # divers
        self.title("Sélection du code à comparer")
        self.police=tkFont.Font(self, size=11, family='Courier')
        self.listecodes = listecodes

        # code nécessaire pour que le listbox suive le redimensionnement de la fenêtre
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # intégration des ascenseurs horizontaux et verticaux.
        self.yScroll = Tkinter.Scrollbar(self, orient=Tkinter.VERTICAL)
        self.xScroll = Tkinter.Scrollbar(self, orient=Tkinter.HORIZONTAL)

        # création du listbox
        self.listbox = Tkinter.Listbox(self, xscrollcommand=self.xScroll.set, yscrollcommand=self.yScroll.set, width=80, height=20, font=self.police)

        # insertion des lignes de texte dans le listbox
        for x in self.listecodes:
            self.listbox.insert(Tkinter.END,x)
        self.listbox.selection_set(0)

        # création des évènements clavier et souris
        self.listbox.event_add('<<selection>>', '<Return>','<KP_Enter>','<Double-1>')
        self.listbox.bind('<<selection>>', self.selection)

        self.yScroll.config(command=self.listbox.yview)
        self.xScroll.config(command=self.listbox.xview)

        # instructions d'affichage
        self.listbox.grid(row=0, column=0, sticky="nesw")

        self.yScroll.grid(row=0, column=1, sticky="nse")
        self.xScroll.grid(row=1, column=0, sticky="sew")

        # il faut que le listbox ait le focus (et pas seulement sa fenêtre!)
        self.listbox.focus()

    def selection(self, event=None):
        """sélectionne la ligne, la stocke dans la variable globale selectcode, et tue la fenêtre"""
        global selectcode
        idx=int(self.listbox.curselection()[0])
        selectcode = self.listecodes[idx]
        self.destroy()

##############################################################################
class Hashsomme(Tkinter.Frame):
    """classe principale de l'application"""

    def __init__(self, master=None):
        """initialisation de la fenêtre lors de l'instanciation de la classe"""
        global repcourant

        Tkinter.Frame.__init__(self, master, background="#dbd7c5")

        self.police=tkFont.Font(self, size=11, family='Courier')

        # création d'un layout_manager sur self
        self.grid()

        # 1ère ligne: création de la partie sélection du hash par bouton radio
        self.varselect = Tkinter.StringVar()
        self.varselect.set("MD5")

        self.select1 = Tkinter.Radiobutton(self, text="MD5", variable=self.varselect, value="MD5", background="#dbd7c5")
        self.select1.grid(row=0, column=1, columnspan=4, padx=3, pady=3, sticky="")

        self.select2 = Tkinter.Radiobutton(self, text="SHA-1", variable=self.varselect, value="SHA", background="#dbd7c5")
        self.select2.grid(row=0, column=4, columnspan=5, padx=3, pady=3, sticky="")

        # 2ème ligne: pour avoir un nom de fichier
        self.bnavig=Tkinter.Button(self, text="Importer", background="#66ccff", activebackground="#3399ff", command=self.importfichier)
        self.bnavig.grid(row=1, column=0, padx=3, pady=3, sticky="we")

        self.varnavig = Tkinter.StringVar()
        self.varnavig.set("")
        self.navig=Tkinter.Entry(self,  background="white", width=50, font=self.police, textvariable=self.varnavig)
        self.navig.grid(row=1,column=1, columnspan=8,padx=3, pady=3, sticky="we")

        # 3ème ligne: création de la partie calcul: lancement et affichage
        self.varcalcul = Tkinter.StringVar()
        self.varcalcul.set("")
        self.calcul=Tkinter.Entry(self,  background="#fffbb6", width=50, font=self.police, textvariable=self.varcalcul)
        self.calcul.grid(row=2,column=1, columnspan=8,padx=3, pady=3, sticky="we")

        self.bcalcul=Tkinter.Button(self, text="Calculer", background="#66ccff", activebackground="#3399ff", command=self.calculer)
        self.bcalcul.grid(row=2, column=9, padx=3, pady=3, sticky="we")

        # 4ème ligne: création de la partie comparer: obtenir un code à comparer et lancement de la comparaison
        self.impcode=Tkinter.Button(self, text="Importer", background="#66ccff", activebackground="#3399ff", command=self.importcode)
        self.impcode.grid(row=3, column=0, padx=3, pady=3, sticky="we")

        self.varcomp = Tkinter.StringVar()
        self.varcomp.set("")
        self.comp=Tkinter.Entry(self,  background="white", width=50, font=self.police, textvariable=self.varcomp)
        self.comp.grid(row=3,column=1, columnspan=8,padx=3, pady=3, sticky="we")

        self.bcomp=Tkinter.Button(self, text="Comparer", background="#66ccff", activebackground="#3399ff", command=self.comparer)
        self.bcomp.grid(row=3, column=9, padx=3, pady=3, sticky="we")

        # 5ème ligne: création de la partie affichage des messages et effacement de toutes les lignes
        self.varmesg = Tkinter.StringVar()
        self.varmesg.set("")
        self.mesg=Tkinter.Entry(self,  background="white", width=50, font=self.police, textvariable=self.varmesg)
        self.mesg.grid(row=4, column=1, columnspan=8, padx=3, pady=3, sticky="we")

        self.efface = Tkinter.Button(self, text="Effacer", background="#66ccff", activebackground="#3399ff", command=self.effacer)
        self.efface.grid(row=4, column=9, padx=3, pady=3, sticky="we")

        # préparation de l'affichage de la fenêtre 'à propos'
        if os.name=="mac":
            self.bind_all("<Shift-Button-1>", self.apropos)
        else:
            self.bind_all("<Button-3>", self.apropos)

        # mettre le focus sur la ligne de navigation (la 1ère ligne)
        self.navig.focus_set()

        # si un argument a été passé au lancement du programme, le considérer comme un fichier à calculer ou un chemin
        if len(sys.argv)>1:
            fichier = sys.argv[1]
            if not (os.path.exists(fichier) and os.path.isfile(fichier)):
                self.varmesg.set("le 1er fichier donné en paramètre n'existe pas")
            else:
                repcourant = os.path.dirname(os.path.normpath(fichier))
                if os.path.basename(fichier)!="":
                    self.varnavig.set(fichier)

    def importfichier(self, event=None):
        """fenêtre de dialogue pour sélectionner un fichier à calculer"""
        global repcourant
        self.varmesg.set("")
        self.rep=repcourant
        self.fic=""
        # fenêtre de dialogue
        self.repfic = tkFileDialog.askopenfilename(title="Sélectionner le fichier:", initialdir=self.rep, \
                        initialfile=self.fic, filetypes = [("All", "*")])
        self.repfic = os.path.normpath(self.repfic)
        # affichage du fichier sélectionné
        self.varnavig.set(self.repfic)
        # on concerve le chemin du fichier trouvé
        repcourant = os.path.dirname(self.repfic)

    def importcode(self, event=None):
        """fenêtre de dialogue pour trouver le code à comparer avec le code calculé"""
        global selectcode, repcourant
        self.varmesg.set("")

        # sélectionne le fichier des codes à comparer
        self.rep = repcourant
        self.fic=""
        self.repfic = tkFileDialog.askopenfilename(title="Sélectionner le fichier des codes:", initialdir=self.rep, \
                        initialfile=self.fic, filetypes = [("All", "*")])
        self.repfic = os.path.normpath(self.repfic)

        # charge le contenu du fichier dans la liste self.listecodes
        f = open(self.repfic, 'r')
        self.listecodes = [x.strip(' \n\r') for x in f]
        f.close()

        # création de la fenêtre sh (toplevel)
        sh = SelectCode(self, self.listecodes)
        centrefenetre(sh)
        sh.focus_set()
        # pour rendre la fenêtre sh modale
        sh.transient(self)
        sh.grab_set()
        self.wait_window(sh)

        # affichage du code sélectionné pour la comparaison: le code doit être en 1er sur la ligne!
        self.varcomp.set(selectcode.split(' ')[0])

    def calculer(self, event=None):
        """lancement du calcul du hash sélectionné sur le fichier donné"""
        fichier = self.varnavig.get()
        self.varcalcul.set("")
        if not (os.path.exists(fichier) and os.path.isfile(fichier)):
            if fichier=="":
                self.varmesg.set("il faut un nom de fichier")
            else:
                self.varmesg.set("le fichier donné n'existe pas")
        else:
            self.varmesg.set("")
            if self.varselect.get()=='MD5':
                self.varcalcul.set(md5somme(self.varnavig.get()))
            else:
                self.varcalcul.set(shasomme(self.varnavig.get()))
        self.navig.focus_set()

    def comparer(self, event=None):
        """lancement d'une comparaison du code calculé avec un code de référence"""
        self.varmesg.set("")
        H1 = self.varcalcul.get().capitalize().strip()
        H2 = self.varcomp.get().capitalize().strip()
        if H1=="":
            self.varmesg.set("il faut un code déjà calculé pour comparer")
            return None
        if H2=="":
            self.varmesg.set("il faut un code de référence pour comparer")
            return None
        if H1==H2:
            self.varmesg.set("Les 2 codes sont identiques")
        else:
            self.varmesg.set("Les 2 codes sont différents")

    def effacer(self, event=None):
        """efface toutes les lignes de saisie mais conserve le répertoire courant et le choix du hash"""
        self.varnavig.set("")
        self.varcalcul.set("")
        self.varcomp.set("")
        self.varmesg.set("")
        self.navig.focus_set()

    def apropos(self, event=None):
        """affiche la fenêtre 'A propos' avec un clic_droit sur la fenêtre (shift+clic_gauche pour le mac)"""
        self.apr = Apropos()
        self.apr.focus_set()

#############################################################################
if __name__ == "__main__":
    fen = Tkinter.Tk()
    fen.title("HashSomme v1.10")
    app = Hashsomme(fen)
    centrefenetre(fen)
    fen.resizable(width=False, height=False)
    fen.mainloop()
