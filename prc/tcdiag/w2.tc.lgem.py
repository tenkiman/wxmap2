#!/usr/bin/env python

from tcbase import *
import M2
import FM

from TCdiag import TcDiag,getDtgsModels,cycleByDtgsModels,getStmids

class TcDiag(TcDiag):


    aidAliases={
        'ngf2':'gfs2',
        'nuk2':'ukm2',
        'nec2':'ecm2',
        'nng2':'ngp2',
        'ncm2':'cmc2',
        'nngc':'ngpc',
        'nnav':'navg',
        }


    def initAD(self,dtg,model,verb=0):

        sdir='/dat3/tc/tmtrkN'

        if(self.trkSource == 'tmtrk'):
            apath="%s/%s/%s/tctrk.atcf.%s.%s.txt"%(sdir,dtg,model,dtg,model)
            spath="%s/%s/%s/tctrk.sink.%s.%s.txt"%(sdir,dtg,model,dtg,model)
        elif(self.trkSource == 'mftrk'):
            apath="%s/%s/%s/wxmap2.v010.%s.%s.*"%(sdir,dtg,model,model,dtg)
            spath=''
        else:
            print 'EEE invalid trkSource: ',trkSource
            sys.exit()

        self.aid=self.adeckaid
        if(not(mf.find(model,'rtfim'))): self.aid=model

        self.aD=AD.Adeck(apath,verb=verb,aliases=self.aidAliases)
        self.apath=apath
        
        # -- since we're only doing one aid, pull first aid in aids
        #
        if(len(self.aD.aids) > 0): self.aidname=self.aD.aids[0]

        self.aDS=AD.AdeckSink(spath,verb=self.verb)
        if(self.verb or verb):
            print 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA apath: ',apath,' self.aid: ',self.aid,' self.adeckaid ',self.adeckaid,' model: ',model
            print 'SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS spath: ',spath

        self.adstm2ids=self.aD.stm2ids


    def setTCtracker(self,stmid,maxtau=168,quiet=0):


        # -- first source is adecks from TMtrker from w2flds...
        #
        if(self.aD != None):

            self.stmid=stmid
            self.getAidtrk(self.dtg,self.stmid)
            self.getAidcards(self.dtg,self.stmid)
            ntaus1=0
            lasttau1=0

            if(self.aidtaus != None):
                aidtrks1=self.aidtrk
                aidtaus1=self.aidtaus
                ntaus1=len(self.aidtaus)
                lasttau1=aidtaus1[-1]
            else:
                # -- bail point 0 -- no tracker taus for aid
                #
                #print 'WWW bail point #0'
                return(0)
                
        else:
            # -- bail point 1 -- no tracker taus for aid
            #
            print 'WWWWW forcing use of tmTrkN...'
            return(0)

        self.aidtrk=aidtrks1
        self.aidtaus=aidtaus1
        self.aidsource='tmTrkN'

        # -- bail point 2 -- no tracker taus for aid
        #
        if(len(self.aidtaus) == 0):
            print 'WWW(%s)'%(self.basename),'no final  tracker taus for dtg: ',self.dtg,' model: ',self.model,' stmid: ',self.stmid,' bailing...'
            return(0)
            
        # -- bail point 3 -- singleton -- rlat 0/0
        #
        if(len(self.aidtaus) == 1):
            trk0=self.aidtrk[self.aidtaus[0]]
            if( len(trk0) >= 2 and trk0[0] == 0.0 or trk0[1] == 0.0):
                print 'WWW(%s)'%(self.basename),'singleton trk = 0,0 taus for dtg: ',self.dtg,' model: ',self.model,' stmid: ',self.stmid,' bailing...'
            return(0)
            
        
        self.diagpath="%s/diag.%s.%s.txt"%(self.pltdir,self.stmid,self.model)

        self.pyppathDiag="%s/diag.%s.pyp"%(self.pltdir,self.stmid)
        self.pyppathHtml="%s/html.%s.pyp"%(self.pltdir,self.stmid)
        self.pyppathData="%s/data.%s.pyp"%(self.pltdir,self.stmid)
        self.diagpathALL="%s/diag.all.%s.%s.txt"%(self.pltdir,self.stmid,self.model)
        self.diagpathWebALL="%s/diag.all.%s.%s.txt"%(self.webdiagdir,self.stmid,self.model)
        
        self.pyppathDataALL="%s/data.all.%s.pyp"%(self.pltdir,self.stmid)
        if(self.doDiagOnly):
            self.diagpath=self.diagpathALL
            self.pyppathData=self.pyppathDataALL

        if(self.aidtrk != None and not(quiet)):
            print 'TCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTC got tracker from aidsource: %-10s'%(self.aidsource),' model: %-6s'%(self.model),' stmid: ',self.stmid,' ntaus: %3d'%(len(self.aidtaus)),' lasttau: %3d'%(self.aidtaus[-1])

        # -- limit taus
        ataus=[]
        if(maxtau != None):
            for atau in self.aidtaus:
                if(atau in self.targetTaus):
                    ataus.append(atau)
            self.aidtaus=ataus


        self.aidMotion={}

        # -- get the motion based on the next tau
        #
        ntaus=len(self.aidtaus)

        for tau in self.aidtaus:
            
            # -- get track for spd/dir calc
            taup0=tau
            (latcp0,loncp0,vmaxcp0,pmincp0)=self.aidtrk[taup0]

            np=self.aidtaus.index(tau)

            # -- check if at end of tau...
            #
            if(np == ntaus-1):
                np=np-1
                taup0=self.aidtaus[np]
                (latcp0,loncp0,vmaxcp0,pmincp0)=self.aidtrk[taup0]

            # -- get track at next tau
            #
            np1=np+1
            taup1=self.aidtaus[np1]
            (latcp1,loncp1,vmaxcp1,pmincp1)=self.aidtrk[taup1]

            dt=taup1-taup0
            if(dt == 0):
                dir=9999.
                spd=9999.
            else:
                (dir,spd,umot,vmot)=rumhdsp(latcp0,loncp0,latcp1,loncp1,taup1-taup0)
                if(dir == 360.0): dir=0.0

            # -- bug in setting the endpoint, bandaid for now...
            #
            if(spd < 0.0):
                spd=9999.
                dir=9999.

            self.aidMotion[tau]=(dir,spd)


        return(1)


def getAtrkFromStmid(tD,stmid,dtg):

    atrk={}
    ttrk=None
    
    (bstmids,btcs)=tD.getDtg(dtg,dupchk=0,verb=0)

    if(tstmid in bstmids):
        dss=tD.getDSsFullStm(tstmid)
        (ttrk,tdtgs)=dss.getMDtrk()

    if(ttrk != None):
        dtg0=dtg
        dtgm12=mf.dtginc(dtg,-12)

        trk0=ttrk[dtg0]
        
        try:
            trkm12=ttrk[dtgm12]
            type=1
        except:
            trkm12=None

        if(trkm12 == None):
            try:
                trkm12 = ttrk[mf.dtginc(dtg0,-6)]
                trk0   = ttrk[mf.dtginc(dtg0,+6)]
                type=2
            except:
                trk0=None
                trkm12=None

        if(trk0 == None):
            try:
                trkm12 = ttrk[mf.dtginc(dtg0,+0)]
                trk0   = ttrk[mf.dtginc(dtg0,+6)]
                type=3

            except:
                print 'WWW(getAtrkFromStmid) -- perverse case of single posit bt for stmid: ',stmid,' dtg: ',dtg
                return(atrk)


        print '000 ',type,trk0
        print '111 ',type,trkm12
        
        atrk[0]   =trk0[0:4]
        atrk[-12] =trkm12[0:4]


    return(atrk)



def Atrk2Icarq(atrk):

    (rlat0,rlon0,rvmax0,rpmin0)=atrk[0]
    (rlatm12,rlonm12,rvmaxm12,rpminm12)=atrk[-12]

    (course,speed,eiu,eiv)=rumhdsp(rlatm12,rlonm12,rlat0,rlon0,12)

    ihead=int(course+0.5)
    ispeed=int(speed+0.5)

    if(rlon0 >= 180.0): rlon0 = rlon0-360.0
    if(rlonm12 >= 180.0): rlonm12 = rlonm12-360.0
    
    print rlat0,rlon0,rvmax0,rpmin0
    print rlatm12,rlonm12,rvmaxm12,rpminm12

    ilat0=int("%5.0f"%(rlat0*10.0))
    ilon0=int("%5.0f"%(rlon0*10.0))
    ivmx0=int("%5.0f"%(rvmax0))
    
    ilatm12=int("%5.0f"%(rlatm12*10.0))
    ilonm12=int("%5.0f"%(rlonm12*10.0))
    ivmxm12=int("%5.0f"%(rvmaxm12))

    iper=ivmx0-ivmxm12

    print rlat0,rlon0,rlatm12,rlonm12
    
    ocard="%10s %5d %5d %5d %5d %5d %5d %5d %5d %5d"%(dtg,ilat0,ilon0,ilatm12,ilonm12,ivmx0,ivmxm12,ihead,ispeed,iper)
    print ocard
    return(ocard)
    



class MyCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',  'run dtgs'],
            2:['modelopt',    'model'],
            }

        self.defaults={
            'doupdate':0,
            'doga':0,
            'dowebserver':0,
            'gaopt':'-g 1024x768',
            'domandonly':0,
            'doStndOnly':0,
            'doDiagOnly':1,
            'dowebserver':0,
            'dotarball':0,
            'doinventory':0,
            'dohtmlvars':0,
            'dols':0,
            }

        self.options={
            'override':['O',0,1,'override'],
            'verb':['V',0,1,'verb=1 is verbose'],
            'quiet':['q',0,1,' run GA in quiet mode'],
            'ropt':['N','','norun',' norun is norun'],
            'stmopt':['S:',None,'a','stmopt'],
            'doplot':['P',0,1,'1 - make diag plots'],
            'dodatcheck':['c',0,1,'1 - check if .ctlpath there, not really needed'],
            'icarqvmax':['i',1,0,'use model Vmax in iships.x vice default of using CARQ'],
            'lsadeck':['l',0,1,'lsadeck'],
            }

        self.purpose='''
purpose -- generate TC large-scale 'diag' file for lgem/ships/stips intensity models
 '''
        self.examples='''
%s 2010052500 gfs2
'''


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#

MF.sTimer(tag='all')

argv=sys.argv
CL=MyCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

tbdir='/dat3/tc/tcanal'

(dtgs,models)=getDtgsModels(CL,dtgopt,modelopt,stmopt=stmopt)
(dtg,model)=cycleByDtgsModels(CL,dtgs,models,stmopt=stmopt)

tG=TcDiag(dtg,model,doplot=doplot,
          gaopt=gaopt,
          domandonly=domandonly,
          doStndOnly=doStndOnly,
          doDiagOnly=doDiagOnly,
          dols=dols,
          dowebserver=dowebserver,
          doga=doga,verb=verb)

if(tG.rcM2 == None and dodatcheck):
    print 'WWW(%s)'%(CL.pyfile),': NNNNNNNNNNNNNNNNNNNNNNNNo data for dtg: ',dtg,' model: ',model
    sys.exit()

MF.ChangeDir(CL.pydir)

#tG.setTCs()
#adstm2ids=None
#if(hasattr(tG,'adstm2ids')): adstm2ids=tG.adstm2ids
#tstmids=getStmids(dtg,tG.stmids,adstm2ids,stmopt=stmopt,dols=1)

# -- tcs -- taken from currently /w21/src/tcdiag/p.fld.lsdiag.py
tG.setTCs()

tstmids=getStmids(dtg,tG.stmids,tG.adstm2ids,stmopt=stmopt,dols=0)


for tstmid in tstmids:

    # -- skip if not nhc storm
    #
    if(not(IsNhcBasin(tstmid))): continue

    rc=tG.setDiagPath(tstmid,tbdir=tbdir)
    
    tG.verb=verb
    rc=tG.setTCtracker(tstmid)

    # -- skip if not w2fld tracker...
    #
    if(not(hasattr(tG,'aidsource')) or rc == 0):continue
    #if(tG.aidsource != 'w2flds'): continue


    aDcarq=AD.getCarqFromDss(tstmid,verb=0)
    #print tstmid,aDcarq.ats.keys()
    if(aDcarq == None):
        print 'WWW(aDcarq): not available for tstmid: ',tstmid,' dtg: ',dtg,' model: ',model
        continue

    # -- first see if there are CARQ cards
    #
    try:
        atrk=aDcarq.ats[dtg]
    except:
        atrk={}

    # -- second try reconstructing from BT
    #
    if(len(atrk) == 0):
        atrk=getAtrkFromStmid(tG.tD,tstmid,dtg)


    # -- if no luck; bail
    #
    if(len(atrk) == 0):
        print 'WWW(atrk): no posits in atrk for tstmid: ',tstmid,' dtg: ',dtg,' model: ',model
        continue


    if(hasattr(tG,'finalDiagPath')):
        diagpath=tG.finalDiagPath
    elif(hasattr(tG,'diagpathALL')):
        diagpath=tG.diagpathALL
    else:
        print 'WWW(diagpath): not available for tstmid: ',tstmid,' dtg: ',dtg,' model: ',model
        continue

    (dir,file)=os.path.split(diagpath)

    shipstxt="%s/ships.txt.%s.%s.%s.txt"%(dir,tstmid,model,dtg)
    shipsadk="%s/ships.adk.%s.%s.%s.txt"%(dir,tstmid,model,dtg)
    shipslog="%s/ships.log.%s.%s.%s.txt"%(dir,tstmid,model,dtg)
    shipscrq="%s/ships.crq.%s.%s.%s.txt"%(dir,tstmid,model,dtg)

    shipsadkw2dir="%s/%s/w2flds/%s"%(TcAdecksEsrlDir,dtg[0:4],dtg)

    if(verb):
        print 'diagpath: ',diagpath
        print 'shipstxt: ',shipstxt
        print 'shipsadk: ',shipsadk
        print 'shipslog: ',shipslog
        print 'shipscrq: ',shipscrq

    if(lsadeck):
        cmd="""(ls -la %s ; ls -la %s ; cat %s ; cat %s | grep 'G, ' ; cat %s  )"""%(shipsadk,diagpath,diagpath,shipsadk,shipstxt)
        mf.runcmd(cmd,ropt)
        sys.exit()

        

    MF.ChkDir(shipsadkw2dir,'mk')

    # -- skip if already run
    #
    if(MF.ChkPath(shipsadk) and not(override)):
        print 'WWW(shipsadk): ',shipsadk,' already done...override = 0...Press....'
        continue
    

    cmd="ln -s -f %s modeldiag.dat"%(diagpath)
    MF.runcmd(cmd,ropt)

    cmd="ln -s -f %s ships.txt"%(shipstxt)
    MF.runcmd(cmd,ropt)

    cmd="ln -s -f %s ships.dat"%(shipsadk)
    MF.runcmd(cmd,ropt)

    cmd="ln -s -f %s ships.log"%(shipslog)
    MF.runcmd(cmd,ropt)

    if(len(atrk) > 0):
        ocard=Atrk2Icarq(atrk)
        MF.WriteString2File(ocard,shipscrq)

    cmd="ln -s -f %s icarq.dat"%(shipscrq)
    MF.runcmd(cmd,ropt)

    # -- run the model
    #
    if(icarqvmax == 0):
        cmd="iships.x -i"
    else:
        cmd="iships.x"

    MF.runcmd(cmd,ropt)

    # -- cp the adeck to the directory with tmtrk output
    #
    cmd="cp %s %s/."%(shipsadk,shipsadkw2dir)
    MF.runcmd(cmd,ropt)

    MF.dTimer(tag='all')

    continue



    tG.replaceAidcards(param=None,aidname='test2')

    aliases={'gfss':'gfs2s','gfsd':'gfs2d','gfsg':'gfs2l'}

    if(MF.ChkPath(shipsadk)):
        aL=AD.Adeck(shipsadk,aliases=aliases)
        aL.ls()

    
sys.exit()



