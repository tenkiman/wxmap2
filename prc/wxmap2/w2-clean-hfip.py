#!/usr/bin/env python

from M import *
MF=MFutils()

from WxMAP2 import *
w2=W2()

def KillLoopGifs(ndayback,type,ropt):

    pltdir=w2.W2LoopPltDir('full')
    if(type == 'all'):
        gifs=glob.glob("%s/*.gif"%(pltdir))
    elif(type == 'prw'):
        gifs=glob.glob("%s/prw.*.gif"%(pltdir))
    elif(type == 'w2loop'):
        gifs=glob.glob("%s/w2loop.*.gif"%(pltdir))
    elif(type == 'gfs.goes'):
        gifs=glob.glob("%s/gfs.goes.*.gif"%(pltdir))

    for gif in gifs:
        rc=mf.PathCreateTime(gif)
        # 20090127 better to use modify time.  create is when i rsync the files from my usb drive -> mac
        #
        rc=mf.PathModifyTime(gif)
        gdtg=rc[2]
        age=mf.dtgdiff(gdtg,curdtg)*(1/24.0)
        if(age > ndayback):
            print 'unlinking: ',gif," age(d): %6.1f "%(age)
            if(ropt != 'norun'):
                os.unlink(gif)
                   
    

def KillDirs(dirs,ndayback,ropt,dosingledtg=0):
    
    for dir in dirs:
        tt=dir.split('/')
        ltt=len(tt)
        kdir=tt[ltt-2]
        kdtg=tt[ltt-1]

        try:
            int(kdtg[0:4])
        except:
            print 'WWW(w2.clean.web.py.KillDirs()): kdtg: ',kdtg,' not a DTG...press...'
            continue
        
        kdtgdiff=mf.dtgdiff(kdtg,curdtg)/24.0

        if(kdtgdiff > ndayback or dosingledtg):
            print 'kkkkkkkkkkkkkkkk killing: ',dir
            cmd="rm -r %s"%(dir)
            mf.runcmd(cmd,ropt)
    
def KillFiles(files,ndayback,ropt,dosingledtg=0):

    excludes=['wx','index','prw2','prwLoop']
    
    for file in files:
        tt=file.split('.')
        kfile=tt[0]
        doit=1

        if(len(tt) >= 3):
            kdtg=tt[len(tt)-2]
        elif(kfile in excludes):
            doit=0
            
        if(doit):
            
            if(len(kdtg) != 10):
                baddtg=1
                kdtgdiff=-999
            else:
                kdtgdiff=mf.dtgdiff(kdtg,curdtg)/24.0
                baddtg=0
                
            if(kdtgdiff > ndayback or baddtg):
                print 'kkkkkkkkkkkkkkkk killing: ',file
                cmd="rm  %s"%(file)
                mf.runcmd(cmd,ropt)
        else:
            print 'SSSSSSSSSSSS skipping ',file


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
            'ndayback':     ['n:',None,'f',''],
            'dtgopt':       ['d:',None,'a','single dtg'],
            'doit':         ['X',0,1,'execute the clean'],
            }

        self.defaults={
            'dosingledtg':0,
            }

        self.purpose='''
clear/purge wxmap2 nwp2 dat on tenki
(c) 2009-%s Michael Fiorino,NOAA ESRL'''%(self.dtg()[0:4])

        self.examples='''
%s -A '''

CL=w2CmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


if(dtgopt != None):
    dtg=mf.dtg_command_prc(dtgopt)
    dosingledtg=1

if(dosingledtg):
    tdtgs=mf.dtg_dtgopt_prc(dtg)
    dtg=tdtgs[0]


#dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddde
# defaults
#

if(w2.onTenki or w2.onGmu and ndayback == None): ndayback=15


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

if(ropt == '' and not(doit)):
    print 'WWW -- must use -X flag to execute...'
    sys.exit()

wbdir=w2.W2BaseDirWebConfig

w2jtdiagDATDir="%s/jtdiag"%(wbdir)
rc=MF.ChangeDir(w2jtdiagDATDir)
jtdirs=glob.glob("????/??????????")
jtdirs.sort()
KillDirs(jtdirs,ndayback,ropt,dosingledtg)
    
w2tddiagDATDir="%s/tcdiag"%(wbdir)
rc=MF.ChangeDir(w2tddiagDATDir)
tddirs=glob.glob("????/??????????")
tddirs.sort()
KillDirs(tddirs,ndayback,ropt,dosingledtg)

w2tcepsDATDir="%s/tceps"%(wbdir)
rc=MF.ChangeDir(w2tcepsDATDir)
tedirs=glob.glob("????/??????????")
tedirs.sort()
KillDirs(tedirs,ndayback,ropt,dosingledtg)

w2tcgenDATDir="%s/tcgen"%(wbdir)
rc=MF.ChangeDir(w2tcgenDATDir)
tgdirs=glob.glob("????/??????????")
tgdirs.sort()
KillDirs(tgdirs,ndayback,ropt,dosingledtg)


sys.exit()

