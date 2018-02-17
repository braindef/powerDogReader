
import time

from pyrrd.rrd import RRD, RRA, DS
from pyrrd.graph import DEF, CDEF, VDEF
from pyrrd.graph import LINE, AREA, GPRINT
from pyrrd.graph import ColorAttributes, Graph

#Vorhandenes RRD öffnen
myRRD = RRD('A1_B1_S14.rrd')

myRRD.info()

exampleNum = 4
filename = 'A1_B1_S1%s.rrd' % exampleNum
graphfile = 'A1_B1_S1%s.png' % exampleNum

day = 24 * 60 * 60
week = 7 * day
month = day * 30
quarter = month * 3
half = 365 * day / 2
year = 365 * day

endTime = int(round(time.time()))
delta = day
startTime = endTime - delta
step = 300
maxSteps = int((endTime-startTime)/step)

# Let's create and RRD file and dump some data in it



# Let's set up the objects that will be added to the graph
def1 = DEF(rrdfile=myRRD.filename, vname='myspeed', dsName="kW")
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

g.filename = graphfile
g.width = 800
g.height = 400
g.write()



