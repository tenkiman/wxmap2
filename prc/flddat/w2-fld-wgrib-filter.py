#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from M2 import *
from FM import FimRunModel2


#llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
#
# local
#


def MakeFdb2(datpath,fdbpath,ropt=''):

    F=open(fdbpath,'w')
    F.writelines(datpath+'\n')
    F.close()

    if(os.path.exists(datpath)):
        cmd="wgrib2 -v2 %s >> %s"%(datpath,fdbpath)
        mf.runcmd(cmd,ropt)
    else:
        print 'WWW no data for fdb2 datpath: ',datpath
    


def GetFdb(fdbpath):
    F=open(fdbpath)
    cards=F.readlines()
    F.close()
    return(cards)



def LevCode2Lev2(lc1,lv1,lc2,lv2):
    levc=None
    if(lc1== 100):
        ld='mb'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 1):
        ld='surface'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 4):
        ld='OC istotherm'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 6):
        ld='max wind'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 7):
        ld='tropopause'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 8):
        ld='top of atmosphere'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 10):
        ld='entire atmosphere'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 101):
        ld='mean sea level'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 102):
        ld='m above mean sea level'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 103):
        ld='m above ground'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 104):
        ld='sigma layer'
        lv=lv1
        levc="%d.%g-%g"%(lc1,lv1,lv2)
    elif(lc1== 106):
        ld='m below ground (layer)'
        lv=lv1
        levc="%d.%d-%-d"%(lc1,int(lv1*0.01),int(lv2*0.01))
    elif(lc1== 108 and lc2 == 108):
        ld='mb layer above ground (layer)'
        lv=lv1
        levc="%d.%d-%-d"%(lc1,int(lv1*0.01),int(lv2*0.01))
    elif(lc1== 109):
        ld='reserved'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 244):
        ld='depth of atmos'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 234):
        ld='high cloud layer'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 224):
        ld='mid cloud layer'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 214):
        ld='low cloud layer'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(lc1== 211):
        ld='total cloud layer'
        lv=lv1
        levc="%d.%g"%(lc1,lv1)
    elif(
        lc1 == 242 or lc1 == 243 or
        lc1 == 232 or lc1 == 233 or
        lc1 == 222 or lc1 == 223 or
        lc1 == 212 or lc1 == 213 or
        lc1 == 200 or
        lc1 == 204
        ):
        ld='NCEP level type %d'%(lc1)
        lv=float(lc1)
        levc="%d.%g"%(lc1,lv1)
    elif(
        lc1 == 220
        ):
        ld='NCEP PBL height %d'%(lc1)
        lv=float(lc1)
        levc="%d.%g"%(lc1,lv1)
    else:
        ld=None
        lv=None
        print 'WWW(LevCode2Lev2.grib2) not defined lc1: ',lc1,lv1,lc2,lv2
        
    return(lv,ld,levc)


def ParseFdb2(cards,verb=0):


    def splitlevcodes(lvl):
        tt=lvl.split('=')
        lll=tt[1].split(',')
        lc=int(lll[0][1:])
        ll2=lll[1][:-1]
        if(lc == 255 or lc == 109 or lc == 104 or lc == 106  or lc == 108):
            if(ll2 == 'missing'):
                ll=-999.
            else:
                ll=float(ll2)
        elif(lc == 100):
            ll=float(ll2)*0.01
        #
        # new parameter from ncep for gfs when lc=103 changes on 2009121512
        #
        elif(lc == 103):
            if(ll2 == 'missing'):
                ll=-999.
            else:
                ll=float(ll2)
        elif(lc == 255):
            ll=-999.
        else:
            ll=float(ll2)
        return(lc,ll)
        
        
    ncards=len(cards)

    recsiz={}
    records={}

    #
    # the first card has the data path
    #

    nrec=0
    nc=1
    for nr in range(nc,ncards):

        card=cards[nr]
        tt=card.split(':')

        recnum=tt[0]
        sizrecp1=int(tt[1])

##        ['1', '0', '00Z07jun2007', 'HGT Geopotential Height [gpm]', 'lvl1=(100,100000) lvl2=(255,0)', '1000 mb', 'anl', '\n']

        var=tt[3].split()[0]
        vardesc=''
        for vt in tt[3].split()[1:]:
            vardesc="%s %s"%(vardesc,vt)
        vardesc=vardesc.lstrip()

        tt4=tt[4].split()
        if(len(tt4) == 4):
            lvl1=tt4[2]
            lvl2=tt4[3]
        else:
            lvl1=tt4[0]
            lvl2=tt4[1]

        (levcode1,lev1)=splitlevcodes(lvl1)
        (levcode2,lev2)=splitlevcodes(lvl2)

        (lev,levd,levc)=LevCode2Lev2(levcode1,lev1,levcode2,lev2)

        levdesc=tt[5]
        levdesc=levd
        timedesc=tt[6]

        rec=(
            recnum,
            sizrecp1,
            var,
            vardesc,
            lev,
            levc,
            levcode1,
            lev1,
            levcode2,
            lev2,
            levdesc,
            timedesc,
            )

        #print ' ',nrec,recnum,var,vardesc,levcode1,lev1,levcode2,lev2,levdesc,levc
        
        records[nrec]=rec
        recsiz[nrec]=sizrecp1
        nrec=nrec+1

    nrectot=ncards

    return(records,recsiz,nrectot)

def SetFieldRequest2(tau,model,spec='test0'):

    request={}

    if(spec == 'test0'):

        plevs=[1000,925,850,700,500,300,250,200,150,100]
        wapplevs=[850,700,500]

        #
        # sfc + ua versions
        #
        request['ugrd']=['103.10']
        request['vgrd']=['103.10']
        request['tmp']=['103.2']
        
        for plev in plevs:
            request['ugrd']=request['ugrd']+ ['100.%d'%(plev)]
            request['vgrd']=request['vgrd']+ ['100.%d'%(plev)]
            request['tmp']=request['tmp']+ ['100.%d'%(plev)]
        
        #
        # just ua
        #
        request['hgt']=[]
        request['rh']=[]
        
        for plev in plevs:
            request['hgt']=request['hgt']+ ['100.%d'%(plev)]
            request['rh']=request['rh']+ ['100.%d'%(plev)]
    
        request['vvel']=[]
        for wapplev in wapplevs:
            request['vvel']=request['vvel']+ ['100.%d'%(wapplev)]

        request['prmsl']=['101.0']
        request['apcp']=['1.0']
        request['acpcp']=['1.0']
        request['cprat']=['1.0']
        request['prate']=['1.0']

        request['ulwrf']=['8.0']
        request['tcdc']=['211.0','214.0','224.0','234.0','244.0']

        request['tmax']=['103.2']
        request['tmin']=['103.2']

        request['pwat']=['200.0']
        
    elif(spec == 'tctrk' or spec == 'w2flds'):

        if(spec == 'tctrk'):
            uvplevs=[850,700,500,200]
            zplevs=[1000,850,700,500,200]
            tplevs=[300]
            rhplevs=[]

        elif(spec == 'w2flds'):
            mplevs=[1000,925,850,700,500,400,300,250,200,150,100]
            uvplevs=mplevs
            zplevs=mplevs
            tplevs=mplevs
            rhplevs=mplevs
            
        
        # sfc + ua versions
        #
        request['ugrd']=['103.10']
        request['vgrd']=['103.10']

        request['tmax']=['103.2']
        request['tmin']=['103.2']
        
        request['hgt']=[]
        request['tmp']=['103.2']
        request['rh']=[]
        
        
        for plev in uvplevs:
            request['ugrd']=request['ugrd']+ ['100.%d'%(plev)]
            request['vgrd']=request['vgrd']+ ['100.%d'%(plev)]
        
        for plev in zplevs:
            request['hgt']=request['hgt']+ ['100.%d'%(plev)]

        for plev in tplevs:
            request['tmp']=request['tmp']+ ['100.%d'%(plev)]

        if(len(rhplevs) > 0):
            for plev in rhplevs:
                request['rh']=request['rh']+ ['100.%d'%(plev)]


        request['ugrd']=request['ugrd']+ ['1.0']
        request['vgrd']=request['vgrd']+ ['1.0']
        request['tmax']=request['tmax']+['1.0']
        request['tmin']=request['tmin']+['1.0']
        request['tmp']=request['tmp']+['1.0']
        # -- 20180717 -- latest UPP from ncep only outputs MSLET - slp using eta reduction
        #
        if(model == 'fv3e' or model == 'fv3g' or model == 'fv7e' or model == 'fv7g'):
            request['mslet']=['101.0']
            request['mslet']=request['mslet']+['3.192']
        else:
            request['prmsl']=['101.0']
            request['prmsl']=request['prmsl']+['1.0']
            
        request['prate']=['1.0']
        request['cprat']=['1.0']
        request['pwat']=['200.0']
        request['apcp']=['1.0']
        request['acpcp']=['1.0']
        


    else:
        
        request['ugrd']=[10,850,500,200]
        request['vgrd']=request['ugrd']
    
        request['tmp']=[850,500,200]
        request['rh']=request['tmp']
        request['hgt']=request['tmp']
    
        request['prmsl']=[0]
        request['apcp']=[0]
        request['acpcp']=[0]
        request['cprat']=[0]
        request['prate']=[0]
    
    request['taus']=[tau]

    return(request)


def Wgrib2VarFilter(records,request,tau,verb=0):

    nr=len(records)

    rtaus=request['taus']
    rtaus.sort()
    rvars=request.keys()
    rvars.sort()

   
    orecs=[]

    nrecs=records.keys()
    nrecs.sort()
    
    for nrec in nrecs:
        

        (
            recnum,
            sizrecp1,
            var,
            vardesc,
            lev,
            levc,
            levcode1,
            lev1,
            levcode2,
            lev2,
            levdesc,
            timedesc,
            )=records[nrec]
    

        var=var.lower()


        for rvar in rvars:
            if(var == rvar):
                rlevs=request[rvar]
                for rlev in rlevs:
                    if(levc == rlev):
                        for rtau in rtaus:
                            if(rtau == tau):
                                if(verb): print 'MMMMMMMMMMMMM(Wgrib2VarFilter): ',	var,lev,tau,nrec,sizrecp1
                                ocard="%s:%d"%(recnum,sizrecp1)
                                ocard=ocard+'\n'
                                orecs.append(ocard)


    return(orecs)


def Wgrib2VarAnal(records,tau):

    nr=len(records)

    vars=[]
    taus=[]
    levs=[]
    levds={}
    
    vardescs={}
    varlevs={}
    varcodes={}

    for n in range(0,nr):
        
        (
            recnum,
            sizrecp1,
            var,
            vardesc,
            lev,
            levc,
            levcode1,
            lev1,
            levcode2,
            lev2,
            levdesc,
            timedesc,
            )=records[n]
    

        var=var.lower()
        vars.append(var)
        taus.append(tau)
        levs.append(levc)
        
        try:
            varlevs[levc,tau].append(var)
        except:
            varlevs[levc,tau]=[var]

        try:
            vardescs[var,tau].append(vardesc)
        except:
            vardescs[var,tau]=[vardesc]

        levds[levc]=levdesc

        try:
            varcodes[var].append(var)
        except:
            varcodes[var]=[var]

    vars=mf.uniq(vars)
    taus=mf.uniq(taus)
    levs=mf.uniq(levs)
    levs.sort()

    levsnp=[]
    levsp=[]

    for lev in levs:
        lc=lev.split('.')[0]
        if(lc == '100'):
            lv=lev.split('.')[1]
            levsp.append(int(lv))
        else:
            levsnp.append(lev)


    levsnp.sort()
    
    levs=[]
    for ll in levsnp:
        levs.append(ll)

    levsp.sort()
    for ll in levsp:
        levs.append("100.%d"%(ll))
                    

    print
    print "Var Inventory by Lev for Tau: ",tau
    print
    for tau in taus:
        for lev in levs:
            vcard="%-15s "%(lev)
            try:
                lvars=varlevs[lev,tau]
                lvars.sort()
                nlvars=len(lvars)
                for nlvar in range(0,nlvars):
                    lvar=lvars[nlvar]
                    vcard="%s %-6s"%(vcard,lvar)
                    if(nlvar > 0 and nlvar%12 == 0):
                        vcard=vcard+'\n '+15*' '
            except:
                vcard=vcard

            if(nlvars > 12):    print 
            print vcard
            if(nlvars > 12):    print 

        print
        print "Var desc:"
        print
        vars.sort()
        for var in vars:
            vv=vardescs[var,tau]
            vv=mf.uniq(vv)
            vc=varcodes[var]
            print "%-6s %6s  %s"%(var,vc[0],vv[0][:-1])


        print
        print "Lev desc:"
        print
        for lev in levs:
            print "%-15s  %s"%(lev,levds[lev])


def Wgrib2Filter(orecs,inpath,outpath,override=0):

    if(os.path.exists(outpath) and override == 0):
        return

    if(not(os.path.exists(inpath))):
        print 'WWW wgrib2filter inpath: ',inpath,' does not exist, returning'
        return
    
    wcmd="wgrib2 -i %s -grib %s"%(inpath,outpath)
    print wcmd

    w=os.popen(wcmd,'w')
    w.writelines(orecs)
    w.close()
    
def IsGrib1(gribtype):
    rc=0
    if(gribtype == 'grb1'):
        rc=1
    return(rc)

def IsGrib2(gribtype):
    rc=0
    if(gribtype == 'grb2'):
        rc=1
    return(rc)

def MakeFdb1(datpath,fdbpath,ropt=''):

    F=open(fdbpath,'w')
    F.writelines(datpath+'\n')
    F.close()

    cmd="wgrib -V %s >> %s"%(datpath,fdbpath)
    mf.runcmd(cmd,ropt)
    

def ParseFdb1(cards,verb=0,doFullPrint=0):

    ncards=len(cards)

    recsiz={}
    records={}
    nrectot=0


    #
    # the first card has the data path
    #

    nc=1
    nrc=0
    while (nc < ncards):

        card=cards[nc]
        lcard=len(card)
        rcards=[]

        if(card[0:3] == 'rec'):

            while(lcard > 1):
                lcard=len(cards[nc])
                if(lcard > 1):
                    rcards.append(cards[nc])
                nc=nc+1

            #
            # initialize
            #
            nxny=0
            blat=blon=elat=elon=dlat=dlon=-999.9

            for n in range(0,len(rcards)):
                rcard=rcards[n]
                type=rcard.split()[0]
                if(type == 'rec'):
                    if(verb): print 'CCC ',n,rcard[:-1]
                    tt=rcard.split()

                    #    0         1                2            3       4
                    #['rec', '5:5513228:date', '2006091800', 'UGRD', 'kpds5=33',
                    #    5            6               7               8        9     10    11        12 
                    # 'kpds6=100', 'kpds7=850', 'levels=(3,82)', 'grid=255', '850', 'mb', 'anl:', 'bitmap:',
                    #    13       14
                    # '344664', 'undef']

                    ttt=tt[1].split(':')
                    nrec=int(ttt[0])
                    sizrecp1=int(ttt[1])

                    var=tt[3]
                    varcode=tt[4].split('=')[1]
                    levcode=tt[5].split('=')[1]
                    lev=tt[6].split('=')[1]
                    lev=int(lev)
                    levcode2=tt[7].split('=')[1]

                    nbitmap=0
                    nre=len(tt)


                    if(nre >=14):
                        if(tt[nre-3] == 'bitmap:'):
                            nbitmap=int(tt[nre-2])
                            timecode=tt[nre-4].split(':')[0]
                            timedesc=tt[nre-5]
                        else:
                            timecode=tt[nre-1].split(':')[0]
                            timedesc=tt[nre-2]

                    else:
                        timecode=tt[nre-1].split(':')[0]
                        timedesc=tt[nre-2]


                    nb=0
                    for n in range(0,nre):
                        if(mf.find(tt[n],'grid=')):
                            nb=n
                            gridcode=tt[nb].split('=')[1]
                            break

                    ne=0
                    for n in range(nb,nre):
                        if(mf.find(tt[n],':')):
                            ne=n
                            break

                    if(timecode != 'anl'):
                        ne=ne-1
                    else:
                        timedesc=0

                    levdesc=''
                    for n in range(nb+1,ne):
                        levdesc=levdesc+' '+tt[n]

                    if(timecode == 'anl'):
                        time=0

                elif(mf.find(type,'=')):
                    if(verb): print 'CCC ',n,rcard[:-1]
                    tt=rcard.split('=')
                    vardesc=tt[1]

                elif(mf.find(type,'timerange')):
                    if(verb): print 'CCC ',n,rcard[:-1]
                    tt=rcard.split()
                    timerangeind=int(tt[1])
                    timerangep1=int(tt[3])
                    timerangep2=int(tt[5])
                    timeunits=int(tt[7])
                    nx=int(tt[9])
                    ny=int(tt[11])
                    gridnum=int(tt[14])

                elif(mf.find(type,'center')):
                    if(verb): print 'CCC ',n,rcard[:-1]
                    tt=rcard.split()
                    centernum=int(tt[1])
                    subcenternum=int(tt[3])
                    processnum=int(tt[5])
                    gribtablenum=int(tt[7])


                elif(mf.find(type,'latlon')):
                    if(verb): print 'CCC ',n,rcard[:-1]
                    tt=rcard.split()
                    blat=float(tt[2])
                    elat=float(tt[4])
                    dlat=float(tt[6])
                    nxny=int(tt[8])

                elif(mf.find(type,'long')):
                    if(verb): print 'CCC ',n,rcard[:-1]
                    tt=rcard.split()
                    blon=float(tt[1])
                    elon=float(tt[3])
                    dlon=float(tt[5].split(',')[0])

                elif(mf.find(type,'min/max')):
                    if(verb): print 'CCC ',n,rcard[:-1]
                    tt=rcard.split()
                    gridvalmin=float(tt[2])
                    gridvalmax=float(tt[3])
                    nbits=int(tt[6])
                    bdsref=float(tt[8])
                    decscale=int(tt[10])
                    binscale=int(tt[12])




            if(nxny == 0 and nx != 0 and ny != 0): nxny=nx*ny
            ndef=nxny-nbitmap
            nundef=nxny-ndef

            tau=GribTime2Tau(timerangeind,timerangep1,timerangep2,timeunits)

            rec=(
                sizrecp1,
                gridcode,
                nx,
                ny,
                nxny,
                ndef,
                nundef,
                blat,
                elat,
                dlat,
                blon,
                elon,
                dlon,
                timecode,
                timedesc,
                timerangeind,
                timerangep1,
                timerangep2,
                timeunits,
                tau,
                varcode,
                var,
                vardesc,
                levcode,
                lev,
                levcode2,
                levdesc,
                gridvalmin,
                gridvalmax,
                nbits,
                bdsref,
                decscale,
                binscale
                )

            records[nrec]=rec
            recsiz[nrec]=sizrecp1

            if(doFullPrint):
                PrintWgrib1Record(nrec,rec)

            nrectot=nrec

    return(records,recsiz,nrectot)

def GribTime2Tau(timerangeind,timerangep1,timerangep2,timeunits):
    #
    # instantaneous
    #
    if(timerangeind == 0 or timerangeind == 8):
        tau=timerangep1
        
    # -- analysis
    #
    elif(timerangeind == 1):
        tau=timerangep1
    #
    # average(?) - put tau at end of interval
    #
    elif(timerangeind == 2):
        tau=timerangep2
    #
    # accumulated - put tau at end of interval
    #
    elif(timerangeind == 4):
        tau=timerangep2
    #
    # average - put tau at end of interval
    #
    elif(timerangeind == 3):
        tau=timerangep2

    elif(timerangeind == 3):
        tau=timerangep2
    #
    # foreast time occupies both p1 and p2
    #
    elif(timerangeind == 10):
        tau=timerangep1*256+timerangep2
        
    # if not one of these return none
    #
    else:
        print 'EEE(time range indicator problem): ',timerangeind,' p1: ',timerangep1,' p2: ',timerangep2
        tau=None

    # -- special case -- non-standard or reserved -- ncep if timeunits == 11 then timeunits = 6hr 
    # -- normally timeunits=1 ==> hours
    #
    if(timeunits == 11): tau=tau*6


    return(tau)


def Wgrib1VarAnal(records):

    nr=len(records)

    vars=[]
    taus=[]
    levs=[]
    
    vardescs={}
    varlevs={}
    varcodes={}

    for n in range(1,nr+1):
        
        (
            sizrecp1,
            gridcode,
            nx,
            ny,
            nxny,
            ndef,
            nundef,
            blat,
            elat,
            dlat,
            blon,
            elon,
            dlon,
            timecode,
            timedesc,
            timerangeind,
            timerangep1,
            timerangep2,
            timeunits,
            tau,
            varcode,
            var,
            vardesc,
            levcode,
            lev,
            levcode2,
            levdesc,
            gridvalmin,
            gridvalmax,
            nbits,
            bdsref,
            decscale,
            binscale
            )=records[n]

        var=var.lower()
        vars.append(var)
        taus.append(tau)
        olev='%s.%s'%(levcode,lev)
        levs.append(olev)
        
        try:
            varlevs[olev,tau].append(var)
        except:
            varlevs[olev,tau]=[var]

        try:
            vardescs[var,tau].append(vardesc)
        except:
            vardescs[var,tau]=[vardesc]

        try:
            varcodes[var].append(varcode)
        except:
            varcodes[var]=[varcode]


    vars=mf.uniq(vars)
    taus=mf.uniq(taus)
    levs=mf.uniq(levs)
    levs.sort()

    for tau in taus:
        for lev in levs:
            vcard="%-8s "%(lev)
            try:
                lvars=varlevs[lev,tau]
                lvars.sort()
                for lvar in lvars:
                    vcard="%s %-6s"%(vcard,lvar)
            except:
                vcard=vcard

            print vcard

        print
        print "Var desc:"
        print
        vars.sort()
        for var in vars:
            vv=vardescs[var,tau]
            vv=mf.uniq(vv)
            vc=varcodes[var]
            print "%-6s  %3s  %s "%(var,vc[0],vv[0][:-1])




def SetFieldRequest1(tau,model,spec='test0'):

    request={}

    if(spec == 'test0'):
        pass
        
    elif(spec == 'tctrk' or spec == 'w2flds'):

        if(spec == 'tctrk'):
            uvplevs=[850,700,500,200]
            zplevs=[1000,850,700,500,200]
            tplevs=[300]
            hurplevs=[]

        elif(spec == 'w2flds'):
            mplevs=[1000,925,850,700,500,400,300,250,200,150,100]
            uvplevs=mplevs
            zplevs=mplevs
            tplevs=mplevs
            hurplevs=mplevs
            

        if(model == 'ecm2' or model == 'ecm4'):

            request['t']=[]
            request['gh']=[]
            request['u']=[]
            request['v']=[]
            if(len(hurplevs) > 0):
                request['r']=[]

            for plev in uvplevs:
                request['u']=request['u']+['100.%d'%(plev)]
                request['v']=request['v']+['100.%d'%(plev)]

            for plev in zplevs:
                request['gh']=request['gh']+['100.%d'%(plev)]

            for plev in tplevs:
                request['t']=request['t']+['100.%d'%(plev)]

            if(len(hurplevs) > 0):
                for plev in hurplevs:
                    request['r']=request['r']+['100.%d'%(plev)]
                
            request['10u']=['1.0']
            request['10v']=['1.0']
            request['msl']=['1.0']
            request['tp']=['1.0']
            request['cp']=['1.0']
            request['lsp']=['1.0']
            request['sstk']=['1.0']
            request['ci']=['1.0']
            request['2t']=['1.0']
            request['mx2t']=['1.0']
            request['mn2t']=['1.0']

        elif(model == 'fim8'):
            
            request['ua']=['109.1']
            # -- since 201111, outputing real 10 m wind
            request['ua']=['105.10']
            request['va']=request['ua']

            request['ta']=[]
            request['zg']=[]
            request['hur']=[]

            for plev in uvplevs:
                request['ua']=request['ua']+['100.%d'%(plev)]
                request['va']=request['va']+['100.%d'%(plev)]

            for plev in zplevs:
                request['zg']=request['zg']+['100.%d'%(plev)]

            for plev in tplevs:
                request['ta']=request['ta']+['100.%d'%(plev)]

            if(len(hurplevs) > 0):
                for plev in hurplevs:
                    request['hur']=request['hur']+['100.%d'%(plev)]

            #
            # fim8 psl
            #

            request['psl']=['102.1']
            request['pr']=['1.1']
            request['prc']=['1.1']
            request['prw']=['1.1']
            request['hfls']=['1.1']
            request['hfss']=['1.1']
            request['ustar']=['1.1']

        # -- run mpas on zeus
        #
        elif(model == 'mpas'):
            
#dset ^mpas.2014013012.f%f3.grb1
#index ^mpas.2014013012.gmp1
#undef 9.999E+20
#title /scratch1/portfolios/BMC/fim/fiorino/w21/dat/nwp2/esrl/mpas/2013110400/mpas.2013110400.f024.grb1.grb
#*  produced by grib2ctl v0.9.12.5p16
#dtype grib 255
#options template
#ydef 361 linear  -90.0 0.5
#xdef 720 linear -180.0 0.5
#tdef 33 linear 12Z30Jan2014 6hr
#zdef 14 levels
#1000 925 850 700 600 500 400 300 200 150 100 50 25 20 
#vars 13
#prc  0  63,  1,  0  ** Convective precipitation [kg/m^2]
#zg  14   7,100,  0 ** Geopotential height [gpm]
#prl  0  62,  1,  0  ** Large scale precipitation [kg/m^2]
#rss  0 111,  1,  0  ** Net short wave (surface) [W/m^2]
#rls  0 112,  1,  0  ** Net long wave (surface) [W/m^2]
#ps   0   1,  1,  0  ** Pressure [Pa]
#psl  0   2,102,  0  ** Pressure reduced to MSL [Pa]
#rh  14  52,100,  0 ** Relative humidity [%]
#ta  14  11,100,  0 ** Temp. [K]
#ua  14  33,100,  0 ** u wind [m/s]
#uas  0  33,105, 10 ** u wind [m/s]
#va  14  34,100,  0 ** v wind [m/s]
#vas  0  34,105, 10 ** v wind [m/s]

            
            request['ua']=['105.10']
            request['va']=request['ua']

            request['ta']=[]
            request['zg']=[]
            request['hur']=[]

            for plev in uvplevs:
                request['ua']=request['ua']+['100.%d'%(plev)]
                request['va']=request['va']+['100.%d'%(plev)]

            for plev in zplevs:
                request['zg']=request['zg']+['100.%d'%(plev)]

            for plev in tplevs:
                request['ta']=request['ta']+['100.%d'%(plev)]

            if(len(hurplevs) > 0):
                for plev in hurplevs:
                    request['hur']=request['hur']+['100.%d'%(plev)]


            request['psl']=['102.0']
            request['prl']=['1.0']
            request['prc']=['1.0']

        elif(model == 'gfsk'):
            
            request['ugrd']=['105.10']
            request['vgrd']=request['ugrd']

            request['tmp']=[]
            request['hgt']=[]
            request['rh']=[]

            for plev in uvplevs:
                request['ugrd']=request['ugrd']+['100.%d'%(plev)]
                request['vgrd']=request['vgrd']+['100.%d'%(plev)]

            for plev in zplevs:
                request['hgt']=request['hgt']+['100.%d'%(plev)]

            for plev in tplevs:
                request['tmp']=request['tmp']+['100.%d'%(plev)]

            if(len(hurplevs) > 0):
                for plev in hurplevs:
                    request['rh']=request['rh']+['100.%d'%(plev)]

            # gfs psl
            #
            request['prmsl']=['102.0']
            request['apcp']=['1.0']
            request['acpcp']=['1.0']
            request['pwat']=['200.0']

        elif(model == 'ukm2'):
            
            # -- 20120217 -- mod $GRIBTAB to use my standard for ukm2 (center# 77)
            #
            
            request['ua']=['1.0']
            request['va']=request['ua']
            request['ta']=['1.0']
            request['zg']=[]

            request['hur']=[]
            
            for plev in uvplevs:
                request['ua']=request['ua']+['100.%d'%(plev)]
                request['va']=request['va']+['100.%d'%(plev)]

            for plev in zplevs:
                request['zg']=request['zg']+['100.%d'%(plev)]

            for plev in tplevs:
                request['ta']=request['ta']+['100.%d'%(plev)]

            if(len(hurplevs) > 0):
                for plev in hurplevs:
                    request['hur']=request['hur']+['100.%d'%(plev)]

            # fim8 psl
            #
            request['psl']=['102.0']
            request['pr']=['1.0']
            request['prc']=['1.0']

        elif(model == 'cmc2'):

            if(model == 'ukm2'):
                request['ugrd']=['1.0']
                request['vgrd']=request['ugrd']
                request['tmp']=['1.0']
            #elif(model == 'cmc2'):
            #    request['ugrd']=['119.10000']
            #    request['vgrd']=request['ugrd']
            #    request['tmp']=['119.10000']
            elif(model == 'cmc2'):
                # 2012020812 changed coding of uas/vas; dropped tas
                request['ugrd']=['105.10']
                request['vgrd']=request['ugrd']
                request['tmp']=['119.1000']

            request['hgt']=[]

            request['rh']=[]
            
            for plev in uvplevs:
                request['ugrd']=request['ugrd']+['100.%d'%(plev)]
                request['vgrd']=request['vgrd']+['100.%d'%(plev)]

            for plev in zplevs:
                request['hgt']=request['hgt']+['100.%d'%(plev)]

            for plev in tplevs:
                request['tmp']=request['tmp']+['100.%d'%(plev)]

            if(len(hurplevs) > 0):
                for plev in hurplevs:
                    request['rh']=request['rh']+['100.%d'%(plev)]

            request['prmsl']=['102.0']
            request['apcp']=['1.0']
            request['crain']=['1.0']

        elif(model == 'ngpc' or model == 'ngpj' or model == 'navg'):

            # -- mod $GRIBTAB -- now using my standard
            #
            request['ua']=['105.10']
            request['va']=request['ua']
            request['ta']=['1.0']
            request['zg']=[]
            request['hur']=[]
            
            for plev in uvplevs:
                request['ua']=request['ua']+['100.%d'%(plev)]
                request['va']=request['va']+['100.%d'%(plev)]

            for plev in zplevs:
                request['zg']=request['zg']+['100.%d'%(plev)]

            for plev in tplevs:
                request['ta']=request['ta']+['100.%d'%(plev)]

            for plev in hurplevs:
                request['hur']=request['hur']+['100.%d'%(plev)]

            request['psl']=['102.0']
            request['pr']=['1.0']
            request['prc']=['1.0']
            request['tmax']=['105.2']
            request['tmin']=['105.2']


        elif(model == 'gfsc'):

            request['ua']=['105.10']
            request['va']=request['ua']
            request['ta']=[]
            request['zg']=[]
            request['hur']=[]
            
            for plev in uvplevs:
                request['ua']=request['ua']+['100.%d'%(plev)]
                request['va']=request['va']+['100.%d'%(plev)]

            for plev in zplevs:
                request['zg']=request['zg']+['100.%d'%(plev)]

            for plev in tplevs:
                request['ta']=request['ta']+['100.%d'%(plev)]

            for plev in hurplevs:
                request['hur']=request['hur']+['100.%d'%(plev)]

            request['wtmp']=['80.1']
            request['tcdc']=['71.200']
            request['prw']=['54.200']
            request['psl']=['102.0']
            request['pr']=['1.0']
            request['prc']=['1.0']

        elif(model == 'ukmc'):

            request['ua']=['1.0']
            request['va']=request['ua']
            request['ta']=[]
            request['zg']=[]
            request['hur']=[]
            
            for plev in uvplevs:
                request['ua']=request['ua']+['100.%d'%(plev)]
                request['va']=request['va']+['100.%d'%(plev)]

            for plev in zplevs:
                request['zg']=request['zg']+['100.%d'%(plev)]

            for plev in tplevs:
                request['ta']=request['ta']+['100.%d'%(plev)]

            for plev in hurplevs:
                request['hur']=request['hur']+['100.%d'%(plev)]

            request['psl']=['102.0']
            request['pr']=['1.0']

        elif(model == 'jmac'):

            request['ua']=['1.0']
            request['va']=request['ua']
            request['ta']=[]
            request['zg']=[]
            request['hur']=[]
            
            for plev in uvplevs:
                request['ua']=request['ua']+['100.%d'%(plev)]
                request['va']=request['va']+['100.%d'%(plev)]

            for plev in zplevs:
                request['zg']=request['zg']+['100.%d'%(plev)]

            for plev in tplevs:
                request['ta']=request['ta']+['100.%d'%(plev)]

            for plev in hurplevs:
                request['hur']=request['hur']+['100.%d'%(plev)]

            request['psl']=['102.0']
            request['pr']=['1.0']


        elif(model == 'ohc'):

            request['ohc']=['1.0']
            request['d26c']=['4.26']
            request['sst']=['1.0']

        elif(model == 'ocn'):

            request['sst']=['1.0']
            request['sic']=['1.0']

        elif(model == 'ww3'):

            request['wvzs']=['1.0']

    else:
        pass
        
    request['taus']=[tau]

    #print 'RRR--request ',request
    return(request)


def PrintWgrib1Record(nrec,rec):


    (
        sizrecp1,
        gridcode,
        nx,
        ny,
        nxny,
        ndef,
        nundef,
        blat,
        elat,
        dlat,
        blon,
        elon,
        dlon,
        timecode,
        timedesc,
        timerangeind,
        timerangep1,
        timerangep2,
        timeunits,
        tau,
        varcode,
        var,
        vardesc,
        levcode,
        lev,
        levcode2,
        levdesc,
        gridvalmin,
        gridvalmax,
        nbits,
        bdsref,
        decscale,
        binscale
        )=rec
    
    
    print
    print 'FFF Record: '
    print '         nrec: ',nrec
    print '     sizrecp1: ',sizrecp1
    print
    print 'FFF Grid: '
    print '     gridcode: ',gridcode
    print '           nx: ',nx
    print '           ny: ',ny
    print '         nxny: ',nxny
    print '         ndef: ',ndef
    print '       nundef: ',nundef
    print
    print '         blat: ',blat
    print '         elat: ',elat
    print '         dlat: ',dlat
    print 
    print '         blon: ',blon
    print '         elon: ',elon
    print '         dlon: ',dlon
    print
    print 'FFF Time: '
    print '     timecode: ',timecode
    print '     timedesc: ',timedesc
    print ' timerangeind: ',timerangeind
    print '  timerangep1: ',timerangep1
    print '  timerangep2: ',timerangep2
    print '    timeunits: ',timeunits
    print '          tau: ',tau
    print
    print 'FFF Var: '
    print '      varcode: ',varcode
    print '          var: ',var
    print '      vardesc: ',vardesc
    print
    print 'FFF Level: '
    print '      levcode: ',levcode
    print '          lev: ',lev
    print '     levcode2: ',levcode2
    print '      levdesc: ',levdesc
    print
    print 'FFF Grid Values: '
    print '   gridvalmin: ',gridvalmin
    print '   gridvalmax: ',gridvalmax
    print
    finalcard="%-8s %s  %-8s  %-10s  %-16s"%(var,vardesc[0:-1],timecode,timedesc,levdesc)
    #finalcard=var,vardesc,timecode,timedesc,levdesc
    #finalcard="%s | %s | %s | "%(var,timecode,levdesc)


    print 'FFF GRIB packing: '
    print '        nbits: ',nbits
    print '       bdsref: ',finalcard,bdsref,gridvalmin,nbits,decscale,binscale
    print '     decscale: ',decscale
    print '     binscale: ',binscale



def Wgrib1VarFilter(records,request,verb=0):

    verb=1
    nr=len(records)

    rtaus=request['taus']
    rtaus.sort()
    rvars=request.keys()
    rvars.sort()

    
    orecs=[]

    nrecs=records.keys()
    nrecs.sort()

    for nrec in nrecs:
        
        (
            sizrecp1,
            gridcode,
            nx,
            ny,
            nxny,
            ndef,
            nundef,
            blat,
            elat,
            dlat,
            blon,
            elon,
            dlon,
            timecode,
            timedesc,
            timerangeind,
            timerangep1,
            timerangep2,
            timeunits,
            tau,
            varcode,
            var,
            vardesc,
            levcode,
            lev,
            levcode2,
            levdesc,
            gridvalmin,
            gridvalmax,
            nbits,
            bdsref,
            decscale,
            binscale
            )=records[nrec]

        var=var.lower()
        clev="%s.%s"%(levcode,lev)

        for rvar in rvars:
            if(var == rvar):
                rlevs=request[rvar]

                for rlev in rlevs:
                    if(clev == rlev):
                        for rtau in rtaus:
                            if(rtau == tau):
                                if(verb): print 'MMMMMMMMMMMMM(Wgrib1VarFilter): ',	var,clev,tau,nrec,sizrecp1
                                ocard="%d:%d"%(nrec,sizrecp1)
                                ocard=ocard+'\n'
                                orecs.append(ocard)


    return(orecs)


def Wgrib1Filter(orecs,inpath,outpath,override=0):

    if(os.path.exists(outpath) and override == 0):
        return

    wcmd="wgrib -s -i -grib -s %s -o %s"%(inpath,outpath)
    print 'WWW111---wgrib.filter: ',wcmd
    w=os.popen(wcmd,'w')
    w.writelines(orecs)
    w.close()



def MakeDataCtl(dtg,taus,ctlpath,gmppath,model,reqtype='w2flds',gribtype=1,ropt='',override=0):

    gtime=mf.dtg2gtime(dtg)

    etau=taus[-1]
    dtau=6

    (gmpdir,gmpfile)=os.path.split(gmppath)

    ntau=etau/dtau+1
    # -- 20180719 -- mod to use mslet vice prmsl for grib2
    #
    if(model == 'gfs2' 
       or model == 'fv3e' or model == 'fv3g'
       or model == 'fv7e' or model == 'fv7g'
       ):

        if(reqtype == 'w2flds'):

            if(model == 'fv3e' or model == 'fv3g'):
                xydef="""xdef 720 linear   0.0 0.5
ydef 361 linear -90.0 0.5"""
            else:
                xydef="""xdef 1440 linear   0.0 0.25
ydef  721 linear -90.0 0.25"""
            
            ctl="""dset ^%s.%s.%s.f%%f3.grb2
index ^%s
undef 9.999E+20
title gfs2 w2fld
*  produced by g2ctl v0.0.4m
* griddef=1:0:(720 x 361):grid_template=0: lat-lon grid:(720 x 361) units 1e-06 input WE:NS output WE:SN res 48 lat 90.000000 to -90.000000 by 0.500000 lon 0.000000 to 359.500000 by 0.500000 #points=259920:winds(N/S)
dtype grib2
%s
tdef %d linear %s %dhr
* PROFILE hPa
zdef 11 levels 100000 92500 85000 70000 50000 40000 30000 25000 20000 15000 10000
options pascals template
vars 19
ts         0,  1,  0   0,  0,  0             ** 2 m above ground Temperature [K]
tas        0,103,  2   0,  0,  0             ** 2 m above ground Temperature [K]
tasmx      0,103,  2   0,  0,  4, 2          ** 2 m above ground Maximum Temperature -6->+0 h [K]
tasmn      0,103,  2   0,  0,  5, 3          ** 2 m above ground Minimum Temperature -6->+0 h [K]
zg        11,100             0,  3,  5       ** (1000 850 700 500) Geopotential Height [gpm]
ta        11,100             0,  0,  0       ** (1000 975 950 925 900.. 70 50 30 20 10) V-Component of Wind [m/s]
hur       11,100             0,  1,  1       ** (1000 850 700 500) RH [%%]
prc        0,  1,  0   0,  1, 10,  1         ** surface Convective Precipitation [kg/m^2]
pr         0,  1,  0   0,  1,  8,  1         ** surface Total Precipitation [kg/m^2]
prw        0,200,  0   0,  1,  3             ** entire atmosphere (considered as a single layer) Precipitable Water [kg/m^2]
prcra      0,  1,  0   0,  1,196             ** AVE surface Convective Precipitation Rate [kg/m^2/s]
prcr       0,  1,  0   0,  1,196,  0         ** surface Convective Precipitation Rate [kg/m^2/s]
prra       0,  1,  0   0,  1,  7             ** AVE surface Precipitation Rate [kg/m^2/s]
prr        0,  1,  0   0,  1,  7,  0         ** surface Precipitation Rate [kg/m^2/s]
psl        0,101,  0         0,  3,192       ** mean sea level MSLP (Eta model reduction) [Pa]
ua        11,100             0,  2,  2       ** (1000 975 950 925 900.. 70 50 30 20 10) U-Component of Wind [m/s]
uas        0,103, 10         0,  2,  2       ** 10 m above ground U-Component of Wind [m/s]
va        11,100             0,  2,  3       ** (1000 975 950 925 900.. 70 50 30 20 10) V-Component of Wind [m/s]
vas        0,103, 10         0,  2,  3       ** 10 m above ground V-Component of Wind [m/s]
endvars"""%(model,reqtype,dtg,gmpfile,xydef,ntau,gtime,dtau)

    elif(model == 'ngp2'):

        if(reqtype == 'w2flds'):

            ctl="""dset ^ngp2.%s.%s.f%%f3.grb2
index ^%s
undef 9.999E+20
title ../../dat/nwp2/w2flds/2009110600/ngp2.w2flds.2009110600.f024.grb2
#  produced by g2ctl v0.0.4m
# griddef=1:0:(360 x 181):grid_template=0: lat-lon grid:(360 x 181) units 1e-06 input WE:SN output WE:SN res 48 lat -90.000000 to 90.000000 by 1.000000 lon 0.000000 to 359.000000 by 1.000000 #points=65160:winds(N/S)
dtype grib2
ydef 181 linear -90.0 1.0
xdef 360 linear   0.0 1.0
tdef %d linear %s %dhr
* PROFILE hPa
zdef 11 levels 100000 92500 85000 70000 50000 40000 30000 25000 20000 15000 10000
options pascals template
vars 11
prc        0,  1,0       0,1,10,1  ** surface acc Convective Precipitation [kg/m^2]
pr         0,  1,  0       0,1,8,1  ** surface acc Total Precipitation [kg/m^2]
zg        11,100   0,3,5 ** (1000 925 850 700 500 400 300 200) Geopotential Height [gpm]
psl        0,101,  0   0,3,1 ** mean sea level Pressure Reduced to MSL [Pa]
hur       11,100   0,1,1 ** (1000 850 700 600 500 400 300) Relative Humidity [%%]
ta        11,100   0,0,0 ** (1000 925 850 700 500 400 300 200) Temperature [K]
ua        11,100   0,2,2 ** (1000 925 850 700 500 400 300 200) U-Component of Wind [m/s]
uas        0,103, 10   0,2,2 ** 10 m above ground U-Component of Wind [m/s]
va        11,100   0,2,3 ** (1000 925 850 700 500 400 300 200) V-Component of Wind [m/s]
vas        0,103, 10   0,2,3 ** 10 m above ground V-Component of Wind [m/s]
tas        0,103,  2   0,  0,  0     ** 2 m above ground Temperature [K]
endvars"""%(reqtype,dtg,gmpfile,ntau,gtime,dtau)


    elif(model == 'ngpc' or model == 'ngpj'):

        if(reqtype == 'w2flds'):

            ctl="""dset ^%s.%s.%s.f%%f3.grb1
index ^%s
undef 9.999E+20
title %s.2007100112.f006.grb2
options template
dtype grib 255
ydef 361 linear -90.0 0.5
xdef 720 linear   0.0 0.5
zdef 11 levels
1000 925 850 700 500 400 300 250 200 150 100
tdef %d linear %s %dhr
* PROFILE hPa
vars 13
prc       0  63,  1,  0 ** Convective precipitation [kg/m^2]
pr        0  61,  1,  0 ** Total precipitation [kg/m^2]
zg       11   7,100,  0 ** Geopotential height [gpm]
psl       0   2,102,  0 ** Pressure reduced to MSL [Pa]
hur      11  52,100,  0 ** Relative humidity [%%]
tasmx     0  15,105,  2 ** Max. temp. [K]
tasmn     0  16,105,  2 ** Min. temp. [K]
ta       11  11,100,  0 ** Temp. [K]
tas       0  11,105,  2 ** Temp. [K]
ua       11  33,100,  0 ** u wind [m/s]
uas       0  33,105, 10 ** u wind [m/s]
va       11  34,100,  0 ** v wind [m/s]
vas       0  34,105, 10 ** v wind [m/s]
endvars"""%(model,reqtype,dtg,gmpfile,model,ntau,gtime,dtau)

    elif(model == 'navg'):

        if(reqtype == 'w2flds'):

            ctl="""dset ^%s.%s.%s.f%%f3.grb1
index ^%s
undef 9.999E+20
title %s.2007100112.f006.grb2
options template
dtype grib 255
ydef 361 linear -90.0 0.5
xdef 720 linear   0.0 0.5
zdef 11 levels
1000 925 850 700 500 400 300 250 200 150 100
tdef %d linear %s %dhr
* PROFILE hPa
vars 13
prc       0  63,  1,  0 ** Convective precipitation [kg/m^2]
pr        0  61,  1,  0 ** Total precipitation [kg/m^2]
zg       11   7,100,  0 ** Geopotential height [gpm]
psl       0   2,102,  0 ** Pressure reduced to MSL [Pa]
hur      11  52,100,  0 ** Relative humidity [%%]
tasmx     0  15,105,  2 ** Max. temp. [K]
tasmn     0  16,105,  2 ** Min. temp. [K]
ta       11  11,100,  0 ** Temp. [K]
tas       0  11,105,  2 ** Temp. [K]
ua       11  33,100,  0 ** u wind [m/s]
uas       0  33,105, 10 ** u wind [m/s]
va       11  34,100,  0 ** v wind [m/s]
vas       0  34,105, 10 ** v wind [m/s]
endvars"""%(model,reqtype,dtg,gmpfile,model,ntau,gtime,dtau)

    elif(model == 'gfsc'):

        if(reqtype == 'w2flds'):

            ctl="""dset ^gfsc.%s.%s.f%%f3.grb1
index ^%s
undef 9.999E+20
title gfsc2 w2fld
dtype grib 255
options template
xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0
zdef 11 levels 1000 925 850 700 500 400 300 250 200 150 100 
tdef %d linear %s %dhr
vars 12
psl      0   2,102,0   ** Pressure reduced to MSL [Pa]
prc      0  63,  1,0   ** Convective precipitation [kg/m^2]
pr       0  61,  1,0   ** Total precipitation [kg/m^2]
prw      0  54,200,0   ** Precipitable water [kg/m^2]
clt      0  71,200,0   ** Total cloud cover [%%]
uas      0  33,105,10  ** u sfc wind [m/s]
vas      0  34,105,10  ** v sfc wind [m/s]
zg      11   7,100,0   ** Geopotential height [gpm]
hur     11  52,100,0   ** Relative humidity [%%]
ta      11  11,100,0   ** Temp. [K]
ua      11  33,100,0   ** u wind [m/s]
va      11  34,100,0   ** v wind [m/s]
endvars"""%(reqtype,dtg,gmpfile,ntau,gtime,dtau)


    elif(model == 'ukmc'):

        if(reqtype == 'w2flds'):

            ctl="""dset ^ukmc.%s.%s.f%%f3.grb1
index ^%s
undef 9.999E+20
title ukmc w2fld
dtype grib 255
options template
xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0
zdef 11 levels 1000 925 850 700 500 400 300 250 200 150 100 
tdef %d linear %s %dhr
vars 9
psl      0   2,102,0   ** Pressure reduced to MSL [Pa]
pr       0  61,  1,0   ** Total precipitation [kg/m^2]
uas      0  33,105,10  ** u sfc wind [m/s]
vas      0  34,105,10  ** v sfc wind [m/s]
zg      11   7,100,0   ** Geopotential height [gpm]
hur     11  52,100,0   ** Relative humidity [%%]
ta      11  11,100,0   ** Temp. [K]
ua      11  33,100,0   ** u wind [m/s]
va      11  34,100,0   ** v wind [m/s]
endvars"""%(reqtype,dtg,gmpfile,ntau,gtime,dtau)



    elif(model == 'jmac'):

        if(reqtype == 'w2flds'):

            ctl="""dset ^jmac.%s.%s.f%%f3.grb1
index ^%s
undef 9.999E+20
title jmac w2fld
dtype grib 255
options template
xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0
zdef 11 levels 1000 925 850 700 500 400 300 250 200 150 100 
tdef %d linear %s %dhr
vars 9
psl      0   2,102,0   ** Pressure reduced to MSL [Pa]
pr       0  61,  1,0   ** Total precipitation [kg/m^2]
uas      0  33,  1,0  ** u sfc wind [m/s]
vas      0  34,  1,0  ** v sfc wind [m/s]
zg      11   7,100,0   ** Geopotential height [gpm]
hur     11  52,100,0   ** Relative humidity [%%]
ta      11  11,100,0   ** Temp. [K]
ua      11  33,100,0   ** u wind [m/s]
va      11  34,100,0   ** v wind [m/s]
endvars"""%(reqtype,dtg,gmpfile,ntau,gtime,dtau)




    elif(model == 'ohc'):

        if(reqtype == 'w2flds'):

            ctl="""dset ^ohc.%s.%s.f%%f3.grb1
index ^%s
undef 9.999E+20
title ohc.2007100112.f006.grb2
options template
dtype grib 255
ydef  350 linear -30.000000 0.2
xdef 1576 linear 35.000000 0.200000
zdef    1 levels 0
tdef %d linear %s %dhr
vars 3
ohc       0 167,  1  ,0  ** OHC [kJ/cm^2]
d26c      0 242,  4, 26  ** depth of 26C ocean isotherm [m]
sst       0  80,  1,  0  ** SST [K]
endvars"""%(reqtype,dtg,gmpfile,ntau,gtime,dtau)


    elif(model == 'ocn'):

        if(reqtype == 'w2flds'):

            ctl="""dset ^ocn.%s.%s.f%%f3.grb1
index ^%s
undef 9.999E+20
title ocn.2007100112.f006.grb2
options template
dtype grib 255
ydef  721 linear -90.0 0.25
xdef 1440 linear   0.0 0.25
zdef    1 levels 0
tdef %d linear %s %dhr
vars 2
sst       0 80,  1  ,0  ** SST [K]
sic       0 91,  1  ,0  ** SIC [fraction]
endvars"""%(reqtype,dtg,gmpfile,ntau,gtime,dtau)

    elif(model == 'ww3'):

        if(reqtype == 'w2flds'):

            ctl="""dset ^ww3.%s.%s.f%%f3.grb1
index ^%s
undef 9.999E+20
title ww3.2007100112.f006.grb2
options template
dtype grib 255
ydef  721 linear -90.0 0.25
xdef 1440 linear   0.0 0.25
zdef    1 levels 0
tdef %d linear %s %dhr
vars 1
wvzs      0 100,  1  ,0  ** Sig height of wind waves and swell [m]
endvars"""%(reqtype,dtg,gmpfile,ntau,gtime,dtau)


    elif(model == 'fim8'):

        if(reqtype == 'tctrk'):
            ctl="""dset ^fim8.%s.%s.f%%f3.grb1
index ^%s
undef 9.999E+20
title fim8.tctrk.2009051200.f120.grb1
*  produced by grib2ctl v0.9.12.5p16
options yrev template
dtype grib 4
xdef 720 linear   0.0 0.5
ydef 361 linear -90.0 0.5
tdef %d linear %s %dhr
zdef 5 levels 1000 850 700 500 200 
vars 8
pr      0  61,  1,  1  ** Total precipitation [kg/m^2]
zg      5   7,100,  0  ** Geopotential height [gpm]
psl     0 129,102,  1  ** Mean sea level pressure (MAPS) [Pa]
ta3     0  11,100,300  ** Temp. [K]
ua      5  33,100,  0  ** u wind [m/s]
uas     0  33,109,  1  ** u wind [m/s]
va      5  34,100,  0  ** v wind [m/s]
vas     0  34,109,  1  ** v wind [m/s]
ENDVARS"""%(reqtype,dtg,dtg,ntau,gtime,dtau)

        elif(reqtype == 'w2flds'):
            
            ctl="""dset ^fim8.%s.%s.f%%f3.grb1
index ^%s
undef 9.999E+20
title fim8.tctrk.2009051200.f120.grb1
*  produced by grib2ctl v0.9.12.5p16
options yrev template
dtype grib 4
xdef 720 linear   0.0 0.5
ydef 361 linear -90.0 0.5
tdef %d linear %s %dhr
zdef 11 levels 1000 925 850 700 500 400 300 250 200 150 100
vars 14
pr      0  61,  1,  1  ** Total precipitation [kg/m^2]
prc     0  63,  1,  1  ** Convective precipitation [kg/m^2]
prw     0  54,  1,  1  ** prw [mm]
hfls    0 121,  1,  1  ** latent heat [mm]
hfss    0 122,  1,  1  ** sensible heat [mm]
ustar   0 253,  1,  1  ** sensible heat [mm]
psl     0 129,102,  1  ** Mean sea level pressure (MAPS) [Pa]
uas     0  33,105, 10  ** u wind [m/s]
vas     0  34,105, 10  ** v wind [m/s]
zg      11   7,100,  0  ** Geopotential height [gpm]
ta      11  11,100,  0  ** Temp. [K]
hur     11  52,100,  0  ** Temp. [K]
ua      11  33,100,  0  ** u wind [m/s]
va      11  34,100,  0  ** v wind [m/s]
ENDVARS"""%(reqtype,dtg,gmpfile,ntau,gtime,dtau)

        else:
            print 'EEEE invalid reqtype: ',reqtype
            sys.exit()

    elif(model == 'mpas'):

        if(reqtype == 'tctrk'):
            print """EEE reqtype == 'tctrk' not supported for model: %s"""%(model)
            sys.exit()

        elif(reqtype == 'w2flds'):
            
            ctl="""dset ^mpas.%s.%s.f%%f3.grb1
index ^%s
undef 9.999E+20
title mpas
*  produced by grib2ctl v0.9.12.5p16
options template
dtype grib 
xdef 720 linear  180.0 0.5
ydef 361 linear  -90.0 0.5
tdef %d linear %s %dhr
zdef 11 levels 1000 925 850 700 500 400 300 250 200 150 100
vars 10
prl     0   62,  1,  0  ** Large-scale precipitation [kg/m^2]
prc     0   63,  1,  0  ** Convective precipitation [kg/m^2]
psl     0    2,102,  0  ** Mean sea level pressure (MAPS) [Pa]
uas     0   33,105, 10  ** u wind [m/s]
vas     0   34,105, 10  ** v wind [m/s]
zg      11   7,100,  0  ** Geopotential height [gpm]
ta      11  11,100,  0  ** Temp. [K]
hur     11  52,100,  0  ** Temp. [K]
ua      11  33,100,  0  ** u wind [m/s]
va      11  34,100,  0  ** v wind [m/s]
ENDVARS"""%(reqtype,dtg,gmpfile,ntau,gtime,dtau)

        else:
            print 'EEEE invalid reqtype: ',reqtype
            sys.exit()


        
    elif(model == 'ecm2'):
        
        if(reqtype == 'tctrk'):
            ctl="""dset ^ecm2.tctrk.%s.f%%f3.grb1
index ^%s
undef 9.999E+20
title ecm2.tctrk.2009051200.f120.grb1
*  produced by grib2ctl v0.9.12.5p16
dtype grib 255
options yrev template
xdef 360 linear 0.000000 1.000000
ydef 181 linear -90.000000 1
tdef %d linear %s %dhr
zdef 5 levels 1000 850 700 500 200 
vars 8
pr      0 228,  1,  0  ** Total precipitation [kg/m^2]
zg      5 156,100,  0  ** Geopotential height [gpm]
psl     0 151,  1,  0  ** Mean sea level pressure (MAPS) [Pa]
ta      0 130,100,300  ** Temp. [K]
ua      5 131,100,  0  ** u wind [m/s]
uas     0 165,  1,  0  ** u wind [m/s]
va      5 132,100,  0  ** v wind [m/s]
vas     0 166,  1,  0  ** v wind [m/s]
ENDVARS"""%(dtg,gmpfile,ntau,gtime,dtau)
            
        elif(reqtype == 'w2flds'):

            ctl="""dset ^%s.w2flds.%s.f%%f3.grb1
index ^%s
undef 9.999E+20
title ecm2.w2flds 
*  produced by grib2ctl v0.9.12.5p16
dtype grib 255
options yrev template
xdef 360 linear 0.000000 1.000000
ydef 181 linear -90.000000 1
tdef %d linear %s %dhr
zdef 11 levels 1000 925 850 700 500 400 300 250 200 150 100
vars 16
tas     0 167,  1,  0  ** 2 m above ground Temperature [K]
tasmx   0 201,  1,  0  ** 2 m above ground Maximum Temperature -3->+0 h [K]
tasmn   0 202,  1,  0  ** 2 m above ground Minimum Temperature -3->+0 h [K]
pr      0 228,  1,  0  ** Total precipitation [kg/m^2]
prl     0 142,  1,  0  ** large-scale precipitation [kg/m^2]
prc     0 143,  1,  0  ** convective precipitation [kg/m^2]
sic     0  31,  1,  0  ** ea-ice cover [(0-1)]
sst     0  34,  1,  0  ** Sea surface temperature [K]
psl     0 151,  1,  0  ** Mean sea level pressure (MAPS) [Pa]
uas     0 165,  1,  0  ** u wind [m/s]
vas     0 166,  1,  0  ** v wind [m/s]
zg     11 156,100,  0  ** Geopotential height [gpm]
ua     11 131,100,  0  ** u wind [m/s]
ta     11 130,100,  0  ** Temp. [K]
va     11 132,100,  0  ** v wind [m/s]
hur    11 157,100,  0  ** RH [%%]
ENDVARS"""%(model,dtg,gmpfile,ntau,gtime,dtau)

        else:
            print 'EEEE invalid reqtype: ',reqtype
            sys.exit()


    elif(model == 'ecm4'):
        
        if(reqtype == 'w2flds'):

            ctl="""dset ^%s.w2flds.%s.f%%f3.grb1
index ^%s
undef 9.999E+20
title ecm4.w2flds
*  produced by grib2ctl v0.9.12.5p16
dtype grib 255
options yrev template
xdef 1440 linear   0.0 0.25
ydef  721 linear -90.0 0.25
tdef %d linear %s %dhr
zdef 9 levels 1000 925 850 700 500 400 300 250 200
vars 16
tas     0 167,  1,  0  ** 2 m above ground Temperature [K]
tasmx   0 201,  1,  0  ** 2 m above ground Maximum Temperature -3->+0 h [K]
tasmn   0 202,  1,  0  ** 2 m above ground Minimum Temperature -3->+0 h [K]
pr      0 228,  1,  0  ** Total precipitation [kg/m^2]
prl     0 142,  1,  0  ** large-scale precipitation [kg/m^2]
prc     0 143,  1,  0  ** convective precipitation [kg/m^2]
sic     0  31,  1,  0  ** ea-ice cover [(0-1)]
sst     0  34,  1,  0  ** Sea surface temperature [K]
psl     0 151,  1,  0  ** Mean sea level pressure (MAPS) [Pa]
uas     0 165,  1,  0  ** u wind [m/s]
vas     0 166,  1,  0  ** v wind [m/s]
zg     11 156,100,  0  ** Geopotential height [gpm]
ua     11 131,100,  0  ** u wind [m/s]
ta     11 130,100,  0  ** Temp. [K]
va     11 132,100,  0  ** v wind [m/s]
hur    11 157,100,  0  ** RH [%%]
ENDVARS"""%(model,dtg,gmpfile,ntau,gtime,dtau)

        else:
            print 'EEEE invalid reqtype: ',reqtype
            sys.exit()



    elif(model == 'gfsk'):
        
        if(reqtype == 'tctrk'):
            print 'EEE tctrk reqtype not implemented for model: ',model
            sys.exit()
            
        elif(reqtype == 'w2flds'):

            ctl="""dset ^%s.w2flds.%s.f%%f3.grb1
index ^%s
undef 9.999E+20
title ecm2.w2flds.2009051200.f120.grb1
*  produced by grib2ctl v0.9.12.5p16
dtype grib 255
options yrev template
xdef 720 linear   0.0 0.5
ydef 361 linear -90.0 0.5
tdef %d linear %s %dhr
zdef 11 levels 1000 925 850 700 500 400 300 250 200 150 100
vars 11
pr       0  61,  1,  0  ** Total precipitation [kg/m^2]
prc      0  63,  1,  0  ** Convective precipitation [kg/m^2]
prw      0  54,200,  0  ** prw [mm]
psl      0   2,102,  0  ** Mean sea level pressure (MAPS) [Pa]
uas      0  33,105, 10  ** u wind [m/s]
vas      0  34,105, 10  ** v wind [m/s]
zg      11   7,100,  0  ** Geopotential height [gpm]
ta      11  11,100,  0  ** Temp. [K]
hur     11  52,100,  0  ** Temp. [K]
ua      11  33,100,  0  ** u wind [m/s]
va      11  34,100,  0  ** v wind [m/s]
ENDVARS"""%(model,dtg,gmpfile,ntau,gtime,dtau)

        else:
            print 'EEEE invalid reqtype: ',reqtype
            sys.exit()

    elif(model == 'ecmn'):
        
            
        if(reqtype == 'w2flds'):

            ctl="""dset ^%s.w2flds.%s.f%%f3.grb2
index ^%s
undef 9.999E+20
options template
title t.grb2
* produced by g2ctl v0.0.4m
* griddef=1:45:(360 x 91):grid_template=0: lat-lon grid:(360 x 91) units 1e-06 input WE:SN output WE:SN res 48 lat 0.000000 to 90.000000 by 1.000000 lon 0.000000 to 359.000000 by 1.000000 #points=32760:winds(N/S)
dtype grib2
xdef 360 linear 0.0 1.0
ydef  91 linear 0.0 1.0
tdef  %d linear %s %dhr
* PROFILE Pa
zdef 8 levels 100000 92500 85000 70000 50000 40000 30000 25000
options pascals
vars 13
pr     0,  1,0   0,1,8 ** surface Total Precipitation [kg/m^2]
tds    0,  1,0   0,0,6 ** surface Dew Point Temperature [K]
zg     8,100     0,3,5 ** (1000 925 850 700 500 400 300 250) Geopotential Height [gpm]
psl    0,  1,0   0,3,1 ** surface Pressure Reduced to MSL [Pa]
hur    8,100     0,1,1 ** (1000 925 850 700 500 400 300 250) Relative Humidity [%%]
tasmax 0,  1,0   0,0,4 ** surface Maximum Temperature [K]
tasman 0,  1,0   0,0,5 ** surface Minimum Temperature [K]
tas    0,  1,0   0,0,0 ** surface Temperature [K]
ta     8,100     0,0,0 ** (1000 925 850 700 500 400 300 250) Temperature [K]
uas    0,  1,0   0,2,2 ** surface U-Component of Wind [m/s]
ua     8,100     0,2,2 ** (1000 925 850 700 500 400 300 250) U-Component of Wind [m/s]
vas    0,  1,0   0,2,3 ** surface V-Component of Wind [m/s]
va     8,100     0,2,3 ** (1000 925 850 700 500 400 300 250) V-Component of Wind [m/s]
ENDVARS"""%(model,dtg,gmpfile,ntau,gtime,dtau)

        else:
            print 'EEEE invalid reqtype: ',reqtype
            sys.exit()


    elif(model == 'ukm2'):

        if(reqtype == 'tctrk'):
            ctl="""dset ^ukm2.tctrk.%s.f%%f3.grb1
index ^%s
undef 9.999E+20
title ukm2.tctrk.2009051200.f120.grb1
*  produced by grib2ctl v0.9.12.5p16
options template
dtype grib 255
xdef 640 linear   0.0 0.5625
ydef 481 linear -90.0 0.375
tdef %d linear %s %dhr
zdef 5 levels 1000 850 700 500 200 
vars 8
pr      0  61,  1,  0  ** Total precipitation [kg/m^2]
zg      5   7,100,  0  ** Geopotential height [gpm]
psl     0   2,102,  0  ** Mean sea level pressure (MAPS) [Pa]
ta3     0  11,100,300  ** Temp. [K]
ua      5  33,100,  0  ** u wind [m/s]
uas     0  33,  1,  0  ** u wind [m/s]
va      5  34,100,  0  ** v wind [m/s]
vas     0  34,  1,  0  ** v wind [m/s]
ENDVARS"""%(dtg,gmpfile,ntau,gtime,dtau)


        elif(reqtype == 'w2flds'):

            grid="""xdef 640 linear   0.0 0.5625
ydef 481 linear -90.0 0.375"""

            # grid res change...2010030912...
            #
            if(mf.dtgdiff('2010030912',dtg) >= 0):
                grid="""xdef 1024 linear   0.0  0.3515625
ydef 769 linear -90.0 0.234375"""
                
            if(mf.dtgdiff('2014072200',dtg) >= 0):
                grid="""xdef 1536 linear 0.0  0.234375
ydef 1153 linear -90.0 0.15625"""

            if(mf.dtgdiff('2017071112',dtg) >= 0):
                grid="""xdef 2560 linear   0.0 0.140625
ydef 1921 linear -90.0 0.093750"""

            ctl="""dset ^ukm2.%s.%s.f%%f3.grb1
index ^%s
undef 9.999E+20
title ukm2.tctrk.2009051200.f120.grb1
*  produced by grib2ctl v0.9.12.5p16
options template
dtype grib 255
%s
tdef %d linear %s %dhr
zdef 7 levels 1000 925 850 700 500 300 200 
vars 11
prc     0 140,  1,  0  ** Convective precipitation [kg/m^2]
pr      0  61,  1,  0  ** Total precipitation [kg/m^2]
psl     0   2,102,  0  ** Mean sea level pressure (MAPS) [Pa]
uas     0  33,  1,  0  ** u wind [m/s]
vas     0  34,  1,  0  ** v wind [m/s]
tas     0  11,  1,  0  ** Temp. [K]
hur     7  52,100,  0  ** HR [%%]
zg      7   7,100,  0  ** Geopotential height [gpm]
ta      7  11,100,  0  ** Temp. [K]
ua      7  33,100,  0  ** u wind [m/s]
va      7  34,100,  0  ** v wind [m/s]
ENDVARS"""%(reqtype,dtg,gmpfile,grid,ntau,gtime,dtau)

# -- native format that goes through w2.fld.ukm2lats.gs comes out in more standard form
#
            ctl="""dset ^ukm2.%s.%s.f%%f3.grb1
index ^%s
undef 9.999E+20
title ukm2.tctrk.2009051200.f120.grb1
*  produced by grib2ctl v0.9.12.5p16
options template
dtype grib 255
%s
tdef %d linear %s %dhr
zdef 7 levels 1000 925 850 700 500 300 200 
vars 11
prc     0  63,  1,  0  ** Convective precipitation [kg/m^2]
pr      0  61,  1,  0  ** Total precipitation [kg/m^2]
psl     0   2,102,  0  ** Mean sea level pressure (MAPS) [Pa]
uas     0  33,105, 10  ** u wind [m/s]
vas     0  34,105, 10  ** v wind [m/s]
tas     0  11,105,  2  ** Temp. [K]
hur     7  52,100,  0  ** HR [%%]
zg      7   7,100,  0  ** Geopotential height [gpm]
ta      7  11,100,  0  ** Temp. [K]
ua      7  33,100,  0  ** u wind [m/s]
va      7  34,100,  0  ** v wind [m/s]
ENDVARS"""%(reqtype,dtg,gmpfile,grid,ntau,gtime,dtau)


    #ccccccccccccccccccccccccccccccccccccccccmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmcccccccccccccccccccccccccccccccccccccc
    #
    #

    elif(model == 'cmc2'):

        if(reqtype == 'w2flds'):
            ctl="""dset ^cmc2.%s.%s.f%%f3.grb1
index ^%s
undef 9.999E+20
title cmc2.tctrk.2009051200.f120.grb1
*  produced by grib2ctl v0.9.12.5p16
options template
dtype grib 255
xdef 360 linear   0.0 1.0
ydef 181 linear -90.0 1.0
tdef %d linear %s %dhr
zdef 11 levels 1000 925 850 700 500 400 300 250 200 150 100
vars 10
pr      0    61,  1,  0  ** Total precipitation [kg/m^2]
psl     0   2,102,  0  ** Mean sea level pressure (MAPS) [Pa]
hur     11  52,100,  0  ** HR [%%]
zg      11   7,100,  0  ** Geopotential height [gpm]
ta      11  11,100,300  ** Temp. [K]
ua      11  33,100,  0  ** u wind [m/s]
va      11  34,100,  0  ** v wind [m/s]
uas     0 33,105,10  ** u wind [m/s]
vas     0 34,105,10  ** v wind [m/s]
tas     0 11,119,10000  ** v wind [m/s]
ENDVARS"""%(reqtype,dtg,gmpfile,ntau,gtime,dtau)


    else:
        print 'EEE invalid model to make .ctl: ',model
        sys.exit()

    
    mf.WriteCtl(ctl,ctlpath)

    chkgmp=0
    dogribmap=1
    gribmapverb='-v'
    gribmapverb=''
    
    if(os.path.exists(gmppath) and chkgmp): dogribmap=0
    if(override): dogribmap=1

    if(dogribmap):
        if(gribtype == 1):
            cmd="gribmap %s -i %s"%(gribmapverb,ctlpath)
        elif(gribtype == 2):
            cmd="gribmap %s -i %s"%(gribmapverb,ctlpath)
            
        mf.runcmd(cmd,ropt)





#oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
# one-off code to reorg files
#
domvonly=0
if(domvonly):
    tdirold="%s/%s/%s"%(w2.Nwp2DataBdir,reqtype,dtg)
    files=glob.glob("%s/*%s*"%(tdirold,model))

    if(len(files) > 0):
        tdir="%s/%s/dat/%s/%s"%(w2.Nwp2DataBdir,reqtype,model,dtg)
        mf.ChkDir(tdir,'mk')
        for file in files:
            cmd="mv %s %s"%(file,tdir)
            mf.runcmd(cmd,ropt)

        sys.exit()


    
                
def rsync2Kishou(tdir,tdirKishou,ropt,onLocal=0):
    
    prcdir=w2.PrcDirFlddatW2
    expath="%s/ex-kaze2kishou.txt"%(prcdir)

    rsyncoptDry='-alvn --timeout=30 --protocol=29 --exclude-from=%s '%(expath)
    rsyncoptDo= '-alv  --timeout=30 --protocol=29 --exclude-from=%s '%(expath)
    rsyncopt=rsyncoptDo
    if(ropt == 'norun'):
        rsyncopt=rsyncoptDry
        ropt=''
    if(onLocal):
        cmd='rsync %s %s %s'%(rsyncopt,tdirKishou,tdir)
    else:
        cmd='rsync %s %s %s'%(rsyncopt,tdir,tdirKishou)
        
    mf.runcmd(cmd,ropt)


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class w2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',    'DTG (YYYYMMDDHH)'],
            2:['model',  '''modelopt - all | gfs2,ecm2,ecm4,fim8,fimx,ukm2,ngp2,cmc2'''],
            }
            
        self.options={
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'forcefdb':         ['F',0,1,'forcefdb'],
            'dotau':            ['t:',None,'i','do individual tau'],
            'doctlonly':        ['C',0,1,'just do .ctl'],
            'reqtype':          ['t:','w2flds','a','do individual tau'],
            'override':         ['O',0,1,'1 - '],
            'override2':        ['o',0,1,'1 - '],
            'rsyncKishou':      ['R',0,1,'rysnc to Kishou if onKaze'],
            }

        self.defaults={
            'dogrib2Togrib1':0,

            }

        self.purpose='''
purpose:

main control script for nwp2 models (gfs2,ecm2,ecm4,ukm2,fim8,ngp2,cmc2,fimx)
using /public/data/grids/ and from wjet

(c) 2009-2010 Michael Fiorino,NOAA ESRL
'''
        self.examples='''
example:

%s ops6 gfs2 (sets incrontab=1)'''


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# cmdline
#

argv=sys.argv

CL=w2CmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr


if(override2): override=2


dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=12)
nmodels=len(model.split(','))

if(len(dtgs) > 1 or model == 'all' or nmodels > 1 ):

    if(nmodels == 1): 
        models=[model]
    elif(model == 'all'): 
        models=w2.Nwp2ModelsActive
    elif(nmodels > 1):
        models=model.split(',')
        
    # cycle by dtgs
    #
    for model in models:
        for dtg in dtgs:
            cmd="%s %s %s"%(pyfile,dtg,model)
            for o,a in CL.opts:
                cmd="%s %s %s"%(cmd,o,a)
            mf.runcmd(cmd,ropt)

    sys.exit()

else:
    dtg=dtgs[0]

m=setModel2(model)
m.verb=verb
if(hasattr(m,'setNwp2Fields')): m.setNwp2Fields(dtg,override=override)
#m.setInventory(dtg=dtg)

if(doctlonly):   fm=m.DataPath(dtg,dofilecheck=0)
else:            fm=m.DataPath(dtg,verb=1)

gribtype=fm.gribtype
datbase=fm.dbase
tdir="%s/%s/dat/%s/%s/"%(w2.Nwp2DataBdir,reqtype,model,dtg)
tdirKishou="%s/%s/dat/%s/%s/"%(w2.Nwp2DataBdir,reqtype,model,dtg)
mf.ChkDir(tdir,'mk')

# -- tdir on kishou
#
tdirKishou=tdirKishou.replace(w2.Nwp2DataBdir,'fiorino@kishou.fsl.noaa.gov:/w21/dat/nwp2')

if(rsyncKishou and (onKaze or onTaifuu) and doctlonly == 0):
    rc=rsync2Kishou(tdir,tdirKishou,ropt,onLocal=onTaifuu)
    sys.exit()

m.setctlgridvar(dtg)

btau=m.btau
etau=m.etau
dtau=m.dtau

taus=[0,24,48,72]
if(reqtype == 'tctrk'):
    taus=range(0,121,6)
elif(reqtype == 'w2flds'):
    taus=range(btau,etau+1,dtau)


if (dotau != None):
    taus=[int(dotau)]

ctlpath="%s/%s.%s.%s.ctl"%(tdir,model,reqtype,dtg)
if(IsGrib1(gribtype)): gmppath="%s/%s.%s.%s.grib1.gmp"%(tdir,model,reqtype,dtg)
if(IsGrib2(gribtype)): gmppath="%s/%s.%s.%s.grib2.gmp"%(tdir,model,reqtype,dtg)

if(doctlonly):
    if(IsGrib1(gribtype)): MakeDataCtl(dtg,taus,ctlpath,gmppath,model,reqtype=reqtype,gribtype=1)
    if(IsGrib2(gribtype)): MakeDataCtl(dtg,taus,ctlpath,gmppath,model,reqtype=reqtype,gribtype=2)
    # -- make the inventory
    fm=m.DataPath(dtg,dtype='w2flds',dowgribinv=1,override=1)
    if(rsyncKishou):
        rc=rsync2Kishou(tdir,tdirKishou,ropt)
    
    sys.exit()

nflds=0
outsize=0

for tau in taus:

    # -- special case -- toss out tau78 for ngp2 -- too little fields
    #
    if(model == 'ngp2' and tau == 78): continue
    if(model == 'ukm2'):
        datpath="%s.%s"%(datbase,gribtype)
        fdbpath='%s/fdb.%s.%s.%s.txt'%(tdir,model,reqtype,dtg)
        # -- see if file from ukmet there...for redoing w2flds from complete grib file
        #
        (dir,file)=os.path.split(datpath)
        ukmetpath="%s/%s_meto.grib"%(dir,dtg)
        siz=MF.getPathSiz(ukmetpath)
        if(siz > 0): datpath=ukmetpath
        
    else:
        datpath="%s.f%03d.%s"%(datbase,tau,gribtype)
        fdbpath='%s/fdb.%s.%s.%s.f%03d.txt'%(tdir,model,reqtype,dtg,tau)
        
    g2path="%s/%s.%s.%s.f%03d.grb2"%(tdir,model,reqtype,dtg,tau)
    g1path="%s/%s.%s.%s.f%03d.grb1"%(tdir,model,reqtype,dtg,tau)

    if(not(os.path.exists(fdbpath)) or forcefdb or (mf.GetPathSiz(fdbpath) < 100) or override == 2 ):
        if(IsGrib1(gribtype)):
            MakeFdb1(datpath,fdbpath,ropt='')
            cards=GetFdb(fdbpath)

            # 20100606 ???  not sure about this logic to  only do one tau for ukm2.alltau
            # the problem is if the entire field does not come in at once, every hour...
            #
            if(m.tautype == 'alltau' and override == 2):
                forcefdb=0
                if(override == 2): override=1
        elif(IsGrib2(gribtype)):
            MakeFdb2(datpath,fdbpath,ropt='')
            cards=GetFdb(fdbpath)
            if(m.tautype == 'alltau'): forcefdb=0
            
    else:
        cards=GetFdb(fdbpath)


    #
    # skip if only one card in the inventory
    #
    redoFdb=1
    
    if((len(cards) == 1 and model != 'ww3') and redoFdb):

        if(IsGrib1(gribtype)):
            MakeFdb1(datpath,fdbpath,ropt='')
            cards=GetFdb(fdbpath)

        elif(IsGrib2(gribtype)):
            MakeFdb2(datpath,fdbpath,ropt='')
            cards=GetFdb(fdbpath)
            if(m.tautype == 'alltau'): forcefdb=0
        
        print 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW only one card in inventory',model,dtg,' with redoFdb'
        
        continue


    elif(len(cards) == 1 and model != 'ww3'):
        print '111111111111111111 only one card in inventory',model,dtg
        continue
    else:
        # -- 9 cards / field from wgrib -V
        #
        nflds=nflds+len(cards)/9

    
    doFullPrint=0
    #if(tau == 6): doFullPrint=1
    if(IsGrib1(gribtype)):      (records,recsiz,nrectot)=ParseFdb1(cards,doFullPrint=doFullPrint)
    if(IsGrib2(gribtype)):      (records,recsiz,nrectot)=ParseFdb2(cards)

    if(verb and IsGrib1(gribtype)):  Wgrib1VarAnal(records)
    if(verb and IsGrib2(gribtype)):  Wgrib2VarAnal(records,tau)
    
    if(IsGrib1(gribtype)):  request=SetFieldRequest1(tau,model,reqtype)
    if(IsGrib2(gribtype)):  request=SetFieldRequest2(tau,model,reqtype)

    dofilt=1

    if(IsGrib1(gribtype) and (dofilt and not(os.path.exists(g1path)) or override > 0)):
        orecs=Wgrib1VarFilter(records,request)
        Wgrib1Filter(orecs,datpath,g1path,override=override)

    if(IsGrib2(gribtype) and (dofilt and not(os.path.exists(g2path)) or override > 0)):
        orecs=Wgrib2VarFilter(records,request,tau)
        Wgrib2Filter(orecs,datpath,g2path,override=override)

    if(os.path.exists(g2path) and dogrib2Togrib1):
        CnvgribG21(g2path,g1path)


    if(IsGrib1(gribtype)):
        try:    outsize=outsize+os.path.getsize(g1path)
        except: outsize=outsize

    if(IsGrib2(gribtype)):
        try:    outsize=outsize+os.path.getsize(g2path)
        except: outsize=outsize
        

# 0000000000000000 no input fields or output files 0 length; clean up tdir and exit
#
if(outsize > 1024*1024):
    outsize=outsize/(1024*1024)

if(nflds == 0 and outsize == 0):
    print "nflds: %d outsize: %d"%(nflds,outsize),' nada nada sayoonara.......'
    sys.exit()
    
elif(nflds == 0 or outsize == 0):
    print "nflds: %d outsize: %d"%(nflds,outsize),' no data in source dir or tdir 0 length files; clean out tdir and sayoonara.......'
    #cmd="rm -f %s/*"%(tdir)
    #mf.runcmd(cmd)
    sys.exit()
    
    

if(IsGrib1(gribtype)):  MakeDataCtl(dtg,taus,ctlpath,gmppath,model,reqtype=reqtype,gribtype=1)
if(IsGrib2(gribtype)):  MakeDataCtl(dtg,taus,ctlpath,gmppath,model,reqtype=reqtype,gribtype=2)

#iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# make inventory using LsGrib Model2 inherited from FimRun
#

# -- use DataPath to make the add w2fld to the inventory
# -- always override for models that come in tau chunks like ngpc
#
fm=m.DataPath(dtg,dtype='w2flds',dowgribinv=1,override=1)

# use m2 class from FM that was put in from HFIP
# to make the grib inventory, add option for not doing lsgrib
#

if(m.dofimlsgrib):
    fm=FimRunModel2(model,dtg,override=override,verb=verb)
    fm.LsGrib(override=override)


# -- rsync over to kishou if onKaze
#
if(w2.onKaze):
    rc=rsync2Kishou(tdir,tdirKishou,ropt)

sys.exit()

