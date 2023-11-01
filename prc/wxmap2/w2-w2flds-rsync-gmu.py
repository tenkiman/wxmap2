#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from M2 import setModel2

def anlGmuOutput(output):

    status=-999
    if(len(output) == 0): return(status)
    if(mf.find(output,'receiving incremental file list')): status=1
    if(mf.find(output,'rsync: change_dir')): status=-1
    if(mf.find(output,'rsync error: ')): status=-2
    if(mf.find(output,'speedup is')): status=1
    
    if(status == -999):
        print 'unable to get status in output:'
        print output
        
    return(status)
    

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#
class w2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',   'dtgopt DTG (YYYYMMDDHH)'],
            2:['model',    'model'],
        }

        self.options={
            'verb':         ['V',0,1,'verb=1 is verbose'],
            'ropt':         ['N','','norun',' norun is norun'],
            'reverse':      ['R',0,1,' reverse direction'],
            }


        self.purpose='''
rsync from tenki6 to tenki7 via  to dat0 (usb3 5 TB drive)
(c) 2009-2019 Michael Fiorino,NOAA ESRL'''

        self.examples='''
%s -N '''

CL=w2CmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

dtgs=mf.dtg_dtgopt_prc(dtgopt)

rsyncOpt='-alv --timeout=120'
if(ropt == 'norun'): rsyncOpt='-alvn'

if(model == 'all'):
    models0618=['gfs2','jgsm','navg','goes']
    models0012=['cgd2','ecm5','gfs2','jgsm','navg','goes']
    
else:
    models0618=[model]
    models0012=[model]
    
    
MF.sTimer('GMU-All')
    
for dtg in dtgs:
    if(MF.is0618Z(dtg)):
        models=models0618
    else:
        models=models0012
    
    for model in models:
        
        m=setModel2(model)
        
        if(model == 'goes'):
            fm=m.DataPath(dtg,dtype='nwp2')
            fd=fm.GetDataStatus(dtg)
            doit=1
            sdir=fm.dbasedir
        else:
            fm=m.DataPath(dtg,dtype='w2flds')
            fd=fm.GetDataStatus(dtg)
    
            doit=fd.dpathexists
            sdir=fd.dbasedir
        
    
        tdir=sdir.replace('/w21','/scratch/mfiorino')
        #tdir="mfiorino@argo.orc.gmu.edu:%s"%(tdir)
        tdir="mfiorino@hopper1.orc.gmu.edu:%s"%(tdir)
    
        if(reverse and not(ropt == 'norun')):
            MF.sTimer('GMU pull for dtg: %s model: %s'%(dtg,model))
            cmd="time rsync %s %s/ %s/"%(rsyncOpt,tdir,sdir)
            output=MF.runcmdLogOutput(cmd,ropt)
            rc=anlGmuOutput(output)

            if(rc == -1):
                print
                print 'WWW -- data did not rsync: ',model,' for: ',dtg,' from mike3 to argo...'
                print
            else:
                print 'rc for dtg: ',dtg,' model: ',model,' rc: ',rc
                
            MF.dTimer('GMU pull for dtg: %s model: %s'%(dtg,model))
            continue
    
        if(doit):
            MF.sTimer('GMU PUSH for dtg: %s model: %s'%(dtg,model))
            cmd="time rsync %s %s/ %s/"%(rsyncOpt,sdir,tdir)
            output=MF.runcmdLogOutput(cmd,ropt)
            rc=anlGmuOutput(output)
            if(rc == 1):
                print 'III-rsync push good...'
            elif(rc == -2):
                print
                print 'EEE -- rsync error in PUSH 2 GMU for: ',model,' dtg: ',dtg,'redo once...'
                print
                cmd="time rsync %s %s/ %s/"%(rsyncOpt,tdir,sdir)
                output=MF.runcmdLogOutput(cmd,ropt)
                rc=anlGmuOutput(output)
                if(rc != 1):
                    print
                    print 'EEE-222 re-rsync failed...press...'
                    print
                    continue
            
            MF.dTimer('GMU PUSH for dtg: %s model: %s'%(dtg,model))
            
        else:
            print 'WWW no data for model: ',model,' dtg: ',dtg,'press...'
            continue

MF.dTimer('GMU-All')
