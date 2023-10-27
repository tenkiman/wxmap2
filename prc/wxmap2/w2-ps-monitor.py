#!/usr/bin/env python

from M import *
MF=MFutils()

from WxMAP2 import *
w2=W2()


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#
class w2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            }

        self.options={
            'verb':         ['V',0,1,'verb=1 is verbose'],
            'ropt':         ['N','','norun',' norun is norun'],
            'doit':         ['X',0,1,'do all clean'],
            'sleepytime':   ['S:',15,'f',' how long to sleep'],
            'nonPSevents':  ['n',0,1,'print out dtg-plus time for non PS events'],
            }

        self.defaults={
            'dosingledtg':0,
            'dow2flds':1,
            'docleanPlotsHtms':0,

            }

        self.purpose='''
log python processes
(c) 2009-2014 Michael Fiorino,NOAA ESRL'''

        self.examples='''
%s -X -S 15 # output every 15 sec'''

CL=w2CmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

# -- setup
#
dol2=0
docagips=0

# -- kill previous runs
#
MF.sTimer("w2-monitor-%s"%(curdtg))


rc=MF.whoIsRunningNew(pyfile, jobopt=None, killjob=-1)

#rc=MF.chkRunning(pyfile, strictChkIfRunning=1,
                 #killjob=-1, verb=1,
                 #nminWait=0)
MF.dTimer("w2-monitor-%s"%(curdtg))

if(not(doit)):
    sys.exit()
    
logpath="%s/w2.ps.monitor.%s.%s.%03d.txt"%(w2.ptmpBaseDir,w2.W2Host.split('.')[0],curdtg,sleepytime)
LP=open(logpath,'a')
print 'logpath',logpath


while(1):

    if(nonPSevents):
        curdtgline='CurDTG+phms: %s'%(mf.dtg('dtg.phms'))+' <<<<<<<<ccccccccccccccccccccccccccccccccccccccccccccccccccccc\n'
        LP.writelines(curdtgline)
        LP.flush()

    # -- grep ps output and output to log
    #
    cmd='ps -ef | grep python | grep -v root | grep -v keeplive | grep -v grep | grep -v wing | grep -v %s | grep -v defunc | grep -v /usr/bin/python | grep -v globus-connect | grep -v jupyter'%(pyfile)
    cards=MF.runcmdLogOutput(cmd,ropt)

    if(len(cards) > 0):

        curdtgline='CurDTG+phms: %s'%(mf.dtg('dtg.phms'))+' <<<<<<<<ccccccccccccccccccccccccccccccccccccccccccccccccccccc\n'
        LP.writelines(curdtgline)
        LP.flush()
        
        for card in cards:
            if(verb): print card
            LP.writelines(card)    
        
        LP.flush()


    time.sleep(sleepytime)



    
