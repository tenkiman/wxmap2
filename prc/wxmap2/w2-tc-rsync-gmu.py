#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from M2 import setModel2

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
            'doit':         ['X',0,1,'execute'],
            'doAll':        ['A',0,1,'do ALL dirs in tc/'],
            'reverse':      ['R',0,1,' reverse direction'],
            }


        self.purpose='''
rsync from tenki7 to argo.orc.gmu.edu
(c) 2009-2021 Michael Fiorino,wxmap2.com'''

        self.examples='''
%s -X # doit '''

CL=w2CmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

rsyncOpt='-alv --timeout=120'
if(reverse): rsyncOpt='-alv --timeout=120'
if(ropt == 'norun'): rsyncOpt='-alvn'
#rsyncOpt="%s --size-only --update"%(rsyncOpt)
rsyncOpt="%s --update"%(rsyncOpt)


sdir=w2.TcDatDir

tdir='mfiorino@argo.orc.gmu.edu:/scratch/mfiorino/dat/tc'
tdir='mfiorino@hopper1.orc.gmu.edu:/scratch/mfiorino/dat/tc'

tcdirs={
    'DSs':'a',
    'adeck':'j',
    'adeck/atcf-form':'n',
    'adeck/cmc':'n',
    'adeck/ecmwf':'n',
    'adeck/esrl':'n',
    'adeck/jtwc':'j',
    'adeck/mftrkN':'n',
    'adeck/tmtrkN':'n',
    'adeck/ncep':'n',
    'adeck/nhc':'n',
    'bdeck/jtwc':'j',
    'bdeck/nhc':'n',
    'bdeck2':'n',
    'bt':'n',
    'carq':'n',
    'cira/mtcswa':'n',
    'cira/mtcswa2':'n',
    'cmc':'n',
    'com/nhc':'n',
    'dis/nhc':'n',
    'ecmwf/wmo-essential':'n',
    'edeck/jtwc':'j',
    'edeck/nhc':'n',
    'fdeck/jtwc':'j',
    'fdeck/nhc':'n',
    'jtwc':'a',
    'mdeck':'j',
    'nhc':'n',
    'names':'a',
    'ncep/tigge':'n',
    'reftrk':'a',
    'stext/jtwc':'j',
    'tcdiag':'n',
    'tceps':'n',
    'ukmo/tigge':'n',
}

yy=curdtg[0:4]
yyp1=int(yy)+1
yyp1=str(yyp1)
mm=curdtg[4:6]
dd=curdtg[6:8]
        

MF.sTimer('GMU tc push')
if(doAll):
    if(reverse):
        ss=sdir
        tt=tdir
        tdir=ss
        sdir=tt
        
    tcanalEx='''--exclude "tcanal"'''
    cmd="rsync %s %s %s/ %s/"%(rsyncOpt,tcanalEx,sdir,tdir)
    mf.runcmd(cmd,ropt)

    tcanalEx='''--exclude "*.dat"'''
    sdirt="%s/tcanal"%(sdir)
    tdirt="%s/tcanal"%(tdir)
    cmd="rsync %s %s %s/ %s/"%(rsyncOpt,tcanalEx,sdirt,tdirt)
    mf.runcmd(cmd,ropt)
    
else:
    
    tcdirKeys=tcdirs.keys()
    tcdirKeys.sort()
    for tcdir in tcdirKeys:
        sbdir='%s/%s/'%(sdir,tcdir)
        tbdir='%s/%s/'%(tdir,tcdir)
        tctype=tcdirs[tcdir]
    
        if(tctype == 'a'):
            sbdirs={
                sbdir:tbdir,
                }
        elif(tctype == 'n'):
            sbdirs={
            "%s/%s"%(sbdir,yy):'%s/%s'%(tbdir,yy),
            }
        elif(tctype == 'j'):
            sbdirs={
        '%s/%s'%(sbdir,yy):'%s/%s'%(tbdir,yy),
        '%s/%s'%(sbdir,yyp1):'%s/%s'%(tbdir,yyp1)
            }
            
        for sbdir in sbdirs.keys():
            tdirtc=sbdirs[sbdir]
            tdirtc="%s/"%(tdirtc)
            sdirtc="%s/"%(sbdir)
            sdirtc=sdirtc.replace('//','/')
            tdirtc=tdirtc.replace('//','/')

            if(reverse):
                tt=tdirtc
                ss=sdirtc
                sdirtc=tt
                tdirtc=ss
                
            cmd="rsync %s %s %s"%(rsyncOpt,sdirtc,tdirtc)
            mf.runcmd(cmd,ropt)
    
    
MF.dTimer('GMU tc push')

