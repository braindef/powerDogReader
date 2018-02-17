import time

from pyrrd.rrd import RRD
myRRD = RRD('A1_B1_S14.rrd')

myRRD.bufferValue(time.time(),  10000)
myRRD.update()


myRRD.info()

"""
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


"""

