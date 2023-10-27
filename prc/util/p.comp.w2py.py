#!/usr/bin/env python

import os,glob
import mf

docp=1
ropt=''
sbase='/wxmap2/trunk/prc'
tbase='/w21/prc'

prcdirs=['fldanal','flddat','gefs','geog','lib/python','tc','tcanal','tcbog','tcclimo','tcdat','tcfilt','tcplt''tcsgp','tcveri','tcww3','util','web','wxmap2']
exts=['py','pl','gs','gsf','c','f']

for prcdir in prcdirs:
    print 'Checking srcdir: ',prcdir
    sdir='%s/%s'%(sbase,prcdir)
    tdir='%s/%s'%(tbase,prcdir)

    for ext in exts:
        spaths=glob.glob("%s/*.%s"%(sdir,ext))
        spaths.sort()

        for spath in spaths:
            psiz=mf.GetPathSiz(spath)
            (dir,file)=os.path.split(spath)
            tpath="%s/%s"%(tdir,file)
            ###print 'tpath: ',tpath
            try:
                tsiz=mf.GetPathSiz(tpath)
            except:
                tsiz=None

            if(tsiz != None):
                tdiff=os.popen("diff %s %s"%(spath,tpath)).readlines()

            if(len(tdiff) != 0):
                if(docp):
                    cpcmd="cp -p %s %s"%(spath,tpath)
                    mf.runcmd(cpcmd,ropt)
                print "DIFF: %d\t%d\t% 60s"%(psiz,tsiz,file)


