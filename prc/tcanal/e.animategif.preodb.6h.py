#!/usr/bin/env python

import sys
import os
import posix
import posixpath
import glob
import string

sys.path.append("/home/fiorino/lib/python")
import mf


dtg=2003030518
pltbdir='/dat/nwp/dat/tc/tcstruct/%s/plot'%(dtg)
convertexe='/usr/local/bin/convert'

btau=0
etau=72

dtau=24

delayfactorbeg=150
delayfactorloop=100

stmid='23s'

model='avn'

gifpath='/tmp/t.anim.%s.%s.%s.gif'%(model,stmid,dtg)

nplt=0

taus=xrange(btau,etau+1,dtau)

for tau in taus:

    nplt=nplt+1
    
    pfile="plt.%s.%s.%03d.png"%(model,stmid,int(tau))
    pfile="%s/%s"%(pltbdir,pfile )

    if(nplt == 1):
        ccmd="-loop 0 -delay %s %s -delay %s"%(delayfactorbeg,pfile,delayfactorloop)
    else:
        ccmd="%s %s"%(ccmd,pfile)

ccmd="%s %s %s"%(convertexe,ccmd,gifpath)
        
print ccmd
os.system(ccmd)


sys.exit()
