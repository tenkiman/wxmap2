#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

# -- kill agent and blow away cache
#  let cron start up again...
#"$w2pdir/cagips/rulebotagent/p.chk.runagent.running.py"

job="RulebotAgent.jar"
curpid=MF.chkIfJobIsRunning(job,killjob=0,nminWait=0,rcPid=1)

ropt='norun'
ropt=''
if(curpid > 0):
    cmd="kill %s"%(curpid)
    mf.runcmd(cmd,ropt)
    MF.ChangeDir(w2.CagipsDatBdir)
    cmd='rm -r .cache'
    mf.runcmd(cmd,ropt)

    cmd='rm -f /tmp/met*.tmp'
    mf.runcmd(cmd,ropt)


sys.exit()

