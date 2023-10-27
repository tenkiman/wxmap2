#!/usr/bin/env python

from M import *

from M2 import setModel2

from tcbase import *

from cardanl import *

import matplotlib.pyplot as plot 


MF=MFutils()


class MdeckCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv

        self.argopts={
            #1:['dtgopt',    'no default'],
            }

        self.defaults={
            'lsopt':'s',
            'doupdate':0,
            'tcvPath':None,
            }

        self.options={
            'dtgopt':         ['d:',None,'a','year'],
            'verb':           ['V',0,1,'verb=1 is verbose'],
            'ropt':           ['N','','norun',' norun is norun'],
            'year':           ['y:','2015','a','Year to display 4 panels of'],
            'dobt':           ['b',0,1,'dobt list bt only'],
            'dols':           ['l',0,1,'do ls of TCs...'],
            'model':          ['m:','gfs2','a','stmopt'],
            'ls9x':           ['9',0,1,'ls9x'],
            'notdoCARQonly':     ['C',0,1,'control on summary plot'],
            'disp':          ['p:',None,'a','plot the variable'],
            'scaled':        ['s',0,1,'scale all storms to same axis 0-1.0'],
            'text':          ['t',0,1,'print out card'],
            }

        self.purpose='''
check status of tmtrkN/mftrkN/TCdiag/TCgen'''
        
        self.examples='''
%s -S 09w.15
%s '''


#################################################################################################################
# main

argv=sys.argv
CL=MdeckCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)

doBT=0
#if(not(dobt)):  doBT=1  # default dobt=0 doBT=1  -- replace all 
if(notdoCARQonly): doBT=1 #Changed the default to doBT=1, and do -C option to   

ymin=9e10
ymax=-9e10
xmin=9e10
xmax=-9e10

yr=year[2:]
stmopts=[]
stmopts.append('w.'+yr)
stmopts.append('e.'+yr)
stmopts.append('s.'+yr)
stmopts.append('l.'+yr)

xidx={}
yidx={}
pnum={}

xidx['w.'+yr]=0
yidx['w.'+yr]=0
xidx['e.'+yr]=0
yidx['e.'+yr]=1
xidx['s.'+yr]=1
yidx['s.'+yr]=0
xidx['l.'+yr]=1
yidx['l.'+yr]=1

pnum['w.'+yr]=1
pnum['e.'+yr]=2
pnum['s.'+yr]=3
pnum['l.'+yr]=4

for stmopt in stmopts:
    print '**************************************', stmopt
    plot.subplot(2,2,pnum[stmopt])
    tD=TcData(stmopt=stmopt)

    stmids=tD.makeStmListMdeck(stmopt)
    stmids.sort()

    meandevt=[]
    meandiss=[]
    countdevt=[]
    countdiss=[]

    for stmid in stmids:

        year=stmid[4:]
        cards=[]
        if int(year)<2015:
            model='ecmt'
        path='/home/amb/michael.natoli/lsdiag/data/'+year+'/'+stmid.upper()+'.'+model+'.dat'
        cards=open(path,'r').readlines()

        storm=stormAnl(cards)
        
        if(text):
            storm.printCard()

        # print storm.getMeanLabel()
        # smean=storm.getPtcMean()
        # print smean
        # print '\n'            

        idev=storm.getIdev()
        pTCdev=storm.pTCdev


        var=disp

        for i in range(idev+1):
            if storm.tmseries[var][idev-i] != None:
                if pTCdev == 1:
                    if i >= len(meandevt):
                        meandevt.append(storm.tmseries[var][idev-i])
                        countdevt.append(1.)
                    else:
                        meandevt[i]=meandevt[i]+storm.tmseries[var][idev-i]
                        countdevt[i]=countdevt[i]+1.
                else:
                    if i >= len(meandiss):
                        meandiss.append(storm.tmseries[var][idev-i])
                        countdiss.append(1.)
                    else:
                        meandiss[i]=meandiss[i]+storm.tmseries[var][idev-i]
                        countdiss[i]=countdiss[i]+1.

        if var !=None:
            ymin1=storm.getMin(var)
            ymax1=storm.getMax(var)
            xmax1=storm.idev*6

            if ymax1>ymax and ymax1 is not None:
                ymax=ymax1

            if ymin1 < ymin and ymin1 is not None:
                ymin=ymin1

            if(scaled):
                storm.plotScaledVar(var)
            else:
                storm.plotVar(var)
                if xmax1>xmax:
                    xmax=xmax1
                    
    
    for i in range(len(meandevt)):
        meandevt[i]=meandevt[i]/countdevt[i]
    for i in range(len(meandiss)):
        meandiss[i]=meandiss[i]/countdiss[i]

    if(disp):
        storm.setYaxis(storm.mins[var],storm.maxes[var])
        xmax=168
        if not scaled:
            storm.setXaxis(0,xmax)
            storm.ax.invert_xaxis()

            colors={'dred':(0.6,0.0,0.0),'dgreen':(0.0,0.35,0.0)}

        xsdiss=np.arange(0,len(meandiss)*6,6)
        ysdiss=np.array(meandiss).astype(np.double)
        maskdiss=np.isfinite(ysdiss)

        xsdevt=np.arange(0,len(meandevt)*6,6)
        ysdevt=np.array(meandevt).astype(np.double)
        maskdevt=np.isfinite(ysdevt)


        plot.plot(xsdiss[maskdiss],ysdiss[maskdiss],color=colors['dred'],linestyle='-',marker='.',linewidth=4.0)
        plot.plot(xsdevt[maskdevt],ysdevt[maskdevt],color=colors['dgreen'],linestyle='-',marker='.',linewidth=4.0)
        
        storm.labelPlot()
storm.showPlot()
