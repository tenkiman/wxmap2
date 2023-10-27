#!/usr/bin/env python

import w2
import TCw2 as TC

from M import *

MF=MFutils()




#llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
#
# local routines


def getHfipGfsEnkfWW3Inventory(w3dir,invpath,dtgopt,verb=0,ropt=''):

    dtgs=[]
    areaStms=[]
    
    DtgStms={}
    StmDtgs={}
    DtgStmPrds={}
    DtgStmPrdTaus={}

    ppaths=glob.glob("%s/*.png"%(w3dir))
    ppaths=glob.glob("%s/??????????/*.gif"%(w3dir))

    for ppath in ppaths:
        (dir,file)=os.path.split(ppath)
        (base,ext)=os.path.splitext(file)
        tt=base.split('_')
        if(tt[0] == 'ellipses'):
            prod=tt[0]
            dtg=tt[1]
            b2id=tt[2]
            stm2id=tt[3]
            # -- bad filename...
            try:
                b1id=TC.Basin2toBasin1[b2id]
            except:
                print 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW bad ellipses file:           ',ppath
                continue
            
            stm=stm2id+b1id
            tau='00'
            itau=int(tau)
            opath="%s/%s%s_%s_gfsenkf_f%02d.png"%(dir,prod,dtg,stm,itau)
            cmd="ln -s -f %s %s"%(ppath,opath)
            mf.runcmd(cmd,ropt)

        else:
            prod=tt[0][0:len(tt[0])-10]
            dtg=tt[0][len(tt[0])-10:]
            stm=tt[1]
            model=tt[2]
            eps=tt[3]
            print prod,dtg,stm,model,eps
            try:
                tau=tt[4].split('.')[0][1:]
                itau=int(tau)
            except:
                print 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW bad tau skip...correct ppath:',ppath
                continue

        MF.appendDictList(DtgStms,stm,dtg)
        MF.appendDictList(StmDtgs,dtg,stm)
        MF.append2TupleKeyDictList(DtgStmPrds,dtg,stm,prod)
        MF.append3TupleKeyDictList(DtgStmPrdTaus,dtg,stm,prod,itau)


    DtgStms=MF.uniqDict(DtgStms)
    StmDtgs=MF.uniqDict(StmDtgs)
    DtgStmPrds=MF.uniqDict(DtgStmPrds)
    DtgStmPrdTaus=MF.uniqDict(DtgStmPrdTaus)
    
    cards=[]
    cards=cards+MF.PrintDict(DtgStms)
    cards=cards+MF.PrintDict(StmDtgs)
    cards=cards+MF.PrintDict(DtgStmPrds)
    cards=cards+MF.PrintDict(DtgStmPrdTaus)

    MF.WriteList2File(cards,invpath,verb=1)
    
    sys.exit()


def rsyncWjetEnkf2Rapb(tdir,dodelete=0):

    sdir="/lfs1/projects/gfsenkf/hurrplots/"
    mf.ChangeDir(tdir)
    expath="%s/ex-gfsenkf.txt"%(pydir)
    server=w2.WjetScpServer
    delopt=''
    if(dodelete): delopt='--delete'
    cmd='''rsync -avz %s --exclude-from=%s  %s:%s %s'''%(delopt,expath,server,sdir,tdir)
    mf.runcmd(cmd,ropt)


def cleanGfsenkfFiles(wdir,keepdtg,ropt):

    MF.ChangeDir(wdir)
    curdtgs=glob.glob("%s??????"%keepdtg[0:4])
    curdtgs.sort()

    for curdtg in curdtgs:
        cdtg=curdtg.split('/')[0]
        dtime=mf.dtgdiff(keepdtg,cdtg)
        if(dtime < 0.0):
            cmd="rm -r %s/%s"%(wdir,curdtg)
            mf.runcmd(cmd,ropt)


    
    

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class MdeckCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',    'no default'],
            }

        self.options={
            'verb':['V',0,1,'verb=1 is verbose'],
            'ropt':['N','','norun',' norun is norun'],
            'doinventory':['I',1,0,"""do NOT do inventory for gfsenkf.php """],
            'dorsync':['R',1,0,"""do NOT rsync plots from wjet to /data/projects/hftp/gfsenkfDAt """],
            'dodelete':['D',0,1,"""do --delete in rsync"""],
            'cleanFiles':['K',0,1,"""clean files <= dtgopt"""],
            }

        self.purpose="""
purpose -- rsync/inventory of jeff whitakers's plots from the T254 engkf
"""
        self.examples='''
%s cur-12
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

dowebupdate=w2.W2doW3Rapb

webdirext="%s/gfsenkf"%(w2.HfipRapbDir)
invpath="%s/inv.hfip.gfsenkf.txt"%(webdirext)
w3dir="%s/../gfsenkfDAT"%(webdirext)


if(cleanFiles):
    dtgs=mf.dtg_dtgopt_prc(dtgopt)
    cleanGfsenkfFiles(w3dir,dtgs[0],ropt=ropt)
    sys.exit()
    

# -- first rsync over the plots...
#
if(dorsync):
    rc=rsyncWjetEnkf2Rapb(w3dir,dodelete=dodelete)

# -- make the inventory
#
if(doinventory):
    getHfipGfsEnkfWW3Inventory(w3dir,invpath,dtgopt,verb=verb)

sys.exit()
