#!/usr/bin/env python

from tcbase import *

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#
class AdeckCmdLine(CmdLine,AdeckSources):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['source',  '''source1[,source2,...,sourceN]'''],
            }

        self.defaults={
            'doupdate':0,
            }

        self.options={
            'yearopt':        ['y:',None,'a','year1,year2,...,yearNNN'],
            'override':       ['O',0,1,'override'],
            'verb':           ['V',0,1,'verb=1 is verbose'],
            'warn':           ['W:',0,1,'warning'],
            'ropt':           ['N','','norun',' norun is norun'],
            'doadecks':       ['A',0,1,'1 - make adecks'],
            
            'doacardout':     ['D',0,1,'1 - output acards'],
            'doputdss':       ['P',0,1,'1 - putDSs'],
            'dochkIfRunning':      ['o',1,0,'do NOT do chkifrunning in M.DataSets MF.chkIfJobIsRunnin'],
            'dols':           ['l',0,1,'1 - list'],
            'dolslong':       ['L',0,1,'1 - long list'],
            
            'stmopt':         ['S:',None,'a','stmopt'],
            'aidopt':         ['T:',None,'a','taid'],

            'doVdeck':        ['v',1,0,"""do NOT run vdeck after doing adeck"""],
            
            }

        self.purpose='''
purpose -- parse and create adeck card data shelves
'''
        self.examples='''
%s test
'''

    def ChkSource(self,year=None):

        if(year != None):
            self.getSourcesbyYear(year)
            
        iok=0
        for s in self.sources:
            if(self.source == s): iok=1 ; break

        return(iok)

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

aliases={}

argv=sys.argv
CL=AdeckCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)


if(dochkIfRunning == 0):

    # -- still getting conflicts when doing updating -- corrupts either zipfile or pypdb
    #    current config
    #jobopt=pyfileopt
    #killjob=1
    #    new config -- wait five minutes before bailing -- don't depend on jobopt
    # -- go back to old settings?
    jobopt=pyfileopt.split()[0]
    # -- this causes a big problem when more than one adk is running -- from fp2 -T
    #killjob=0
    killjob=1
    pyfile='w2-tc-dss-adeck.py'

    MF.sTimer('adk-chkIfJobIsRunning pyfile: %s jobopt: %s killjob: %s'%(pyfile,jobopt,killjob))
    rc=MF.chkIfJobIsRunning(pyfile,jobopt=jobopt,killjob=killjob,verb=verb,nminWait=1,timesleep=5)
    MF.dTimer('adk-chkIfJobIsRunning pyfile: %s jobopt: %s killjob: %s'%(pyfile,jobopt,killjob))

iyearopt=yearopt
if(yearopt == 'cur' or yearopt == 'ops' or yearopt == None):
    yearopt=curyear
    year=curyear

sources=source.split(',')
years=yearopt.split(',')
stmopts=stmopt.split(',')

if(len(sources) > 1 or source == 'all' or len(years) > 1):

    for year in years:
        for source in sources:
            if(source == 'all'): sources=CL.getSourcesbyYear(year)
            cmd="%s %s -y %s"%(CL.pypath,source,year)
            for o,a in CL.opts:
                if(o != '-y'):
                    cmd="%s %s %s"%(cmd,o,a)
            mf.runcmd(cmd,ropt)

    sys.exit()

# -- multiple stmopts
#
elif(len(stmopts) > 1):
    
    for stmopt in stmopts:
        cmd="%s %s -S %s"%(CL.pypath,source,stmopt)
        for o,a in CL.opts:
            if(o != '-S'):
                cmd="%s %s %s"%(cmd,o,a)        
        mf.runcmd(cmd,ropt)
        
    sys.exit()    
    

if(len(years) == 1): year=years[0]

if(not(CL.ChkSource(year=year))):

    if(verb): print 'WWW not a standard source:',source,' try using setAdeckSource method in AdeckSources class in the command line...'
    (ad,aliases)=CL.setAdeckSource(source,year)

    if(ad == None):
        print """EEE don't know how to make AdeckSource class for: """,source
        sys.exit()


if(stmopt != None):

    if(not(mf.find(stmopt,'cur'))):
        tstmids=MakeStmList(stmopt,verb=verb)

    elif(mf.find(stmopt,'cur')):
        dtgs=mf.dtg_dtgopt_prc(stmopt,ddtg=6)
        print dtgs
        tstmids=[]
        for dtg in dtgs:
            (stmids,btcs)=tD.getDtg(dtg)
            tstmids=tstmids+stmids
            tstmids=mf.uniq(tstmids)
    
else:
    tstmids=MakeStmList(stmopt,verb=verb,dofilt9x=1)


if(tstmids == None): pass

elif(len(tstmids) == 0): errAD('tstmids')

if(tstmids != None and iyearopt == None):
    years=getYearsFromStmids(tstmids)

if(len(years) > 1):
    print 'EEE too many years for ada: ',years
    sys.exit()

year=years[0]
print 'qqqqqqqqqqqqq ',tstmids,year

# --- get mdecks
#
dsbdir="%s/DSs"%(TcDataBdir)

dbname='mdecks'
dbfile="%s.pypdb"%(dbname)
mDS=DataSets(bdir=dsbdir,name=dbfile,dtype=dbname,verb=verb)
mD=mDS.getDataSet(key=year).md

# -- get adecks
#
dbtype='adeck'
dbname="%s_%s_%s"%(dbtype,source,year)
dbfile="%s.pypdb"%(dbname)

aDS=DataSets(bdir=dsbdir,name=dbfile,dtype=dbtype,verb=verb,doDSsWrite=1)


if(aidopt != None):  taids=aidopt.split(',')
else:                taids=None

(omodel,smodel,ostmids)=makeEnsMeanAdeck(aDS,mD,source,tstmids,year,verb=verb,override=override)


if(doVdeck and len(ostmids) > 0):

    overopt=''
    if(override): overopt='-O'

    modelopt=''
    if(omodel != None and smodel != None):
        modelopt='-T %s,%s'%(omodel,smodel)

    for stmid in ostmids:
        cmd="w2.tc.dss.vdeck.py %s -S %s %s %s"%(source,stmid,modelopt,overopt)
        MF.runcmd(cmd,ropt)


sys.exit()

        


