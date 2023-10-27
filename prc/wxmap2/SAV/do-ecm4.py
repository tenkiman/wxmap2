#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from M2 import setModel2

class w2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['dtgopt',    'DTG (YYYYMMDDHH)'],
        }

        self.options={
            'verb':                 ['V',0,1,'verb=1 is verbose'],
            'ropt':                 ['N','','norun',' norun is norun'],
            'dotest':               ['t',0,1,'only do TCs...no plots'],
            'override':             ['O',0,1,'1 - '],
        }


        self.purpose='''
run w2.nwp2.py on tenki to kill off nwp2 fields but save w2flds
(c) 2009-%s Michael Fiorino,NOAA ESRL CIRES'''%(w2.curyear)

        self.examples='''
%s cur12 '''



#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# cmdline
#
maxtau=240
argv=sys.argv

CL=w2CmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr
model='ecm4'
m=setModel2(model)
dtgs=mf.dtg_dtgopt_prc(dtgopt)

for dtg in dtgs:

    MF.sTimer('ALL-do-ecm4: %s'%(dtg))
    # -- check if running and w2flds done already...problem is we kill off the nwp2 fields so will always try to rsync
    #
    rc=w2.ChkIfRunningNWP(dtg,pyfile,model)
    if(rc > 0 and ropt != 'norun'):
        print 'AAA allready running...'
        sys.exit()

    fm=m.DataPath(dtg,dtype='w2flds')
    fd=fm.GetDataStatus(dtg)
    doit=(fd.dslastTau == None or fd.dslastTau < maxtau)
    if(not(doit) and fd.dslastTau == maxtau): doit=0

    if(not(doit) and not(override)): 
        print 'WWW-%s already done for dtg: %s at curtime: %s ...press...'%(CL.pyfile,dtg,CL.curtime)
        sys.exit()

    topt=''
    if(dotest): topt='-t'
        
    overopt=''
    if(override): overopt='-O '
    cmd="w2.nwp2.py %s ecm4 %s %s"%(dtg,topt,overopt)
    mf.runcmd(cmd,ropt)

    cmd="w2.nwp2.py %s ecm4 -K"%(dtg)
    mf.runcmd(cmd,ropt)
    MF.dTimer('ALL-do-ecm4: %s'%(dtg))
