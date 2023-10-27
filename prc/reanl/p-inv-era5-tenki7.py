#!/usr/bin/env python

from WxMAP2 import *


sdirwx2='/home3/mfiorino/dat/nwp2/w2flds/dat/era5'
invfilewx2='inv-era5-wxmap2.txt'
invpathwx2="%s/%s"%(sdirwx2,invfilewx2)

sdir='/w21/dat/nwp2/w2flds/dat/era5'
invpath="%s/inv-era5-tenki7.txt"%(sdir)
invpathwx2Local="%s/%s"%(sdir,invfilewx2)

# -- get inv from wxmap2
#
ropt=''
cmd="""rsync -alv --rsh="ssh -p2222"  mfiorino@wxmap2.com:%s %s/"""%(invpathwx2,sdir)
mf.runcmd(cmd,ropt)

dpaths=glob.glob('%s/????/??????????'%(sdir))

dtgsDone={}

for dpath in dpaths:
    grbs=glob.glob("%s/*sfc.grb"%(dpath)) + glob.glob("%s/*ua.grb2"%(dpath))
    (ddir,dtg)=os.path.split(dpath)
    
    stat=0
    if(len(grbs) == 2):  stat=1
    
    dtgsDone[dtg]=stat
    
dtgs=dtgsDone.keys()
dtgs.sort()


dtgsDoneWx2={}
cardswx2=MF.ReadFile2List(invpathwx2Local)

for card in cardswx2:
    (dtg,stat)=card.split()
    stat=int(stat)

    if(stat == 1):
        dtgsDoneWx2[dtg]=stat


dtgs=dtgsDoneWx2.keys()
dtgs.sort()

dtgsStillOnWx2={}

for dtg in dtgs:
    dtgNot=0
    try:
        dtgstat=dtgsDone[dtg]
    except:
        dtgNot=1

    if(dtgNot == 1):
        dtgsStillOnWx2[dtg]=1


dtgs=dtgsStillOnWx2.keys()
dtgs.sort()

cards=[]

for dtg in dtgs:
    card="%s %d"%(dtg,dtgsStillOnWx2[dtg])
    cards.append(card)


rc=MF.WriteList2Path(cards,invpath)

cmd="""rsync -alv --rsh="ssh -p2222" %s mfiorino@wxmap2.com:%s"""%(invpath,sdirwx2)
mf.runcmd(cmd,ropt)

# -- put inv to wxmap2
#

print 'Wxmap2: ',invpathwx2Local
print 'Tenki7: ',invpath




                                    
