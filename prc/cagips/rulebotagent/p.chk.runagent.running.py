#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

job="RulebotAgent.jar"
rc=MF.chkIfJobIsRunningOld(job)

shjob='runagent.sh'
if(rc == 0):
    MF.ChangeDir(w2.CagipsPrcDir)
    os.system("%s &"%(shjob))

else:
    print '%s running...'%(shjob)
    

