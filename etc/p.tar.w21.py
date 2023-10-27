#!/usr/bin/env python

"""
%s

purpose:

usages:

  dtgopt -t tbtype [-N -V]

-t tbtype :: tARbALL type !! REQuIRED !!

   dat.geog
   dat.nwp2
   dat.w2flds
   

(c) 2009 Michael Fiorino
"""

import os
import sys
import glob
import time
import getopt

import mf
import w2

curdtg=mf.dtg()
curphr=mf.dtg('phr')
curyear=curdtg[0:4]
curtime=mf.dtg('curtime')
curdir=os.getcwd()
pypath=sys.argv[0]
(pydir,pyfile)=os.path.split(pypath)

#
#  defaults
#
ropt=''
tbtype='web'
tbtype=None

narg=len(sys.argv)-1

if(narg >= 2):

    dtgopt=sys.argv[1]
    
    try:
        (opts, args) = getopt.getopt(sys.argv[2:], "NVt:")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
        sys.exit(2)

    for o, a in opts:
        if o in ("-N",""): ropt='norun'
        if o in ("-V",""): verb=1
        if o in ("-t",""): tbtype=a

    if(tbtype == None):
        mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
        sys.exit(2)
        
                
else:
    mf.usage(__doc__,pyfile,curdtg,curtime,curphr)
    sys.exit(1)

#llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
#
# local
#

def appTarball(dtype,dtg,taropt,tdirwp,arch='macos'):

    mf.ChangeDir(w2.W2Dir)

    if(dtype == 'grads'):

        arch='noarch'
        tarball="%s/w2.app.grads.%s.tgz"%(tdir,arch)
        cmd="tar %s %s app/grads"%(taropt,tarball)
        mf.runcmd(cmd,ropt)
        return

    elif(dtype == 'opengrads1.10'):
        
        return

    else:
        print 'invalid dtype in appTarball: ',dtype
        sys.exit()

    return
    
def datTarball(dtype,dtg,taropt,tdirwp):

    mf.ChangeDir(w2.W2Dir)

    if(dtype == 'climo'):

        taropt=' --exclude \"*.svn*\"  --exclude \".DS_*\"  --exclude \"cmean*\" -czvf'
        tarball="%s/w2.dat.climo.tgz"%(tdir)
        cmd="tar %s %s dat/climo"%(taropt,tarball)
        mf.runcmd(cmd,ropt)
        return

    elif(dtype == 'geog'):

        print 'ttttttt ',tdir,taropt
        tarball="%s/w2.dat.geog.tgz"%(tdir)
        cmd="tar %s %s dat/geog"%(taropt,tarball)
        mf.runcmd(cmd,ropt)
        return

    elif(dtype == 'nwp2'):

        dats=glob.glob("dat/nwp2/*/*/%s"%(dtg))
        dats=dats+glob.glob("dat/nwp2/*/%s"%(dtg))
        for dat in dats:
            tt=dat.split('/')
            if(len(tt) == 4):
                tbname="%s"%(tt[2])

            elif(len(tt) == 5):
                tbname="%s.%s"%(tt[2],tt[3])

            tarball="%s/w2.dat.nwp2.%s.%s.tgz"%(tdir,tbname,dtg)
            print dat,tarball

            cmd="tar %s %s %s"%(taropt,tarball,dat)
            mf.runcmd(cmd,ropt)
        return

    elif(dtype == 'w2flds'):

        dats=glob.glob("dat/nwp2/w2flds/%s"%(dtg))
        for dat in dats:
            tt=dat.split('/')
            if(len(tt) == 4):
                tbname="%s"%(tt[2])

            elif(len(tt) == 5):
                tbname="%s.%s"%(tt[2],tt[3])

            tarball="%s/w2.dat.nwp2.%s.%s.tgz"%(tdir,tbname,dtg)
            print 'WWWW ',dat,tarball

            cmd="tar %s %s %s"%(taropt,tarball,dat)
            mf.runcmd(cmd,ropt)
        return

    else:
        print 'invalid dtype in datTarball: ',dtype
        sys.exit()

    return
    


def webTarball(taropt,tdir):
    
    htms=[]
    links=[]

    mf.ChangeDir(w2.W2Dir)
    
    paths=glob.glob("web/.*")
    for path in paths:
        if(os.path.islink(path)):
            print 'a link...',path 
            links.append(path)

    paths=glob.glob("web/*")
    for path in paths:
        if(os.path.islink(path)):
            print 'a link...',path 
            links.append(path)


    paths=glob.glob("web/*%s.htm"%(dtg))
    for path in paths:
        htms.append(path)

    configs=['web/config']

    tarball="%s/w2.web.%s.base.tgz"%(tdir,dtg)
    cmd="tar %s %s "%(taropt,tarball)
    pps=links+htms+configs
    for p in pps:
        cmd="%s %s"%(cmd,p)
    mf.runcmd(cmd,ropt)

    plts=glob.glob("web/plt_*/%s"%(dtg))
    webs=glob.glob("web/web_*/%s"%(dtg))
    tcs=glob.glob("web/tc/*/*%s*"%(dtg))
    tcs=tcs+glob.glob("web/tc/*/%s/*%s*"%(dtg[0:4],dtg))

    tcepss=glob.glob("web/tc/tceps/*")

    print
    for plt in plts:
        print 'ppppppppppppppp ',plt
        tt=plt.split('/')
        pt=tt[1]
        tarball="%s/w2.web.%s.%s.tgz"%(tdir,dtg,pt)
        cmd="tar %s %s %s"%(taropt,tarball,plt)
        mf.runcmd(cmd,ropt)

    print
    for web in webs:
        tt=web.split('/')
        print 'ppppppppppppppp ',web
        pt=tt[1]
        tarball="%s/w2.web.%s.%s.tgz"%(tdir,dtg,pt)
        cmd="tar %s %s %s"%(taropt,tarball,web)
        mf.runcmd(cmd,ropt)

    tarball="%s/w2.web.%s.tc.tgz"%(tdir,dtg)
    print
    cmd="tar %s %s"%(taropt,tarball)
    for tc in tcs:
        if(os.path.islink(tc)):
            print 'tc is a link: ',tc
        else:
            print 'tc          : ',tc
        cmd="%s %s"%(cmd,tc)

    mf.runcmd(cmd,ropt)


    print
    addpaths=[]
    for path in tcepss:
        (dir,file)=os.path.split(path)
        if(os.path.islink(path)):
            addpaths.append(path)

        if(len(file) == 4):
            try:
                ifile=int(file)
            except:
                ifile=-999

            if(ifile >= 2006 and ifile <= 2010):
                continue
            else:
                addpaths.append(path)

        elif(file == '-1'):
            continue

        else:
            addpaths.append(path)

    tarball="%s/w2.web.%s.tceps.tgz"%(tdir,dtg)
    cmd="tar %s %s"%(taropt,tarball)

    for a in addpaths:
        if(os.path.islink(a)):
            print 'tceps is a link: ',a
        else:
            print 'tceps          : ',a
        cmd="%s %s"%(cmd,a)

    mf.runcmd(cmd,ropt)
    
    return


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main
#

taropt=' --exclude \"*.svn*\"  --exclude \".DS_*\" -czvf'
tdir='/ptmp'

dtgs=mf.dtg_dtgopt_prc(dtgopt)

dtg=dtgs[0]
if(tbtype == 'web'):
    rc=webTarball(taropt,tdir)

elif(mf.find(tbtype,'dat')):

    try:
        dtype=tbtype.split('.')[1]
    except:
        print 'invalid -t dat.* opt'
        print 'valid types: dat.climo | dat.geog | dat.nwp2 | dat.w2flds '
        sys.exit()

    rc=datTarball(dtype,dtg,taropt,tdir)

elif(mf.find(tbtype,'app')):

    try:
        dtype=tbtype.split('.')[1]
    except:
        print 'invalid -t app.* opt'
        print 'valid types: app.grads'
        sys.exit()

    rc=appTarball(dtype,dtg,taropt,tdir)

else:
    print 'invalid tbtype: ',tbtype
    sys.exit()


    
