
import time

from pyrrd.rrd import RRD, RRA, DS
from pyrrd.graph import DEF, CDEF, VDEF
from pyrrd.graph import LINE, AREA, GPRINT
from pyrrd.graph import ColorAttributes, Graph

from pyrrd.rrd import RRD
myRRD = RRD('A1_B1_S14.rrd')

myRRD.bufferValue(time.time(),  10000)
myRRD.update()

myRRD.info()
