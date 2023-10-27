#!/usr/bin/env python

from MD import *
from tcbase import LsAidsStormsDss

MF=MFutils()

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class MdeckCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
#            1:['year',    'no default'],
            }

        self.defaults={
            'stattype':'s',
            'doupdate':0,
            }

        self.options={
            'yearopt':['y:',None,'a','year1,year2,...,yearNNN'],
            'override':['O',0,1,'override'],
            'verb':['V',0,1,'verb=1 is verbose'],
            'ropt':['N','','norun',' norun is norun'],
            'dols':['l',0,1,'1 - list'],
            'dolslong':['L',0,1,'1 - long list'],
            'dolsgen':['G',0,1,'1 - ls genesis dtgs only'],
            'stmopt':['S:',None,'a','stmopt'],
            'warn':['W:',0,1,'warning'],
            'update':['u',0,1,'only update mdeck'],
            }

        self.purpose='''
purpose -- parse mdecks create TC data shelves
%s 2009
'''
        self.examples='''
%s 2009
'''

    def ChkSource(self):

        iok=0
        for s in self.sources:
            if(self.source == s): iok=1 ; break

        return(iok)

#eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
# errors

def errAD(option,opt=None):

    if(option == 'tstmids'):
        print 'EEE # of tstmids = 0 :: no stms to verify...stmopt: ',stmopt
    elif(option == 'tstms'):
        print 'EEE # of tstms from stmopt: ',stmopt,' = 0 :: no stms to verify...'
    else:
        print 'Stopping in errAD: ',option

    sys.exit()
        


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#


MF.sTimer(tag='mdeck')

argstr="pyfile -y 2010 -S w.10 -P"
argv=argstr.split()
argv=sys.argv
CL=MdeckCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


if(yearopt == 'cur' or yearopt == 'ops' or yearopt == None):
    yearopt=curyear
    year=curyear

years=yearopt.split(',')

dsbdir="%s/DSs"%(TcDataBdir)
dbname='mdecks'

dbfile="%s.pypdb"%(dbname)
DSs=DataSets(bdir=dsbdir,name=dbfile,dtype=dbname,verb=verb)

if(stmopt != None): tstmids=MakeStmList(stmopt,dofilt9x=1,verb=verb)
else: tstmids=None

if(tstmids == None): pass
elif(len(tstmids) == 0): errAD('tstmids')

if(stattype == 's'):

    def lsstm(tag,tstmid,stmname,vmax,nwstate,nwage):
        print '%s  %s %-12s  vmax: %3d  age(%s): %5.0f  %5.2f [d]'%(tag,tstmid,stmname,vmax,nwstate,nwage*24,nwage)

        
    if(stmopt == None): print 'EEE must set stmopt for stattype: ',stattype; sys.exit()

    dsname='mdeck_stmstats'
    mdSS=DSs.getDataSet(key=dsname)
    fs=mdSS.FinalStmStats
    stmids=fs.keys()
    stmids.sort()

    minprewarn=0.5
    maxprewarn=5.0
    prewarnage=[]
    for tstmid in tstmids:
        if(tstmid in stmids):
            ss=fs[tstmid]
            (stmname,Latmin,Latmax,Latmean,Lonmin,Lonmax,Lonmean,Vmax,
             Ace,sAceDays,sTCd,
             nRi,nED,nRd,
             TimePeriodsWarn,
             TimePeriodsTC)=ss

            try: nw=TimePeriodsWarn[0]
            except:
                print 'WWW no warnings issued for tstmid: ',tstmid,' Press!'  ; continue
            
            nwstate=nw[0]
            nwage=nw[1]
            prewarnage.append(nwage)

            try: wn=TimePeriodsWarn[1]
            except: wn=None

            if(wn != None):
                wnstate=wn[0]
                wnage=wn[1]

            if(nwage <= minprewarn):
                lsstm('Short 9X: ',tstmid,stmname,Vmax,nwstate,nwage)

            if(nwage >= maxprewarn):
                lsstm(' Long 9X: ',tstmid,stmname,Vmax,nwstate,nwage)

    rc=SimpleListStats(prewarnage,hasflag=0)
    (mean,amean,sigma,max,min,n)=rc
    print "mean prewarnage: %5.0f  %5.2f[d] sigma: %5.2f  max: %5.2f  min: %5.2f N: %d"%(mean*24,mean,sigma,max,min,n)

    

MF.dTimer(tag='mdeck')
sys.exit()




if(dols or dolslong or lstype == 'g' or dolsgen):
    if(dolslong): lsopt='l'
    if(dols): lsopt='s'
    if(dolsgen): lstype='g'
    stms=LsStormsDss(DSs,year,tstmids,lsopt=lsopt,lstype=lstype)
    sys.exit()

if(domdecks):
    print 'MMMMMMMMMMMMMMMMMM doing mdeck for ',year
    mdD=DSs.getDataSet(key='mdeck_dtg')
    mdDg=DSs.getDataSet(key='mdeck_dtg_gen')
    mdDs=DSs.getDataSet(key='mdeck_stmid')
    md=Mdeck(year,mdD,mdDg,mdDs)

if(doputdss):
    print 'PPPPPPPPPPPPPPPPPP putting dataset md...'
    DSs.putDataSet(md.ds,key=year)
    DSs.putDataSet(md.mdD,key='mdeck_dtg')
    DSs.putDataSet(md.mdDg,key='mdeck_dtg_gen')
    DSs.putDataSet(md.mdDs,key='mdeck_stmid')

if(dostmstats):
    print 'SSSSSSSSSSSSSSSSSSSSSS dostmstats...'
    dsname='mdeck_stmstats'
    mdSS=DSs.getDataSet(key=dsname)
    ms=MdeckSimple(year,mdSS,verb=verb)
    ms.analyzeBt(verb=verb)
    DSs.putDataSet(ms,key=dsname)


MF.dTimer(tag='mdeck')

sys.exit()


        


