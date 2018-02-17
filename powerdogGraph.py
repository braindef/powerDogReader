#coding=utf-8
from pyrrd.rrd import RRD, RRA, DS
from pyrrd.graph import DEF, CDEF, VDEF
from pyrrd.graph import LINE, AREA, GPRINT
from pyrrd.graph import ColorAttributes, Graph

#Abbreviations
#-------------

#RRD: Round Robin Database
#RRA: Round Robin Archive
#DS: Data Source
#DST: Data Source Type
#min: Minimum Acceptable Value
#max: Maximum Acceptable Value

#CF: Consolidation Function (Consolidates the values from the
#PDP: Primary Data Point  
#XFF: xfiles factor ( this is the percentage of PDPs that can be unknown without making the recorded value unknown. )
#Steps: Defines how many Primary Data Points (PDPs) are consolidated using the Consolidation Function (CF) to create the stored value.
#Rows: Defines the number of Rows (records) stored in this RRA.

#CDP: Consolidated Data Point

#DEF: DEF:var_name_1=some.rrd:ds_name:CF // DEF:inbytes=mrtg.rrd:in:AVERAGE
#cdef: CDEF:var_name_2=RPN_expression // CDEF:inBITS=inBYTES,8,*

#rra: 
#rras
#vname: 

exampleNum = 1
filename = 'example%s.rrd' % exampleNum
graphfile = 'example%s.png' % exampleNum

# Let's create and RRD file and dump some data in it     https://apfelboymchen.net/gnu/rrd/create/
dss = []  #Data Sources
rras = [] #
ds1 = DS(dsName='kW', dsType='GAUGE', heartbeat=600)    # https://www.heise.de/make/artikel/Kurvenzeichner-2714517.html
#ds2 = DS(dsName='kWh', dsType='COUNTER', heartbeat=600)
dss.append(ds1)
#dss.append(ds2)
rra1 = RRA(cf='AVERAGE', xff=0.5, steps=1, rows=144)      # PDP, alle 10 minuten einen Datenpunkt, für einen Tag                     Anleitung: https://oss.oetiker.ch/rrdtool/doc/rrdcreate.en.html
rra2 = RRA(cf='AVERAGE', xff=0.5, steps=6, rows=24)       # CDP, immer 6 Punkte (1h) zu einem zusammenfassen, das 24h lang
rra3 = RRA(cf='AVERAGE', xff=0.5, steps=24, rows=30)      # CDP, immer 24 Punkte (1 Tag) zu einem zusammenfassen, das 30 Tage lang
rra4 = RRA(cf='AVERAGE', xff=0.5, steps=30, rows=12)      # CDP, immer 30 Punkte (1 Monat) zu einem zusammenfassen, das 12 Monate lang
rra5 = RRA(cf='AVERAGE', xff=0.5, steps=12, rows=100)     # CDP, immer 12 Punkte (1 yahr) zu einem zusammenfassen, das 100 Jahre lang

rras.append(rra1)
rras.append(rra2)
rras.append(rra3)
rras.append(rra4)
rras.append(rra5)

myRRD = RRD(filename, ds=dss, rra=rras, start=920804400)
myRRD.create()
myRRD.bufferValue('920805600', '12363')
myRRD.bufferValue('920805900', '12363')
myRRD.bufferValue('920806200', '12373')
myRRD.bufferValue('920806500', '12383')
myRRD.bufferValue('920806800', '12393')
myRRD.bufferValue('920807100', '12399')
myRRD.bufferValue('920807400', '12405')
myRRD.bufferValue('920807700', '12411')
myRRD.bufferValue('920808000', '12415')
myRRD.bufferValue('920808300', '12420')
myRRD.bufferValue('920808600', '12422')
myRRD.bufferValue('920808900', '12423')
myRRD.update()

# Let's set up the objects that will be added to the graph
def1 = DEF(rrdfile=myRRD.filename, vname='myspeed', dsName=ds1.name)
#cdef1 = CDEF(vname='kmh', rpn='%s,3600,*' % def1.vname)
#vdef1 = VDEF(vname='mymax', rpn='%s,MAXIMUM' % def1.vname)
line1 = LINE(value=100, color='#990000', legend='Maximum Allowed')
#area1 = AREA(defObj=cdef1, color='#006600', legend='Good Speed')
#gprint1 = GPRINT(vdef1, '%6.2lf kph')
#gprint1 = GPRINT(def1, '%6.2lf kph')

# Now that we've got everything set up, let's make a graph
g = Graph(graphfile, start=920805000, end=920810000, vertical_label='km/h')
#g.data.extend([def1, cdef1,  vdef1,  line1, area1, gprint1])
g.data.extend([def1,  line1 ])
g.write()

