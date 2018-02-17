
import time

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
rra1 = RRA(cf='AVERAGE', xff=0.5, steps=1, rows=144) #alle 10 Minuten ein Wert
rra2 = RRA(cf='AVERAGE', xff=0.5, steps=6, rows=24)  #24h mal 1h
rra2 = RRA(cf='AVERAGE', xff=0.5, steps=24, rows=30) #30 Tage mal 24h
rra2 = RRA(cf='AVERAGE', xff=0.5, steps=30, rows=12) #12 Monate mal 30 Tage
rra2 = RRA(cf='AVERAGE', xff=0.5, steps=12, rows=10) #10 Jahre mal 12 Monate
rras.append(rra1)
rras.append(rra2)
rras.append(rra2)
rras.append(rra2)
rras.append(rra2)

myRRD = RRD(filename, ds=dss, rra=rras, start=startTime)
myRRD.create()

myRRD.update()
myRRD.info()


