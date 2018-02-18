#coding=utf-8

import argparse
import time
import os.path
import requests
import sys
import re
import glob

from pyrrd.rrd import RRD, RRA, DS
from pyrrd.graph import DEF, CDEF, VDEF
from pyrrd.graph import LINE, AREA, GPRINT
from pyrrd.graph import ColorAttributes, Graph

#auf UTF-8 Zeichensatz einstellen
reload(sys)
sys.setdefaultencoding('utf8')

#debug variable, auf True wird mehr debug info angezeigt
debug = False
#debug = True


day = 24 * 60 * 60
week = 7 * day
month = day * 30
quarter = month * 3
half = 365 * day / 2
year = 365 * day

endTime = int(round(time.time()))
delta = 2 * day
startTime = endTime - delta
step = 300
maxSteps = int((endTime-startTime)/step)

#in welchem Verzeichnis wir die Powerdog FTP Daten holen
basepath = "/home/toni/"

#PowerDOG String selection
allStrings = ["B2_A2_S1","B2_A2_S2","B2_A3_S1","B2_A3_S2"]

#Powerdog File selection, die anderen files werden aus diesen konsolidiert von Powerdog
allFiles = ["global","event"]

#PowerDOG Value Selection
allValues = ["timestamp","address","bus","strings","stringid","pac","pdc","udc","temp"]
allGraphValues =  ["pac","pdc","udc","temp"]

#Eingabeparameter verarbeiten
# Instantiate the parser
def parseArgs():

        #kommando parameter anzeigen und auswählen
	parser = argparse.ArgumentParser(description='Liest Werte aus Powerdog FTP Daten aus z.B: $ python get.py --file "B2_A2_S1"')
        
        parser.add_argument('--create', action="store_true", dest="create", help='gibt an dass die RRD Files und das Configfile generiert werden')
        parser.add_argument('--update', action="store_true", dest="update", help='gibt an dass ein neuer Wert hinzugefügt werden soll')
        parser.add_argument('--render', action="store_true", dest="render", help='gibt an dass die Grafik(en) gerendert werden sollen')

        #noch nicht implementiert
        parser.add_argument('--config', action="store", dest="configfile", help='gibt den Pfad des Configfiles an')

	args = parser.parse_args()

        if (args.create is None and args.update is None and args.graph is None):
            print "bitte angeben ob --create, --update oder --render"
        
        if args.create is True:
            if debug: print "Create"
            createAll()

        if args.update is True:
            if debug: print "Update"
            updateAll()

        if args.render is True:
            #TODO start und end Timestamp angeben
            if debug: print "Render"
            renderAll()


def getAllStrings():
    #TODO: ist im moment noch statisch angegeben, einen default wert von einem Tag wenn nichts angegeben


def createAll():
        if debug: print "Enter Function createAll()"
	for i in allStrings:
		for j in allGraphValues:
			create(basepath+i, j)

def updateAll():
        if debug: print "Enter Function updateAll()"
	for i in allStrings:
		for j in allGraphValues:
                        if debug: print ("updateAll"+basepath+i)
			update(basepath+i, j )

def renderAll():
        if debug: print "Enter Function createAll()"
	for i in allStrings:
		for j in allGraphValues:
			render(basepath+i, j)



def create(filename, value):
        if debug: print "Enter Function create(filename, value)"
	# Let's create and RRD file and dump some data in it
	dss = []
	ds1 = DS(dsName='kW', dsType='GAUGE', heartbeat=600) #alle 10 Minuten einen Wert
	dss.append(ds1)

        rras = [] #round robin archives mit, xff=0.5 also wenn 20 Minuten kein wert kommt wirds leer angezeigt:
	rra1 = RRA(cf='AVERAGE', xff=0.5, steps=1, rows=144) #alle 10 Minuten ein Wert
	rra2 = RRA(cf='AVERAGE', xff=0.5, steps=6, rows=24)  #24h mal 1h
	rra3 = RRA(cf='AVERAGE', xff=0.5, steps=24, rows=30) #30 Tage mal 24h
	rra4 = RRA(cf='AVERAGE', xff=0.5, steps=30, rows=12) #12 Monate mal 30 Tage
	rra5 = RRA(cf='AVERAGE', xff=0.5, steps=12, rows=10) #10 Jahre mal 12 Monate
	rras.append(rra1)
	rras.append(rra2)
	rras.append(rra3)
	rras.append(rra4)
	rras.append(rra5)

        #round robbin database file anlegen mit der Startzeit startTime (jetzt)
	myRRD = RRD(filename+"_"+value+".rrd", ds=dss, rra=rras, start=startTime)
	myRRD.create()

	myRRD.update()
        if debug: myRRD.info()



def update(filename, value):
        if debug: print "Enter Function update(filename, value)"
        
        #round robbing database file öffnen
	myRRD = RRD(filename+"_"+value+".rrd")

	#Wert in round robbin database eintragen
        myRRD.bufferValue(time.time(), getValue(filename, value))          #DAS DANN WIEDER äNDERN
	myRRD.update()
        if debug: myRRD.info()


def render(filename, value):
        if debug: print "Enter Function render(filename, value)"
	
        #balken zeichnen
        def1 = DEF(rrdfile=filename+"_"+value+".rrd", vname='kW', dsName="kW")  #command fetches data from the rrd
	area1 = AREA(defObj=def1, color='#FFA902', legend='kW')
        
        #mittelwert linie zeichnen (muss noch berechnet werden
        line1 = LINE(value=100, color='#990000', legend='Average')

	# Let's configure some custom colors for the graph
	ca = ColorAttributes()
	ca.back = '#333333'
	ca.canvas = '#333333'
	ca.shadea = '#000000'
	ca.shadeb = '#111111'
	ca.mgrid = '#CCCCCC'
	ca.axis = '#FFFFFF'
	ca.frame = '#AAAAAA'
	ca.font = '#FFFFFF'
	ca.arrow = '#FFFFFF'

	# Now that we've got everything set up, let's make a graph
	startTime = endTime - (10 * 60 * 60) #10h anzeigen, sollte noch variabel sein
	g = Graph(filename+"_"+value+".png", start=startTime, end=endTime, vertical_label='data', color=ca)
	g.data.extend([def1, area1, line1])

	g.width = 800
	g.height = 400
	g.write()


def getValue(filenameWithPath, column):
    if debug: print "Enter Function getValue(filename, column)"
    
    #alle dateien des Strings (im sinne von Solaranlagen String) finden
    if debug: print filename
    files = glob.glob( filenameWithPath + '_global_*.txt')
    
    #die neuste datei wählen
    if debug: print files
    filename = max(files, key = os.path.getctime)


    with open(filename, 'r') as myfile:

            maximumTime =  0
            maximumTimeValue = 0
            n=0
            for line in myfile:
                n+=1                #header der datei wegschneiden
                if n>1:
                    if line.split(";")[0]>maximumTime:
                        maximumTime = line.split(";")[0];
                        maximumTimeValue = line.split(";")[allValues.index(column)]

            #lastLine = list(myfile)[-1]
            #if debug: print lastLine      #last line geht nicht weil das ganze zeug komplett unsortiert daher kommt
            
            return maximumTimeValue




parseArgs()


