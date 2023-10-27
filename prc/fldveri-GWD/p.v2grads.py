#!/usr/bin/env python

from WxMAP2 import *
w2=W2()                               # w2 obj with vars/methods

verb=0
bdtg='2014062200'
bdtg='2014050918'
#bdtg='2013122400'
#bdtg='2014051000'

rmask="/w21/dat/nwp2/ensFC/STATS/%s/*single*"%(bdtg)
runs=glob.glob(rmask)
#print 'rrrrrrrrrr',runs
#sys.exit()
allRuns=[]
rdict={}

etau=240
dtau=24
otaus=range(0,etau+1,dtau) 

olevs=[850,700,500,250,200,100]

oareas=['nhem', 'shem', 'tropics']

ovars=['hur', 'ta', 'ua', 'uva', 'va', 'wa', 'zg']

def parseRunCards(run,cards):
    
    levsA=[]
    tausA=[]
    areasA=[]
    varsA=[]
    
    for card in cards:
        tt=card.split()
        run=tt[0]
        allRuns.append(run)
        area=tt[3]
        tau=int(tt[4])
        var=tt[5]
        lev=int(tt[6])
        
        levsA.append(lev)
        tausA.append(tau)
        areasA.append(area)
        varsA.append(var)
        
        stats=[]

        rdict[run,area,tau,var,lev]=stats
        allRuns.append(run)
        for i in range(7,len(tt)):
            stats.append(float(tt[i]))
            #print tt[i]
        #print 'qqq',run,area,tau,var,lev,stats
        
    levsA=mf.uniq(levsA)
    tausA=mf.uniq(tausA)
    areasA=mf.uniq(areasA)
    varsA=mf.uniq(varsA)
    
    return(run,levsA,tausA,areasA,varsA)


   
allRuns=mf.uniq(allRuns)
opath='all.%s.dat'%(bdtg)
oB=open(opath,'wb')

for run in runs:

    (dir,file)=os.path.split(run)
    cards=open(run).readlines()
    rc=parseRunCards(file,cards)
    
    (orun,levsA,tausA,areasA,varsA)=rc
    
    levsA.reverse()
    
    print 'f______ 0 0 ',orun
    if(verb):
        print 'levsA',levsA
        print 'tausA',tausA
        print 'areasA',areasA
        print 'varsA',varsA
    
    for tau in otaus:
        for var in ovars:
            for lev in olevs:
                for area in oareas:
                    ostats=[-999.0,-999.0,-999.0,-999.0,-999.0,-999.0]
                    try:
                        ostats=rdict[orun,area,tau,var,lev]
                    except:
                        ostats=[-999.0,-999.0,-999.0,-999.0,-999.0,-999.0]
                        
                    
                    stnrec = struct.pack('6f',ostats[0],ostats[1],ostats[2],ostats[3],ostats[4],ostats[5])
                    if(verb): print 'qqqqqqqqqqq',orun,tau,var,lev,area,ostats
                    oB.write(stnrec)
                    
                        
    
    #print rdict
    #sys.exit()
   
sys.exit()
