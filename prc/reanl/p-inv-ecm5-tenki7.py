#!/usr/bin/env python

from WxMAP2 import *

class Ecm5CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):


        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
#            1:['year',  '''source1[,source2,...,sourceN]'''],
            }

        self.defaults={
            }
            
        self.options={
            'override':            ['O',0,1,"""override"""],
            'verb':                ['V',0,1,'verb is verbose'],
            'ropt':                ['N','norun','norun','must use -X to run'],
            'doIt':                ['X',0,1,'run it norun is norun'],
            'doByDtgs':            ['d',0,1,'do rsync by dtgs'],
            }

        self.purpose='''
pull ecm5 inventory from wxmap2.com 
do ecm5 inventory on tenki7 NOT done and rsync to wxmap2.com'''
        
        self.examples='''
%s -N'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

CL=Ecm5CmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


sdirwx2='/home3/mfiorino/dat/nwp2/w2flds/dat/ecm5'
invfilewx2='inv-ecm5-wxmap2.txt'
invpathwx2="%s/%s"%(sdirwx2,invfilewx2)

sdir='/w21/dat/nwp2/w2flds/dat/ecm5'
invpath="%s/inv-ecm5-tenki7.txt"%(sdir)
invpathwx2Local="%s/%s"%(sdir,invfilewx2)

# -- get inv from wxmap2
#
if(doIt or verb): ropt=''
cmd="""rsync -alv --rsh="ssh -p2222"  mfiorino@wxmap2.com:%s %s/"""%(invpathwx2,sdir)
mf.runcmd(cmd,ropt)

dpaths=glob.glob('%s/????/??????????'%(sdir))

dtgsDone={}

dpaths.sort()
for dpath in dpaths:
    grbs=glob.glob("%s/*sfc.grb2"%(dpath)) + glob.glob("%s/*ua.grb2"%(dpath))
    (ddir,dtg)=os.path.split(dpath)
    
    stat=0
    if(len(grbs) == 2):  stat=1
    
    dtgsDone[dtg]=stat
    
dtgs=dtgsDone.keys()
dtgs.sort()

dtgsDoneWx2={}
cardswx2=MF.ReadFile2List(invpathwx2Local)

for card in cardswx2:
    (dtg,stat,gsiz)=card.split()
    stat=int(stat)

    if(stat == 1):
        dtgsDoneWx2[dtg]=stat
        
    if(verb):
        print 'ON wxmap2---',dtg,stat

dtgs=dtgsDoneWx2.keys()
dtgs.sort()

# -- get the dtgs not done but on wxmap2.com
# -- dtgNot is by default 1 and is either 0 (not done on tenki7) or not in the wxmap2.com dtgs
#
dtgsStillOnWx2={}

for dtg in dtgs:
    dtgNot=1
    try:
        dtgNot=dtgsDone[dtg]
    except:
        dtgNot=0

    if(dtgNot == 0):
        dtgsStillOnWx2[dtg]=0
        
dtgs=dtgsStillOnWx2.keys()
dtgs.sort()

cards=[]

for dtg in dtgs:
    card="%s %d"%(dtg,dtgsStillOnWx2[dtg])
    
    if(verb): print 'NOT local and ON wxmap2: ',card
    cards.append(card)

rc=MF.WriteList2Path(cards,invpath)

# -- sleep before doing push to wxmap2
#
sleep(3)
cmd="""rsync -alv --rsh="ssh -p2222" %s mfiorino@wxmap2.com:%s"""%(invpath,sdirwx2)
mf.runcmd(cmd,ropt)

# -- put inv to wxmap2
#

print 'Wxmap2: ',invpathwx2Local
print 'Tenki7: ',invpath
