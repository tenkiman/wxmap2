#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from tcbase import Basin2toBasin1,Basin1toBasin2

class tcTrk(MFbase):
    
    def __init__(self,
                 stmid=None,
                 vmax=None,
                 rlat=None,
                 rlon=None,
                 dirmotion=-999,
                 spdmotion=-999,
                 r34=-999,
                 r50=-999,
                 positsource='X',
                 tcflag='XX',
                 warnflag='XX',
                 tdo='XXX',
                 landfrac=None,
                 ):
        
        self.stmid=stmid
        self.vmax=vmax
        self.rlat=rlat
        self.rlon=rlon
        self.dirmotion=dirmotion
        self.spdmotion=spdmotion
        self.r34=r34
        self.r50=r50
        self.positsource=positsource
        self.tcflag=tcflag
        self.warnflag=warnflag
        self.tdo=tdo
        self.landfrac=landfrac
        self.tcname=GetTCName(stmid)
        
        
        
        
        
#llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
# local unbounded methods

def getSdirTbdir(stmid):

    bdir='/w21/dat/tc/mtcswa'
    #bdir='/dat10/dat/tc/cira/mtcswa_Late'
    # -- relocate to prj dir
    #
    obdir='/w21/prj/tc/2013/20131112_mtcswa_cecile_tc_intensity_change/mtcswa'

    tt=stmid.split('.')
    
    if(len(tt) == 1): 
        year=tt[0]
        odir=bdir
        sdir='%s/%s'%(bdir,year)
    elif(len(tt) == 2):
        stm3id=tt[0]
        b1id=stm3id[-1]
        basin=Basin1toFullBasin[b1id]
        year=tt[1]
        odir="%s-basin/%s"%(obdir,basin)
        MF.ChkDir(odir,'mk')

    tbdir='%s/%s'%(bdir,year)
    MF.ChkDir(tbdir,'mk')

    return(sdir,tbdir,odir)

def reorgMtcswaByYear(year,override,ropt):
    
    (sdir,tbdir,odir)=getSdirTbdir(year)
    wins=glob.glob("%s/*/*.WIN"%(sdir))
    wins=glob.glob("%s/*.WIN"%(sdir))
    
    # -- get stmids
    #
    s1ids=[]
    for win in wins:
        (wdir,wfile)=os.path.split(win)
        (base,ext)=os.path.splitext(wfile)
        tt=base.split('_')
        dtg=tt[-1]
        b2id=tt[0][4:6]
        snum=tt[0][6:8]
        b1id=Basin2toBasin1[b2id].lower()
        s1id="%s%s"%(b1id,snum)
        s1ids.append(s1id)
        
        
    s1ids=mf.uniq(s1ids)
    
    MF.ChangeDir(tbdir)
    
    if(len(s1ids) == 0):
        s1ids=glob.glob("???")
        s1ids.sort()

    for s1id in s1ids:
        
        mask="*%s%s*"%(Basin1toBasin2[s1id[0].upper()],s1id[-2:])
        tdir="%s"%(s1id)
        if(ropt != 'norun'):
            mf.ChkDir(tdir,'mk')
        
        spaths=glob.glob(mask)
        if(len(spaths) > 0):
            cmd="mv %s %s/."%(mask,tdir)
            mf.runcmd(cmd,ropt)
        
        zpath="%s-%s.zip"%(s1id,year)
        if(MF.ChkPath(zpath) == 0):
            cmd="zip -r -u -m %s %s/*"%(zpath,s1id)
            mf.runcmd(cmd,ropt)
            
            cmd="rmdir %s"%(s1id)
            mf.runcmd(cmd,ropt)
    
        #tdir="%s/%s"%(tbdir,dtg)
        #MF.ChkDir(tdir,'mk')
        
        #cpopt='-n -p'
        #if(override): cpopt="-p"
        #cmd="cp %s %s %s/."%(cpopt,win,tdir)
        #mf.runcmd(cmd,ropt)



def getTrk(tstmid,dtvmax=24):

    trk={}
    
    ocards=tcD.lsDSsStmCards(tstmid,set9xfirst=1,dobt=2)
    odtgs=ocards.keys()
    if(len(odtgs) > 1):
        odtgs.remove('summary')
    odtgs.sort()
    
    # -- last card is the summary
    #
    for odtg in odtgs:
        ocard=ocards[odtg]

        tt=ocard.split()
        
            #ooooo 0 2014062712
            #ooooo 1 A1L.2014
            #ooooo 2 015
            #ooooo 3 1016
            #ooooo 4 34.3N
            #ooooo 5 81.3W
            #ooooo 6 ---
            #ooooo 7 ---
            #ooooo 8 132.1
            #ooooo 9 6.7
            #ooooo 10 b
            #ooooo 11 DB
            #ooooo 12 NW
            #ooooo 13 ---
            #ooooo 14 1/15
            #ooooo 15 lf:
            #ooooo 16 0.97            

        dtg=tt[0][0:10]
        stmid=tt[1]
        
        stmid=get9XstmidFromNewForm(stmid)
        vmax=int(tt[2])

        pmin=tt[3]
        if(not(mf.find(pmin,'-'))): pmin=float(tt[3])   
        
        clat=tt[4]
        clon=tt[5]
        
        (rlat,rlon)=Clatlon2Rlatlon(clat,clon)

        if(tt[6] == '---'): r34=-999
        else:               r34=int(tt[6])

        if(tt[7]== '---'):  r50=-999
        else:               r50=int(tt[6])
            
        dirmotion=float(tt[8])
        spdmotion=float(tt[9])
        ewkey=tt[5][-1]
        if(ewkey == 'W'): 
            rlon=360.0-rlon
            # -- use <0 for deg W
            #
            if(rlon <= 180.0): rlon=-rlon
            
            
        nskey=clat[-1]
        if(nskey == 'S' and rlat > 0.0): rlat=-rlat
        positsource=tt[10]
        tcflag=tt[11]
        warnflag=tt[12]
        tdo=tt[13]
        landfrac=float(tt[16])
        
        trk[dtg]=tcTrk(stmid,vmax,rlat,rlon,dirmotion,spdmotion,r34,r50,
                       positsource,tcflag,warnflag,tdo,landfrac)
        
    dtgs=trk.keys()
    dtgs.sort()
    
    for dtg in dtgs:

        dtgp24=mf.dtginc(dtg,dtvmax)
        vmaxp00=trk[dtg].vmax

        if(dtgp24 in dtgs):
            vmaxp24=trk[dtgp24].vmax
            dvmax=vmaxp24-vmaxp00
            trk[dtg].dvmax=dvmax
        else:
            trk[dtg].dvmax=-999
            
    return(trk)
        

def getClosestMtcswa(tdir,slat,slon,distmax=200.0):
    
    mts=glob.glob("%s/*.WIN"%(tdir))
    
    gotit=0
    for mt in mts:  
        cards=open(mt).readlines()
        
        n=0
        #while (n<=20):
        #    print n,cards[n][0:-1]
        #    n=n+1
        
        if(len(cards) == 0):
            return([],-999,-999,-999,-999)    
            
        stmname=cards[2].split()[0]
        tt=cards[9].split()
        mtlat=float(tt[2])
        mtlon=float(tt[3])
        
        if(mtlon < 0.0): mtlon=360.0+mtlon
        mtvmax=int(float(tt[4]))

        # -- deg west -- for cpac which is in deg east
        #
        if(mtlon > 180.0): mtlon=mtlon-360.0
        mtdist=gc_dist(slat, slon, mtlat, mtlon)
        
        if(mtdist <= distmax):
            gotit=1
            #print 'mmmm',stmname,mtlat,mtlon,mtvmax,'dist:',mtdist
            return(cards,mtlat,mtlon,mtvmax,mtdist)
        
    if(gotit == 0):
        return([],-999,-999,-999,-999)    
    
            
def getMtcswaWinds(cards,verb=0):
    
    # -- grid params
    #
    tt=cards[15].split()
    
    n=0
    x0=float(tt[n]) ; n=n+1
    xmax=float(tt[n]) ; n=n+1
    dx=float(tt[n]) ; n=n+1
    ix=int(tt[n]) ; n=n+1
    y0=float(tt[n]) ; n=n+1
    ymax=float(tt[n]) ; n=n+1
    dy=float(tt[n]) ; n=n+1
    jy=int(tt[n]) ; n=n+1
    
    rcgrid=(x0,dx,ix,y0,dy,jy)
    # -- v comp - tangential wind
    #
    if(verb): print 'GGG',x0, xmax, dx, ix, y0, ymax, dy, jy
    
    nbv=20
    tt=cards[nbv].split()
    sfv=float(tt[6])
    
    nv0=nbv+2
    nv1=nv0+ix
    
    if(verb): print 'vvv ',sfv,nbv,nv0,nv1

    vouts=[]
    for n in range(nv0,nv1+1):
        vv=cards[n].split()
        ovcard="v %03d "%(n-nv0+1)
        for v in vv[1:]:
            vout=float(v)*sfv
            ovcard=ovcard+" %5.1f"%(vout)
        vouts.append(ovcard)
    
    # -- u comp (radial wind)
    #
    nbu=nv1+4
    tt=cards[nbu].split()
    sfu=float(tt[6])
    
    nu0=nbu+2
    nu1=nu0+ix
    
    if(verb): print 'uuu ',sfu,nbu,nu0,nu1
    
    uouts=[]
    for n in range(nu0,nu1+1):
        uu=cards[n].split()
        oucard="u %03d "%(n-nu0+1)
        for u in uu[1:]:
            uout=float(u)*sfu
            oucard=oucard+" %5.1f"%(uout)
        uouts.append(oucard)

    # -- total wind speed
    #
    wouts=[]
    for n in range(0,ix):
        vcard=vouts[n].split()
        ucard=uouts[n].split()
        
        owcard="w %03d "%(n+1)
        for k in range(2,len(ucard)):
            us=ucard[k]
            vs=vcard[k]
            u=float(us)
            v=float(vs)
            w=sqrt(u*u+v*v)
            owcard=owcard+" %5.1f"%(w)
            
        wouts.append(owcard)
        if(n <= 2 and verb): 
            print vouts[n]
            print uouts[n]
            print wouts[n]
    
    return(vouts,uouts,wouts,rcgrid)
            
def writeHeader(dtg,trk,rcmtc,O):
    
    (cards,mtlat,mtlon,mtvmax,mtdist)=rcmtc
    
    if(len(cards) == 0):
        ocard="NNN %s TC: %s %-12s %5.1f %6.1f %3d"%(dtg,trk.stmid,trk.tcname,trk.rlat,trk.rlon,trk.vmax)
    else:
        ocard="YYY %s TC: %s %-12s %5.1f %6.1f %3d   MTC: %5.1f %6.1f %3d"%(dtg,trk.stmid,trk.tcname,trk.rlat,trk.rlon,
                                                                           trk.vmax,
                                                                           mtlat,mtlon,mtvmax)            
        
        ocard=ocard+"   dVmax: %4d  dir: %5.1f  spd: %5.1f"%(trk.dvmax,trk.dirmotion,trk.spdmotion)
        
        ocard=ocard+"  TCstate: %s WARN: %s dir-spd-source: %s landfrac: %4.2f"%(trk.tcflag,trk.warnflag,
                                                                                 trk.positsource,
                                                                                 trk.landfrac)
        
    ocard=ocard+'\n'
    O.writelines(ocard)
    return
        
def writeGrid(rcgrid,grid,O):
    
    (x0,dx,nx,y0,dy,ny)=rcgrid
    
    ocard="grid: x0: %5.1f dx: %5.1f nx: %3d  y0: %5.1f dy: %5.1f ny: %d\n"%(x0,dx,nx,y0,dy,ny)
    O.writelines(ocard)
    for g in grid:
        O.writelines("%s\n"%(g))
        
    return
    
    
    
    

         
#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class CiraCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            #1:['year',  '''year to reorg'''],
            }

        self.defaults={
            }

        self.options={
            'year':           ['y:',None,'a','year'],
            'override':       ['O',0,1,'override'],
            'verb':           ['V',0,1,'verb=1 is verbose'],
            'ropt':           ['N','','norun',' norun is norun'],
            'stmopt':         ['S:',None,'a','stmopt'],
            'aidopt':         ['T:',None,'a','taid'],
            'reorgDat':       ['R',0,1,'reorg the year'],
            }

        self.purpose='''
reorg mtcswa win files'''
        
        self.examples='''
%s -y 2014 -R
%s -S l.14 # reformat/org 2014 lant into '''

        
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main

MF.sTimer('all')
CL=CiraCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)

if(year != None and reorgDat):
    tt=year.split('.')
    if(len(tt) == 2):
        years=mf.yyyyrange(tt[0],tt[1])
    else:
        years=[year]
        
    for year in years:
        rc=reorgMtcswaByYear(year,override,ropt)
        
    sys.exit()

if(stmopt != None):

    from tcbase import *
    tstmids=MakeStmList(stmopt,dofilt9x=1)


    for tstmid in tstmids:
        
        tcD=TcData(stmopt=tstmid)

        trk=getTrk(tstmid)
        
        (sdir,tbdir,odir)=getSdirTbdir(tstmid)
        
        ostmid=tstmid.replace('.','-')
        
        year=tstmid.split('.')[1]
        stm3id=tstmid.split('.')[0].lower()
        tcname=GetTCName(tstmid).upper()
        opath="%s/mtcswa-%s-%s-%s.txt"%(odir,year,stm3id,tcname)
        O=open(opath,'w')
        print 'opath: ',opath
        
        dtgs=trk.keys()
        dtgs.sort()
        
        for dtg in dtgs:
            
            slat=trk[dtg].rlat
            slon=trk[dtg].rlon

            tdir="%s/%s"%(tbdir,dtg)
            
            rcmtc=getClosestMtcswa(tdir,slat,slon)
            (cards,mtlat,mtlon,mtvmax,mtdist)=rcmtc

            rc=writeHeader(dtg,trk[dtg],rcmtc,O)        
            
            if(len(cards) > 0):
                print 'YYY mtcswa for dtg:',dtg
                (vouts,uouts,wouts,rcgrid)=getMtcswaWinds(cards)
                rc=writeGrid(rcgrid,wouts,O)
            else:
                print 'NNN no joy for dtg:',dtg
                
            
else:
    print 'EEE if not doing reorg, then must specify at stmopt'

    
