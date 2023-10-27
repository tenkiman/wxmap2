import mf
import sys
import glob
import TCw2 as TC
import TCtdos

from math import sqrt,atan2,fabs

doplot=1

root2=sqrt(2.0)

def XeYeRotate(xe,ye):
    dye0=(ye-xe)/root2
    xe0=xe
    ye0=dye0
    return(xe0,ye0)

def XeYe2Rquad(xe,ye):
    r=sqrt(xe*xe+ye*ye)
    d=atan2(xe,ye)
    dd=d*mf.rad2deg
    ir=mf.nint(r)
    id=mf.nint(dd)
    if(id < 0): id=360+id
    if(id >= 0 and id <= 90): quad='NE'
    if(id > 90 and id <= 180): quad='SE'
    if(id > 180 and id <= 270): quad='SW'
    if(id > 270 and id <= 360): quad='NW'
    
    return(ir,id,quad)


def DfeGetErrorsByDtg(year,stmids,pfemode,tdoopt,aaidopt,taidopt,verb=0):

    vhash={}

    xehash={}
    xevdtgs={}
    yehash={}
    yevdtgs={}

    modopts=['%s.ofci'%(aaidopt),'%s.ofci'%(taidopt)]

    yeopt=modopts[1]
    xeopt=modopts[0]

    stmids.sort()

    vtaus=TC.Vtaus
    vtau=72

    nxe=0

    for stmid in stmids:

        b1id=stmid[2:3]
        vstmid="%s.%s"%(stmid,year)
        rulebase='JtwcOps'
        if(b1id == 'L' or b1id == 'E' or b1id == 'C'):
            rulebase='NhcOps'
            tccenter='NHC'

        xevdtgs[stmid]=[]
        yevdtgs[stmid]=[]

        for modopt in modopts:

            #
            # use homo cache
            #
            VTC=TC.GetTcVitalsHomoHash(stmid,year,[modopt],verb=0)
            vits=VTC.Vitals
            dfes=VTC.DfeVitals

            vks=TC.GetKeys(vits,'vits',verb)
            dks=TC.GetKeys(dfes,'dfes',verb)

            for dk in dks:
                dtau=dk[4]
                dmodcomp=dk[2]
                if(dtau == vtau):
                    if(dmodcomp == xeopt):
                        bvdtg=dk[2]
                        dvdtg=dk[1]
                        xehash[stmid,dvdtg]=dfes[dk]
                        dbdtg=mf.dtginc(dvdtg,-vtau)
                        xevdtgs[stmid].append(dvdtg)
                        nxe=nxe+1

                    elif(dmodcomp == yeopt):
                        dvdtg=dk[1]
                        yehash[stmid,dvdtg]=dfes[dk]
                        yevdtgs[stmid].append(dvdtg)

    ngt0stmids=[]
    nv=0
    for stmid in stmids:

        xedtgs=xevdtgs[stmid]
        try:
            xedtgs=mf.uniq(xedtgs)
            n=len(xedtgs)
            ngt0stmids.append(stmid)
        except:
            xedtgs=[]
            n=0
        nv=nv+len(xedtgs)


    fes=[]
    xes=[]
    yes=[]
    tdos=[]
    bdtgs=[]
    vdtgs=[]

    for stmid in ngt0stmids:

        xedtgs=xevdtgs[stmid]
        xedtgs=mf.uniq(xedtgs)
        xedtgs.sort()

        for xedtg in xedtgs:

            xe=xehash[stmid,xedtg]

            try:
                ye=yehash[stmid,xedtg]
            except:
                continue

            fyf1=float(ye[0])
            fyf2=float(ye[1])
            fxf1=float(xe[0])
            fxf2=float(xe[1])

            yy=float(ye[3])
            xx=float(xe[3])
            
            yy1=float(ye[4])
            xx1=float(xe[4])

            if(pfemode == 'fe'):
                yy1=float(ye[2])
                xx1=float(xe[2])
            elif(pfemode == 'pacom'):
                yy1=float(ye[4])
                xx1=float(xe[4])
            elif(pfemode == 'scaled'):
                yy1=float(ye[3])
                xx1=float(xe[3])

            else:
                print 'EEE invalid pfemode: ',pfemode
                sys.exit()

            tdo=xe[5]


            xes.append(xx1)
            yes.append(yy1)
            tdos.append(tdo)

            felist=[fxf1,fxf2,fyf1,fyf2]
            fes.append(felist)

            bdtg=mf.dtginc(xedtg,-vtau)
            bdtgs.append(bdtg)
            vdtgs.append(xedtg)


    rc=(xes,yes,fes,bdtgs,vdtgs,tdos,
        modopts,rulebase)
    
    return(rc)



def DfeTcotAnal(xe1,ye1,pfetype):


    dolinearfit=0
    docenter=1

    if(dolinearfit):
        m,b = polyfit(xe1,ye1,1)
        x1=[]
        y1=[]
        for x in range(-200,200,1):
            xx=float(x)
            x1.append(xx)
            yy=m*xx+b
            y1.append(yy)

    else:
        b=0.0
        m=1.0



    nxe=len(xe1)

    x2=[]
    y2=[]
    r2=[]

    minx=9.9e20
    maxx=-9.9e20
    miny=9.9e20
    maxy=-9.9e20
    meanx=0.0
    meany=0.0
    meanxl=0.0
    meanyl=0.0
    maxall=maxx

    n=0
    while(n<nxe):

        xl=xe1[n]
        yl=ye1[n]

        if(xl < minx): minx=xl
        if(xl > maxx): maxx=xl
        if(yl < miny): miny=yl
        if(yl > maxy): maxy=yl

        if(fabs(xl) > maxall): maxall=fabs(xl)
        if(fabs(yl) > maxall): maxall=fabs(yl)

        if(docenter):
            yel=m*xl + b
            dye=yl-yel
            dye0=(yl-xl)/root2
            xl0=root2*xl+(dye0)
            xl0=xl
        else:
            dye0=yl
            xl0=xl
            yel=xl
            dye=yl

        x2.append(xl0)
        y2.append(dye0)

        meanx=meanx+xl
        meany=meany+yl
        meanxl=meanxl+xl0
        meanyl=meanyl+dye0

        n=n+1

    meanxl=meanxl/float(n)
    meanyl=meanyl/float(n)
    meanx=meanx/float(n)
    meany=meany/float(n)

    print 'meanx, meany:   ',meanx,meany
    print 'meanxl, meanyl: ',meanxl,meanyl
    print 'minx, maxx:     ',minx,maxx
    print 'miny, maxy:     ',miny,maxy
    print 'MAXALL:         ',maxall

    n=0
    while(n<nxe):

        xl0c=x2[n]-meanxl
        dye0c=y2[n]-meanyl
        r=sqrt(xl0c*xl0c+dye0c*dye0c)
        r2.append(r)
        n=n+1

    #
    # do circ calcs
    #
    if(pfetype == 'circ'):

        if(doplot):
            from pylab import polyfit,hist
        else:
            dcirc=100.0
            maxall=100.0
            meanxl=100.0
            meanyl=100.0
            return(x2,y2,dcirc,maxall,meanxl,meanyl)
            
        nbins=50
        (n,bins,patches)=hist(r2,nbins,normed=0)

        ncirc=70.0

        na=[]
        nall=0
        np=len(n)

        for i in range(0,np):
            nall=nall+n[i]
            nfrac=(float(nall)/float(len(r2)))*100.0
            na.append(nfrac)

        for i in range(0,np):
            nfrac=na[i]
            if(nfrac > 70.0):
                nup=na[i]
                nlo=na[i-1]
                bup=bins[i]
                blo=bins[i-1]
                d1=(nup-ncirc)/(bup-blo)
                dcirc=bup-(d1*(bup-blo))
                break
    else:
        dcirc=None


    return(x2,y2,dcirc,maxall,meanxl,meanyl)



def DfeGetErrorsByTdo(year,stmids,pfemode,tdoopt,aaidopt,taidopt,verb=0):

    vhash={}

    xehash={}
    xevdtgs={}
    yehash={}
    yevdtgs={}

    modopts=['%s.ofci'%(aaidopt),'%s.ofci'%(taidopt)]

    (tdocolor,Color2Hex)=TCtdos.TdoColors()

    yeopt=modopts[1]
    xeopt=modopts[0]

    stmids.sort()

    vtaus=TC.Vtaus
    vtau=72

    nxe=0

    for stmid in stmids:

        b1id=stmid[2:3]
        vstmid="%s.%s"%(stmid,year)
        rulebase='JtwcOps'
        if(b1id == 'L' or b1id == 'E' or b1id == 'C'):
            rulebase='NhcOps'
            tccenter='NHC'

        xevdtgs[stmid]=[]
        yevdtgs[stmid]=[]

        for modopt in modopts:

            #
            # use homo cache
            #
            VTC=TC.GetTcVitalsHomoHash(stmid,year,[modopt],verb=0)
            vits=VTC.Vitals
            dfes=VTC.DfeVitals

            vks=TC.GetKeys(vits,'vits',verb)
            dks=TC.GetKeys(dfes,'dfes',verb)

            for dk in dks:
                dtau=dk[4]
                dmodcomp=dk[2]
                if(dtau == vtau):
                    if(dmodcomp == xeopt):
                        bvdtg=dk[2]
                        dvdtg=dk[1]
                        xehash[stmid,dvdtg]=dfes[dk]
                        dbdtg=mf.dtginc(dvdtg,-vtau)
                        xevdtgs[stmid].append(dvdtg)
                        nxe=nxe+1

                    elif(dmodcomp == yeopt):
                        dvdtg=dk[1]
                        yehash[stmid,dvdtg]=dfes[dk]
                        yevdtgs[stmid].append(dvdtg)

    ngt0stmids=[]
    nv=0
    for stmid in stmids:

        xedtgs=xevdtgs[stmid]
        try:
            xedtgs=mf.uniq(xedtgs)
            n=len(xedtgs)
            ngt0stmids.append(stmid)
        except:
            xedtgs=[]
            n=0
        nv=nv+len(xedtgs)


    fes=[]
    xe1=[]
    ye1=[]
    tdos=[]

    tdoxe1={}
    tdoye1={}
    tdofes={}
    tdobdtgs={}

    data=[]

    for stmid in ngt0stmids:

        xedtgs=xevdtgs[stmid]
        xedtgs=mf.uniq(xedtgs)

        for xedtg in xedtgs:

            xe=xehash[stmid,xedtg]

            try:
                ye=yehash[stmid,xedtg]
            except:
                continue

            fyf1=float(ye[0])
            fyf2=float(ye[1])
            fxf1=float(xe[0])
            fxf2=float(xe[1])

            yy=float(ye[3])
            xx=float(xe[3])
            
            yy1=float(ye[4])
            xx1=float(xe[4])

            if(pfemode == 'fe'):
                yy1=float(ye[2])
                xx1=float(xe[2])
            elif(pfemode == 'pacom'):
                yy1=float(ye[4])
                xx1=float(xe[4])
            elif(pfemode == 'scaled'):
                yy1=float(ye[3])
                xx1=float(xe[3])

            else:
                print 'EEE invalid pfemode: ',pfemode
                sys.exit()

            tdo=xe[5]

            tdos.append(tdo)
            ye1.append(yy1)
            xe1.append(xx1)

            felist=[fxf1,fxf2,fyf1,fyf2]
            fes.append(felist)

            tdobdtg=mf.dtginc(xedtg,-vtau)

            try:
                tdobdtgs[tdo].append([tdobdtg,stmid])
            except:
                tdobdtgs[tdo]=[]
                tdobdtgs[tdo].append([tdobdtg,stmid])

            try:
                tdoxe1[tdo].append(xx1)
            except:
                tdoxe1[tdo]=[xx1]

            try:
                tdoye1[tdo].append(yy1)
            except:
                tdoye1[tdo]=[yy1]

            try:
                tdofes[tdo].append(felist)
            except:
                tdofes[tdo]=[felist]


    rc=(tdos,tdoxe1,tdoye1,tdofes,tdoopt,
        tdobdtgs,tdocolor,Color2Hex,
        xe1,ye1,
        modopts,rulebase)
    
    return(rc)



def DfeStatAnalByTdo(allstats,tdos,
                     aaidopt,
                     xehash,yehash,feshash,
                     runopts,tdoopt,dcirc,meanxl,meanyl,pfetype):

    import mf
    from math import sqrt,atan2


    (stmopt,stmids,year,bid1,bchk,
     modopts,tdoopt,ruleopt,rulebase,
     pfemode,pfetype,tdocolor,tdobdtgs)=runopts


    (nall,mfes,mx,my,mr,md,
           sxe,sye,sr,sd)=allstats

    doSumReportOnly=0

    stats={}
    report=[]
    tdocases={}

    modoptxe=modopts[0].split('.')[0]
    modoptye=modopts[1].split('.')[0]
    tmodel=modoptye.split('.')[0]
    bgmodel=modopts[0].split('.')[1]

    Xname=modoptxe.upper()
    Yname=modoptye.upper()
    Bname=bgmodel.upper()

    card="TCOT analysis for TCs: %s year: %s"%(stmopt,year)
    report.append(card)

    card="comparing xe: %s  v  ye: %s with bg: %s"%(Xname,Yname,Bname)
    report.append(card)

    card="pfemode: %s  pfetype: %s"%(pfemode,pfetype)
    report.append(card)
    report.append(' ')
    

    if(tdoopt != None):
        tdos=[tdoopt]

    ntot=0
    for tdo in tdos:
        xes=xehash[tdo]
        ntot=ntot+len(xes)


    sumStatsTdos={}
    doD={}
    
    
    for tdo in tdos:

        xes=xehash[tdo]
        yes=yehash[tdo]
        fes=feshash[tdo]
        bdtgs=tdobdtgs[tdo]
        
        npts=len(xes)

        mfestdo=[0.0,0.0,0.0,0.0]
        mxtdo=0.0
        mytdo=0.0
        mrtdo=0.0
        mdtdo=0.0
        
        sxetdo=0.0
        syetdo=0.0
        srtdo=0.0
        sdtdo=0.0

        s2xetdo=0.0
        s2yetdo=0.0
        s2rtdo=0.0
        s2dtdo=0.0
        
        for n in range(0,npts):
            xe=xes[n]
            ye=yes[n]
            fe=fes[n]

            for i in range(0,4):
                mfestdo[i]=mfestdo[i]+fe[i]
                
            r=sqrt(xe*xe+ye*ye)
            d=atan2(xe,ye)
            
            mxtdo=mxtdo+xe
            mytdo=mytdo+ye
            s2xetdo=s2xetdo+xe*xe
            s2yetdo=s2yetdo+ye*ye
            
            mrtdo=mrtdo+r
            mdtdo=mdtdo+d
            s2rtdo=s2rtdo+r*r
            s2dtdo=s2dtdo+d*d
            
        #
        # tdo metrics
        #
        
        if(npts > 0):

            srtdo=sqrt( (s2rtdo/npts) - (mrtdo/npts)*(mrtdo/npts) )
            sdtdo=sqrt( (s2dtdo/npts) - (mdtdo/npts)*(mdtdo/npts) )*mf.rad2deg
            sxetdo=sqrt( (s2xetdo/npts) - (mxtdo/npts)*(mxtdo/npts) )
            syetdo=sqrt( (s2yetdo/npts) - (mytdo/npts)*(mytdo/npts) )

            for i in range(0,4):
                mfestdo[i]=mfestdo[i]/npts

            mxtdo=mxtdo/npts
            mytdo=mytdo/npts
            mrtdo=mrtdo/npts
            mdtdo=mdtdo/npts
            mdtdo=mdtdo*mf.rad2deg

            fextdo=mfestdo[0]
            feytdo=mfestdo[2]
            febtdo=mfestdo[1]
            febxtdo=mfestdo[3]
            
            feb=mfes[1]

            dofdifftdo=int(((febtdo-feb)/(feb))*100.0+0.5)

            dfexbtdo=febxtdo-fextdo
            dfeybtdo=febtdo-feytdo
            
            gainxbtdo=((febtdo-fextdo)/febtdo)*100.0
            gainybtdo=((febtdo-feytdo)/febtdo)*100.0
            gainxytdo=((fextdo-feytdo)/fextdo)*100.0


        else:
            print 'EEEEEEEEEEEEEe hmmm, no points for tdo',tdo
            sys.exit()
            
        doD[tdo]=dofdifftdo

        cases=[]
        for n in range(0,npts):
            xe=xes[n]
            ye=yes[n]
            fe=fes[n]
            bdtg=bdtgs[n][0]
            stmid=bdtgs[n][1]
            case=[stmid,bdtg,fe[0],fe[2],fe[1],xe,ye]
            cases.append(case)

        tdocases[tdo]=cases


        rc=(npts,mxtdo,mytdo,mrtdo,mdtdo,
            srtdo,sdtdo,sxetdo,syetdo,
            fextdo,feytdo,febtdo,febxtdo,feb,dofdifftdo,
            dfexbtdo,dfeybtdo,
            gainxbtdo,gainybtdo,gainxytdo)
        
        sumStatsTdos[tdo]=rc


    #
    # order TDOs by Degree of Difficulty
    #
    tdosdof=sorted(doD, key=doD.__getitem__, reverse=True)


    for tdo in tdosdof:

        (npts,mxtdo,mytdo,mrtdo,mdtdo,
         srtdo,sdtdo,sxetdo,syetdo,
         fextdo,feytdo,febtdo,febxtdo,feb,dofdifftdo,
         dfexbtdo,dfeybtdo,
         gainxbtdo,gainybtdo,gainxytdo)=sumStatsTdos[tdo]
        
        coltdo=tdocolor[tdo]
        if(not(doSumReportOnly)):
            report.append(' ')
        fracfc=(float(npts)/float(ntot))*100.0
        if(not(doSumReportOnly)):
            card1="Final Stats for TDO: %s N=%d  %%Ntot=%4.1f ; Colorized: %s"%(tdo,npts,fracfc,coltdo)
            report.append(card1)
            card2="Degree of Difficulty: %i  MeanBG: %4.0f TdoBG: %4.0f"%(dofdifftdo,feb,febtdo)
            report.append(card2)
            report.append("Mean  xe,ye,r,d: %6.1f %6.1f %6.1f %6.1f"%(mxtdo,mytdo,mrtdo,mdtdo))
        dbo1=mxtdo-mytdo
        if(not(doSumReportOnly)):
            report.append("Sigma xe,ye,r,d: %6.1f %6.1f %6.1f %6.1f"%(sxetdo,syetdo,srtdo,sdtdo))

        if(not(doSumReportOnly)):
            report.append("  Mean FE x,y,b: %6.1f %6.1f %6.1f "%(fextdo,feytdo,febtdo))

        if(not(doSumReportOnly)):
            report.append("Mean FE dxb dyb: %6.1f %6.1f"%(dfexbtdo,dfeybtdo))

        if(not(doSumReportOnly)):
            report.append("    Gain x on b: %6.1f%%"%(gainxbtdo))

        if(not(doSumReportOnly)):
            report.append("    Gain y on b: %6.1f%%"%(gainybtdo))

        if(not(doSumReportOnly)):
            report.append("    Gain x on y: %6.1f%%"%(gainxytdo))

        if(pfetype == 'circ'):
            
            report.append(' ')
            idcirc=mf.nint(dcirc)
            card="Cases for TDO: %s       X: %s     Y: %s     B: %s   TCOT:  %i nm"%(tdo,Xname,Yname,Bname,idcirc)
            report.append(card)

            cases=tdocases[tdo]
            ncase=len(cases)
            for case in cases:
                (stmid,bdtg,xfe,yfe,bfe,xe,ye)=case
                (xe0,ye0)=XeYeRotate(xe,ye)
                xe0c=xe0-meanxl
                ye0c=ye0-meanyl
                (ir0,id0,quad)=XeYe2Rquad(xe0c,ye0c)
                ixe0=mf.nint(xe0)
                iye0=mf.nint(ye0)
                if(ir0 > idcirc):
                    balert="==>>>"
                    if(ixe0 < 0):
                        balert="<<<>>"
                        calert=' Bad  HS/TDO! :( on U!'
                    else:
                        balert="++++>"
                        calert=' Good HS/TDO  :) %s > OFCI'%(aaidopt)

                else:
                    if(ixe0 < 0):
                        balert=" --- "
                    else:
                        balert="  +  "
                    calert=' -----'
                card="%s %s %s   xFE: %5.1f  yFE: %5.1f  bFE: %5.1f   xe: %6.1f ye: %6.1f"%(balert,stmid,bdtg,xfe,yfe,bfe,xe,ye)
                card=card+"  TCOT(x,y,r): % 4i,%4i,%4i,%4i %s  %s"%(ixe0,iye0,ir0,id0,quad,calert)
                report.append(card)

            card="Total Cases: %i "%(ncase)
            report.append(card)
            report.append(' ')

        #
        # new page!!!
        #
        report.append(mf.NewPageChar)

        stats[tdo]=[npts,mxtdo,mytdo,mrtdo,mdtdo,
                    sxetdo,syetdo,srtdo,sdtdo]


    report.append(' ')
    report.append("Final Stats for: ALL TDOs N=%d"%(nall))
    report.append("Mean  xe,ye,r,d: %6.1f %6.1f %6.1f %6.1f"%(mx,my,mr,md))
    dbo1=mx-my
    report.append("Sigma xe,ye,r,d: %6.1f %6.1f %6.1f %6.1f"%(sxe,sye,sr,sd))

    fex=mfes[0]
    fey=mfes[2]
    feb=mfes[3]
    febx=mfes[1]
    report.append("  Mean FE x,y,b: %6.1f %6.1f %6.1f "%(fex,fey,feb))

    dfexb=febx-fex
    dfeyb=feb-fey
    report.append("Mean FE dxb dyb: %6.1f %6.1f"%(dfexb,dfeyb))

    gainxb=((feb-fex)/feb)*100.0
    report.append("    Gain x on b: %6.1f%%"%(gainxb))

    gainyb=((feb-fey)/feb)*100.0
    report.append("    Gain y on b: %6.1f%%"%(gainyb))

    gainxy=((fex-fey)/fex)*100.0
    report.append("    Gain x on y: %6.1f%%"%(gainxy))

    stats['all']=[nall,mx,my,mr,md,
                  sxe,sye,sr,sd]


    return(stats,report)



def DfeStatAnalAll(tdos,xehash,yehash,feshash,
                   runopts,tdoopt):


    (stmopt,stmids,year,bid1,bchk,
     modopts,tdoopt,ruleopt,rulebase,
     pfemode,pfetype,tdocolor,tdobdtgs)=runopts


    mfes=[0.0,0.0,0.0,0.0]
    
    mx=0.0
    my=0.0
    mr=0.0
    md=0.0
    nall=0

    sxe=0.0
    sye=0.0
    sr=0.0
    sd=0.0

    s2xe=0.0
    s2ye=0.0
    s2r=0.0
    s2d=0.0

    if(tdoopt != None):
        tdos=[tdoopt]


    ntot=0
    for tdo in tdos:
        try:
            xes=xehash[tdo]
            ntot=ntot+len(xes)
        except:
            return(None)
            


    nall=0
    for tdo in tdos:

        xes=xehash[tdo]
        yes=yehash[tdo]
        fes=feshash[tdo]
        
        npts=len(xes)
        nall=nall+npts
        
        for n in range(0,npts):
            xe=xes[n]
            ye=yes[n]
            fe=fes[n]

            for i in range(0,4):
                mfes[i]=mfes[i]+fe[i]
                
            mx=mx+xe
            my=my+ye
            s2xe=s2xe+xe*xe
            s2ye=s2ye+ye*ye
            
            r=sqrt(xe*xe+ye*ye)
            d=atan2(xe,ye)
            
            mr=mr+r
            md=md+d
            s2r=s2r+r*r
            s2d=s2d+d*d

    if(nall > 0):

        for i in range(0,4):
            mfes[i]=mfes[i]/nall
            
        sr=sqrt( (s2r/nall) - (mr/nall)*(mr/nall) )
        sd=sqrt( (s2d/nall) - (md/nall)*(md/nall) )*mf.rad2deg
        sxe=sqrt( (s2xe/nall) - (mx/nall)*(mx/nall) )
        sye=sqrt( (s2ye/nall) - (my/nall)*(my/nall) )

        mx=mx/nall
        my=my/nall
        mr=mr/nall
        md=md/nall
        mds=md*mf.rad2deg

    else:
        sr=-999.9
        sd=-999.9
        sxe=-999.9
        sye=-999.9

        mx=-999.9
        my=-999.9
        mr=-999.9
        md=-999.9
        md=-999.9


    allstats=[nall,mfes,mx,my,mr,md,
           sxe,sye,sr,sd]

    return(allstats)





def DfeStatFigureTable(stats,aaidopt,tdos):

    table={}
    
    colLabels = ('N', '%s-ofci'%(aaidopt), 'aid-ofci', '%s-aid'%(aaidopt))
    rowLabels = ['%d year' % x for x in (100, 50, 20, 10, 5)]
    data=[]
    ctxt=[]
    
    rowLabels = []
    for tdo in tdos:
        rlab="%s"%(tdo)
        rowLabels.append(rlab)

        st=stats[tdo]

        n=st[0]
        xe=st[1]
        ye=st[2]
        dbo=xe-ye
        row=[n,xe,ye,dbo]
        data.append(row)
        
        cn="%d"%(st[0])
        cxe="%6.0f"%(xe)
        cye="%6.0f"%(ye)
        cdbo="%6.0f"%(xe-ye)
        cn=cn.strip()
        cxe=cxe.strip()
        cye=cye.strip()
        cdbo=cdbo.strip()

        crow=[cn,cxe,cye,cdbo]
        ctxt.append(crow)
        

    table['clab']=colLabels
    table['rlab']=rowLabels
    table['data']=data
    table['ctxt']=ctxt
    

    return(table)




def tcotTopTitle(pfemode,bchk,nxe,
                 tccenter,tcbasin,tdoopt,
                 aaidopt,taidopt,baidopt,
                 stmid,year,
                 meanxtdo,meanytdo,
                 meanxl,meanyl,
                 meanan,meanob,meanbg,
                 dcirc):


    if(pfemode == 'fe'):
        circunit='nm'
        xlab='BG dFE (ofci-%s) [nm]'%(aaidopt)
        ylab='OB dFE (ofci-%s) [nm]'%(taidopt)
    elif(pfemode == 'pacom'):
        xlab='(ofci-%s)/PACOM (150 nm @ 72 h) [%]'%(aaidopt)
        ylab='(ocfi-%s)/PACOM [%%]'%(taidopt)
        circunit='%'

    if(bchk != None):
        if(tdoopt != None):
            tdoname=TCtdos.TdoNameTitles()
            tdotitle=tdoname[tdoopt.upper()]
            tt0="%s(x|BG) v %s(y|OB) 72-h FC -- %s %s Season N=%d "%(tdotitle,taidopt,tcbasin,year,nxe)
        else:
            tt0="TCOT dFE %s(x|BG) v %s(y|OB) 72-h FC %s %s  N=%d "%(aaidopt.upper(),taidopt.upper(),tcbasin,year,nxe)
    else:
        tt0='%s(x|BG) v %s(y|OB) 72-h FC : %s %s  N=%d'%(aaidopt.upper(),taidopt.upper(),stmid,year,nxe)


    ttdo="'TDO Circle of Trust' (70%%, recentered) R=%3.0f %s"%(dcirc,circunit)
    t1in="TDO BG gain: %3.0f  ALLTDO gain: %3.0f"%(meanxtdo,meanxl)
    t2in="TDO OB gain: % 3.0f  ALLTDO gain: %3.0f"%(meanytdo,meanyl)

    if(meanan != None):
        t3in="storm: %s  FE summary"%(stmid)
        t4in="AN(%s): %3.0f OB(%s): %3.0f BG(%s): %3.0f"%(aaidopt,meanan,
                                                          taidopt,meanob,
                                                          baidopt,meanbg)


    else:
        t3in=None
        t4in=None


    t1="%s\n%s"%(tt0,ttdo)

    return(t1,xlab,ylab,t1in,t2in,t3in,t4in)

def TcotCircPlot(t1,xlab1,ylab1,
                 dobatch,
                 t1in,t2in,t3in,t4in,
                 meanxl,meanyl,dcirc,
                 meanxtdo,meanytdo,
                 xlint,ylint,
                 ticsx,ticsy,
                 xl1,xl2,yl1,yl2):

    #from pylab import axhline,axvline,title,xlabel,ylabel,plot,scatter,cos
    if(doplot):
        from pylab import *
        from matplotlib.patches import Rectangle

    an = linspace(0,2*pi,100)

    #pppppppppppppppppppp
    #
    # x,y axis properties
    #
    axhline(0,color='b',linewidth=1.25)
    axvline(0,color='b',linewidth=1.25)

    #ppppppppppppppppppppp
    #
    # top title
    #
    title(t1)

    #ppppppppppppppppppppp
    #
    # x,y labels
    #
    xlabel(xlab1)
    ylabel(ylab1)
    #ppppppppppppppppppppp
    #
    # tcot
    #
    plot( dcirc*cos(an) + meanxl, dcirc*sin(an) + meanyl , '-gr', linewidth=3)

    #ppppppppppppppppppppp
    #
    # line from origin to mean x,y
    #
    x02mean=[0.0,meanxl]
    y02mean=[0.0,meanyl]
    plot (x02mean, y02mean, '-gg', linewidth=4)

    
    #ppppppppppppppppppppp
    #
    # axis ticks
    #
    xticks(ticsx)
    yticks(ticsy)

    #ppppppppppppppppppppp
    #
    # FINALLY  set the limits of the plot
    #


    #ppppppppppppppppppppp
    #
    # inplot text
    #
    print xlint
    #t1in="TDO BG gain: %3.0f  ALLTDO gain: %3.0f"%(meanxtdo,meanxl)
    #t2in="TDO OB gain: % 3.0f  ALLTDO gain: %3.0f"%(meanytdo,meanyl)

    dyall=yl2-yl1
    dxall=xl2-xl1

    dxtxt=0.0
    dytxt=dyall*0.05

    dybox=dytxt*1.45
    dxbox=dxall*0.48

    #
    # left text box
    #
    
    x1off=dxall*0.015
    y1off=dytxt*1.15
    
    x1tin=xl1+x1off
    y1tin=yl2-y1off

    x2tin=x1tin
    y2tin=y1tin-dytxt*0.65

    x1box=x1tin-dxbox*0.005
    y1box=y2tin-0.05*dytxt


    # 
    # right text box
    #

    x3off=dxall*0.51
    y3off=dytxt*1.15
    
    x3tin=xl1+x3off
    y3tin=yl2-y3off

    x4tin=x3tin
    y4tin=y3tin-dytxt*0.65

    x3box=x3tin-dxbox*0.005
    y3box=y4tin-0.05*dytxt


    #ppppppppppppppppppppp
    #
    # draw filled rectangle
    #

    text(x1tin,y1tin,t1in,size=11)
    text(x2tin,y2tin,t2in,size=10)

    if(t3in != None):
        text(x3tin,y3tin,t3in,size=11)
        text(x4tin,y4tin,t4in,size=10)

    ax=gca()

    pbox1=Rectangle( (x1box,y1box), dxbox, dybox, fill=True)
    pbox1.set_fc('y')
    pbox1.set_ec('y')
    pbox1.set_alpha(1.0)
    ax.add_patch(pbox1)

    pbox3=Rectangle( (x3box,y3box), dxbox, dybox, fill=True)
    pbox3.set_fc('salmon')
    pbox3.set_ec('salmon')
    pbox3.set_alpha(1.0)
    ax.add_patch(pbox3)

    print 'tttttttttttt ',xl1,yl1,x1tin,y1tin,x2tin,y2tin
    print 'adsfasdf ',xl1,xl2,yl1,yl2

        
    xlim(xl1,xl2)
    ylim(yl1,yl2)




#tttttttttttttttttttttttttttttttttt
#
#  circle of trust by tdos
#
def DfePlotTcotByTdo(itdos,uniqtdos,tdoopt,
                     bchk,tccenter,
                     baidopt,aaidopt,taidopt,
                     tdocolor,Color2Hex,
                     stmid,year,tcbasin,
                     pfetype,pfemode,pfefocus,
                     dcirc,
                     maxall,meanxl,meanyl,
                     pltdir,dobatch,
                     x2,y2,fecs,nxe,
                     doprinter):


    if(doplot):
        from pylab import *

    #
    # clear frame from histgram calc for tcot
    #
    clf()
    
    tdoxe1c={}
    tdoye1c={}

    n=0
    while(n<nxe):

        ctdo=itdos[n]
        x=x2[n]
        y=y2[n]

        try:
            tdoxe1c[ctdo].append(x)
        except:
            tdoxe1c[ctdo]=[x]

        try:
            tdoye1c[ctdo].append(y)
        except:
            tdoye1c[ctdo]=[y]

        n=n+1

    #mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
    #
    #  mean fes
    # 

    meanan=0.0
    meanob=0.0
    meanbg=0.0
    
    for n in range(0,nxe):
        meanan=meanan+fecs[n][0]
        meanob=meanob+fecs[n][2]
        meanbg=meanbg+fecs[n][1]

    meanan=meanan/nxe
    meanob=meanob/nxe
    meanbg=meanbg/nxe

    if(pfemode == 'fe'):
        xl1=-500
        xl2=500
        xlint=100
        xl1=-300
        xl2=300
        xlint=50
        if(pfefocus):
            xl1=-75
            xl2=75
            xl1=-100
            xl2=100
            xlint=25


    elif(pfemode == 'pacom'):
        xl1=-300
        xl2=300
        xlint=50

    yl1=xl1
    yl2=xl2
    ylint=xlint


    doAxisScale=0
    if(not(doAxisScale) and not(pfefocus)):
        xlint=100
        ylint=xlint
        xl2=yl2=(int(maxall/xlint)+1)*xlint
        xl1=yl1=-xl2

    ticsx = arange(xl1+xlint,xl2+1,xlint)     
    ticsy = arange(yl1,yl2+1,ylint)     

    if(tdoopt != None):
        uniqtdos=[tdoopt.upper()]

    nn=0
    meanxtdo=0.0
    meanytdo=0.0

    for tdo in uniqtdos:
        pxe1c=tdoxe1c[tdo]
        pye1c=tdoye1c[tdo]

        npx=len(pxe1c)
        nn=nn+npx

        if(npx == 0):
            print 'EEEEEEEEEE no points to plot!'
            sys.exit()

        for n in range(0,npx):
            meanxtdo=meanxtdo+pxe1c[n]
            meanytdo=meanytdo+pye1c[n]

        ctdo=tdocolor[tdo]
        chtdo=Color2Hex[ctdo]
        scatter(pxe1c,pye1c,s=50,c=chtdo,alpha=0.70)


    meanxtdo=meanxtdo/nn
    meanytdo=meanytdo/nn

    nxe=nn

    (t1,xlab1,ylab1,
     t1in,t2in,t3in,t4in)=tcotTopTitle(pfemode,bchk,nxe,
                                       tccenter,tcbasin,tdoopt,
                                       aaidopt,taidopt,baidopt,
                                       stmid,year,
                                       meanxtdo,meanytdo,
                                       meanxl,meanyl,
                                       meanan,meanob,meanbg,
                                       dcirc)


    TcotCircPlot(t1,xlab1,ylab1,
                 dobatch,
                 t1in,t2in,t3in,t4in,
                 meanxl,meanyl,dcirc,
                 meanxtdo,meanytdo,
                 xlint,ylint,
                 ticsx,ticsy,
                 xl1,xl2,yl1,yl2)


    
    if(bchk != None):
        if(tdoopt != None):
            ohead="%s.%s.%s.%s.%s.%s.%s"%(aaidopt.lower(),tdoopt.lower(),taidopt,tcbasin,year,pfemode,pfetype)
        else:
            ohead="%s.%s.%s.%s.%s.%s"%(aaidopt.lower(),taidopt,tcbasin,year,pfemode,pfetype)
    else:
        ohead="%s.%s.%s.%s.%s.%s.%s"%(aaidopt.lower(),taidopt,stmid,tcbasin,year,pfemode,pfetype)

    if(pfefocus):
        ohead="%s.center"%(ohead)

    psfile="%s.ps"%(ohead)
    pngfile="%s.png"%(ohead)
    giffile="%s.gif"%(ohead)
    pspath="%s/%s"%(pltdir,psfile)
    pngpath="%s/%s"%(pltdir,pngfile)
    
    pngfilemask="%s.*.png"%(ohead)
    pngpaths=[]
    
    #ppppppppppppppppppppp
    #
    # output to file(s)
    #
    print 'pspath:  ',pspath
    print 'pngpath: ',pngpath

    pngpaths.append(pngpath)
    
    savefig(pspath,orientation='landscape')
    savefig(pngpath,orientation='landscape')

    if(doprinter):
        cmd="lp -dtekcol %s"%(pspath)
        mf.runcmd(cmd,ropt)

    dogifloop=0
    if(dogifloop):
        
        gifloopfile="%s.loop.gif"%(ohead)



        #ppppppppppppppppppppp
        #
        # scatter plot
        #

        np=1
        for tdo in uniqtdos:

            #
            # clear frame from histgram calc for tcot
            #
            clf()

            pxe1c=tdoxe1c[tdo]
            pye1c=tdoye1c[tdo]

            npx=len(pxe1c)
            nn=nn+npx

            if(npx == 0):
                print 'EEEEEEEEEE no points to plot!'
                sys.exit()

            ctdo=tdocolor[tdo]
            chtdo=Color2Hex[ctdo]
            scatter(pxe1c,pye1c,s=50,c=chtdo,alpha=0.70)


            TcotCircPlot(t1,xlab1,ylab1,
                         dobatch,
                         t1in,t2in,t3in,t4in,
                         meanxl,meanyl,dcirc,
                         meanxtdo,meanytdo,
                         xlint,ylint,
                         ticsx,ticsy,
                         xl1,xl2,yl1,yl2)


            pngfile="%s.%s.%02d.png"%(ohead,tdo,np)
            pspath="%s/%s"%(pltdir,psfile)
            pngpath="%s/%s"%(pltdir,pngfile)
            print 'pngpath: ',pngpath
            pngpaths.append(pngpath)
            savefig(pngpath,orientation='landscape')

            np=np+1
            print 'nnnnnnnn ',np,pxe1c


    rc=(pngfilemask,pngpaths)
    




#eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
#
#  circle of trust by dtgs
#
def DfePlotTcotByDtg(
    xecs,yecs,fecs,tdocs,bdtgcs,
    bchk,tccenter,tdoopt,
    aaidopt,taidopt,baidopt,
    stmid,year,tcbasin,
    pfetype,pfemode,pfefocus,
    dcirc,
    maxall,meanxl,meanyl,
    pltdir,dobatch,doxv,ropt,
    ):

    if(doplot):
        from pylab import *

    (tdocolor,Color2Hex)=TCtdos.TdoColors()

    if(pfemode == 'fe'):
        xl1=-500
        xl2=500
        xlint=100
        xl1=-300
        xl2=300
        xlint=50
        if(pfefocus):
            xl1=-75
            xl2=75
            xl1=-125
            xl2=125
            xlint=25


    elif(pfemode == 'pacom'):
        xl1=-300
        xl2=300
        xlint=50

    yl1=xl1
    yl2=xl2
    ylint=xlint


    doAxisScale=0
    if(doAxisScale and not(pfefocus)):
        xlint=100
        ylint=xlint
        xl2=yl2=(int(maxall/xlint)+1)*xlint
        xl1=yl1=-xl2

    ticsx = arange(xl1+xlint,xl2+1,xlint)     
    ticsy = arange(yl1,yl2+1,ylint)     

    nxe=len(xecs)



    #mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
    #
    #  mean fes
    # 

    meanan=0.0
    meanob=0.0
    meanbg=0.0
    
    for n in range(0,nxe):
        meanan=meanan+fecs[n][0]
        meanob=meanob+fecs[n][2]
        meanbg=meanbg+fecs[n][1]

    meanan=meanan/nxe
    meanob=meanob/nxe
    meanbg=meanbg/nxe


    #tttttttttttttttttttttttttttttttttttttttt
    #
    # titles/text
    #


    (t1,xlab1,ylab1,
     t1in,t2in,t3in,t4in)=tcotTopTitle(pfemode,bchk,nxe,
                                       tccenter,tcbasin,tdoopt,
                                       aaidopt,taidopt,baidopt,
                                       stmid,year,
                                       meanxl,meanyl,
                                       meanxl,meanyl,
                                       meanan,meanob,meanbg,
                                       dcirc)

    if(bchk != None):
        if(tdoopt != None):
            ohead="%s.%s.%s.%s.%s.%s.%s"%(aaidopt.lower(),tdoopt.lower(),taidopt,tcbasin,year,pfemode,pfetype)
        else:
            ohead="%s.%s.%s.%s.%s.%s"%(aaidopt.lower(),taidopt,tcbasin,year,pfemode,pfetype)
    else:
        ohead="%s.%s.%s.%s.%s.%s.%s"%(aaidopt.lower(),taidopt,stmid,tcbasin,year,pfemode,pfetype)

    if(pfefocus):
        ohead="%s.center"%(ohead)



    #---------------------------------------
    # 
    #  paths
    #

    pngpaths=[]
    pngloopdelay=[]

    psfile="%s.ps"%(ohead)
    pngfile="%s.png"%(ohead)
    giffile="%s.gif"%(ohead)
    giffileloop="%s.loop.gif"%(ohead)
    pspath="%s/%s"%(pltdir,psfile)
    pngpath="%s/%s"%(pltdir,pngfile)
    pngfilemask="%s.*.png"%(ohead)

    #llllllllllllllllllllllllllllllllllllll
    #
    # set loop delay by distance outside the circle
    #

    loopinside=50
    loopoutside=150
    idcirc=mf.nint(dcirc)
    for n in range(0,nxe):
        (ir,id,quad)=XeYe2Rquad(xecs[n],yecs[n])

        if(ir > idcirc):
            dout=(float(ir-idcirc)/dcirc)
            pngloopdelay.append(int((dout+1.0)*loopoutside))
        else:
            dout=0.0
            pngloopdelay.append(loopinside)
            


    #ppppppppppppppppppppp
    #
    # scatter plot
    #
    
    for np in range(0,nxe):

        #
        # -- clear from histogram calc..
        #
        clf()

        for n in range(0,np+1):

            pxe1c=[]
            pye1c=[]
            pxe1c.append(xecs[n])
            pye1c.append(yecs[n])
        
            tdo=tdocs[n]
            ctdo=tdocolor[tdo]
            chtdo=Color2Hex[ctdo]
            bdtgc=bdtgcs[n]

            sscat=80
            scatter(pxe1c,pye1c,s=sscat,c=chtdo,faceted=False,edgecolor='#51588E',alpha=0.60)

        if(np > 0):

            for n in range(1,np+1):
            
                x0c=xecs[n-1]
                x1c=xecs[n]
                y0c=yecs[n-1]
                y1c=yecs[n]
                xline=[x0c,x1c]
                yline=[y0c,y1c]
                cline='-gg'
                wline=1
                if(x1c < 0):
                    cline='-gr'
                    wline=2
                    
                plot(xline,yline,cline,linewidth=1)
            


        t1in="%s :: %s"%(bdtgc,tdo)
        t2in="FE AN:%s %3.0f  OB:%s %3.0f  BG:%s %3.0f"%(
            aaidopt,fecs[n][0],
            taidopt,fecs[n][2],
            baidopt,fecs[n][1],
            )
        
        xlim(xl1,xl2)
        ylim(yl1,yl2)

        TcotCircPlot(t1,xlab1,ylab1,
                     dobatch,
                     t1in,t2in,t3in,t4in,
                     meanxl,meanyl,dcirc,
                     meanxl,meanyl,
                     xlint,ylint,
                     ticsx,ticsy,
                     xl1,xl2,yl1,yl2)


        pngfile="%s.%s.%s.%02d.png"%(ohead,bdtgc,tdo,np)
        pspath="%s/%s"%(pltdir,psfile)
        pngpath="%s/%s"%(pltdir,pngfile)
        

        print 'pngpath: ',pngpath
        savefig(pngpath,orientation='landscape')

        pngpaths.append(pngpath)

        #cmd="xv %s"%(pngpath)
        #mf.runcmd(cmd,'')
        #sys.exit()

        np=np+1
        print 'nnnnnnnn ',np,pxe1c

    if(doxv):
        cmd="xv %s/%s"%(pltdir,pngfilemask)
        mf.runcmd(cmd)

    dogifloop=1
    if(dogifloop):

        convertexe='convert'
        looppath="%s/%s"%(pltdir,giffileloop)
        
        npngs=len(pngpaths)

        for n in range(0,npngs):

            if(n == 0):
                cmd="%s -loop 0 -delay %s %s "%(convertexe,pngloopdelay[n],pngpaths[n])
            elif(n == npngs-1):
                cmd="%s -delay %s %s"%(cmd,pngloopdelay[n],pngpaths[n])
            else:
                cmd="%s -delay %s %s"%(cmd,pngloopdelay[n],pngpaths[n])

        cmd="%s %s"%(cmd,looppath)
        mf.runcmd(cmd,ropt)

        print 'llllllllllllllllllllll ',looppath


    sys.exit()    

    #ppppppppppppppppppppp
    #
    # output to file(s)
    #
    print 'pspath:  ',pspath
    print 'pngpath: ',pngpath

    savefig(pspath,orientation='landscape')
    savefig(pngpath,orientation='landscape')

    if(doprinter):
        cmd="lp -dtekcol %s"%(pspath)
        mf.runcmd(cmd,ropt)




