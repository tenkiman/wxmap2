#!/usr/bin/env python

from M import *
MFs=MFutils()

MFs.sTimer('startup')
from WxMAP2 import *
w2=W2()
MFs.dTimer('startup')


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class w2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['diropt',    'DTG (YYYYMMDDHH)'],
            }
            
        self.options={
            'verb':         ['V',0,1,'verb=1 is verbose'],
            'ropt':         ['N','','norun',' norun is norun'],
            'dtgopt':       ['d:',None,'a','dtgopt'],
            'subdiropt':    ['S:',None,'a','subdiropt']
            }


        self.purpose='''
make usage.py report
(c) 2009-2013 Michael Fiorino,NOAA ESRL'''
        
        self.examples='''
%s dat.tc -S adeck         # du of all adeck subdirs
%s nwp2.w2flds -d cur12    # du of w2flds for cur12 dtg
%s nwp2 -S ecmwf           # du of all ecmwf models in nwp2 dir'''


        
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# cmdline
#

argv=sys.argv

CL=w2CmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

if(diropt == 'all'):
    dirs=['dat.tc','nwp2','nwp2.w2flds']
else:
    dirs=[diropt]

MFs.sTimer('all.du')
print 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB at:', mf.dtg('curtime'),' BBBBBBBBBBBBBBB'

totsize=0
for dir in dirs:

    print
    print 'BBBBBBBBBBBBegin dir: %-70s'%(dir),' at:', mf.dtg('curtime'),' BBBBBBBBBBBBBBB','dtgopt: ',dtgopt
    
    if(dir == 'dat'):
        
        sdir=w2.W2BaseDirDat
        if(subdiropt != None):
            sdir="%s/%s"%(sdir,subdiropt)

        canDoDtg=0
    
    elif(dir == 'dat.tc'):
        
        sdir=w2.TcDatDir
        if(subdiropt != None):
            sdir="%s/%s"%(sdir,subdiropt)

        canDoDtg=0
    
    elif(dir == 'nwp2'):
        
        sdir=w2.Nwp2DataBdir
        if(subdiropt != None):
            sdir="%s/%s"%(sdir,subdiropt)
            
        canDoDtg=1

    elif(dir == 'nwp2.w2flds'):
        sdir=w2.Nwp2DataBdir+'/w2flds/dat'
        canDoDtg=1


    if(dtgopt != None and canDoDtg):
        adirs=[]
        dtgs=mf.dtg_dtgopt_prc(dtgopt)
        print 'base sdir: ',sdir
        print
        if(dir == 'nwp2'):
            models=[]
            
            if(subdiropt == None): centers=os.listdir(sdir)
            else:                  centers=[subdiropt]
                
            for center in centers:

                if(subdiropt == None):  mdls=os.listdir("%s/%s"%(sdir,center))
                else:                   mdls=os.listdir(sdir)

                for mdl in mdls:
                    if(subdiropt == None):  model="%s/%s"%(center,mdl)
                    else:                  model=mdl
                    models.append(model)
                    
        elif(dir == 'nwp2.w2flds'):
            models=os.listdir(sdir)
            

        for dtg in dtgs:
            
            for model in models:
                testdir="%s/%s/%s"%(sdir,model,dtg)
                if(MF.ChkDir(testdir,quiet=1)):
                    adirs.append(testdir)
        sdirs=adirs
                 
    else:
        sdirs=[sdir]

    for sdir in sdirs:
        cmd='usage.py %s -T'%(sdir)
        output=MF.runcmdLog(cmd,quiet=1)

        for o in output:
            if(mf.find(o,'Total...')):
                osize=o.split()[2].replace(',','')
                totsize=totsize+int(osize)
            if(len(o) > 0): print o

        print


    mf.PrintCurrency('Grand Total............',amount=totsize)
    print
    print 'DDDDDDDDDDDDDone dir: %-70s'%(dir),'at:', mf.dtg('curtime'),' EEEEEEEEEEEEEEE'
    print

MFs.dTimer('all.du')
