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

years = []
months = []
days = []


day = 24 * 60 * 60
week = 7 * day
month = day * 30
quarter = month * 3
half = 365 * day / 2
year = 365 * day

endTime = int(round(time.time()))
startTime = endTime - (10 * 60 * 60)
delta = 2 * day
startTime = endTime - delta
step = 300
maxSteps = int((endTime-startTime)/step)

#in welchem Verzeichnis wir die Powerdog FTP Daten holen
baseDir = "/home/toni/"         #needs trailing /

#PowerDOG String selection
allStrings = []

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
        parser.add_argument('--createFromHistory', action="store_true", dest="createFromHistory", help='generiert die RRD Files basierend an hand der Vergangenen Daten im FTP Verzeichnis')
        parser.add_argument('--update', action="store_true", dest="update", help='gibt an dass ein neuer Wert hinzugefügt werden soll')
        parser.add_argument('--render', action="store_true", dest="render", help='gibt an dass die Grafik(en) gerendert werden sollen')
        parser.add_argument('--getStrings', action="store_true", dest="getStrings", help='gibt an dass die Grafik(en) gerendert werden sollen')

        parser.add_argument('--starttime', action="store", dest="starttime", help='gibt den startzeitpunkt für die Grafik an')
        parser.add_argument('--endtime', action="store", dest="endtime", help='gibt den startzeitpunkt für die Grafik an')


        #noch nicht implementiert
        parser.add_argument('--config', action="store", dest="configfile", help='gibt den Pfad des Configfiles an')

	args = parser.parse_args()

        global startTime
        global endTime

        if not (args.starttime is None):
            startTime = args.starttime
            print startTime

        if not (args.endtime is None):
            endTime = args.endtime
            print endTime

        if (args.create is None and args.update is None and args.graph is None):
            print "bitte angeben ob --create, --update oder --render"
        
        if args.create is True:
            if debug: print "Create"
            createAll()

        if args.createFromHistory is True:
            if debug: print "CreateFromHistory"
            createAllFromHistory2()

        if args.update is True:
            if debug: print "Update"
            updateAll()

        if args.render is True:
            #TODO start und end Timestamp angeben
            if debug: print "Render"
            renderAll()

#        if args.getStrings is True:
#            if debug: print "getAllStrings()"
#            getAllStrings()



def getAllStrings():
    print "Enter Function getAllStrings()"

    global allStrings

    mylist = []

    files = glob.glob( baseDir + 'B*.txt')
    #if debug: print files
    for file in files:
        file = os.path.basename(file)
        file = file[0:8]
        if debug: print file
        mylist.append(file)
    mylist = list(set(mylist))  #doppelte einträge aus liste löschen
    print mylist
    allStrings = mylist

def createAll():
        if debug: print "Enter Function createAll()"
	for stringName in allStrings:
		for key in allGraphValues:
			create(stringName, key)


def createAllFromHistory2():

    if debug: print "Enter Function createAllFromHistory()"
    createAll()
    for stringName in allStrings:
        contentOfAllFiles = []
        line = []
        files = glob.glob ( baseDir + stringName + "_global_*.txt")
        for file in files:
            with open(file) as f:
                for line in f:
                    if "timestamp" in line: continue
                    contentOfAllFiles.append(line)
                #print allFiles
        #print lines
        sortedList = sorted(list(set(contentOfAllFiles)))   #sort and remove duplicates since the PowerDOG saves values duplicated
        for s in sortedList:
            for key in allGraphValues:
                #print "test"

                if debug: print (stringName +" "+ s.split(";")[0] +" "+ key +" "+ s.split(";")[allValues.index(key)])
                update(stringName, s.split(";")[0], key, s.split(";")[allValues.index(key)])


def createAllFromHistory():
#deprecated use createAllFromHistory2()

    createAll()
    if debug: print "Enter Function createAllFromHistory()"
    if debug: print "ALLSTRINGS: " + str(allStrings)
    for stringName in allStrings:
        years=[]
        months=[]
        days=[]
        if debug: print "STRING:" + stringName
        files = glob.glob ( baseDir + stringName + "_global_*.txt")
        if debug: print str(stringName) + ": " + str(files)
        for file in files:
            if debug: print os.path.basename(file)
            years.append (os.path.basename(file).split("_")[6][0:4])
        if debug: print years
        files = glob.glob ( baseDir + stringName + "_global_" + "*" + min(years) + ".txt")
        for file in files:
            if debug: print os.path.basename(file)
            months.append(os.path.basename(file).split("_")[4])
        if debug: print months
        
        for y in range(int(min(years)), int(time.strftime("%Y"))+1):
            if debug: print y
            for m in range(1,13):
                if debug: print str(y)+"-"+str(m)
                for d in range(1,32):
                    if debug: print str(y)+"-"+str(m)+"-"+str(d)
                    parseDataFile(baseDir + stringName + "_global_" + str(m) + "_" + str(d) + "_" + str(y) + ".txt")


def parseDataFile(filename):
    if os.path.exists(filename):
        print "Parsing: " + filename
        for key in allGraphValues:
            #create(filename, key)

            with open(filename,'r') as f:
                lines = f.readlines()
            lines.sort()
            for line in lines:
                if "timestamp" in line: continue
                for key in allGraphValues:
                    if debug: print line.split(";")[0]
                    if debug: print line.split(";")[allValues.index(key)]
                    update(os.path.basename(filename)[0:8], line.split(";")[0], key, line.split(";")[allValues.index(key)])

def updateAll():
        if debug: print "Enter Function updateAll()"
	for stringName in allStrings:
		for key in allGraphValues:
                        if debug: print ("updateAll"+baseDir+stringName+"_"+key)
			update(stringName, time.time(), key, getCurrentValue(stringName, key) )

def renderAll():
        if debug: print "Enter Function renderAll()"
	for stringName in allStrings:
		for key in allGraphValues:
			render(stringName, key, startTime, endTime)



def create(stringName, key):
        if debug: print "Enter Function create(stringName, key)"
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
	#myRRD = RRD(baseDir + stringName + "_" + key + ".rrd", ds=dss, rra=rras, start=startTime)
	myRRD = RRD(baseDir + stringName + "_" + key + ".rrd", ds=dss, rra=rras, start=1483228800)
	myRRD.create()

	myRRD.update()
        if debug: myRRD.info()



def update(stringName, timestamp, key, value):
        if debug: print "Enter Function update(stringName, key, value)"
        
        #round robbing database file öffnen
	myRRD = RRD(baseDir + stringName + "_" + key + ".rrd")

	#Wert in round robbin database eintragen
        try:
            myRRD.bufferValue(timestamp, value)
	    myRRD.update()
        except:
            print "value in the past"
        
        if debug: myRRD.info()



def render(stringName, key, startTime, endTime):
        if debug: print "Enter Function render(filename, value)"
	
        #balken zeichnen
        def1 = DEF(rrdfile = baseDir + stringName + "_" + key + ".rrd", vname='kW', dsName="kW")  #command fetches data from the rrd
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
	#startTime = endTime - (10 * 60 * 60) #10h anzeigen, sollte noch variabel sein
	g = Graph(baseDir + stringName + "_" + key + ".png", start=startTime, end=endTime, vertical_label='data', color=ca)
	g.data.extend([def1, area1, line1])

	g.width = 800
	g.height = 400
	g.write()


def getCurrentValue(stringName, key):
    if debug: print "Enter Function getCurrentValue(filename, key)"
    
    #alle dateien des Strings (im sinne von Solaranlagen String) finden
    if debug: print baseDir+stringName
    files = glob.glob( baseDir + stringName + '_global_*.txt')
    
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
                        maximumTimeValue = line.split(";")[allValues.index(key)]

            #lastLine = list(myfile)[-1]
            #if debug: print lastLine      #last line geht nicht weil das ganze zeug komplett unsortiert daher kommt
            
            return maximumTimeValue



getAllStrings()
parseArgs()


