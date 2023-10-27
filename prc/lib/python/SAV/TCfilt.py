import os
import sys
import time
import glob

import math
from math import atan2
from math import atan
from math import pi
from math import fabs
from math import cos
from math import sin
from math import log
from math import tan
from math import acos
from math import sqrt


import w2
import mf
import TCveri
import TCw2 as TC

from const import  *


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# module constants
#

xsiz=1024
ysiz=768

xsizfl=xsiz
ysizfl=ysiz+100

cundef='1e20'


def TcFiltFields(fcstmids,fclatlons,fcstmidstcfilt,fclatlonstcfilt,
                 fldpath,gtime,gtimedat,
                 ofldopt,model,dtg,itaufld,dtaumod,itau,
                 doallflds=0,dowdrive=0,forcedat=0,verb=0):


    #
    # time factors to interpolate in time
    #

    phr0=0
    phr1=dtaumod
    tfact0=(1.0-float(itau-itaufld)/float(dtaumod))
    tfact1=(1.0 - tfact0)
    plevup=200
    if(model == 'ecmn'): plevup=250
    if(model == 'ecm2'): plevup=200

    if(verb):
        print 'fffffffffffff ',model,itaufld,dtaumod,' dtg,itau: ',dtg,itau,plevup
        print 'ppppppp ',phr0,phr1,'tttttttttttt ',tfact0,tfact1
        print 'ggggggg ',gtime,gtimedat

    bdatdir=w2.TcTcfiltDatDirRT
        
    year=dtg[0:4]
    bdatdir="%s/%s/%s"%(bdatdir,year,dtg)
    mf.ChkDir(bdatdir,'mk')
    gspath="%s/tcfilt.fld.gs"%(bdatdir)
    uvpath="%s/tcfilt.fld.uv.dat"%(bdatdir)
    filetitle="%s.%s.%03d"%(model,dtg,itau)
    ifldpath="%s/tcfilt.fld.input.%s.dat"%(bdatdir,filetitle)
    ictlpath="%s/tcfilt.fld.input.%s.ctl"%(bdatdir,filetitle)
    ofldpath="%s/tcfilt.fld.output.%s.dat"%(bdatdir,filetitle)
    octlpath="%s/tcfilt.fld.output.%s.ctl"%(bdatdir,filetitle)
    positpath="%s/tcfilt.posits.%s.%s.%03d.txt"%(bdatdir,model,dtg,itau)
    positpathtcfilt="%s/tcfilt.posits.%s.%s.%03d.tcfilt.txt"%(bdatdir,model,dtg,itau)
    
    P=open(positpath,'w')
    PT=open(positpathtcfilt,'w')

    if(verb):
        print 'ppppppp ',positpath
        print 'ppppppp ',positpathtcfilt

    for stmid in fcstmids:
        stm3id=stmid.split('.')[0]
        (fclat,fclon,fcvmax)=fclatlons[stmid]
        card="%3s %4.1f %5.1f \n"%(stm3id,fclat,fclon)
        P.writelines(card)

    P.close()

    for stmid in fcstmidstcfilt:
        stm3id=stmid.split('.')[0]
        (fclat,fclon,fcvmax)=fclatlonstcfilt[stmid]
        card="%3s %4.1f %5.1f \n"%(stm3id,fclat,fclon)
        PT.writelines(card)

    PT.close()

    verb=0

    uvlev=850

    regrid=0
    if(w2.IsModel2(model) or model == 'fim8' or model == 'fim9'): regrid=1

    pslfact=None
    if(w2.IsModel2(model) or model == 'fim8' or model == 'fim9'): pslfact=0.01

    #
    # make sure file is there
    #

    if(os.path.exists(fldpath)):
        print

    else:
        print "EEE fldpath: %s does not exits"%(fldpath)
        return(999)


    TcfiltCtl(ifldpath,ictlpath,gtime,ofldopt)
    if(doallflds):
        TcfiltCtlAll(ofldpath,octlpath,gtime,ofldopt)
    else:
        TcfiltCtl(ofldpath,octlpath,gtime,ofldopt)


    def goutvar(var,regrid,dlon=1,dlat=1,regridmethod='bs',plev=None,pfact=None):

        def tvar(var,phr0,phr1,tfact0,tfact1,plev):
            if(plev != None):
                if(tfact1 == 0.0):
                    varexpr="( (%s(lev=%d,time+%dhr)*%4.2f) )"%(var,plev,phr0,tfact0)
                else:
                    varexpr="( (%s(lev=%d,time+%dhr)*%4.2f) + (%s(lev=%d,time+%dhr)*%4.2f) )"%(var,plev,phr0,tfact0,var,plev,phr1,tfact1)
            else:
                if(tfact1 == 0.0):
                    varexpr="( (%s(time+%dhr)*%4.2f) )"%(var,phr0,tfact0)
                else:
                    varexpr="( (%s(time+%dhr)*%4.2f) + (%s(time+%dhr)*%4.2f) )"%(var,phr0,tfact0,var,phr1,tfact1)

            if(pfact != None):
                varexpr="((%s)*%f)"%(varexpr,pfact)
                
            return(varexpr)

        varexpr=tvar(var,phr0,phr1,tfact0,tfact1,plev)
        
        if(regrid):
            #varexpr="regrid2(%s,%d,%d,%s)"%(varexpr,dlon,dlat,regridmethod)
            varexpr="re(%s,360,linear,0.0,%d,181,linear,-90.0,%d,%s)"%(varexpr,dlon,dlat,regridmethod)

        varexpr="const(%s,%s,-u)"%(varexpr,cundef)
        
        G("'d %s'"%(varexpr))

        return(varexpr)
            
    def goutfld(ofldopt):

        if(ofldopt == 'shear'):
            goutvar('ua',regrid,plev=850)
            goutvar('va',regrid,plev=850)
            goutvar('ua',regrid,plev=plevup)
            goutvar('va',regrid,plev=plevup)
            
        elif(ofldopt == 'basic'):

            if(pslfact != None):
                goutvar('psl',regrid,pfact=pslfact)
            else:
                goutvar('psl',regrid)
            
            goutvar('uas',regrid)
            goutvar('vas',regrid)
            
            goutvar('ua',regrid,plev=850)
            goutvar('va',regrid,plev=850)
            goutvar('ua',regrid,plev=500)
            goutvar('va',regrid,plev=500)
            goutvar('ua',regrid,plev=plevup)
            goutvar('va',regrid,plev=plevup)
            
            goutvar('zg',regrid,plev=500)
            
    
            
    gs=[]
    G=gs.append
    

    G("function main(args)")
    G("rc=gsfallow('on')")
    G("rc=const()")

    G("fn=ofile('%s')"%(fldpath))
    G("print 'fn 'fn")
    G("if(fn = 0) ; 'quit' ; endif")
    G("rc=metadata1(fn)")
    G("print 'nx... '_nx' '_ny")

    G("'set x 1 '_nx")
    G("'set y 1 '_ny")
    G("'set lon 0 359'")
    G("'set lat -90 90'")
    G("'set time %s'"%(gtimedat))
    G("'set lev %s'"%(uvlev))
    G("'set fwrite %s'"%(uvpath))
    G("'set gxout fwrite'")
    goutvar('ua',regrid)
    vexpr=goutvar('va',regrid)
    G("rcd=datachk('%s')"%(vexpr))
    G("'set gxout fwrite'")
    G("print 'rcd: 'rcd")
    G("'disable fwrite'")
    G("'set fwrite %s'"%(ifldpath))

    goutfld(ofldopt)
    
    G("'quit'")
    G("return")
    G("end")
    
    gsfile=open(gspath,'w')

    for gg in gs:
        gg=gg+'\n'
        if(verb): print gg[:-1]
        gsfile.write(gg)
    verb=0
    
    gsfile.close()

    if(not(os.path.exists(ifldpath)) or forcedat):
        cmd="grads2 -lbc \"run %s\""%(gspath)
        mf.runcmd(cmd,'')
    print 'DDDDD gspath: ',gspath
    paths=[uvpath,ifldpath,ictlpath,ofldpath,octlpath,positpath,positpathtcfilt]
    dirs=[bdatdir]
    
    return(paths,dirs)



def TcfiltCtl(fldpath,ctlpath,gtime,ofldopt):
    
    #
    # make .ctl for shear files
    #

    (flddir,fldfile)=os.path.split(fldpath)

    if(ofldopt == 'shear'):
        ctl="""dset ^%s
title input fields
undef %s
xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0
zdef   1 levels 1013
tdef   1 linear %s 6hr
vars 4
u8 0 0 u8
v8 0 0 v8
u2 0 0 u2
v2 0 0 v2
endvars"""%(fldfile,cundef,gtime)
        
    elif(ofldopt == 'basic'):
        ctl="""dset ^%s
title input fields
undef %s
xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0
zdef   1 levels 1013
tdef   1 linear %s 6hr
vars 10
psl 0 0 psl
uas 0 0 u8
vas 0 0 v8
u8 0 0 u8
v8 0 0 v8
u5 0 0 u8
v5 0 0 v8
u2 0 0 u2
v2 0 0 v2
z5 0 0 u8
endvars"""%(fldfile,cundef,gtime)

        
    c=open(ctlpath,'w')
    c.writelines(ctl)
    c.close()

    return
    


def TcfiltCtlAll(fldpath,ctlpath,gtime,ofldopt):
    
    (flddir,fldfile)=os.path.split(fldpath)
    #
    # make .ctl for shear files
    #

    if(ofldopt == 'shear'):
        ctl="""dset ^%s
title input fields
undef %s
xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0
zdef   1 levels 1013
tdef   1 linear %s 6hr
vars 28
u8    0 0 input u
u8s   0 0 whole-field smoothed u
u8d   0 0 disturbance u (u-us); in hurricane zone = uhd + uhz
u8fd  0 0 vortectomised ud
u8hd  0 0 hurricane part of ufd
u8hz  0 0 non-hurricane part of ud in hurricane zone
u8f   0 0 final vortectomised u
v8    0 0 input v
v8s   0 0 whole-field smoothed v
v8d   0 0 disturbance v (v-vs); in hurricane zone = vhd + vhz
v8fd  0 0 vortectomised ud
v8hd  0 0 hurricane part of vfd
v8hz  0 0 non-hurricane part of vd in hurrican zone
v8f   0 0 final vortectomised v = us + ufd
u2    0 0 input u
u2s   0 0 whole-field smoothed u
u2d   0 0 disturbance u (u-us); in hurricane zone = uhd + uhz
u2fd  0 0 vortectomised ud
u2hd  0 0 hurricane part of ufd
u2hz  0 0 non-hurricane part of ud in hurricane zone
u2f   0 0 final vortectomised u
v2    0 0 input v
v2s   0 0 whole-field smoothed v
v2d   0 0 disturbance v (v-vs); in hurricane zone = vhd + vhz
v2fd  0 0 vortectomised ud
v2hd  0 0 hurricane part of vfd
v2hz  0 0 non-hurricane part of vd in hurrican zone
v2f   0 0 final vortectomised v = us + ufd
endvars"""%(fldfile,cundef,gtime)
        

    c=open(ctlpath,'w')
    c.writelines(ctl)
    c.close()

    return


def TcFiltPlots(paths,fcstmids,reffclatlons,fclatlons,model,
                dtg,dtgfld,itau,itauplt,
                r0opt,ofldopt,doallflds=0,dowdrive=0,verb=0):


    ttsf=-0.9
    
    vtimecolor=2
    if(itauplt <= 0): vtimecolor=3
    

    amodel=model
    ###if(w2.IsModel2(model)): amodel=model[0:3]

    vdtg=mf.dtginc(dtgfld,itau)
    vtime=mf.dtg2vtime(vdtg)

    gs=[]

    gsb=[]
    
    umodel=amodel.upper()

    if(dowdrive):
        pltdir="%s/tcfilt"%(w2.WdriveFtpBaseDir)
    else:
        pltdir=w2.TcTcfiltWebDir
        
    year=dtg[0:4]
    pltdir="%s/%s/%s"%(pltdir,year,dtg)
    mf.ChkDir(pltdir,'mk')

    bmdir="%s/basemap"%(pltdir)
    mf.ChkDir(bmdir,'mk')
    
    for fcstmid in fcstmids:
        fcstmid=fcstmid.split('.')[0]
        stmpltdir="%s/%s"%(pltdir,fcstmid)
        mf.ChkDir(stmpltdir,'mk')

    if(itauplt >= 0):
        ctau="%03d"%(itauplt)
        ctauplt="+%d h"%(itauplt)
    else:
        ctau="m%02d"%(abs(itauplt))
        ctauplt="-%d h"%(abs(itauplt))
        
    baseplt="%s.%s.%s"%(amodel,dtg,ctau)

    gspath='/%s/g.gs'%(pltdir)
    gsbpath='/%s/gb.gs'%(pltdir)


    gs=[]

    ipath=paths[2]
    opath=paths[4]

    positpath=paths[5]

    gsprod=1
    
    if(verb): print 'ipath ',ipath,' opath ',opath

    
    cbarnsf=0.75
    digsiz=0.045


    dlatall=35.0
    polefact=0.65
    dlatpole=dlatall*polefact
    dlateq=dlatall*(1.0-polefact)

    dlonall=55.0
    hemifact=0.65
    dlonE=dlonall*hemifact
    dlonW=dlonall*(1.0-hemifact)

    dlatoff=0
    dlonoff=dlatoff*1.5
    
    xlint=10
    ylint=5

    #
    # force grads to remake basemap; for testing
    #
    forcebasemap=0

    def phead(dotimelab=1):

        G("""
 
function main(args)
rc=gsfallow('on')
rc=const()
rc=jaecol()

'set mpdset mres'
'set grads off'

""")
        if(dotimelab):
            G("'set timelab on'")
            
        G("fi=ofile('%s')"%(ipath))
        if(verb): G("print 'fi 'fi")
        G("if(fi = 0) ; 'quit' ; endif")
        G("fo=ofile('%s')"%(opath))
        if(verb): G("print 'fo 'fo")
        G("if(fo = 0) ; 'quit' ; endif")

        print G

    def denv():

        pagellpath="%s/%s/pagell.%s.txt"%(pltdir,stm3id,stm3id)

        ref=reffclatlons[stmid]
        #ref=(reffclat,reffclon,reffcvmax,latplotmin,latplotmax,lonplotmin,lonplotmax)
        
        reflat=ref[0]
        reflon=ref[1]

        clat=reflat
        clon=reflon

        ilat=int(int((clat+1.0)/2)*2)
        ilon=int(int((clon+1.0)/2)*2)

        if(ilat > 0):
            lt1=ilat-dlateq+dlatoff
            lt2=lt1+dlatall
            ln1=ilon-dlonE-dlonoff
            ln2=ln1+dlonall
        else:
            lt1=ilat-dlatpole-dlatoff
            lt2=lt1+dlatall
            ln1=ilon-dlonE+dlonoff
            ln2=ln1+dlonall

        latplotmin=ref[3]
        latplotmax=ref[4]
        lonplotmin=ref[5]
        lonplotmax=ref[6]
        
        lt1=latplotmin
        lt2=latplotmax

        ln1=lonplotmin
        ln2=lonplotmax

        dlnplot=ln2-ln1
        if(dlnplot <= 20.0):
            bskip=1
        elif(dlnplot > 20.0 and dlnplot <= 40.0):
            bskip=2
        elif(dlnplot > 40.0 and dlnplot <= 60.0):
            bskip=3
        elif(dlnplot > 60.0 and dlnplot <= 100.0):
            bskip=4
        else:
            bskip=6

        #
        # define the bskip
        #

        G("_bskip=%d"%(bskip))
        
        G("'set lat %s %s'"%(lt1,lt2))
        G("'set lon %s %s'"%(ln1,ln2))

        G("'set gxout contour'")
        G("'set cmin 10000'")
        G("'d lat'")
        G("rc=plotdims()")
        G("'q xy2w 0 0'")
        G("plonw=subwrd(result,3)")
        G("plats=subwrd(result,6)")
        G("'q xy2w '_pagex' '_pagey")
        G("plone=subwrd(result,3)")
        G("platn=subwrd(result,6)")
        G("if(plon2 > 180.0); plonw=plonw-360.0; endif")
        G("if(plone > 180.0); plone=plone-360.0; endif")
        G("pagell='coordinates= 'platn', 'plonw', 'plats', 'plone")
        G("rc=write('%s',pagell)"%(pagellpath))
        G("rc=close('%s')"%(pagellpath))

        G("bt1='vortectomy opts: %s'"%(r0opt))
        


    def psetup(dotimelab=1):

        G("'c'")
        G("'set grads off'")
        if(dotimelab):
            G("'set timelab on'")


        G("'set grid on 3 15'")

        G("'set xlint %d'"%(xlint))
        G("'set ylint %d'"%(ylint))
        G("'set clopts -1 -1 0.09'")
        G("nplot=0")


    #pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp
    #
    # 850
    
    def p850(ua,va,ma,t1,t2,ppath,dosmth9,scol=1,dobasemap=1):

        psetup()

        if(dosmth9):
            G("pu='smth9(smth9(smth9(%s)))'"%(ua))
            G("pv='smth9(smth9(smth9(%s)))'"%(va))
            G("pm='smth9(smth9(smth9(%s)))'"%(ma))
            t2=t2+" smth9: 3X"
        else:
            G("pu='%s'"%(ua))
            G("pv='%s'"%(va))
            G("pm='%s'"%(ma))
            t2=t2+" smth9: NO"

        G("'set gxout contour'")
        G("'set cstyle 3'")
        G("'set cint 5'")
        G("'set rbrange 0 50'")
        G("'d 'pm")
        G("'set gxout barb'")
        G("'set ccolor 1'")
        G("'set digsiz %5.3f'"%(digsiz))
        G("'d skip('pu','_bskip');'pv")
        G("'set gxout stream'")
        G("'set strmden 3'")
        G("'set ccolor 7'")
        G("'set rbrange 0 15'")
        G("'set cint 5'")
        G("'d 'pu';'pv';'pm")
        G("'cbarn %3.2f'"%(cbarnsf))

        G("rc=plotdims()")
        G("'set clip '_xlplot' '_xrplot' '_ybplot' '_ytplot")
        G("rc=pltposit('%s')"%positpath)
        G("rc=tcplt(%d)"%(scol))
        G("'set clip 0 '_pagex' 0 '_pagey")

        G("t1='%s'"%(t1))
        G("t2='%s'"%(t2))
        G("if(nplot = 0); t2='NO DATA.....' ; endif")
        G("rc=toptitle(t1,t2,%3.1f,1,%d)"%(ttsf,vtimecolor))
        G("rc=bottitle(bt1,bt2,%3.1f,1,%d)"%(ttsf,vtimecolor))

        if(dobasemap):
            G("'printim %s -b %s -t 0 x%d y%d png'"%(ppath,bmppath,xsiz,ysiz))
        else:
            G("'printim %s x%d y%d'"%(ppath,xsiz,ysiz))
        ####G("print '%s'"%(ppath))

    #pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp
    #
    # psl
            
    def ppsl(psl,uas,vas,t1,t2,ppath,dosmth9,scol=1,dobasemap=1):

        psetup()

        dosmthuas=0
        
        G("'set clopts 1 -1 0.06'")
        if(dosmth9):
            G("ppsl='smth9(smth9(smth9(%s)))'"%(psl))
            if(dosmthuas):
                G("puas='smth9(smth9(smth9(%s)))'"%(uas))
                G("pvas='smth9(smth9(smth9(%s)))'"%(vas))
            else:
                G("puas='%s'"%(uas))
                G("pvas='%s'"%(vas))
            G("bt2=' smth9: 3X'")

                
        else:
            G("ppsl='%s'"%(psl))
            G("puas='%s'"%(uas))
            G("pvas='%s'"%(vas))
            G("bt2=' smth9: NO'")

        G("rcnp=npvalid(ppsl)")
        G("if(rcnp > 0.0 & rcnp != 999.0)")
        G("nplot=nplot+1")

        G("'set gxout contour'")
        G("'set cstyle 1'")
        G("'set ccolor rainbow'")
        G("'set cint 2'")
        G("'d 'ppsl")

        G("endif")

        G("rcnp=npvalid(puas)")
        G("if(rcnp > 0 & rcnp != 999.0)")
        G("nplot=nplot+1")

        G("'set gxout barb'")
        G("'set ccolor 1'")
        G("'set digsiz 0.045'")
        G("'d skip('puas','_bskip');'pvas")

        G("endif")

        G("if(rcnp > 0 & rcnp != 999.0)")
        G("nplot=nplot+1")

        G("rc=plotdims()")
        G("'set clip '_xlplot' '_xrplot' '_ybplot' '_ytplot")
        G("rc=pltposit('%s')"%positpath)
        G("rc=tcplt(%d)"%(scol))

        G("endif")

        G("'set clip 0 '_pagex' 0 '_pagey")
        G("t1='%s'"%(t1))
        G("t2='%s'"%(t2))
        G("if(nplot = 0); t2='NO DATA.....' ; endif")
        G("rc=toptitle(t1,t2,%3.1f,1,%d)"%(ttsf,vtimecolor))
        G("rc=bottitle(bt1,bt2,%3.1f,1,%d)"%(ttsf,vtimecolor))

        if(dobasemap):
            G("'printim %s -b %s -t 0 x%d y%d png'"%(ppath,bmppath,xsiz,ysiz))
        else:
            G("'printim %s x%d y%d'"%(ppath,xsiz,ysiz))
        ####G("print '%s'"%(ppath))

    #pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp
    #
    # 500 zg

    def pz500(z5,t1,t2,ppath,dosmth9,dobasemap=1,scol=1):

        psetup()

        if(dosmth9):
            G("pz5='smth9(smth9(smth9(%s)))'"%(z5))
        else:
            G("pz5='%s'"%(z5))
            t2=t2+" smth9: NO"

        G("'set gxout contour'")
        G("'set cstyle 1'")
        G("'set cint 10'")
        G("'set ccolor rainbow'")
        G("'d 'pz5")
        
        G("rc=plotdims()")
        G("'set clip '_xlplot' '_xrplot' '_ybplot' '_ytplot")
        G("rc=pltposit('%s')"%positpath)
        G("rc=tcplt(%d)"%(scol))
        G("'set clip 0 '_pagex' 0 '_pagey")

        G("t1='%s'"%(t1))
        G("t2='%s'"%(t2))
        G("if(nplot = 0); t2='NO DATA.....' ; endif")
        G("rc=toptitle(t1,t2,%3.1f,1,%d)"%(ttsf,vtimecolor))
        G("rc=bottitle(bt1,bt2,%3.1f,1,%d)"%(ttsf,vtimecolor))

        if(dobasemap):
            G("'printim %s -b %s -t 0 x%d y%d png'"%(ppath,bmppath,xsiz,ysiz))
        else:
            G("'printim %s x%d y%d'"%(ppath,xsiz,ysiz))
        ####G("print '%s'"%(ppath))

    #pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp
    #
    # 850-200 shear

        
    def pshr(us,vs,ms,t1,t2,ppath,dosmth9,scol=1,dobasemap=1):

        if(dosmth9):
            G("pu='smth9(smth9(smth9(%s)))'"%(us))
            G("pv='smth9(smth9(smth9(%s)))'"%(vs))
            G("pm='smth9(smth9(smth9(%s)))'"%(ms))
            G("bt2=' smth9: 3X'")

        else:
            G("pu='%s'"%(us))
            G("pv='%s'"%(vs))
            G("pm='%s'"%(ms))
            G("bt2=' smth9: NO'")
            
        psetup()

        G("rcnp=npvalid(pm)")
        G("if(rcnp > 0.0 & rcnp != 999.0)")
        G("nplot=nplot+1")

        G("'set gxout contour'")
        G("'set cstyle 3'")
        G("'set cint 10'")
        G("'set clevs 5 10 20 30 40'")
        G("'set rbrange 0 40'")
        G("'d maskout('pm',40-'pm')'")
        
        G("'set gxout barb'")
        G("'set ccolor 1'")
        G("'set digsiz 0.045'")
        G("'d skip('pu','_bskip');'pv")
        
        G("'set gxout stream'")
        G("'set strmden 3'")
        G("'set cint 10'")
        G("'set clevs 5 10 20 30 40'")
        G("'set rbrange 0 40'")
        G("'d maskout('pu',100040.0-'pm');'pv';'pm")
        G("'cbarn %3.2f'"%(cbarnsf))

        G("rc=plotdims()")
        G("'set clip '_xlplot' '_xrplot' '_ybplot' '_ytplot")
        G("rc=pltposit('%s')"%positpath)
        G("rc=tcplt(%d)"%(scol))
        G("'set clip 0 '_pagex' 0 '_pagey")
        
        G("endif")

        G("t1='%s'"%(t1))
        G("t2='%s'"%(t2))

        G("if(nplot = 0); t2='NO DATA.....' ; endif")
        G("rc=toptitle(t1,t2,%3.1f,1,%d)"%(ttsf,vtimecolor))
        G("rc=bottitle(bt1,bt2,%3.1f,1,%d)"%(ttsf,vtimecolor))

        if(dobasemap):
            G("'printim %s -b %s -t 0 x%d y%d png'"%(ppath,bmppath,xsiz,ysiz))
        else:
            G("'printim %s x%d y%d'"%(ppath,xsiz,ysiz))
        ####G("print '%s'"%(ppath))


    def pmcadie(vrt8,u2,v2,z5,t1,t2,ppath,dosmth9,scol=45,dobasemap=1):

        if(dosmth9):
            #
            # don't smooth vort for mcadie chart
            #
            # G("pvrt='smth9(smth9(smth9(%s)))'"%(vrt8))
            G("pvrt='%s'"%(vrt8))
            G("pu2='smth9(smth9(smth9(%s)))'"%(u2))
            G("pv2='smth9(smth9(smth9(%s)))'"%(v2))
            G("pz5='smth9(smth9(smth9(%s)))'"%(z5))
            G("bt2=' smth9: 3X'")

        else:
            G("pvrt='%s'"%(vrt8))
            G("pu2='%s'"%(u2))
            G("pv2='%s'"%(v2))
            G("pz5='%s'"%(z5))
            G("bt2=' smth9: NO'")

            
        psetup()

        G("rcnp=npvalid(pvrt)")
        G("if(rcnp > 0.0 & rcnp != 999.0)")
        G("nplot=nplot+1")

        G("'set gxout shaded'")
        G("'set csmooth on'")
        G("'set clevs   4   6    8    10    12    14   16  18    20   24   28   32   40'")
        G("'set ccols 0   39  37   35    22   24    26   27   28   51    53   55   57   6'")
        G("'d 'pvrt")
        G("'cbarn %3.2f'"%(cbarnsf))
        G("endif")

        G("rcnp=npvalid(pz5)")
        G("if(rcnp > 0.0 & rcnp != 999.0)")
        G("nplot=nplot+1")

        G("'set gxout contour'")
        G("'set cstyle 1'")
        G("'set cint 10'")
        G("'set clopts 1 -1 0.06'")
        G("'set clskip 3 3.0'")
        G("'set ccolor rainbow'")
        G("'set ccolor 7'")
        G("'d 'pz5")
        G("endif")
        
        G("rcnp=npvalid(pu2)")
        G("if(rcnp > 0.0 & rcnp != 999.0)")
        G("nplot=nplot+1")

        G("'set gxout barb'")
        G("'set ccolor 1'")
        G("'set digsiz 0.045'")
        G("'d skip('pu2','_bskip');'pv2")
        
        G("'set ccolor 0'")
        G("'set cthick 10'")
        G("'d skip('pu2','_bskip');maskout('pv2',('pvrt')-4)'")
        
        G("'set ccolor 1'")
        G("'set cthick 3'")
        G("'d skip('pu2','_bskip');maskout('pv2',('pvrt')-4)'")

        G("rc=plotdims()")
        G("'set clip '_xlplot' '_xrplot' '_ybplot' '_ytplot")
        G("rc=pltposit('%s')"%positpath)
        G("rc=tcplt(%d)"%(scol))
        G("endif")

        G("'set clip 0 '_pagex' 0 '_pagey")

        G("t1='%s'"%(t1))
        G("t2='%s'"%(t2))
        
        G("if(nplot = 0); t2='NO DATA.....' ; endif")
        G("rc=toptitle(t1,t2,%3.1f,1,%d)"%(ttsf,vtimecolor))
        G("rc=bottitle(bt1,bt2,%3.1f,1,%d)"%(ttsf,vtimecolor))

        if(dobasemap):
            G("'printim %s -b %s -t 0 x%d y%d png'"%(ppath,bmppath,xsiz,ysiz))
        else:
            G("'printim %s x%d y%d'"%(ppath,xsiz,ysiz))
        ####G("print '%s'"%(ppath))

    def dvarshr():

        G("'u8i=u8.1*'_ms2kt")
        G("'v8i=v8.1*'_ms2kt")
        G("'u2i=u2.1*'_ms2kt")
        G("'v2i=v2.1*'_ms2kt")

        G("'cf=lat/abs(lat)'")
        G("'cf=const(cf,1,-u)'")
        
        G("'rvrt8i=hcurl(u8.1,v8.1)*1e5*cf'")
        G("'rvrt8o=hcurl(u8.2,v8.2)*1e5*cf'")

        if(doallflds):
            G("'u8o=u8f.2*'_ms2kt")
            G("'v8o=v8f.2*'_ms2kt")
            G("'u2o=u2f.2*'_ms2kt")
            G("'v2o=v2f.2*'_ms2kt")
        else:
            G("'u8o=u8.2*'_ms2kt")
            G("'v8o=v8.2*'_ms2kt")
            G("'u2o=u2.2*'_ms2kt")
            G("'v2o=v2.2*'_ms2kt")

        G("'m8i=mag(u8i,v8i)'")
        G("'m8o=mag(u8o,v8o)'")

        G("'m2i=mag(u2i,v2i)'")
        G("'m2o=mag(u2o,v2o)'")

        #
        # use maskout of big values for new type of failure of
        # tcfilt.x made with g95 and
        #

        domask=1
        if(domask):
            G("'rvrt8o=maskout(rvrt8o,1e8-abs(rvrt8o))'")
            
            G("'u2o=maskout(u2o,1e8-abs(u2o))'")
            G("'v2o=maskout(v2o,1e8-abs(v2o))'")
            G("'m2o=maskout(m2o,1e8-abs(m2o))'")
            
            G("'u8o=maskout(u8o,1e8-abs(u8o))'")
            G("'v8o=maskout(v8o,1e8-abs(v8o))'")
            G("'m8o=maskout(m8o,1e8-abs(m8o))'")
            


    def dvarbasic():
        
        G("'psli=psl.1'")
        G("'uasi=uas.1*'_ms2kt")
        G("'vasi=vas.1*'_ms2kt")
        G("'z5i=z5.1'")
        
        G("'pslo=psl.2'")
        G("'z5o=z5.2'")
        G("'uaso=uas.2*'_ms2kt")
        G("'vaso=vas.2*'_ms2kt")

        G("'pslo=maskout(pslo,1e8-abs(pslo))'")
        G("'z5o=maskout(z5o,1e8-abs(z5o))'")
        G("'uaso=maskout(uaso,1e8-abs(uaso))'")
        G("'vaso=maskout(vaso,1e8-abs(vaso))'")

    def setpltpath(product,pltdir,stmid,baseplt,r0opt):

        fcstmid=stmid.split('.')[0].upper()
        
        pltfull="/%s/%s/%s.%3s.%s.full.%s.png"%(pltdir,fcstmid,baseplt,fcstmid,product,r0opt)
        pltvrtm="/%s/%s/%s.%3s.%s.vrtm.%s.png"%(pltdir,fcstmid,baseplt,fcstmid,product,r0opt)
        return(pltfull,pltvrtm)


    def dplotbasic():

        (pltfull,pltvrtm)=setpltpath('psl',pltdir,stmid,baseplt,r0opt)

        ti1="%s: %s `3t`0= %s for: %s total psl"%(umodel,dtg,ctauplt,stmid)
        ti2="Verify: %s"%(vtime)
        ppsl('psli','uasi','vasi',ti1,ti2,pltfull,0)
        
        to1="%s: %s `3t`0= %s for: %s `2vortectomised`0 psl"%(umodel,dtg,ctauplt,stmid)
        ppsl('pslo','uasi','vasi',to1,ti2,pltvrtm,1)

        doz500=0
        if(doz500):
            (pltfull,pltvrtm)=setpltpath('z500',pltdir,stmid,baseplt,r0opt)
            ti1="%s: %s `3t`0= %s for: %s total z500"%(umodel,dtg,ctauplt,stmid)
            ti2="Verify: %s"%(vtime)

            pz500('z5i',ti1,ti2,pltfull,0)
            
            to1="%s: %s `3t`0= %s for: %s `2vortectomised`2 z500"%(umodel,dtg,ctauplt,stmid)
            pz500('z5o',to1,ti2,pltvrtm,1)


        

    def dplotshr():

        
        G("'usi=u2i-u8i'")
        G("'vsi=v2i-v8i'")
        G("'uso=u2o-u8o'")
        G("'vso=v2o-v8o'")
        G("'msi=mag(usi,vsi)'")
        G("'mso=mag(uso,vso)'")

        (pltfull,pltvrtm)=setpltpath('uv850',pltdir,stmid,baseplt,r0opt)
        (pltshri,pltshro)=setpltpath('sh200',pltdir,stmid,baseplt,r0opt)

        do850=0

        if(do850):
            #
            # 850 full
            #
            t8i1="%s: %s `3t`0= %s for: %s total 850 flow"%(umodel,dtg,ctauplt,stmid)
            t8i2="Verify: %s"%(vtime)

            p850('u8i','v8i','m8i',t8i1,t8i2,pltfull,0)

            #
            # 850 vortectomised
            #
            t8o1="%s: %s `3t`0= %s for: %s `2vortectomised`0  850 flow"%(umodel,dtg,ctauplt,stmid)
            t8i2="Verify: %s"%(vtime)

            p850('u8o','v8o','m8o',t8o1,t8o2,pltvrtm,1)
        
        #
        # full 850-200 shear
        #
        tsi1="%s: %s `3t`0= %s for: %s total 200-850 shear"%(umodel,dtg,ctauplt,stmid)
        tsi2="Verify: %s"%(vtime)

        pshr('usi','vsi','msi',tsi1,tsi2,pltshri,0)

        #
        # vortectomised 850-200 shear
        #
        tso1="%s: %s `3t`0= %s for: %s `2vortectomised`0 200-850 shear"%(umodel,dtg,ctauplt,stmid)
        tso2="Verify: %s"%(vtime)

        pshr('uso','vso','mso',tso1,tso2,pltshro,1)



    def dplotmcadie():

        (pltfull,pltvrtm)=setpltpath('vt850',pltdir,stmid,baseplt,r0opt)
        
        #
        # full 850-200 shear
        #
        ti1="%s: %s `3t`0= %s for: %s 850 vort + 500 z + 200 wind"%(umodel,dtg,ctauplt,stmid)
        ti2="Verify: %s"%(vtime)

        pmcadie('rvrt8i','u2i','v2i','z5i',ti1,ti2,pltfull,0)


        #
        # vortectomised 850-200 shear
        #
        to1="%s: %s `3t`0= %s for: %s `2vortectomised 850`0 vort + 500 z + 200 wind"%(umodel,dtg,ctauplt,stmid)
        to2="Verify: %s"%(vtime)

        print 'PPP TCfilt.py: ',pltfull
        pmcadie('rvrt8i','u2o','v2o','z5o',to1,to2,pltvrtm,1)



    def pbasemap():

        G("'c'")
        G("'set grads off'")
        G("'set grid on 3 15'")

        G("'set xlint %d'"%(xlint))
        G("'set ylint %d'"%(ylint))

        G("'set timelab off'")
        G("'set rgb 90 100 50 25'")
        G("'set rgb 91 10 20 85'")
        G("lcol=90")
        G("ocol=91")

        G("'set cmin 10e10'")
        G("'d psl(t=1)'")

        G("'basemap.2 L 'lcol' 1'")
        G("'basemap.2 O 'ocol' 1'")
        
        G("'set map 0 0 10'")
        G("'draw map'")
          
        G("'set cmin 10e10'")
        G("'d psl(t=1)'")

        G("'set map 1 0 3'")
        G("'draw map'")

        G("'printim %s x%d y%d'"%(bmppath,xsiz,ysiz))



    def setbmpath(stmid):

        bmstmid=stmid.split('.')[0].lower()
        bmplt="basemap.%s.%s.png"%(dtg,bmstmid)
        bmppath="%s/%s"%(bmdir,bmplt)
        return(bmppath)


    def pfinal():

        if(gsprod == 1):
            G("'quit'")
        else:
            G("return")

        G("""function tcplt(scol)
    i=1
    while(i<=_ncmd)

      'q w2xy '_dlnlt.i
      x1=subwrd(result,3)
      y1=subwrd(result,6)

      ssym=41
      ssiz=0.35
      sthk=5
      'draw wxsym 'ssym' 'x1' 'y1' 'ssiz' 'scol' 'sthk

      ftm=3
      ftc=3
      ftci=2

      ftsiz=0.080
      ftsizs=ftsiz+0.020
      ftsizi=ftsiz-0.040

      'set line 0'
      'draw mark 'ftm' 'x1' 'y1' 'ftsizs

      'set line 'ftc
      'draw mark 'ftm' 'x1' 'y1' 'ftsiz
      
      'set line 'ftci
      'draw mark 'ftm' 'x1' 'y1' 'ftsizi

      
      i=i+1
    endwhile""")


        

    #mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
    #
    # main
    #

    
    fcstmids.sort()

    #
    # make basemap
    #

    mask="%s/basemap.*.png"%(bmdir)
    bmaps=glob.glob(mask)
    if(verb): print 'llllllllllllllllllllll len(bmaps) len(fcstmsids) :',len(bmaps),len(fcstmids)

    if(len(bmaps) < len(fcstmids) or forcebasemap):

        G=gsb.append
        phead(dotimelab=0)
        for stmid in fcstmids:
            
            stm3id=stmid.split('.')[0].upper()
            bmppath=setbmpath(stmid)
            if(verb): print 'BBBBB making: ',bmppath
            denv()
            pbasemap()

        G("'quit'")

        mf.WriteList(gsb,gsbpath)

        gradsopt='-lbc'
        cmd="grads %s \"run %s\" -g 800x600+0+0"%(gradsopt,gsbpath)
        mf.runcmd(cmd)


    #
    # make plot .gs
    #
        
    G=gs.append

    phead()
    
    
    for stmid in fcstmids:
        
        bmppath=setbmpath(stmid)
        stm3id=stmid.split('.')[0].upper()

        denv()
        
        if(ofldopt == 'shear'):
            dvarshr()
            dplotshr()
            
        elif(ofldopt == 'basic'):
            dvarbasic()
            dvarshr()
            dplotbasic()
            dplotshr()
            dplotmcadie()

        if(gsprod == 0): G("'q pos'")

    pfinal()


    mf.WriteList(gs,gspath)

    gradsopt='-lc'
    if(gsprod == 1): gradsopt='-lbc'
    cmd="grads %s \"run %s\" -g 800x600+0+0"%(gradsopt,gspath)
    mf.runcmd(cmd)

    return(gspath)
    

def TcFiltTar(bdatdir,model,dtg,ctau):


    bmask="%s.%s.%s"%(model,dtg,ctau)
    tarfile="tcfilt.%s.tar"%(bmask)
    tarpath="%s/%s"%(bdatdir,tarfile)
    tarmask="tcfilt.fld.output.%s*"%(bmask)
    tarmask="%s tcfilt.posits.%s* *%s*png"%(tarmask,bmask,bmask)
    inputmask="*.gs *.dat tcfilt.fld.input.%s.%s.%s.*"%(model,dtg,ctau)

    tarcmd="(cd %s ; tar -civf %s %s)"%(bdatdir,tarpath,tarmask)
    mf.runcmd(tarcmd)
        
    tarcmd="(cd %s ; rm %s %s)"%(bdatdir,tarmask,inputmask)
    mf.runcmd(tarcmd)

    return(tarfile)


def TcFiltFlCfg(flfofpath,coordinatecard):

    cfg="""
# config file for my stuff
#backcolor=0x800000
backcolor=#fcf1da

controls=startstop, step, speed, zoom, looprock, refresh, location, toggle
controls_tooltip = Start and stop , step, change speed, zoom, Toggle between looping and rocking, Refresh the images from the server, Toggle lat/lon tooltip, right click on block to enable/disable; shift+click to single step 


file_of_filenames=%s

#transparency = #ffffff
transparency =#000000

active_zoom=true
pause=750

start_looping=true
rocking=false

keep_zoom=true

%s
coordinates_style = 0x40b0b0b0, 0x000000, , LAT=, LON=, 1

location_label=LatLon
location_labels = Show Lat/Lon, Hide Lat/Lon, 100 

font_size = 11

#318 252 1.25 56.25
"""%(flfofpath,coordinatecard)

    return(cfg)


def TcFiltFlHtml(flswfpath,flcfgpath):

    html="""<html>
<body>
<table>
<tr>
<td width='%d' align=left>

<OBJECT classid='clsid:D27CDB6E-AE6D-11cf-96B8-444553540000'
codebase='http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=9,0,0,0'
 WIDTH='%d' HEIGHT='%d' id='FlAniS'>

      <PARAM NAME='movie' VALUE='%s'>
      <PARAM NAME='quality' VALUE='high'>
      <PARAM NAME='menu' value='false'>
      <PARAM NAME='FlashVars' value='configFilename=%s'>

      <EMBED src='%s' NAME='FlAniS' swLiveConnect='false' quality='high' menu='false'
         WIDTH='%d' HEIGHT='%d' TYPE='application/x-shockwave-flash'
         PLUGINSPAGE='http://www.macromedia.com/go/getflashplayer' scale='noscale'
         FlashVars='configFilename=%s'>
      </EMBED>
 </OBJECT>
</td>
</tr>
</table>

</body>
</html>
"""%(xsizfl,xsizfl,ysizfl,flswfpath,flcfgpath,flswfpath,xsizfl,ysizfl,flcfgpath)

    return(html)


    

        
def TcFiltDb(model,dtg,dowdrive=0,verb=0):


    def reordertaus(taus):
        itaus=[]
        otaus=[]
        for tau in taus:
            if(tau[0] == 'm'):
                itau=int(tau[1:])*-1
                itaus.append(itau)
            else:
                itau=int(tau)
                itaus.append(itau)
                
        itaus.sort()
        for itau in itaus:
            if(itau < 0):
                otau="m%02d"%(itau*-1)
            else:
                otau="%03d"%(itau)
            otaus.append(otau)

        return(otaus)

    def reorderfof(ppp):

        pphash={}
        oppp=[]
        
        for pp in ppp:
            ctau=pp.split('.')[2]
            
            if(ctau[0] == 'm'):
                itau=int(ctau[1:])*-1
            else:
                itau=int(ctau)
                
            pphash[itau]=pp

        kk=pphash.keys()
        kk.sort()

        for k in kk:
            oppp.append(pphash[k])

        return(oppp)

        

    amodel=model
    ###if(w2.IsModel2(model)): amodel=model[0:3]

    umodel=amodel.upper()

    if(dowdrive):
        dbdir="%s/tcfilt"%(w2.WdriveFtpBaseDir)
        pltdir="%s/tcfilt"%(w2.WdriveFtpBaseDir)
    else:
        dbdir=w2.TcTcfiltWebDir
        pltdir=w2.TcTcfiltWebDir
        
    
    year=dtg[0:4]
    pltdir="%s/%s/%s"%(pltdir,year,dtg)

    mask="%s/???/%s.*png"%(pltdir,amodel)
    
    if(verb): print 'mask: ',mask

    plts=glob.glob(mask)
    if(len(plts) == 0):
        print 'nada plots...'
        return

    stms=[]
    pplts=[]
    pptypes=[]
    
    stmplts={}
    stmtauplts={}
    stmpplts={}

    for plt in plts:
        (dir,file)=os.path.split(plt)
        tt=dir.split('/')
        stm=tt[len(tt)-1]
        stms.append(stm)
        tt=file.split('.')
        tau=tt[2]
        pplt=tt[4]
        pptype=tt[5]
        pplts.append(pplt)
        pptypes.append(pptype)

        try:
            stmplts[stm].append((tau,pplt))
        except:
            stmplts[stm]=[]
            stmplts[stm].append((tau,pplt))

        try:
            stmtauplts[stm,tau].append(file)
        except:
            stmtauplts[stm,tau]=[]
            stmtauplts[stm,tau].append(file)

        try:
            stmpplts[stm,pplt,pptype].append(file)
        except:
            stmpplts[stm,pplt,pptype]=[]
            stmpplts[stm,pplt,pptype].append(file)
            


    stms=mf.uniq(stms)
    pplts=mf.uniq(pplts)
    pptypes=mf.uniq(pptypes)

    for stm in stms:
        fldir="%s/%s"%(pltdir,stm)
        coordpath="%s/%s/pagell.%s.txt"%(pltdir,stm,stm)
        cc=open(coordpath).readlines()
        coordinatecard=cc[0]

        for pplt in pplts:
            for pptype in pptypes:
                
                flfoffile="flanis.%s.%s.%s.fof.txt"%(amodel,pplt,pptype)
                flcfgfile="flanis.%s.%s.%s.cfg"%(amodel,pplt,pptype)
                flhtmfile="flanis.%s.%s.%s.htm"%(amodel,pplt,pptype)
                flswfpath="../../../../../swf/flanis.swf"
                
                flfofpath="%s/%s"%(fldir,flfoffile)
                flcfgpath="%s/%s"%(fldir,flcfgfile)
                flhtmpath="%s/%s"%(fldir,flhtmfile)

                pp=stmpplts[stm,pplt,pptype]
                pp=reorderfof(pp)

                w2.WriteList2File(flfofpath,pp)
                cfg=TcFiltFlCfg(flfoffile,coordinatecard)
                w2.WriteString2File(flcfgpath,cfg)
                html=TcFiltFlHtml(flswfpath,flcfgfile)
                w2.WriteString2File(flhtmpath,html)
    
    dbcards=[]

    dbcards.append(dtg)

    dbcard=stms[0]
    for stm in stms[1:]:
        dbcard="%s %s"%(dbcard,stm)

    dbcards.append(dbcard)

    for stm in stms:
        
        taus=[]
        pplts=[]
        dbfcards=[]
        
        for (tau,pplt) in stmplts[stm]:
            taus.append(tau)
            pplts.append(pplt)


        taus=mf.uniq(taus)
        taus=reordertaus(taus)
        
        pplts=mf.uniq(pplts)

        dbcardt="%s"%(stm)
        
        for tau in taus:
            dbcardt="%s %s"%(dbcardt,tau)
            dbfcard="%s %s"%(stm,tau)
            for file in stmtauplts[stm,tau]:
                dbfcard="%s %s"%(dbfcard,file)
            dbfcards.append(dbfcard)

        dbcards.append(dbcardt)
        
        dbcardp="%s"%(stm)
        for pplt in pplts:
            dbcardp="%s %s"%(dbcardp,pplt)
        dbcards.append(dbcardp)

        dbcards=dbcards+dbfcards

    dbpath="%s/db.%s.%s.txt"%(dbdir,amodel,dtg)

    if(verb): print 'ddddddddddddddddddd ',dbpath
    w2.WriteList2File(dbpath,dbcards)
        

    return(plts)
        


