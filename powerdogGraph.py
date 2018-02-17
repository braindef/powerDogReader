
import time
from math import sin, pi
from random import random

from pyrrd.rrd import RRD, RRA, DS
from pyrrd.graph import DEF, CDEF, VDEF
from pyrrd.graph import LINE, AREA, GPRINT
from pyrrd.graph import ColorAttributes, Graph

exampleNum = 4
filename = 'A1_B1_S1%s.rrd' % exampleNum
graphfile = 'A1_B1_S1%s-small.png' % exampleNum
graphfileLg = 'A1_B1_S1%s.png' % exampleNum

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
dss = []
ds1 = DS(dsName='kW', dsType='GAUGE', heartbeat=300)
dss.append(ds1)

rras = []
rra1 = RRA(cf='AVERAGE', xff=0.5, steps=1, rows=1460)
rra2 = RRA(cf='AVERAGE', xff=0.5, steps=1, rows=1460)
rras.append(rra1)
rras.append(rra2)

myRRD = RRD(filename, ds=dss, rra=rras, start=startTime)
myRRD.create()

# let's generate some data...
currentTime = startTime
print maxSteps
for i in xrange(maxSteps):
    print i
    currentTime += step
    # lets update the RRD/purge the buffer ever 100 entires
    myRRD.update(debug=False)
    # let's do two different sets of periodic values
    #value1 = int( sin(i/20)*1000 )
    value1 = sin(i/(2*pi))*10+i 
    print value1
    myRRD.bufferValue(currentTime, value1)
# add anything remaining in the buffer
myRRD.update()

myRRD.info()

# Let's set up the objects that will be added to the graph
def1 = DEF(rrdfile=myRRD.filename, vname='myspeed', dsName=ds1.name)
#def2 = DEF(rrdfile=myRRD.filename, vname='mysilliness', dsName=ds2.name)
#def3 = DEF(rrdfile=myRRD.filename, vname='myinsanity', dsName=ds3.name)
#def4 = DEF(rrdfile=myRRD.filename, vname='mydementia', dsName=ds4.name)
#vdef1 = VDEF(vname='myavg', rpn='%s,AVERAGE' % def1.vname)
area1 = AREA(defObj=def1, color='#FFA902', legend='kW')
#area2 = AREA(defObj=def2, color='#DA7202', legend='Raw Data 3')
#area3 = AREA(defObj=def3, color='#BD4902', legend='Raw Data 2')
#area4 = AREA(defObj=def4, color='#A32001', legend='Raw Data 1')
#line1 = LINE(defObj=vdef1, color='#01FF13', legend='Average', stack=True)

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
#g.data.extend([def1, def2, def3, def4, vdef1, area4, area3, area2, area1])
g.data.extend([def1, area1])
g.write()

g.filename = graphfileLg
g.width = 800
g.height = 400
g.write()
