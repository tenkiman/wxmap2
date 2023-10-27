#!/usr/bin/env python

from M import *
MF=MFutils()

from WxMAP2 import *
w2=W2()


def KillLoopGifs(ndayback,type,ropt):

    pltdir=w2.W2LoopPltDir('full')
    sbtdir="%s/sbt"%(w2.ptmpBaseDir)
    if(type == 'all'):
        gifs=glob.glob("%s/*.gif"%(pltdir))
    elif(type == 'prw'):
        gifs=glob.glob("%s/prw.*.gif"%(pltdir))
    elif(type == 'w2loop'):
        gifs=glob.glob("%s/w2loop.*.gif"%(pltdir))
    elif(type == 'gfs.goes'):
        gifs=glob.glob("%s/gfs.goes.*.gif"%(pltdir))
        
    elif(type == 'sbt.goes'):
        gifs=glob.glob("%s/gfs.goes.*"%(sbtdir))
        
        
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

    excludes=['wx','index','prw2','prwLoop','crontab']
    
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
            'doall':        ['A',0,1,'do all clean'],
            'dofullrsync':  ['R',0,1,''],
            'dopublic':     ['P',0,1,''],
            'dowebserver':  ['W',0,1,''],
            }

        self.defaults={
            'dosingledtg':0,
            'dow2flds':1,
            'docleanPlotsHtms':0,

            }

        self.purpose='''
clear/purge wxmap2 web
(c) 2009-2012 Michael Fiorino,NOAA ESRL'''

        self.examples='''
%s -A '''

CL=w2CmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


if(dtgopt != None):
    dtg=dtg_command_prc(dtgopt)
    dosingledtg=1

if(dosingledtg):
    tdtgs=mf.dtg_dtgopt_prc(dtg)
    dtg=tdtgs[0]


#dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddde
# defaults
#

if(ndayback == None):
    ndayback=w2.W2NdayClean
    
ndaybackprw=w2.W2NdayCleanPrwLoop
ndaybacktcanal=w2.W2NdayCleanTcanal
ndaybacktcfilt=w2.W2NdayCleanTcfilt

if(ndayback != w2.W2NdayClean):
    ndaybackprw=ndayback

if(verb):
    print 'NNNNNNNNNNNNNNNNNNNNNNN ndayback:       ',ndayback
    print 'NNNNNNNNNNNNNNNNNNNNNNN ndaybackprw:    ',ndaybackprw
    print 'NNNNNNNNNNNNNNNNNNNNNNN ndaybacktcfilt: ',ndaybacktcfilt
    print 'NNNNNNNNNNNNNNNNNNNNNNN ndaybacktcanal: ',ndaybacktcanal

webbdir=w2.W2BaseDirWeb
if(dopublic):
    webbdir=w2.wxhWebPub

if(dowebserver): webbdir=w2.EsrlHttpIntranetDocRoot

os.chdir(webbdir)


if(dosingledtg):
    tcfiltdirs=glob.glob("tc/tcfilt/%s/%s"%(dtg[0:4],dtg))
    tcanalbdirs=glob.glob("tc/tcanal/%s/%s"%(dtg[0:4],dtg))
    mask="web_*/%s"%(dtg)
    webdirs=glob.glob(mask)
    pltdirs=glob.glob("plt_*/%s"%(dtg))
else:
    tcfiltdirs=glob.glob("tc/tcfilt/%s/??????????"%(curdtg[0:4]))
    tcanaldirs=glob.glob("tc/tcanal/%s/??????????"%(curdtg[0:4]))
    webdirs=glob.glob("web_*/??????????")
    pltdirs=glob.glob("plt_*/??????????")


    
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#
# -- clean up gfs sbt pngs in /ptmp
#
KillLoopGifs(ndayback,'sbt.goes',ropt)

#-- kill big anim.gif
#

KillLoopGifs(ndaybackprw,'prw',ropt)
KillLoopGifs(ndayback,'w2loop',ropt)
KillLoopGifs(ndayback,'gfs.goes',ropt)

#-- html and plts
#

KillDirs(webdirs,ndayback,ropt,dosingledtg)
KillDirs(pltdirs,ndayback,ropt,dosingledtg)


#-- tcfilt plts
#
KillDirs(tcfiltdirs,ndaybacktcfilt,ropt,dosingledtg)

#-- tcanal plts
#
KillDirs(tcanaldirs,ndaybacktcanal,ropt,dosingledtg)

#-- html files
#
if(dosingledtg):
    htmfiles=glob.glob("*%s*.htm*"%(dtg))
else:
    htmfiles=glob.glob('*.htm*')
    
KillFiles(htmfiles,ndayback,ropt,dosingledtg)

if(dofullrsync and w2.W2doW3RapbRsync):
    os.chdir(curdir)
    cmd="w2.rsync.web.2.outside.dtg.py cur -A"
    mf.runcmd(cmd,ropt)


sys.exit()
