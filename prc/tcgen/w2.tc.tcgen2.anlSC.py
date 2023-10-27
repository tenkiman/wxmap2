#!/usr/bin/env python
from WxMAP2 import *
w2=W2()

from tcbase import *
from TCtrk import TcPrBasin,tcgenModels,tcgenW3DatDir,tcgenW3Dir,tcgenModelLabel,getBasinOptFromStmids,tcgenBasins,getGentaus

# -- kaze/kishou location of tcgen.pypdb

if(w2.onTaifuu or w2.onKishou or w2.onTenki):
    ttcgbdir="/w21/dat/tc/tcgen"

ttcgbdir=TcGenDatDir
anlSCdir="%s/anlSC"%(ttcgbdir)
MF.ChkDir(anlSCdir,'mk')

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#

def ctype2ndx(ctype):
    
    ndx=999
    
    if(ctype == 'SC1'): ndx=1
    elif(ctype == 'DIS'): ndx=2
    elif(ctype == 'FPT'): ndx=101
    elif(ctype == 'GPT'): ndx=102
    elif(ctype == 'FTC'): ndx=201
    elif(ctype == 'GTC'): ndx=202
    elif(ctype == 'FMT'): ndx=203
    elif(ctype == 'FNT'): ndx=301
    elif(ctype == 'GNT'): ndx=302
    elif(ctype == 'FGT'): ndx=401
    elif(ctype == 'GGT'): ndx=402
    elif(ctype == 'GMT'): ndx=501
    
    return(ndx)

def parseZoomOpt(zoomOpt):
    (zlat1,zlat2,zlon1,zlon2,zxlint,zylint)=zoomOpt.split(':')
    zlat1=float(zlat1)
    zlat2=float(zlat2)
    zlon1=float(zlon1)
    zlon2=float(zlon2)
    if(zlon1 < 0): zlon1=360.0+zlon1
    if(zlon2 < 0): zlon2=360.0+zlon2
    zxlint=float(zxlint)
    zylint=float(zylint)
    return(zlat1,zlat2,zlon1,zlon2,zxlint,zylint)
    

def parseSCcard(bdtg,dtg,card,
                obs,SCvars,SCstms,zoomOpt,
                whichCndx=1,
                minsTDd=None,
                maxcpsB=10.0,
                mincpsVTl=-0.0,
                mincpsVTu=-0.0,
                undef999=-9999.0,
                verb=0):

    ddtg=mf.dtgdiff(bdtg,dtg)
    scss=card.split('_')[0]
    scsg=card.split('_')[-1]

    scs=scss.split('|')
    
    tt=scs[0].split()
    pr=float(tt[5])
    prc=float(tt[7])
    rc2t=float(tt[9])
    
    ngen=100
    genstdds=0.0
    
    # -- process tcgen-- only one gen stm / dtg?
    #
    ttg=scsg.split()
    if(ttg[0] != 'no-gen'):
        
        gentc=ttg[1]

        #for n in range(0,len(ttg)):
        #    print n,ttg[n]

        # -- use ob lat/lon/sTDd
        #
        cndx=99
        genlat=float(ttg[8])
        genlon=float(ttg[9])
        gensTDd=float(ttg[6])
        gencpsB=undef999
        gencpsVTl=undef999  
        gencpsVTu=undef999

        OgensTDd=ttg[6]
        
        if(ttg[10] == 'NA'):
            print 'NNNNNNNNNNNNNN dtg: ',dtg,' got NA in ttg[10]'
            MF.appendDictList(SCstms,gentc,0)

        elif(ttg[10] != 'FAILED'):
            # -- if no minsTDd test for genesis
            #
            if(minsTDd != None and float(ttg[11]) >= minsTDd):
                None
            else:
                gensTDd=float(ttg[11])
                genlat=float(ttg[13])
                genlon=float(ttg[14])
                gencpsB=float(ttg[19])
                gencpsVTl=float(ttg[20])
                gencpsVTu=float(ttg[21])
                cndx=2
                ngen=ngen+1
                genstdds=genstdds+gensTDd
                MF.appendDictList(SCstms,gentc,1)
        else:
            MF.appendDictList(SCstms,gentc,0)
            
            
        
        if(cndx == -99): print 'ggggg----',genlat,genlon,cndx,gensTDd,gencpsB,gencpsVTl,gencpsVTu
        MF.appendDictList(obs,ddtg,[genlat,genlon,cndx,gensTDd,gencpsB,gencpsVTl,gencpsVTu])

        (pcrlat,pcrlon)=Rlatlon2Clatlon(genlat,genlon)
        print 'GEN: ',ddtg,ngen,gentc,'    lat/lon:',pcrlat,pcrlon,'M sTDd/B/VTl/VTu: ',gensTDd,gencpsB,gencpsVTl,gencpsVTu,'Ob sTDd: ',OgensTDd

        MF.appendDictList(SCvars,ddtg,[ngen,genstdds,pr,prc,rc2t])
    
    nsc1=0
    stdds=0.0
    
    zlat1=None
    lltest=1
    if(zoomOpt != None):
        (zlat1,zlat2,zlon1,zlon2,zxlint,zylint)=parseZoomOpt(zoomOpt)
        
        
    for n in range(1,len(scs)):
        # tg0008     GTC sTDd:  4.4 120 CPS(B,VTl,VTu):    -1    33    57  Pos(tau,lat,lon): 132  10.9N  98.2W
        tt=scs[n].split()
        ctype=tt[1]
        cstd=float(tt[3])
        cstlife=float(tt[4])
        ccpsB=float(tt[6])
        ccpsVTl=float(tt[7])
        ccpsVTu=float(tt[8])
        cclat=tt[-2]
        cclon=tt[-1]
        (crlat,crlon)=Clatlon2Rlatlon(cclat, cclon)
        
        cndx=ctype2ndx(ctype)
        if(cndx == 999):
            print 'no joy for ctype: ',ctype
            sys.exit()
        
        if(zoomOpt != None):
            lltest=(crlat <= zlat2 and crlat >= zlat1 and crlon <= zlon2 and crlon >= zlon1)
        
        # -- filter out weak sTDd
        #
        if(minsTDd != None and cstd < minsTDd):
            if(verb > 1 and cndx == whichCndx): print 'sTDd filt:',dtg,n,ctype,cstd,cstlife,crlat,crlon,ccpsB,ccpsVTl,ccpsVTu
            continue

        # -- filter non-tropical
        #
        if(maxcpsB != None and abs(ccpsB) > maxcpsB and ccpsB != undef999):
            if(verb > 1 and cndx == whichCndx): print 'cpsBbbbbbbbbbb filt:',dtg,n,ctype,cstd,cstlife,crlat,crlon,ccpsB,ccpsVTl,ccpsVTu
            continue
        
        if(mincpsVTl != None and ccpsVTl < mincpsVTl and ccpsVTl != undef999):
            if(verb > 1 and cndx == whichCndx): print 'cpsVTlllllllll filt:',dtg,n,ctype,cstd,cstlife,crlat,crlon,ccpsB,ccpsVTl,ccpsVTu
            continue

        if(mincpsVTu != None and ccpsVTu < mincpsVTu and ccpsVTu != undef999):
            if(verb and cndx == whichCndx): print 'cpsVTuuuuuuuuu filt:',dtg,n,ctype,cstd,cstlife,crlat,crlon,ccpsB,ccpsVTl,ccpsVTu
            continue
        
        # -- filter out obs outside zoombox
        #
        if(zlat1 != None and not(lltest)):
            continue
        else:
            
            if(cndx == whichCndx):
                (pcrlat,pcrlon)=Rlatlon2Clatlon(crlat,crlon)
                if(verb): print 'SC1: ',ddtg,cndx,'sTDd: %2.1f'%(cstd),' lat/lon:',pcrlat,pcrlon,\
                  'B,VTl,VTu: %3.0f %4.0f %4.0f'%(ccpsB,ccpsVTl,ccpsVTu)
                MF.appendDictList(obs,ddtg,[crlat,crlon,cndx,cstd,ccpsB,ccpsVTl,ccpsVTu])
                nsc1=nsc1+1     
                stdds=stdds+cstd
    
    MF.appendDictList(SCvars,ddtg,[nsc1,stdds,pr,prc,rc2t])

    return
        
        
        
    
class gaStationData(MFbase):
    
    stndt=0.0

    # stnlev=0 end of time group
    #
    stnlev=1

    # stnflag = 0 no sfc
    #
    stnflag=1
    
    # -- names of output vars
    #
    varNames={
        0:['sndx','ndx for storm state 1=SC1 2=DIS...',('1','-100 100')],
        1:['stdd','scaled TD days [d]',('0.25','0 2.5')],
        1:['stdd','scaled TD days [d]',(
            ' 0   0.25  0.50   0.75  1.0   1.25  1.50  1.75  2.0  2.25  2.5',
            '41 42    43    45    47    49    21     23    25   27    28     39',
            )],
        2:['cpsb','CPS B',('1.0','-5.0 25.0')],
        3:['cpsvtl','CPS Vtlo',('10.0','-50.0 200.0')],
        4:['cpsvth','CPS Vthi',('10.0','-50.0 200.0')],
    }        

    def __init__(self,byear,bdtg,obs,SCvars,SCstms,
                 model,basin,gentau,zoomOpt,filtOpt,
                 undef=1e20,
                 obsbase='/ptmp/sC-obs',
                 minsTDd=None,
                 maxcpsB=None,
                 mincpsVTl=None,
                 mincpsVTu=None,
                 undef999=-999.,
                 onlySC1=1,
                 dogenPlot=0,
                 verb=0):
        
        
        self.byear=byear
        self.dogenPlot=dogenPlot
        
        stmids=SCstms.keys()
        stmids.sort()
        nstmids=len(stmids)
        
        ngenCOR=0
        
        for stmid in stmids:
            print 'SSS',stmid,SCstms[stmid]
            ncor=0
            for ngen in SCstms[stmid]:
                if(ngen): ncor=ncor=1
                
            print 'SSS',stmid,SCstms[stmid],ncor
            if(ncor > 0): ngenCOR=ngenCOR+1
                
                
        if(nstmids > 0):
            genPercent=(float(ngenCOR)/float(nstmids))*100.0
        else:
            genPercent=undef999
        
        self.stmids=stmids
        self.nstmids=nstmids
        self.ngenCOR=ngenCOR
        self.genPercent=genPercent
        
        self.model=model
        self.basin=basin
        self.gentau=gentau
        
        if(minsTDd == None):   minsTDd=undef999
        if(maxcpsB == None):   maxcpsB=undef999
        if(mincpsVTl == None): mincpsVTl=undef999
        if(mincpsVTu == None): mincpsVTu=undef999
        
        self.minsTDd=minsTDd
        self.maxcpsB=maxcpsB
        self.mincpsVTl=mincpsVTl
        self.mincpsVTu=mincpsVTu

        self.zoomOpt=zoomOpt
        self.filtOpt=filtOpt
        
        if(zoomOpt != None):
            (zlat1,zlat2,zlon1,zlon2,zxlint,zylint)=parseZoomOpt(zoomOpt)
        
        SCtimes=SCvars.keys()
        times=obs.keys()
        times.sort()
        SCtimes.sort()
        
        self.ntimes=len(times)
        if(self.ntimes < 2):
            print 'EEE gsStationData: not enough data points...ja sayounara'
            sys.exit()
        
        edtg=mf.dtginc(bdtg,times[-1])
        self.dtgrange="%s - %s"%(bdtg,edtg)

        obsbaseF="%s-%s-%s-%s-%s-%03d"%(obsbase,model,basin,bdtg,edtg,gentau)
        
        if(filtOpt != None):
            ofiltOpt=filtOpt.replace(',','-')
            obsbaseF="%s-filtOpt-%s"%(obsbaseF,ofiltOpt)
            
        if(dogenPlot):
            obsbaseF="%s-dogenplot"%(obsbaseF)

        if(onlySC1):
            obsbaseF="%s-onlySC1"%(obsbaseF)

        if(zoomOpt != None):
            obsbaseF=obsbaseF+'-%02.0f-%02.0f-%03.0f-%03.0f'%(zlat1,zlat2,zlon1,zlon2)

        self.obspath=obsbaseF+'.obs'
        self.smppath=obsbaseF+'.smp'
        self.ctlpath=obsbaseF+'.ctl'
        self.gspath=obsbaseF+'.gs'
        self.pngpath=obsbaseF+'.png'
        self.txtpath=obsbaseF+'.txt'

        # -- get stats
        #
        
        meanPr=0.0
        meanPrc=0.0
        meanRc2t=0.0
        
        totalGTCs_hit=0
        totalGTCs_miss=0
        
        totalSCs=0
        totalsTDd=0.0
        
        nPr=0
        nPrc=0
        
        for time in SCtimes:
            
            for SCvar in SCvars[time]:
                nt=SCvar[0] 
                stdd=SCvar[1]
            
                if(nt == 101):
                    totalGTCs_hit=totalGTCs_hit+1
                    
                elif(nt == 100):
                    totalGTCs_miss=totalGTCs_miss+1
                    
                else:
                    
                    totalSCsCur=nt
                    totalsTDdCur=stdd
                    meanPrCur=SCvar[2]
                    meanPrcCur=SCvar[3]
                    meanRc2tCur=SCvar[4]
                    
                    totalSCs=totalSCs+totalSCsCur
                    totalsTDd=totalsTDd+totalsTDdCur
                
                    oSC1=((onlySC1 and nt > 0 ) or not(onlySC1))
                    if(str(meanPrCur) != 'nan' and meanPrCur > 0 and oSC1 ):
                        nPr=nPr+1
                        meanPr=meanPr+meanPrCur
                    
                    if(meanPrcCur > 0 and oSC1 ):
                        nPrc=nPrc+1
                        meanPrc=meanPrc+meanPrcCur
                        meanRc2t=meanRc2t+meanRc2tCur
                        
        
        if(nPr > 0):
            meanPr=meanPr/nPr
            
        if(nPrc > 0):
            meanPrc=meanPrc/nPrc
            meanRc2t=meanRc2t/nPrc
            
            
        self.nPr=nPr
        self.meanPr=meanPr
        self.meanPrc=meanPrc
        self.meanRc2t=meanRc2t
        self.totalSCs=totalSCs
        self.totalsTDd=totalsTDd
        self.totalGTCs_hit=totalGTCs_hit
        self.totalGTCs_miss=totalGTCs_miss
        self.totalGTCs=self.totalGTCs_hit+self.totalGTCs_miss
        self.FAR=undef999
        if(self.totalGTCs > 0):
            self.FAR=(float(self.totalSCs)/float(self.totalGTCs))*100
        
        print 'Stats -- nPr: ',nPr,self.totalSCs,self.totalsTDd,self.meanPr,self.meanPrc,self.meanRc2t
        print 'Stats -- gen: ',nPr,self.totalGTCs_hit,totalGTCs_miss
        
        
        ocard="%-6s %-6s %4d %d %3.0f %4.0f  %d"%(model,basin,int(self.byear),self.gentau,
                                                  self.genPercent,self.FAR,
                                                  self.totalGTCs)
        
        MF.WriteString2File(ocard,self.txtpath,verb=1)
        
        self.parea='prw'+basin[0].upper()+basin[1:]
        self.parea='trop'+basin
        self.aW2=getW2Area(self.parea)
        
        # -- zooming
        #
        if(zoomOpt != None):

            self.aW2.latS=zlat1
            self.aW2.latN=zlat2
            self.aW2.lonW=zlon1
            self.aW2.lonE=zlon2
            self.aW2.xlint=zxlint
            self.aW2.ylint=zylint
            
        
        ddtg=12
        if(self.ntimes > 1): 
            ddtg=times[1]-times[0]
            ddtg=int(ddtg)
            
        self.bgtime=mf.dtg2gtime(bdtg)
            
        ob0=obs[times[0]][0]
        self.nvals=len(ob0[2:])
        #print 'asdfasdfasdf',ob0,self.nvals
        #sys.exit()
        
        # -- make the .ctl
        #
        ctl='''dset %s
title spuricane anl obs
dtype station
stnmap %s
undef %g
tdef %d linear %s %dhr
vars %d'''%(self.obspath,self.smppath,undef,len(times),self.bgtime,ddtg,
            self.nvals)
        novarname=0
        for n in range(0,self.nvals):
            try:
                (ovarname,ovardesc)=self.varNames[n][0:2]
            except:
                ovarname='ob%02d'%(n)
                ovardesc='ob var #%02d'%(n)
            
            ctl=ctl+'''
%s 0 99 %s'''%(ovarname,ovardesc)
            
        ctl=ctl+'''
endvars'''
            
        MF.WriteString2File(ctl,self.ctlpath)

        # -- make the .obs
        #
        oB=open(self.obspath,'wb')
        
        nstn=0
        for time in times:
            tndx=mf.nint(time/ddtg)
            #print 'tttt',time,tndx
            for ob in obs[time]:
                stnid="%07d "%(nstn)
                (rlat,rlon)=ob[0:2]
                vals=ob[2:]

                stnhead=struct.pack('8sfffii',stnid,rlat,rlon,self.stndt,self.stnlev,self.stnflag)
                stndata=struct.pack('1f',vals[0])
                for val in vals[1:]:
                    # -- undef from CPS
                    if(val == -9999.): val=undef
                    stndata=stndata+struct.pack('1f',val)
                oB.write(stnhead)
                oB.write(stndata)

                nstn=nstn+1
        
            stnhead=struct.pack('8sfffii',stnid,rlat,rlon,self.stndt,0,0)
            oB.write(stnhead)
            
        # -- make the .smp
        #
        oB.close()
        
        ropt=''
        stnverb=''
        if(verb): stnverb='-v'
        cmd='stnmap %s -i %s'%(stnverb,self.ctlpath)
        mf.runcmd(cmd,ropt)
        
    def plotSC1(self):
        
        
        lcol=90
        ocol=91
        landcol='tan'
        oceancol='lightblue'
        
        wC=w2Colors()

        hex=wC.W2Colors[landcol]
        (r,g,b)=wC.hex2rgb(hex)
        lcolrgb='set rgb %d %d %d %d'%(lcol,r,g,b)
             
        hex=wC.W2Colors[oceancol]
        (r,g,b)=wC.hex2rgb(hex)
        ocolrgb='set rgb %d %d %d %d'%(ocol,r,g,b)        
        
        xsize=1024
        xsize=1440
        ysize=int(xsize*(3.0/4.0))
        
        gridctl=w2.GradsGslibDir+'/dum.ctl'
        
        omodel=tcgenModelLabel[self.model]
        
        if(self.meanPrc < 0):
            omeanPrc='---'
            omeanRc2t='---'
        else:
            omeanPrc="%5.2f"%(self.meanPrc)
            omeanRc2t="%4.2f"%(self.meanRc2t)
            
        t1="SC1 Basin: %s Model: %s tau=%03d"%(self.basin.upper(),omodel,self.gentau)
        t1=t1+" nPr: %03d Pr: %5.2f Prc: %s RC2T: %s nSCs: %d sTDd: %5.1f"%(self.nPr,self.meanPr,omeanPrc,omeanRc2t,
                                                                            self.totalSCs,self.totalsTDd)
        
        
        pvarN=1
        
        mapres='mres'
        if(self.zoomOpt != None): mapres='hires'
        
        t1=t1.replace('  ',' ')
        t1=t1.replace('  ',' ')
        t2='# genTCS: %2d %%GENESIS: %3.0f %%FAR: %4.0f   #genHITS: %2d  #genMISS: %2d  #genTOT: %2d'%\
            (self.nstmids,self.genPercent,self.FAR,self.totalGTCs_hit,self.totalGTCs_miss,self.totalGTCs)
        t3="DTGrange: %s  :: colorized by %s  "%(self.dtgrange,self.varNames[pvarN][0])
        t3=t3+"minsTDd: %2.1f maxcpsB: %3.0f mincpsVTl: %3.0f mincpsVTu: %3.0f"%(self.minsTDd,
                                                                                 self.maxcpsB,
                                                                                 self.mincpsVTl,
                                                                                 self.mincpsVTu)
        
        
        gs="""
function main(args)
rc=gsfallow(on)
rc=const()
rc=jaecol2()
'set grads off'
'set timelab on'
digsiz=0.15
digBfact=0.35
digsiz0=digsiz+digBfact*digsiz

digsizG=digsiz*1.75
digsiz0G=digsiz0*1.75

digsizG99=digsizG*0.75
digsiz0G99=digsiz0G*0.75

'open %s'
'open %s'

dogen=%d
'set xsize %d %d'
'set lat %6.1f %6.1f'
'set lon %6.1f %6.1f'

'%s'
'%s'

'set xlint %6.1f'
'set ylint %6.1f'

'set map 15 0 8'
'set mpdset %s'

'set cmax 1000'
'd const(lat,0,-a)'

'basemap.2 L %d'
'basemap.2 O %d'

'draw map'

'set dfile 2'
'set t 1'

t1='%s'
t2='%s'
t3='%s'

'set cint 0.25'

'set gxout stnmark'

'set cmark 3'
'set digsiz 'digsiz0
'set ccolor 0'
'set map 0 0 0'

dexpr='maskout(%s(t+0,t+%d),1.1-sndx(t+0,t+%d))'
'd const('dexpr',0)'

'set cmark 3'
'set ccolor rainbow'
'set digsiz 'digsiz
'set clevs %s'
'set ccols %s'

'd 'dexpr
'cbarn 0.80'

# -- do title in case there is no data for the last 'd 'dexpr of dogen = 1, i.e., no misses!!!
#
t3scl=0.75
rc=toptle3(t1,t2,t3,t3scl)
 
if(dogen = 1)
    dexpr='maskout(maskout(%s(t+0,t+%d),sndx(t+0,t+%d)-1.9),2.1-sndx(t+0,t+%d))'
    
    'set cmark 9'
    'set digsiz 'digsiz0G
    'set ccolor 0'
    'set map 0 0 0'
    'd const('dexpr',0)'
    
    'set cmark 9'
    'set ccolor rainbow'
    'set digsiz 'digsizG
    'set clevs %s'
    'set ccols %s'
    
    'd 'dexpr
    
    dexpr='maskout(maskout(%s(t+0,t+%d),sndx(t+0,t+%d)-2.1),99.1-sndx(t+0,t+%d))'
    
    'set cmark 5'
    'set digsiz 'digsiz0G99
    'set ccolor 0'
    'set map 0 0 0'
    'd const('dexpr',0)'
    
    'set cmark 5'
    'set ccolor rainbow'
    'set digsiz 'digsizG99
    'set clevs %s'
    'set ccols %s'
    'd 'dexpr
endif


#'gxyat -v -x %%d -y %%d %%s'
'gxprint %s x%d y%d'

'q pos'
'quit'

"""%(
       gridctl,
       self.ctlpath,self.dogenPlot,
       xsize,ysize,
       self.aW2.latS,self.aW2.latN,
       self.aW2.lonW,self.aW2.lonE,
       lcolrgb,ocolrgb,
       self.aW2.xlint,self.aW2.ylint,
       mapres,
       lcol,ocol,
       t1,t2,t3,
       self.varNames[pvarN][0],self.ntimes,self.ntimes,
       self.varNames[pvarN][-1][0],self.varNames[pvarN][-1][1],
       
       self.varNames[pvarN][0],self.ntimes,self.ntimes,self.ntimes,
       self.varNames[pvarN][-1][0],self.varNames[pvarN][-1][1],

       self.varNames[pvarN][0],self.ntimes,self.ntimes,self.ntimes,
       self.varNames[pvarN][-1][0],self.varNames[pvarN][-1][1],

       self.pngpath,xsize,ysize,
       
     )

        ropt=''
        MF.WriteString2File(gs,self.gspath)
        cmd="grads -lc %s"%(self.gspath)
        mf.runcmd(cmd,ropt)

        cmd="cp %s ~/Dropbox/anlSC/."%(self.pngpath)
        mf.runcmd(cmd,ropt)
        #self.gaP=procGA(self.ctlpath)
        #(ga,ge,gp)=self.gaP.getGAfromGaProc()
        
        
def getFiltMins(tt):
    
    (minsTDd,maxcpsB,mincpsVTl,mincpsVTu)=(None,None,None,None)
    
    if(len(tt) == 4): (minsTDd,maxcpsB,mincpsVTl,mincpsVTu)=tt
    if(len(tt) == 3): (minsTDd,maxcpsB,mincpsVTl)=tt
    if(len(tt) == 2): (minsTDd,maxcpsB)=tt  
    if(len(tt) == 1): (minsTDd)=tt[0]
    
    if(minsTDd != None):   minsTDd=float(minsTDd)
    if(maxcpsB != None):   maxcpsB=float(maxcpsB)
    if(mincpsVTl != None): mincpsVTl=float(mincpsVTl)
    if(mincpsVTu != None): mincpsVTu=float(mincpsVTu)
    
    return(minsTDd,maxcpsB,mincpsVTl,mincpsVTu)

        
        

class AdgenCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv is None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['dtgopt',  'run dtgs'],
            2:['modelopt',    'model|model1,model2|all|allgen'],
        }

        self.defaults={
            'doupdate':0,
            'BMoverride':0,
        }

        self.options={
            'override':      ['O',0,1,'override'],
            'trkoverride':   ['o',0,1,'override in dotrk'],
            'verb':          ['V',0,1,'verb=1 is verbose'],
            'dogenPlot':     ['G',0,1,'plot genesis points and SC1s'],
            'onlySC1':       ['s',0,1,'calc pr stats for SC1 maps only'],
            'quiet':         ['q',1,0,' run GA in NOT quiet mode'],
            'diag':          ['d',0,1,' extra diagnostics'],
            'ropt':          ['N','','norun',' norun is norun'],
            'doplot':        ['P',1,0,'do NOT make plots'],
            'anlTag':        ['T:','misc','a','tag for the spuricane .pyp'],
            'gentauOpt':     ['t:','all','a','gentauOpt -- fc tau for genesis'],
            'basinopt':      ['b:','all','a',' basin with gen adecks'],
            'filtOpt':       ['f:',None,'a','minsTDd,maxcpsB,mincpsVTl,mincpsVTu SC1s'],
            'anlType':       ['A:','sum','a','anlType - sum |'],
            'zoomOpt':       ['Z:',None,'a','setup subarea zoom box lat1:lat2:lon1;lon2:ylint:xlint'],
            'dochkIfRunning':['c',1,0,'do NOT using MF.chkIfJobIsRunning'],
        }



        self.purpose='''-- analyze spuricane SC'''
        self.examples='''%s 201405.12 gfs2,ecm2 -b lant -T 2014 -t 132'''

argv=sys.argv
CL=AdgenCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


MF.sTimer('all')

dtgs=mf.dtg_dtgopt_prc(dtgopt)
models=modelopt.split(',')
if(modelopt == 'all'): models=tcgenModels
if(basinopt == 'all'): basins=tcgenBasins
else:                  basins=basinopt.split(',')

gentaus=getGentaus(gentauOpt)

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main 

# -- get stmids and gendtgs
#
stmids=None
gendtgs=None

minsTDd=maxcpsB=mincpsVTl=mincpsVTu=None

if(filtOpt != None):
    tt=filtOpt.split(',')
    if(len(tt) == 0 or len(tt) > 4):
        print 'EEE in filtOpt: ',filtOpt
        sys.exit()
    else:
        (minsTDd,maxcpsB,mincpsVTl,mincpsVTu)=getFiltMins(tt)
else:
    # defaults
    minsTDd=maxcpsB=mincpsVTl=mincpsVTu=None
        
print 'fffffffffff: ',minsTDd,maxcpsB,mincpsVTl,mincpsVTu

# -- AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
#

ttcgbdir=anlSCdir
dsname='spuricane-%s'%(anlTag)
MF.sTimer('getpyp')
sC=DataSet(name=dsname,bdir=ttcgbdir,verb=verb)
rc=sC.getPyp()
if(rc == None): 
    print 'EEE(%s) unable to open spuricane pyp: '%(pyfile),dsname,'use -T anlTag'
    sys.exit()
    
spurCards=rc.data

MF.dTimer('getpyp')

bdtg=dtgs[0]

# -- assume nhem season
#
byear=bdtg[0:4]
for model in models:
    for basin in basins:
        for gentau in gentaus:
            obs={}
            SCvars={}
            SCstms={}
            
            for dtg in dtgs:
                
                try:
                    card=spurCards[model,dtg,basin,gentau]
                except:
                    card=None
                    
                if(card == None):
                    print 'No data for: ',model,dtg,basin,gentau,'...press...'''
                else:
                    parseSCcard(bdtg,dtg,card,obs,SCvars,SCstms,zoomOpt,
                                minsTDd=minsTDd,
                                maxcpsB=maxcpsB,
                                mincpsVTl=mincpsVTl,
                                mincpsVTu=mincpsVTu,
                                verb=verb)
              
            if(doplot):  
                gSC=gaStationData(byear,bdtg,obs,SCvars,SCstms,
                                  model,basin,gentau,zoomOpt,filtOpt,
                                  dogenPlot=dogenPlot,
                                  onlySC1=onlySC1,
                                  minsTDd=minsTDd,
                                  maxcpsB=maxcpsB,
                                  mincpsVTl=mincpsVTl,
                                  mincpsVTu=mincpsVTu)
                gSC.plotSC1()

MF.dTimer('all')
sys.exit()

