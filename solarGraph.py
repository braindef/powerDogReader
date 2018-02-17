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

import get as powerDogGet

#auf UTF-8 Zeichensatz einstellen
reload(sys)
sys.setdefaultencoding('utf8')


#debug = False
debug = True


exampleNum = "temp"
filename = 'A1_B1_S1%s.rrd' % exampleNum
graphfile = 'A1_B1_S1%s.png' % exampleNum

day = 24 * 60 * 60
week = 7 * day
month = day * 30
quarter = month * 3
half = 365 * day / 2
year = 365 * day

endTime = int(round(time.time()))
delta = 2* day
startTime = endTime - delta
step = 300
maxSteps = int((endTime-startTime)/step)

#PowerDOG String selection
allStrings = ["B2_A2_S1","B2_A2_S2","B2_A3_S1","B2_A3_S2"]

#Powerdog File selection
allFiles = ["global","event"]

#PowerDOG Value Selection
allValues = ["timestamp","address","bus","strings","stringid","pac","pdc","udc","temp"]
allGraphValues =  ["pac","pdc","udc","temp"]

#Eingabeparameter verarbeiten
# Instantiate the parser
def parseArgs():
	parser = argparse.ArgumentParser(description='Liest Werte aus Powerdog FTP Daten aus z.B: $ python get.py --file "B2_A2_S1"')
	#parser.add_argument('--csv', action="store_true", default=False, help='gibt alle Daten als CSV aus')
        parser.add_argument('--create', action="store_true", dest="create", help='gibt an dass die RRD Files und das Configfile generiert werden')
        parser.add_argument('--update', action="store_true", dest="update", help='gibt an dass ein neuer Wert hinzugefügt werden soll')
        parser.add_argument('--render', action="store_true", dest="render", help='gibt an dass die Grafik(en) gerendert werden sollen')

        parser.add_argument('--config', action="store", dest="configfile", help='gibt den Pfad des Configfiles an')


	args = parser.parse_args()
	if not (args.create is None and args.update is None and args.graph is None):
                filelist = glob.glob(args.file+"_global_*")
                if debug: print filelist
                if debug: print sorted(filelist) #ah der dämliche powerDOG lässt sich nicht mal sortieren weil die leading zeros fehlen, NERV...
                files = glob.glob(args.path +"/"+ args.file+'_global_*.txt')
                filename = max(files, key = os.path.getctime)
                if debug: print filename
                if debug: print str(args.value) + " = " + str(allValues.index(args.value)) #die spalte in der CSV also z.B. bei pdc die 6. spalte
                print getValue(filename,args.value)

def createAll():
	for i in allStrings:
		for j in allGraphValues:
			create(i, j)

def updateAll():
	for i in allStrings:
		for j in allGraphValues:
			update(i, powerDogGet(i, j))
	

def renderAll():
	for i in allStrings:
		for j in allGraphValues:
			render(i, j)



def create(filename, value):
	# Let's create and RRD file and dump some data in it
	dss = []
	ds1 = DS(dsName='kW', dsType='GAUGE', heartbeat=300)
	dss.append(ds1)

	rras = []
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

	myRRD = RRD(filename+"_"+value+".rrd", ds=dss, rra=rras, start=startTime)
	myRRD.create()

	myRRD.update()
	myRRD.info()



def update(filename, value):
	myRRD = RRD(filename+"_"+value+".rrd")
	myRRD.bufferValue(time.time(),  powerDogGet(filename, value))
	print powerDogGet(filename, value)
	myRRD.update()
	myRRD.info()


def render(filename, value):
# Let's set up the objects that will be added to the graph
	def1 = DEF(rrdfile=filename+".rrd", vname='kW', dsName="kW")
	area1 = AREA(defObj=def1, color='#FFA902', legend='kW')

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
	startTime = endTime - 2 * day
	g = Graph(graphfile, start=startTime, end=endTime, vertical_label='data', color=ca)
	g.data.extend([def1, area1])

	g.filename = filename+"_"+value+".rrd"
	g.width = 800
	g.height = 400
	g.write()


#getAllStrings()
parseArgs()


