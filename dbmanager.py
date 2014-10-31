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
import sqlite3


db =  path.join(getcwd(), 'data/bd_keywords_prensa.sqlite')

conn = sqlite3.connect(db)          # connexion BD
cur = conn.cursor()    

## SQL CREATE  TABLE "main"."flujitos_glob" ("ID" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE  DEFAULT CURRENT_TIMESTAMP, "mots" VARCHAR NOT NULL  UNIQUE , "occurences" INTEGER, "tipo" BOOL)
## CREATE  INDEX "main"."glob_flujitos" ON "flujitos_glob" ("ID" ASC, "mots" ASC, "occurences" ASC, "tipo" ASC)