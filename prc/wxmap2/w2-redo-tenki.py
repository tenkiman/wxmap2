#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# -- command line setup
#

class w2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['dtgopt',    'dtgopt'],
            2:['model',    'model to redo'],
        }

        self.options={
            'verb':                 ['V',0,1,'verb=1 is verbose'],
            'override':             ['O',0,1,'override for models'],
            'ropt':                 ['N','','norun',' norun is norun'],
        }

        self.purpose='''
redo tc, etc processing on tenki
(c) 2009-%s Michael Fiorino,NOAA ESRL CIRES'''%(w2.curyear)

        self.examples='''
%s cur12 '''

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# -- cmdline
#

argv=sys.argv

CL=w2CmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


MF.sTimer('redo-ALL')

prcdirtd=w2.PrcDirTcdatW2
prcdirtt=w2.PrcDirTctrkW2
prcdirtg=w2.PrcDirTcgenW2
prcdirld=w2.PrcDirTcdiagW2
prcdirfa=w2.PrcDirFldanalW2
prcdirwb=w2.PrcDirWebW2

idtgopt=dtgopt
dtgs=mf.dtg_dtgopt_prc(dtgopt)

overOpt=''
if(override): overOpt='-O'
for dtg in dtgs:
    
    MF.sTimer('redo-%s'%(dtg))
    # -- first do the tracking...
    #

    MF.sTimer('redo-%s'%(dtg))
    MF.ChangeDir(prcdirtt)
    cmd="w2-tc-runTrks.py %s %s %s"%(dtg,model,overOpt)
    mf.runcmd(cmd,ropt)
    MF.dTimer('redo-%s'%(dtg))
    
    if(model == 'gfs2'):
        # -- now the loops
        #
        MF.sTimer('redo-loops-%s'%(dtg))
        MF.ChangeDir(prcdirfa)
        cmd="w2-prw-loop.py %s all -A %s"%(dtg,overOpt)
        mf.runcmd(cmd,ropt)
        
        cmd="w2-gfs-goes-loop.py %s all -A %s"%(dtg,overOpt)
        mf.runcmd(cmd,ropt)
        MF.dTimer('redo-loops-%s'%(dtg))
    
    # -- tcgen
    #
    MF.sTimer('redo-tcgen-%s'%(dtg))
    MF.ChangeDir(prcdirtg)
    cmd="w2-tc-tcgen2.py %s %s %s -C"%(dtg,model,overOpt)
    mf.runcmd(cmd,ropt)
    MF.dTimer('redo-tcgen-%s'%(dtg))
    
    # -- tcdiag
    #
    MF.sTimer('redo-tcdiag-%s'%(dtg))
    MF.ChangeDir(prcdirld)
    cmd="w2-tc-lsdiag.py %s %s %s -C"%(dtg,model,overOpt)
    mf.runcmd(cmd,ropt)
    MF.dTimer('redo-tcdiag-%s'%(dtg))
    
    # -- wxmap2 plots
    #
    MF.sTimer('redo-plots-%s'%(dtg))
    MF.ChangeDir(prcdirfa)
    cmdplt="w2-plot.py %s %s %s"%(dtg,model,overOpt)
    mf.runcmd(cmdplt,ropt)

    plot='op06'
    tau=0
    cmdplt="w2-plot.py %s %s -t %d -p %s %s"%(dtg,model,tau,plot,overOpt)
    mf.runcmd(cmdplt,ropt)
    MF.dTimer('redo-plots-%s'%(dtg))
    
    # -- now the web...
    #
    MF.ChangeDir(prcdirwb)
    webopt='-u'
    cmdplt="w2-web.py %s %s "%(dtg,webopt)
    mf.runcmd(cmdplt,ropt)
    MF.dTimer('redo-%s'%(dtg))
    
    
MF.dTimer('redo-ALL')

