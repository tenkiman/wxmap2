#!/usr/bin/env python

from tcbase import *

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
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
            'doit':         ['X',0,1,'run...'],
            'year':         ['y:',None,'a','year to clean'],
        }

        self.purpose='''
purpose -- rsync from kaze-kishou|wxmap2 tc data sets'''

        self.examples='''
%s -V -N'''
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main
#

CL=w2CmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

#w2.ls('Tc')

sdirs=[
    [w2.TcAdecksNhcDir,5],
    [w2.TcAdecksJtwcDir,5],
    [w2.TcBdecksNhcDir,5],
    [w2.TcBdecksJtwcDir,5],
    [w2.TcAdecksCmcDir,5],
    [w2.TcAdecksEcmwfDir,5],
    [w2.TcAdecksuKmoDir,5],
    [w2.TcAdecksEsrlDir,5],
    [w2.TcAdecksLocalDir,5],
    [w2.TcAdecksFinalDir,5],
    ["%s/%s"%(w2.TcDatDir,'adeck/tmtrkN'),5],
    ["%s/%s"%(w2.TcDatDir,'adeck/mftrkN'),5],
    ["%s/%s"%(w2.TcDatDir,'reftrk/tmtrkN'),5],
    # -- atcf-form
    [TcAdecksAtcfFormDir,5],
    
    [w2.TcTcepsDatDir,6],
    
    [w2.TcMtcswaLateDatDir,1],

    [w2.TcMtcswaDatDir,3],

    [w2.TcTcanalDatDir,4],

    [w2.TcTcdiagDatDir,2],

    ["%s/%s"%(w2.TcDatDir,'tcvitals'),7],
    ["%s/%s"%(w2.TcDatDir,'tcgen'),7],
]

ropt='norun'
if(doit): ropt=''

for (sdir,stype) in sdirs:

    sdirKill="%s/%s"%(sdir,year)
    
    print
    print 'SSSSSSSSSSSSSSSSSSSSSSSSSSS: ',sdirKill
    print
    
    if(stype == 1):
        kfiles=glob.glob("%s/*%s*"%(sdirKill,year))
        for kfile in kfiles:
            cmd="rm %s"%(kfile)
            mf.runcmd(cmd,ropt)

    elif(stype == 2):
        kdirs=glob.glob("%s/%s??????"%(sdirKill,year))
        kdirs.sort()
        
        for kdir in kdirs:
            cmd="rm -r %s"%(kdir)
            mf.runcmd(cmd,ropt)
            
    elif(stype == 3):
        kdirs=glob.glob("%s/*"%(sdirKill))
        kdirs.sort()
        
        for kdir in kdirs:
            cmd="rm -r %s"%(kdir)
            mf.runcmd(cmd,ropt)
            
    elif(stype == 4):
        kdirs=glob.glob("%s/%s??????"%(sdir,year))
        kdirs.sort()
        for kdir in kdirs:
            cmd="rm -r %s"%(kdir)
            mf.runcmd(cmd,ropt)
            
    elif(stype == 5):
        cmd="rm -r %s"%(sdirKill)
        mf.runcmd(cmd,ropt)

    elif(stype == 6):
        kdirs=glob.glob("%s/*/%s"%(sdir,year))
        kdirs.sort()
        for kdir in kdirs:
            cmd="rm -r %s"%(kdir)
            mf.runcmd(cmd,ropt)

    elif(stype == 7):
        kfiles=glob.glob("%s/*%s??????*"%(sdir,year))
        for kfile in kfiles:
            cmd="rm %s"%(kfile)
            mf.runcmd(cmd,ropt)

    
sys.exit()
