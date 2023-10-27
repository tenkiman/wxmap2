#!/usr/bin/env python

from WxMAP2 import *

curActYears=[2006,2008,2009,2010,2018]
curActYears=[1999,2000,2001]

sdir='/w21/dat/nwp2/w2flds/dat/era5'

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
            'doAll':          ['A',0,1,'do all months'],
            'verb':           ['V',0,1,'verb=1 is verbose'],
            'ropt':           ['N','','norun',' norun is norun'],
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

cards={}
sizTot={}
sizAll=0

for year in years:
    # -- set dtgopt based on pull
    #
    sizTot[year]=0.0
    
    # -- nhem pull
    #
    moOpt='%d06.%d10.12'%(year,year)
    
    # -- force years < 1998 to the default shem
    #
    if(doShem and year >= 1979): moOpt='%d01.%d05.12,%d11.%d12.12'%(year,year,year,year)
    if(year == 2019): moOpt="%d09.12"%(year)
    if(doAll): moOpt='%d01.%d12.12'%(year,year)
    
    dtgs=mf.dtg_dtgopt_prc(moOpt)
    for dtg in dtgs:
        eyear=dtg[0:4]
        gmask1="%s/%s/%s/*.grb2"%(sdir,eyear,dtg)
        gmask2="%s/%s/%s/*sfc.grb"%(sdir,eyear,dtg)
        gpaths=glob.glob(gmask1)
        gpaths=gpaths+glob.glob(gmask2)
        #print 'ddddd',dtg,eyear,gmask1,gmask2,gpaths
        if(len(gpaths) == 2): 
            gpath=gpaths[0]
            gdir,gfile=os.path.split(gpath)
            gsizu=MF.GetPathSiz(gpath)
            gsizs=MF.GetPathSiz(gpaths[1])
            gsiz=gsizu+gsizs
            rc=MF.PathModifyTimei(gpath)
            
            gage=rc[-1]
            ogage="%s %s"%(gage[0:8],gage[-7:-2])
            gsiz=gsiz/(1024*1024)

            if(gsiz == 0):
                card="0-  %s %s %d %s <--- 0 size problem"%(dtg,gfile,gsiz,ogage)
            else:
                card="  %s   %4d MB     %s"%(dtg,gsiz,ogage)
                
            status=1
            sizTot[year]=sizTot[year]+gsiz*1.0
        else:
            card='N-%s <---missing problem'%(dtg)
            status=0
            
            
        cards[year,dtg]=(status,card)
        
    sizAll=sizAll+sizTot[year]
        
    
            
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
        if(status == 0 and cdtgdiff < 0.0):
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
        
    st=sizTot[cyear]/(1024.0)
    ocards.append("SSSS -- sizTot:  %5.0f GB for year: %s"%(st,cyear))
    ocards.append(' ')

sta=sizAll/1024.0
ocards.append("FFFF -- sizAll: %6.0f GB"%(sta))
ocards.append(' ')
            
if(doLess):
    opath='/tmp/era5-active.txt'
    MF.WriteList2Path(ocards, opath)
    cmd="less %s"%(opath)
    mf.runcmd(cmd,ropt)
    
else:
    for ocard in ocards:
        print ocard
        

    

