#!/usr/bin/env python

"""%s

purpose:

examples:

"""

import os,sys,time
import getopt,glob
from socket import gethostname

import mf


def MakeNamelist(dtg,atcfname,stswitch,itmphrs):

    yy=int(dtg[2:4])
    mm=int(dtg[4:6])
    dd=int(dtg[6:8])
    hh=int(dtg[8:10])
    
    namelist="""&datein 
  inp%%byy=%02d,
  inp%%bmm=%02d,
  inp%%bdd=%02d,
  inp%%bhh=%02d, 
  inp%%model=1
/
&stormlist
  %s
/
&fhlist 
  %s
/
&atcfinfo 
  atcfnum=81,
  atcfname='%s',
  atcfymdh=%s
/
&phaseinfo 
  phaseflag='n',
  phasescheme='cps'
/
&structinfo
  structflag='n',
  ikeflag='n'
/
"""%(yy,mm,dd,hh,stswitch,itmphrs,atcfname,dtg)

    return(namelist)
          
           



#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main

ropt=''
member=1
override=0

curdtg=mf.dtg()
curphr=mf.dtg('phr')
(tttdtg,curphr)=mf.dtg_phr_command_prc(curdtg) 
curyear=curdtg[0:4]
curtime=mf.dtg('curtime')
pypath=sys.argv[0]
(pydir,pyfile)=os.path.split(pypath)

narg=len(sys.argv)-1

if(narg >= 1):

    dtgopt=sys.argv[1]

    try:
        (opts, args) = getopt.getopt(sys.argv[2:], "m:VNO")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime)
        print "EEE invalid getopt opt"
        sys.exit(2)

    for o, a in opts:
        if o in ("-m",""): member=a
        if o in ("-V",""): verb=1
        if o in ("-N",""): ropt='norun'
        if o in ("-O",""): override=1

else:
    mf.usage(__doc__,pyfile,curdtg,curtime)
    sys.exit(1)



nmembers=21
host=gethostname()
dtgs=mf.dtg_dtgopt_prc(dtgopt)

onWjet=(mf.find(host,'wfe') or mf.find(host,'wcron'))
onTacc=(mf.find(host,'ranger.tacc'))

tcvitdir='/lfs1/projects/rtfim/tcvitals'
tctkrdir='/lfs1/projects/rtfim/tracker'

ndxcmd="%s/bin/grbindex"%(tctkrdir)
trkcmd="%s/bin/gettrk.gfs.x"%(tctkrdir)

#ccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# cycle by dtgs

if(len(dtgs) > 1):

    for dtg in dtgs:
        cmd="%s %s"%(pypath,dtg)
        for o,a in opts:
            cmd="%s %s %s"%(cmd,o,a)
        mf.runcmd(cmd,ropt)
    sys.exit()

else:

    dtg=dtgs[0]

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# cycle by members

if(member == 'all'):
    for n in range (1,nmembers+1):
        cmd="%s %s -m %s"%(pypath,dtg,n)
        for o,a in opts:
            if(o != '-m'):
                cmd="%s %s %s"%(cmd,o,a)
        mf.runcmd(cmd,ropt)
    sys.exit()

else:
    member=int(member)



adeckname="GE%02d"%(member)
atcfname=adeckname

#print 'qqqqqqqqqqqqqqqqqqqqqqqqqqq ',dtg,member,atcfname
#sys.exit()

sdir="/lfs1/projects/fim/whitaker/gfsenkf_200907/%s/ens20"%(dtg)
tdir="/lfs1/projects/fim/fiorino/tmp/tracker/enkf/%s"%(dtg)
mf.ChkDir(tdir,'mk')

allgrib="%s/mem%03d.tracker.%s.grib1"%(tdir,member,dtg)
allgribix="%s/mem%03d.tracker.%s.grib1.ix"%(tdir,member,dtg)
print allgrib


gribs=glob.glob("%s/pgrb_%s_fhr*mem%03d"%(sdir,dtg,member))
gribs.sort()

firsttime=0
if(not(os.path.exists(allgrib)) or override):
    cmd="touch %s"%(allgrib)
    mf.runcmd(cmd,ropt)
    firsttime=1
    
taus=[]
for path in gribs:
    (dir,file)=os.path.split(path)
    siz=os.path.getsize(path)
    tt=file.split('_')
    tau=int(tt[2][3:])
    print 'ppppp ',path,tau,siz
    if(siz > 0):
        taus.append(tau)
    else:
        continue

    if(firsttime):
        cmd="cat %s >> %s"%(path,allgrib)
        mf.runcmd(cmd,ropt)

taus.sort()

tcvdir='/work/01233/mfiorino/w21/dat/tc/tcvitals'
itcvitals="%s/tcvitals.%s.txt"%(tcvitdir,dtg)
otcvitals="%s/tcvitals.txt"%(tdir)

if(os.path.exists(itcvitals)):
    if(not(os.path.exists(otcvitals))):
        cmd="cp %s %s"%(itcvitals,otcvitals)
        mf.runcmd(cmd,ropt)

else:
    print 'EEEEEEEE no tcs for ',dtg
    sys.exit()
    


if(not(os.path.exists(allgribix))):
    cmd="%s %s %s"%(ndxcmd,allgrib,allgribix)
    mf.runcmd(cmd,ropt)


# make itmphrs card in gettrk namelist
#    
itmphrs='itmphrs = '

maxtaus=65
for n in range(0,maxtaus):
    try:
        tau=taus[n]
        ctau="%04d"%(tau)
    except:
        ctau='99'
    
    itmphrs="%s %s"%(itmphrs,ctau)

print itmphrs


# make stswitch card in gettrk namelist -- storms to track
#

maxstms=15
cmd="cat %s | wc -l "%(otcvitals)
cards=os.popen(cmd).readlines()

nstms=int(cards[0].strip())

stswitch='stswitch = '

for n in range(0,maxstms):
    if(n < nstms):
        stswitch="%s 1"%(stswitch)
    else:
        stswitch="%s 3"%(stswitch)
        
# change to tracker dir, make namelist and run app
#

mf.ChangeDir(tdir)
namelist=MakeNamelist(dtg,atcfname,stswitch,itmphrs)

print namelist
inamelist='./namelist'

mf.WriteCtl(namelist,inamelist)

track="%s/track.%s.%s"%(tdir,dtg,adeckname)
igrib=allgrib
igribix=allgribix
itcvitals=otcvitals
otrack=track

print 'igrib:      ',igrib
print 'igribix:    ',igribix
print 'inamelist:  ',inamelist
print 'itcvitals:  ',itcvitals
print 'adeckname:  ',adeckname
print 'otrack:     ',otrack

fort11='fort.11'
fort12='fort.12'
fort31='fort.31'
fort64='fort.64'
namelist='namelist'

forts=[fort11,fort12,fort31,fort64]

for fort in forts:
    cmd="rm -f %s"%(fort)
    mf.runcmd(cmd,ropt)

cmd="ln -s %s %s"%(igrib,fort11)
mf.runcmd(cmd,ropt)

cmd="ln -s %s %s"%(igribix,fort31)
mf.runcmd(cmd,ropt)

cmd="ln -s %s %s"%(itcvitals,fort12)
mf.runcmd(cmd,ropt)

cmd="ln -s %s %s"%(otrack,fort64)
mf.runcmd(cmd,ropt)

cmd="%s < namelist"%(trkcmd)
mf.runcmd(cmd,ropt)

