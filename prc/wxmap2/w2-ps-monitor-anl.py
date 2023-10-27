#!/usr/bin/env python

from M import *
MF=MFutils()

from WxMAP2 import *
w2=W2()


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#
class w2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',    'DTG (YYYYMMDDHH)'],
            }

        self.options={
            'verb':         ['V',0,1,'verb=1 is verbose'],
            'ropt':         ['N','','norun',' norun is norun'],
            'doCurPids':    ['C',0,1,'ls current PIDS only'],
            'killLongPS':   ['K',0,1,'kill long running PS'],
            'PSls':         ['P:',None,'a','ps to list'],
            'sortBy':       ['s:',None,'a','sort by 1: time...'],
            'mikeM':        ['M:',None,'a','set mikeN...'],
            }

        self.defaults={
            'dosingledtg':0,
            'dow2flds':1,
            'docleanPlotsHtms':0,
            'sleepytime':15.0,

            }

        self.purpose='''
analyze log of python processes
(c) 2009-2020 Michael Fiorino,NOAA ESRL'''

        self.examples="""
%s cur-6           # output every 15 sec
%s cur-6 -s 1:PPP  # 1=> sort by reverse order by time consumption; display PPP=%%
%s cur-6 -P conv   # print processes with \'conv\'"""

CL=w2CmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

rtimeMaxPS={
    
    # -- models
    #
    #'do-gfs2.py':180.0,
    'do-cgd2.py':240.0,
    #'do-ecm5.py':180.0,
    'do-jgsm.py':180.0,
    
    # -- model field pull
    #
    'w2-fld-rsync-ecm5-wxmap2.py':90.0,
    'w2-fld-cmc-gdps-wget-mirror.py':180.0,
    'w2-fld-get_gfs_pl-gfs2.py':90.0,
    'w2.fld.nomads.curl.gfs0p25.py':25.0,
    'w2-fld-curl-jgsm.py':125.0,
    #'w2-fld-tigge-ecmwf.py':110.0, # -- 20211130 -- working with vsmf2
    'w2-fld-tigge-ecmwf.py':99999.0, # -- 20211130 -- redo by month 
    
    # -- GMU
    #
    'w2-products-rsync-gmu.py':250.0,
    'w2-pr-rsync-gmu.py':30.0,

    # -- TCs
    #
    'w2-tc-ecmwf-wmo-essential-bufr-json.py':20.0,
    'w2-tc-all-eps.py':25.0,  # -- 20211213 -- takes a long time sometimes...
    #'w2-tc-convert-tm-mftrkN-to-atcf-adeck.py':100.0, # -- to do year end
    'w2-tc-convert-tm-mftrkN-to-atcf-adeck.py':100.0,
    'w2-tc-stm-trkplt.py':10.0,
    'w2-tc-dss-vd2-anl.py':10.0,
    'w2-tc-dss-ad2.py':25.0,
    'w2-tc-dss-mdeck.py':5.0,
    'w2-tc-mftrkN.py':10.0, # -- cgd2 takes a long time
    'w2-tc-tmtrkN.py':40.0, # -- 20211125 -- cgd2 takes a long time becaus of i/o of hi-res grids
    'w2-tc-tcgen2.py':50.0, # -- cgd2 - can cycle with other tcgen runs
    'w2-tc-zip-adeck-tmtrkN.py':5.0,

    "w2-tc-runTrks.py":9999., # -- 20220103-- run era5 trackers for 202110
    #'w2-tc-runTrks.py':45.0,
    
    #   9999.0:['rsync'], # -- 20210515 -- rsync from gmu of fields on mike4
    #'rsync':75.0,         # -- 20210216 -- big rsync on mike4
    
    'w2-tc-dss-mdeck.py':20.0,  # -- 20210222 -- hung because of bad mdecks.pypdb...
    'w2-tc-ops-dat.py':20.0,    # -- 20210222 -- got stock because of bad mdecks
    
    'w2-fld-pr-qmorph.py':10.0,
    #'w2-fld-pr-qmorph-products.py':5.0,
    'w2-fld-pr-qmorph-global-products.py':5.0,
    
    'w2-web.py':30.0,        # -- 20211122 tune up on mike4
    'w2-web-main.py':5.0, 
    'w2-gfs-goes-loop.py':40.0,  # -- 20211122 tune up on mike4 and revised to only do at end
}

rtimeMaxPSJobs=rtimeMaxPS.keys()

# -- check if running...
#
rc=MF.whoIsRunningNew(pyfile, jobopt=None, killjob=-1)

# -- get current jobs
#
curPidPSs=getCurrentPids(pyfile)

# -- locate the logfile from w2-ps-monitor  -- redone every 24 h in cron
#

dtgs=mf.dtg_dtgopt_prc(dtgopt)
dtg=dtgs[0]
dtgm24=mf.dtginc(dtg,-24)

mhost=w2.W2Host.split('.')[0]
if(mikeM != None):
    mhost='tenki7-m%s'%(mikeM)
lmask="%s/w2.ps.monitor.%s.%s*txt"%(w2.ptmpBaseDir,mhost,dtg[0:8])
logpaths=glob.glob(lmask)
logpaths.sort()
if(verb):
    print 'LLL',lmask
    print 'LLLL',logpaths
    
logpathsm24=glob.glob("%s/w2.ps.monitor.%s.%s*txt"%(w2.ptmpBaseDir,mhost,dtgm24[0:8]))


#if(len(logpaths) == 0 or len(logpathsm24) == 0):
if(len(logpaths) == 0):
    print 'EEE no monitor for dtg: ',dtg,'sayounara....'
    sys.exit()
    
# -- get the log with times...
#
if(len(logpaths) != 0): logpath=logpaths[-1]
elif(len(logpathsm24) != 0): logpath=logpathsm24[-1]

logpath=logpaths[-1]
if(verb): print 'LLLLLL',logpath
(ddir,dfile)=os.path.split(logpath)
dd=dfile.split('.')
if(len(dd) == 7): sleepytime=float(dd[-2])
cards=open(logpath).readlines()

PSs={}
PStimes={}

PSbyTimes={}
PSbyTimetimes={}

pscards=[]
for card in cards:
    
    if(mf.find(card,'CurDTG')):
        if(len(pscards) > 0):
            #fiorino  22673 25758  4 12:07 ?        00:00:00 python ./g.tc.bt.climo.ll.py -y 1993070100.1994011406 -b global -d /data/amb/users/fiorino/w21/plt/tc/ops/climo/2014.shem -p tcace
            for pscard in pscards:
                tt=pscard.split()
                
                psUser=tt[0]
                psId=int(tt[1])
                psClocktime=tt[4]
                psTime=tt[6]
                if(len(tt) > 8):     
                    for n in range(8,len(tt)):
                        if(n == 8): psName=tt[8]
                        else:       psName="%s %s"%(psName,tt[n])

                elif(len(tt) == 8):  psName=tt[7]
                else:                print 'EEE tt: ',tt ; sys.exit()
                
                PSs[psId]=(psClocktime,psTime,psName)
                MF.appendDictList(PStimes, psId, psPhrtime)
                if(verb == 2): print 'cccc',psDtg,psPhrtime,psUser,psId,psClocktime,psTime,psName
        tt=card.split()
        psDtg=tt[1]
        tt=tt[2].split(':')
        psPhr=float(tt[0])+float(tt[1])/60.0 + float(tt[2])/(60.*60.)
        psPhrtime="%s+%06.3f"%(psDtg,psPhr)
        psPhrtime="%s %02d:%02d:%02d"%(psDtg,int(tt[0]),int(tt[1]),int(tt[2]))
        pscards=[]
    else:
        pscards.append(card)
        
        
psids=PSs.keys()
for psid in psids:
    etime=PStimes[psid][-1]
    ntimes=len(PStimes[psid])
    MF.appendDictList(PSbyTimes,etime,(psid,ntimes,PSs[psid]))
    if(verb == 2): print 'ppp  %10d %s %04d'%(psid,etime,ntimes),PSs[psid][-1],PSs[psid][0]
        
pstimes=PSbyTimes.keys()
pstimes.sort()

byRtimeCards={}
killPSs=[]

percentBy=1.0
if(sortBy != None and len(sortBy.split(":")) == 2):
    (sortBy,percentBy)=sortBy.split(":")
    sortBy=int(sortBy)
    percentBy=float(percentBy)*0.01
elif(sortBy != None):
    sortBy=1
else:
    sortBy=0
    sortBy=1
    
for pstime in pstimes:
    card="%s"%(pstime)
    psdtg=card[0:10]
    gotdtg=0
    for dtg in dtgs:
        if(dtg == psdtg): gotdtg=1
        
    if(not(gotdtg)): continue
    
    
    PSbys=PSbyTimes[pstime]
    
    n=1
    for PSby in PSbys:
        #print 'ppp',PSby
        pid=PSby[0]
        rtime=(PSby[1]*sleepytime)/60.0
        job=PSby[2][-1]
        jj=job.split()
        (pdir,pfile)=os.path.split(jj[0])
        
        try:
            popt1=jj[1]
        except:
            popt1=''

        if(doCurPids and not(pid in curPidPSs)): continue
        
        # -- make print card
        #
        for nn in range(1,len(jj)):
            pfile=pfile+' '+jj[nn]

        cardBy="%s %10d  %6.2f  %-70s"%(pstime,pid,rtime,pfile[0:70])
        if(n == 1):
            card="%s %10d  %6.2f  %-70s"%(card,pid,rtime,pfile[0:70])
        else:
            card="                    %10d  %6.2f  %-70s"%(PSby[0],rtime,pfile[0:70])
            
        if(PSls != None and mf.find(pfile, PSls)):
            MF.appendDictList(byRtimeCards,rtime,cardBy)
        elif(PSls == None):
            MF.appendDictList(byRtimeCards,rtime,cardBy)
    
        if(pid in curPidPSs):   
            if(verb): print 'PSMA--rrrrr',pid,job,rtime
            
        # -- find long ps only in current
        #
        if(killLongPS and pid in curPidPSs):
            
            pyjob=pfile.split()[0]
            if(pyjob in rtimeMaxPSJobs):
                rtimeMax=rtimeMaxPS[pyjob]
                if(rtime > rtimeMax):
                    print 'LLLOOONNNGGG-%s: pyjob: %s  rtime: %6.2f  rtimeMax: %6.2f'%(pyfile,pyjob,rtime,rtimeMax)
                    killPSs.append(pid)
                else:
                    oktime=mf.dtg('curtime')
                    print 'oookkkaaayyy-%s: pyjob: %40s  rtime: %6.2f  rtimeMax: %6.2f'%\
                          (pyfile,pyjob,rtime,rtimeMax),'time: ',oktime
        
        
    n=n+1
    if(not(killLongPS)):
        if(PSls == None):
            if(sortBy != 1 and not(doCurPids)):
                print card

            elif(PSby[0] in curPidPSs.keys() and sortBy != 1):
                print card
                
        elif(PSls != None and mf.find(pfile, PSls)): 
            if(sortBy != 1 and not(doCurPids)):
                print cardBy

            elif(sortBy != 1 and PSby[0] in curPidPSs.keys()):
                print cardBy
            
if(sortBy == 1 and not(killLongPS)):
    rtimes=byRtimeCards.keys()
    rtimes=mf.uniq(rtimes)
    rtimes.reverse()
    
    nprint=int(len(rtimes)*percentBy)
    
    for n in range (0,nprint):
        for card in byRtimeCards[rtimes[n]]:
            print card
        
# -- 20160730 -- redo mdeck if got stuck...
# -- 20210915 -- remove...not here...
#
if(killLongPS and len(killPSs) > 0):
    
    for killPS in killPSs:
        if(killPS in curPidPSs.keys()):
            killPSJob=curPidPSs[killPS]
            killtime=mf.dtg('curtime')
            MF.sTimer('longPS kill')
            print 'KKKKKKKKKKKKKKKilling: curPidPSs:',killPSJob,' PS: ',killPS,'rtimeMax: ',rtimeMaxPS[killPSJob],'time: ',killtime
            cmd="kill -9 %s"%(killPS)
            mf.runcmd(cmd,ropt)
            MF.dTimer('longPS kill')


sys.exit()
