#!/usr/bin/env python

"""%s

purpose:

 ls processes

  -A add to list in spinning archive
  -d dtgopt
  -V verb for lsopt='arch'

examples:

"""

import os,sys,time
import getopt,glob

import mf
verb=0
ropt=''

curdtg=mf.dtg()
(tttdtg,curphr)=mf.dtg_phr_command_prc(curdtg) 
curyear=curdtg[0:4]
curtime=mf.dtg('curtime')
pypath=sys.argv[0]
(pydir,pyfile)=os.path.split(pypath)

narg=len(sys.argv)-1

if(narg >= 1):

    lsopt=sys.argv[1]
    
    try:
        (opts, args) = getopt.getopt(sys.argv[2:], "OSACDGVd:")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime)
        print "EEE invalid getopt opt"
        sys.exit(2)

    for o, a in opts:
        if o in ("-S",""): dostatus=1
        if o in ("-A",""): doarch=1
        if o in ("-C",""): prcopt='Cfiles'
        if o in ("-D",""): prcopt='dat'
        if o in ("-G",""): prcopt='grib'
        if o in ("-O",""): dooverride=1
        if o in ("-d",""): dtgopt=a
        if o in ("-V",""): verb=1

else:
    mf.usage(__doc__,pyfile,curdtg,curtime)
    sys.exit(1)


who=os.popen('whoami').readlines()
who=who[0].strip()
print 'wwwwwwwwwwww ',who

def LsPids(who,lsopt=''):

    def isInteresting(pname,pscmd):
        interesting=1
        if(
            mf.find(pname,'kdeinit') or
            mf.find(pname,'/usr/X11R6/bin/xterm') or
            mf.find(pname,pyfile) or
            mf.find(pname,pscmd) or
            pname == '-csh'
            
           ): interesting=0

        return(interesting)

        
    #iiii  0 mfiorino
    #iiii  1 3465
    #iiii  2 3464
    #iiii  3 64
    #iiii  4 15:43
    #iiii  5 pts/6
    #iiii  6 00:02:47
    #iiii  7 gddiag

    #
    # get executing processes
    #

    pscmd='ps -ef --cols 256'
    processes=os.popen(pscmd).readlines()
    pids=[]
    for i in range(1,len(processes)):
        process=processes[i]
        pname=process[48:-1]
        tt=process.split()
        
        owner=tt[0]
        pidchild=int(tt[1])
        pidparent=int(tt[2])
        pidruntime=tt[6]
        piddate=tt[4]
        
        if( (owner == who and pidparent != 1 and isInteresting(pname,pscmd)) or lsopt == 'all'):
            pids.append( (pidchild,pidparent,piddate,pidruntime,pname) )

    return(pids)

pids=LsPids(who)

npids=[]

for pid in pids:
    
    print pid
