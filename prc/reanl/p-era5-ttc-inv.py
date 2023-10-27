#!/usr/bin/env python

from WxMAP2 import *
from tcbase import *

curActYears=[2012]

sdir='/w21/dat/tc/adeck/tmtrkN'

class MdeckCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv

        self.argopts={
            1:['yearOpt', 'no default'],
            }        

        self.options={
            'onlyThere':      ['E',0,1,'print only there there'],
            'doLess':         ['l',0,1,'print only there there'],
            'doShem':         ['S',1,0,'do NOT do SHEM pull'],
            'doAllMonths':    ['A',0,1,'do all months in the year'],
            'verb':           ['V',0,1,'verb=1 is verbose'],
            'ropt':           ['N','','norun',' norun is norun'],
            'override':       ['O',0,1,' override tcV'],
            }

        self.purpose='''
list ERA5'''
        
        self.examples='''
%s -y 2006'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# -- main
#

MF.sTimer('all')

argv=sys.argv
CL=MdeckCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

if(mf.find(yearOpt,'cur')):
    years=curActYears
else:
    tt=yearOpt.split('.')
    tt1=yearOpt.split(',')
    
    if(len(tt1) > 1):
        years=[]
        for tt in tt1:
            years.append(int(tt))
            
    elif(len(tt) == 2):
        years=MF.YearRange(int(tt[0]),int(tt[1]))
    else:
        years=[int(yearOpt)]

prcdir=os.getenv('W2_PRC_DIR')
if(prcdir == None): print 'bad env var' ; sys.exit()

MF.sTimer("TTC-inv-all")

cards={}
for year in years:
    # -- set dtgopt based on pull
    #
    moOpt='%d06.%d10.12'%(year,year)
    if(doShem): moOpt='%d01.%d05.12,%d11.%d12.12'%(year,year,year,year)
    if(year == 2019): moOpt="%d09.12"%(year)
    if(doAllMonths): moOpt='%d01.%d12.12'%(year,year)
    
    dtgs=mf.dtg_dtgopt_prc(moOpt)
    tcD=TcData(years=years)
    
    for dtg in dtgs:
        
        # -- get TCs first as in tmtrkN
        #
        tcV=tcD.getTCvDtg(dtg)
        tcVcards=tcV.makeTCvCards(verb=verb,override=override)
        nTCs=len(tcVcards.split('\n')) - 1

        gmask="%s/%s/%s/tctrk.atcf.%s.era5.txt"%(sdir,year,dtg,dtg)
        gpaths=glob.glob(gmask)

        if(len(gpaths) == 1): 
            gpath=gpaths[0]
            gdir,gfile=os.path.split(gpath)
            gsiz=MF.GetPathSiz(gpath)
            rc=MF.PathModifyTimei(gpath)
            
            gage=rc[-1]
            ogage="%s %s"%(gage[0:8],gage[-7:-2])

            if(gsiz == 0):
                card="0-  %s %s %d %s <--- 0 size problem"%(dtg,gfile,gsiz,ogage)
            else:
                card="  %s nTCs: %2d  %s %6d %s"%(dtg,nTCs,gfile,gsiz,ogage)
            status=1
        else:
            if(nTCs != 0):
                card='N-%s <---missing problem'%(dtg)
                status=-1
            else:
                card='T-%s <--- NO TCs'%(dtg)
                status=0
                
        cards[year,dtg]=(status,card)
            
# -- make list
#
cdtgs={}
cyears=[]
for k in cards.keys():
    (year,dtg)=k
    cyears.append(int(year))
    MF.appendDictList(cdtgs, year, dtg)
    
cyears=mf.uniq(cyears)

ocards=[]

for cyear in cyears:
    
    MF.sTimer("ttc-inv-%s"%(cyear))
    dtgs=cdtgs[cyear]
    dtgs.sort()
    ndtgs=len(dtgs)
    
    ocards.append('  %s <-----yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'%(cyear))
    ocards.append('\n')
    
    # -- look for missing
    #
    lastdtg=dtgs[0]
    for i in range(ndtgs-1,0,-1):
        there=cards[cyear,dtgs[i]][0]
        if(there == 1):
            lastdtg=dtgs[i]
            break
            
    for dtg in dtgs:

        if(doShem and mf.find(dtg,'110100')): ocards.append('\n')

        (status,card)=cards[cyear,dtg]
        cdtgdiff=mf.dtgdiff(lastdtg,dtg)
        if(status == -1 and cdtgdiff < 0.0):
            card='MMMMissing: %s'%(dtg)
            ocards.append(card)
        elif(cdtgdiff <= 0.0 and onlyThere):
            ocards.append(card)
        elif(not(onlyThere)):
            ocards.append(card)
    if(len(cyears) > 1):
        ocards.append('\n')
    else:
        ocards.append(' ')

    rc=MF.dTimer("ttc-inv-%s"%(cyear))
    ocards.append(rc)

rc=MF.dTimer("TTC-inv-all")
ocards.append(rc)
            
if(doLess):
    opath='/tmp/era5-active.txt'
    MF.WriteList2Path(ocards, opath)
    cmd="less %s"%(opath)
    mf.runcmd(cmd,ropt)
    
else:
    for ocard in ocards:
        print ocard

    

