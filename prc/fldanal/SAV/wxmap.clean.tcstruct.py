#!/usr/bin/env python

import sys
import posixpath
import glob
import mf


adir="/tdocommon/tdocommon/JTWC_ARCHIVE"
sdir="/tdocommon/wxmap/tcstruct"
ropt=''
#ropt='norun'

curdtg=mf.dtg()

ndayback=30

olddtg=mf.dtginc(curdtg,ndayback*(-24))

print curdtg,olddtg

mask="%s/2???????*"%(sdir)
ls=glob.glob(mask)

ls.sort()
for l in ls:
    (d,f)=posixpath.split(l)
    ff=f.split('.')
    if(len(ff) == 4):
        d=ff[2]
    else:
        d=ff[0]
    if(d <= olddtg):
        cyear=d[0:4]
        tdir="%s/%s/WXMAP/TCSTRUCT"%(adir,cyear)
        if not(posixpath.isdir(tdir)) :
            print "tdir ",tdir," is not there -- mkdir"
            os.system('mkdir -p %s'%(tdir))
                        
        cmd="(cd %s ; tar -cvf %s/tcstruct.%s.tar *%s* ; rm -r *%s*)"%(sdir,tdir,d,d,d)
        mf.runcmd(cmd,ropt)


