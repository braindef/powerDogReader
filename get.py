#coding=utf-8
import argparse
import time
import os.path
import requests
import sys
import re
import glob

#auf UTF-8 Zeichensatz einstellen
reload(sys)
sys.setdefaultencoding('utf8')


#debug = False
debug = True


#Adresse der Webseite(n)
#---------------------------------------------------------------------------
url1 = 'http://*****URL*****'		#Adresse der Steuerung bzw. des Webinterfaces
url2 = url1 + '?s=1,0'
url3 = url1 + '?s=1,1'

#Username for interfaces that need to login and get data
payload = {'make': 'send','user': '*****USERNAME*****','pass': '*****PASSWORD*****'}
#---------------------------------------------------------------------------


#Alle Verfügbaren Werte (Keys) um die Werte (Values) abzufragen, falls die Steuerungssoftware geändert wird muss das angepasst werden

#PowerDOG String selection
allKeys = ["B2_A2_S1","B2_A2_S2","B2_A3_S1","B2_A3_S2"]

#Powerdog File selection
allFiles = ["global","event"]

#PowerDOG Value Selection
allValues = ["timestamp","address","bus","strings","stringid","pac","pdc","udc","temp"]


#Aktueller Monat als Dateiname für die CSV Datei, Pro Monat eine Datei
currentMonth = time.strftime("%Y%m")
filenameCSV = './Heizung_'+currentMonth+'.csv'

#Aktueller Zeitstempel, da sich die Heizung träge verhält macht es keinen Sinn mehr als 1x alle 10 Min abzufragen
currentHour = time.strftime("%Y%m%d%H")+str(int(time.strftime("%M"))/10)
#filename = './'+currentMonth+'/'+currentHour+'.dump'
#print filename

#print filename


#Eingabeparameter verarbeiten
# Instantiate the parser
def parseArgs():
	parser = argparse.ArgumentParser(description='Liest Werte aus Powerdog FTP Daten aus z.B: $ python get.py --file "B2_A2_S1"')
	#parser.add_argument('--csv', action="store_true", default=False, help='gibt alle Daten als CSV aus')
        parser.add_argument('--path', action="store", dest="path", help='gibt den zu verwendenden Pfad an, z.B. /home/toni')
        parser.add_argument('--file', action="store", dest="file", help='gibt die CSV Datei an, Parameter: B2_A2_S1')
        parser.add_argument('--value', action="store", dest="value", help='gibt den wert an, pac, pdc, udc...')
	args = parser.parse_args()
	if not (args.file is None):
                filelist = glob.glob(args.file+"_global_*")
                if debug: print filelist
                if debug: print sorted(filelist) #ah der dämliche powerDOG lässt sich nicht mal sortieren weil die leading zeros fehlen, NERV...
                files = glob.glob(args.path +"/"+ args.file+'_global_*.txt')
                filename = max(files, key = os.path.getctime)
                if debug: print filename
                if debug: print str(args.value) + " = " + str(allValues.index(args.value)) #die spalte in der CSV also z.B. bei pdc die 6. spalte
                print getValue(filename,args.value)

def getValue(filename, column):
    #print value
        with open(filename, 'r') as myfile:
            
            lastLine = list(myfile)[-1]
            if debug: print lastLine
            
            returnValue = lastLine.split(";")[allValues.index(column)]
            
            return returnValue













#------------------------------------------------------------------------------
#Hole die drei Werteseiten von der STIEBEL ELTRON Steuerunngs Webseite v2.5.6
def getFile():
	response1 = requests.post(url1, data=payload, headers={'Connection':'close'})
	response2 = requests.post(url2, data=payload, headers={'Connection':'close'})
	response3 = requests.post(url3, data=payload, headers={'Connection':'close'})

	file = open(filename, 'w')
	file.write(response1.content)  #hänge die drei dateien aneinander
	file.write(response2.content)
	file.write(response3.content)
	file.close()

#gibt die abgefragten Webseiten der Steuerung aus (nur für Testzwecke)
def printResponse():
	print(response1.text)
	print(response1.status_code)

	print(response2.text)
	print(response2.status_code)

	print(response3.text)
	print(response3.status_code)


#Hole die Temparatur Minimalwerte aus dem gespeicherten File
def getMin():
	with open(filename, 'r') as fin:
		for line in fin:
			if re.search('charts', line):
				##print line
				if re.search('min', line):
					return line.split(",")[11].split("]")[0]

#Hole die Temparatur Mittelwerte aus dem gespeicherten File
def getMiddle():
	with open(filename, 'r') as fin:
		for line in fin:
			if re.search('charts', line):
				##print line
				if re.search('mittel', line):
					return line.split(",")[11].split("]")[0]

#Hole die Temparatur Maximalwerte aus dem gespeicherten File
def getMax():
	with open(filename, 'r') as fin:
		for line in fin:
			if re.search('charts', line):
				##print line
				if re.search('max', line):
					return line.split(",")[11].split("]")[0]

#Hole die Temparatur Mittelwerte aus dem gespeicherten File
def getHeizen():
	with open(filename, 'r') as fin:
		for line in fin:
			if re.search('charts\[2\]', line):
				##print line
				if re.search('line', line):
					return line.split(",")[11].split("]")[0]

#Hole die Temparatur Mittelwerte aus dem gespeicherten File
def getWarmwasser():
	with open(filename, 'r') as fin:
		for line in fin:
			if re.search('charts\[3\]', line):
				if re.search('line', line):
					return line.split(",")[11].split("]")[0]


#Hole die Live Daten aus dem gespeicherten File
def getLive(value):
	#print value
	with open(filename, 'r') as fin:
		for line in fin:
			if re.search(">"+value+"<", line): #suche nach ">NAMEDERVARIABEL<"
				return fin.next().split(">")[1].split(" ")[0].replace(",",".");


#fügt alle aktuelle Werte zum CSV dazu
def addToCSV():
	if not os.path.exists(filenameCSV):		#Header in die CSV Datei schreiben falls sie neu erstellt wurde
		with open(filenameCSV, 'a') as fout:
			fout.write("Date")
			for i in allKeys:
				fout.write(","+i)
			fout.write(",MIN,MIDDLE,MAX,HEIZEN,WARMWASSER")
			fout.write("\n")
			fout.close()

	with open(filenameCSV, 'a') as fout:		#Akutelle Werte in die CSV schreiben
		fout.write(time.strftime("%Y-%m-%d %H:%M:%S"))
		for i in allKeys:
			fout.write(","+getLive(i))
		fout.write(","+getMin()) #history Daten
		fout.write(","+getMiddle())
		fout.write(","+getMax())
		fout.write(","+getHeizen())
		fout.write(","+getWarmwasser())
		fout.write("\n")


#-----------------------------------------
# MAIN: Hauptprogramm, hier startet alles
#-----------------------------------------
#if not os.path.exists("./"+currentMonth):
#	os.makedirs("./"+currentMonth)
#if not os.path.exists(filename):#Holt das Datenfile vom Server wenn es diese Stunde nicht schon einmal geholt wurde und die Datei schon existiert
#	getFile()		
#	addToCSV()		#Fügt die Daten dem CSV hinzu
parseArgs()			#je nach Aufrufparameter (Args) wird dann die Funktion für den Entsprechenden wert aufgerufen


