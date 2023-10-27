#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

def killTmtrkN(f,bdtg,doit):

    ropt='norun'
    if(doit): ropt=''
    n=0
    (dir,fdtg)=os.path.split(f)


    dt=mf.dtgdiff(bdtg,fdtg)
    print f,bdtg,fdtg,dt
    if(dt < 0):
        cmd="rm -r %s"%(f)
        if(doit):
            n=n+1
            print 'RRR(tmtrkN) deleting: ',f
            mf.runcmd(cmd,ropt)
        else:
            print 'WWW(tmtrkN) will delete: ',f
            mf.runcmd(cmd,ropt)


def killTcanalDirs(f,bdtg,doit):

    ropt='norun'
    if(doit): ropt=''
    n=0
    (dir,fdtg)=os.path.split(f)


    dt=mf.dtgdiff(bdtg,fdtg)
    print f,bdtg,fdtg,dt
    if(dt < 0):
        cmd="rm -r %s"%(f)
        if(doit):
            n=n+1
            print 'RRR(tcanalDir) deleting: ',f
            mf.runcmd(cmd,ropt)
        else:
            print 'WWW(tcanalDir) will delete: ',f
            mf.runcmd(cmd,ropt)


def killTcanalFiles(f,bdtg,doit):

    ropt='norun'
    if(doit): ropt=''
    n=0
    tt=f.split('.')
    if(len(tt) == 3):
        fdtg=tt[1]
    if(len(tt) == 2):
        fdtg=bdtg


    dt=mf.dtgdiff(bdtg,fdtg)
    print f,bdtg,fdtg,dt
    if(dt <= 0):
        cmd="rm  %s"%(f)
        if(doit):
            n=n+1
            print 'RRR(tcanalFile) deleting: ',f
            mf.runcmd(cmd,ropt)
        else:
            print 'WWW(tcanalfile) will delete: ',f
            mf.runcmd(cmd,ropt)



def killCira(f,bdtg,doit):

    n=0
    (dir,ffile)=os.path.split(f)
    (file,ext)=os.path.splitext(ffile)

    tt=file.split("_")
    if(mf.find(file,'db.') or mf.find(file,'Thum') or
       mf.find(f,'.py') or
       mf.find(ffile,'list.txt')
       ):

        return(n-1)

    #/data/amb/users/fiorino/w21/dat/tc/cira/mtcswa/2018/05w/2017NORp75.07211200.18.GIF
    if(mf.find(ffile,'GOES')):
        print 'WWW---GOES file: ',ffile
        fdtg=tt[4][0:10]

    elif(mf.find(ffile,'pmqpf') or mf.find(ffile,'p75.') or mf.find(ffile,'p50.') or mf.find(ffile,'p25.')):
        dd=dir.split('/')
        year=dd[-2]
        tt=ffile.split('.')
        mmddhh=tt[-3][0:6]
        fdtg=year+mmddhh
        print 'WWW--pmqpf/p?? file: ',file,' fdtg: ',fdtg
        
    elif(mf.find(ffile,'awips2.nc')):
        tt=ffile.split('_')
        yyyymmdd=tt[0]
        hh=tt[1]
        fdtg=yyyymmdd+hh
        print 'WWW--awips2.nc file: ',file,' fdtg: ',fdtg
        

    else:
        
        try:
            fdtg=tt[2]
        except:
            fdtg=''
            print 'WWW----- in killCira: failed to find dtg for file: ',file,'kill it...'

    if(len(fdtg) == 0):
        dt=-999
    else:
        try:
            dt=mf.dtgdiff(bdtg,fdtg)
        except:
            print 'WWW----- in killCira: failed to find dtg for file: ',file,'kill it...'
            dt=-999

    if(dt < 0):
        if(doit):
            n=n+1
            print 'RRR deleting: ',f
            os.unlink(f)
        else:
            print 'WWW will delete: ',f

    return(n)


def killTceps(f,bdtg,doit):

    ropt='norun'
    if(doit): ropt=''
    n=0
    (dir,fdtg)=os.path.split(f)


    dt=mf.dtgdiff(bdtg,fdtg)
    if(dt < 0):
        cmd="rm -r %s"%(f)
        if(doit):
            n=n+1
            print 'RRR(tceps) deleting: ',f
            mf.runcmd(cmd,ropt)
        else:
            print 'WWW(tceps) will delete: ',f
            mf.runcmd(cmd,ropt)


class TcOpsCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv

        self.argopts={
            1:['dtgopt',    'no default'],
        }

        self.defaults={
        }

        self.options={
            'doit':            ['X',0,1,' norun is norun'],
            'ropt':            ['N','','norun',' norun is norun'],
            'verb':            ['V',0,1,'verb=1 is verbose'],
            'typeopt':         ['T:',None,'a',"""cur(cira)|late(cira)|tceps|tmtrkN"""],
        }

        self.purpose='''
clean off cira | tceps | tmtrkN data'''

        self.examples='''
%s cur-d5    : kill off files <= cur-d5'''


MF.sTimer('all')

argv=sys.argv
CL=TcOpsCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)

bdtg=dtgs[-1]

year=bdtg[0:4]

if(typeopt != None):
    if(typeopt == 'all'):
        types=['cur','late','tceps','tmtrkN','tcanal']
    else:
        types=typeopt.split(',')
else:
    types=['cur','late']
    types=['tceps']
    types=['tmtrkN']
    types=['tcanal']


ffiles=[]
for type in types:

    if(type == 'cur'):

        if(year == '2018'):
            print 'FFF--- killCira does not work for data >= 2018 --- sayounara'
            sys.exit()

        tbdir=w2.TcMtcswaDatDir
        ff=glob.glob("%s/%s/???/*"%(tbdir,year))

    elif(type == 'late'):
        tbdir=w2.TcMtcswaLateDatDir
        ff=glob.glob("%s/%s/*"%(tbdir,year))

    elif(type == 'tceps'):
        tbdir="%s/%s"%(w2.TcDatDir,'tceps')
        ff=glob.glob("%s/*/%s/??????????"%(tbdir,year))

    elif(type == 'tmtrkN'):
        tbdir="%s/%s"%(w2.TcDatDir,type)
        ff=glob.glob("%s/??????????"%(tbdir))

    elif(type == 'tcanal'):
        tbdir="%s"%(w2.TcTcanalDatDir)
        ff=glob.glob("%s/%s??????"%(tbdir,year))
        ffiles=glob.glob("%s/*.pypdb"%(tbdir))

    else:
        print 'EEE invalid type: ',type
        sys.exit()

    ff.sort()

    n=0
    for f in ff:

        if(type == 'tceps'):
            rc=killTceps(f,bdtg,doit)
        elif(type == 'tmtrkN'):
            rc=killTmtrkN(f,bdtg,doit)
        elif(type == 'tcanal'):
            rc=killTcanalDirs(f,bdtg,doit)
        else:
            rc=killCira(f,bdtg,doit)

    if(len(ffiles) == 0):
        for ff in ffiles:
            if(type == 'tcanal'):
                rc=killTcanalFiles(ff,bdtg,doit)
