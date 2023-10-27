#!/usr/bin/env python

from M2 import setModel2
from ptcCL import *

import matplotlib.dates as datespy

from datetime import datetime

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
            'stmopt':         ['S:',None,'a','stmopt'],
            'dobt':           ['b',0,1,'dobt list bt only'],
            'dols':           ['l',0,1,'do ls of TCs...'],
            'model':          ['m:','gfs2','a','stmopt'],
            'dosmooth':       ['M',0,1,' do smoothingstmopt'],
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


stmids=['09W.2015','C4W.2015','C5W.2015']

for stmid in stmids:
    year='2015'
    cards=[]
    path='/home/amb/michael.natoli/lsdiag/data/'+year+'/'+stmid.upper()+'.'+model+'.dat'
    cards=open(path,'r').readlines()

    storm=stormAnl(cards)

    if(text):
        storm.printCard()

    print storm.getMeanLabel()
    print storm.getPtcMean()

    idev=storm.getIdev()
    
    print '\n'
    var=disp

    if var != None:

        dates=[]
        if stmid == '09W.2015':
            end='2015070400'
            col='.c-'
        elif stmid == 'C5W.2015':
            end='2015063012'
            col='.g-'
        else:
            end='2015070200'
            col='.r-'

        for dtg in storm.dtgs[:storm.dtgs.index(end)]:
            year=int(dtg[:4])
            month=int(dtg[4:6])
            day=int(dtg[6:8])
            hour=int(dtg[8:])
            date=datetime(year,month,day,hour)
            dates.append(date)

        dates=datespy.date2num(dates)
        
        
        ys=storm.tmseries[var]
        ys=np.array(storm.tmseries[var]).astype(np.double)
        if(dosmooth): ys=smooth(ys)

        plot.plot_date(dates,ys[:storm.dtgs.index(end)],col,linewidth=2.0)


yearsFmt = datespy.DateFormatter('%m/%d')
#fig, ax = plot.subplots()
ax=plot.gca()

ax.xaxis.set_major_locator(datespy.DayLocator(interval=2))
ax.xaxis.set_major_formatter(yearsFmt)
ax.xaxis.set_minor_locator(datespy.DayLocator())

plot.xlabel('Date')
plot.ylabel(storm.longvar[storm.vars.index(var)])
plot.title('94W (Red) and 95W (Green) during Fujiwhara Interaction')

plot.show()

