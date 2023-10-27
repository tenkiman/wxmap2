#!/usr/bin/env python

#from WxMAP2 import *
import collections
from eccodes import *
from tcbase import *
w2=W2()

def comp2BTstmids(rlat,rlon,btlatlons,
                  tolNN,tol9X,
                  aid,
                  verb=0):

    rc=None
    odist=None
    for stmid in btlatlons.keys():
        btlat=btlatlons[stmid][0]
        btlon=btlatlons[stmid][1]
        if(IsNN(stmid)): tol=tolNN
        else:            tol=tol9X
        
        dist=gc_dist(rlat, rlon, btlat, btlon)
        if(verb): print 'CCC-comp2BTstmids: ',stmid,aid,btlat,btlon,'bufr: ',rlat,rlon,' dist: ',dist,' tol: ',tol
        if(dist < tol): 
            odist=dist
            rc=stmid
            return(rc,odist)
        
    return(rc,odist)


def bufr_decode(input_file,btlatlons,
                tolNN=240.0,tol9X=180.0, # -- 20180706 for 02L tollNN was too small
                tau00min=12,
                verb=0,warn=0):

    data = collections.defaultdict(dict)
    
    def getAid(nm):
        if(nm == 52):
            aid="emdt"
        elif(nm == 51):
            aid="emcn"
        else:
            aid="em%02d"%(nm)
        aid=aid.upper()
        return(aid)

    f = open(input_file)
    
    
    cnt = 0
 
    # loop for the messages in the file
    while 1:
        # get handle for message
        bufr = codes_bufr_new_from_file(f)
        if bufr is None:
            break
 
        if(verb): print('**************** MESSAGE: ', cnt + 1, '  *****************')
 
        # we need to instruct ecCodes to expand all the descriptors
        # i.e. unpack the data values
        codes_set(bufr, 'unpack', 1)
 
        numObs = codes_get(bufr, "numberOfSubsets")
        year = codes_get(bufr, "year")
        month = codes_get(bufr, "month")
        day = codes_get(bufr, "day")
        hour = codes_get(bufr, "hour")
        minute = codes_get(bufr, "minute")
        
        bufrDtg="%04d%02d%02d%02d"%(year,month,day,hour)
 
        if(verb): print('Date and time: ', day, '.', month, '.', year, '  ', hour, ':', minute)
 
        stormIdentifier = codes_get(bufr, "stormIdentifier")
        if(verb): print('Storm identifier: ', stormIdentifier)
        
        # How many different timePeriod in the data structure?
        numberOfPeriods = 0
        while True:
            numberOfPeriods = numberOfPeriods + 1
            try:
                codes_get_array(bufr, "#%d#timePeriod" % numberOfPeriods)
            except CodesInternalError as err:
                break
                # the numberOfPeriods includes the analysis (period=0)
 
        # Get ensembleMemberNumber
        memberNumber = codes_get_array(bufr, "ensembleMemberNumber")
        memberNumberLen = len(memberNumber)
 
        # Observed Storm Centre
        significance = codes_get(bufr, '#1#meteorologicalAttributeSignificance')
        latitudeCentre = codes_get(bufr, '#1#latitude')
        longitudeCentre = codes_get(bufr, '#1#longitude')
 
        if significance != 1:
            print('ERROR: unexpected #1#meteorologicalAttributeSignificance')
            return 1
 
        gotObCenter=1
        if (latitudeCentre == CODES_MISSING_DOUBLE) and (longitudeCentre == CODES_MISSING_DOUBLE):
            if(warn): print('Observed storm centre position missing')
            gotObCenter=0
        else:
            if(verb): print('Observed storm centre: latitude=', latitudeCentre, ' longitude=', longitudeCentre)
 
        # Location of storm in perturbed analysis
        #significance = codes_get(bufr, '#2#meteorologicalAttributeSignificance')

        #if (significance != 5 and significance != 4):
            #print('ERROR: unexpected #2#meteorologicalAttributeSignificance')
            #return 1
 
        latitudeAnalysis = codes_get_array(bufr, '#2#latitude')
        longitudeAnalysis = codes_get_array(bufr, '#2#longitude')
        pressureAnalysis = codes_get_array(bufr, '#1#pressureReducedToMeanSeaLevel')*0.01
 
        # Location of Maximum Wind
        significance = codes_get(bufr, '#3#meteorologicalAttributeSignificance')
 
        if significance != 3:
            print('ERROR: unexpected #3#meteorologicalAttributeSignificance=', significance)
            return 1
 
        latitudeMaxWind0 = codes_get_array(bufr, '#3#latitude')
        longitudeMaxWind0 = codes_get_array(bufr, '#3#longitude')
        windMaxWind0 = codes_get_array(bufr, '#1#windSpeedAt10M')*ms2knots
 
        if len(latitudeAnalysis) == len(memberNumber) and len(latitudeMaxWind0) == len(memberNumber):
            for k in range(len(memberNumber)):
                try:
                    rmax=gc_dist(latitudeAnalysis[k], longitudeAnalysis[k],
                                 latitudeMaxWind0[k], longitudeMaxWind0[k])
                        
                    data[k][0] = [latitudeAnalysis[k], longitudeAnalysis[k], pressureAnalysis[k],
                                  latitudeMaxWind0[k], longitudeMaxWind0[k], windMaxWind0[k],
                                  rmax]
                except:
                    data[k][0] = [CODES_MISSING_DOUBLE, CODES_MISSING_DOUBLE, CODES_MISSING_DOUBLE, 
                                  CODES_MISSING_DOUBLE, CODES_MISSING_DOUBLE, CODES_MISSING_DOUBLE]
 
        else:
            for k in range(len(memberNumber)):
                try:
                    rmax=gc_dist(latitudeAnalysis[k], longitudeAnalysis[k],
                                 latitudeMaxWind0[k], longitudeMaxWind0[k])
                    data[k][0] = [latitudeAnalysis[0], longitudeAnalysis[0], pressureAnalysis[k], latitudeMaxWind0[0],
                                  longitudeMaxWind0[0], windMaxWind0[k], 
                                  rmax]
                except:
                    data[k][0] = [CODES_MISSING_DOUBLE, CODES_MISSING_DOUBLE, CODES_MISSING_DOUBLE, 
                                  CODES_MISSING_DOUBLE, CODES_MISSING_DOUBLE, CODES_MISSING_DOUBLE]
                    
 
        timePeriod = [0 for x in range(numberOfPeriods)]
        for i in range(1, numberOfPeriods):
            rank1 = i * 2 + 2
            rank3 = i * 2 + 3
 
            ivalues = codes_get_array(bufr, "#%d#timePeriod" % i)
 
            if len(ivalues) == 1:
                timePeriod[i] = ivalues[0]
            else:
                for j in range(len(ivalues)):
                    if ivalues[j] != CODES_MISSING_LONG:
                        timePeriod[i] = ivalues[j]
                        break
 
            # Location of the storm
            values = codes_get_array(bufr, "#%d#meteorologicalAttributeSignificance" % rank1)
            if len(values) == 1:
                significance = values[0]
            else:
                for j in range(len(values)):
                    if values[j] != CODES_MISSING_LONG:
                        significance = values[j]
                        break
 
            if significance == 1:
                lat = codes_get_array(bufr, "#%d#latitude" % rank1)
                lon = codes_get_array(bufr, "#%d#longitude" % rank1)
                press = codes_get_array(bufr, "#%d#pressureReducedToMeanSeaLevel" % (i + 1))*0.01
            else:
                print('ERROR: unexpected meteorologicalAttributeSignificance=', significance)
 
            # Location of maximum wind
            values = codes_get_array(bufr, "#%d#meteorologicalAttributeSignificance" % rank3)
            if len(values) == 1:
                significanceWind = values[0]
            else:
                for j in range(len(values)):
                    if values[j] != CODES_MISSING_LONG:
                        significanceWind = values[j]
                        break
 
            if significanceWind == 3:
                latWind = codes_get_array(bufr, "#%d#latitude" % rank3)
                lonWind = codes_get_array(bufr, "#%d#longitude" % rank3)
                wind10m = codes_get_array(bufr, "#%d#windSpeedAt10M" % (i + 1))*ms2knots
            else:
                print('ERROR: unexpected meteorologicalAttributeSignificance=', significanceWind)
 
            for k in range(len(memberNumber)):
                try:
                    rmax=gc_dist(lat[k], lon[k], latWind[k], lonWind[k])
                except:
                    rmax=0
                    
                try:
                    data[k][i] = [lat[k], lon[k], press[k], latWind[k], lonWind[k], wind10m[k], rmax]
                except:
                    data[k][i] = [CODES_MISSING_DOUBLE, CODES_MISSING_DOUBLE, CODES_MISSING_DOUBLE, 
                                  CODES_MISSING_DOUBLE, CODES_MISSING_DOUBLE, CODES_MISSING_DOUBLE]

            # ---------------------------------------- Print the values -------------
 
        for m in range(len(memberNumber)):
            
            aid=getAid(memberNumber[m])
            if(verb): 
                print("== Member  %d  aid: %s" % (memberNumber[m],aid))
                print("step  latitude  longitude   pressure  latitude   longitude    wind    rmax")
                
            # -- check intital tau...if 0,6,12 okay -- otherwise skip
            #
            tau00Check=data[m][0][0] != CODES_MISSING_DOUBLE and data[m][0][1] != CODES_MISSING_DOUBLE
            try:
                tau06Check=data[m][1][0] != CODES_MISSING_DOUBLE and data[m][1][1] != CODES_MISSING_DOUBLE
            except:
                tau06Check=0
                
            try:
                tau12Check=data[m][2][0] != CODES_MISSING_DOUBLE and data[m][2][1] != CODES_MISSING_DOUBLE
            except:
                tau12Check=0
                                    
            if tau00Check:
                rlat00=data[m][0][0]
                rlon00=data[m][0][1]
                (stmid,dist)=comp2BTstmids(rlat00,rlon00,btlatlons,tolNN,tol9X,
                                           aid,verb=verb)
                if(stmid != None):
                    if(verb): print "AAA tau000000 -- stmid: ",stmid,' bufrDtg: ',bufrDtg,\
                      ' itau00: %02d'%(timePeriod[0]),' aid: ',aid,\
                      'rlat/lon00: %5.1f %6.1f'%(rlat00,rlon00),' dist: %4.0f'%(dist)
                    
                else:  continue
            
            elif tau06Check:
                rlat06=data[m][1][0]
                rlon06=data[m][1][1]
                (stmid,dist)=comp2BTstmids(rlat06,rlon06,btlatlons,tolNN,tol9X,
                                           aid,verb=verb)
                # -- require NN storms to have a tau0 posit
                #
                if(stmid != None and Is9X(stmid)):
                    if(verb): print "AAA tau666666 -- stmid: ",stmid,' bufrDtg: ',bufrDtg,\
                      ' itau06: %02d'%(timePeriod[1]),' aid: ',aid,\
                      'rlat/lon06: %5.1f %6.1f'%(rlat06,rlon06),' dist: %4.0f'%(dist)
                    
                else:  continue
                
            elif tau12Check:
                rlat12=data[m][2][0]
                rlon12=data[m][2][1]
                (stmid,dist)=comp2BTstmids(rlat12,rlon12,btlatlons,tolNN,tol9X,
                                           aid,verb=verb)
                if(stmid != None and Is9X(stmid)):
                    if(verb): print "AAA tau121212 -- stmid: ",stmid,' bufrDtg: ',bufrDtg,\
                      ' itau12: %02d'%(timePeriod[2]),' aid: ',aid,\
                      'rlat/lon12: %5.1f %6.1f'%(rlat12,rlon12),' dist: %4.0f'%(dist)
                    
                else:  continue
                
            else:
                continue
                
            for s in range(len(timePeriod)):
                
                if data[m][s][0] != CODES_MISSING_DOUBLE and data[m][s][1] != CODES_MISSING_DOUBLE:
                    
                    #if(verb):
                        #print(" {:>3d}{}{:>6.1f}{}{:>6.1f}{}{:>8.1f}{}{:>6.1f}{}{:>6.1f}{}{:>6.1f}{}{:>6.1f}".format(
                            #timePeriod[s], '  ', data[m][s][0], '     ', data[m][s][1], '     ', data[m][s][2], '  ',
                            #data[m][s][3], '     ', data[m][s][4], '     ', data[m][s][5],'     ', data[m][s][6]))
                    
                    itau=timePeriod[s]
                    rlat=data[m][s][0]
                    rlon=data[m][s][1]
                    pmin=data[m][s][2]
                    vmax=data[m][s][-2]
                    rmax=data[m][s][-1]
                    (clat,clon,ilat,ilon,hemns,hemew)=Rlatlon2ClatlonFull(rlat,rlon)
                    ipmin=mf.nint(pmin)
                    ivmax=mf.nint(vmax)
                    irmax=mf.nint(rmax)
                    acard=makeAdeckCard(stmid,aid,dtg,itau,ilat,ilon,hemns,hemew,ipmin,ivmax,irmax)
                    if(verb): print acard.strip()
                    MF.append2KeyDictList(acards, stmid, aid, acard)
                    
                # -----------------------------------------------------------------------
                
        
        cnt += 1
 
        # release the BUFR message
        codes_release(bufr)
 
    # close the file
    f.close()
    
    return
    

def getBTlatlons(dtg,tD,dupchk=0,selectNN=1):

    btlatlons={}
    (bstmids,btcs)=tD.getStmidBtcsDtg(dtg,dupchk=dupchk,selectNN=selectNN)

    for bstmid in bstmids:
        rc=btcs[bstmid]
        btlatlons[bstmid]=rc[0:2]
        
    return(btlatlons)
        

def crackBufr(dtg,btlatlons,tdir,odir,
              odirS=None,
              override=0,verb=0,
              tolNN=180.0,tol9X=240.0,bypass77=0):
    

    def getlat(clat):
        basin=clat[-1]
        tt=clat.split('deg')
        t1=tt[0]
        t2=tt[1]
        if(mf.find(t1,'p')):
            rll=float(t1.replace('p','.'))
        else:
            rll=float(t1)
        if(basin == 'W'): rll=360+rll
        return(rll)


    def doDfile(dfile,override=0,verb=0):
        
        detFile=0
        if(dfile in dfiles): detFile=1
        
        tt=dfile.split('_')
        blat=tt[-2]
        blon=tt[-3]
        bname=tt[-4]
        rlat=getlat(blat)
        rlon=getlat(blon)
        if(verb): print '11111---- %12s  %5.1f %6.1f  dfile: %s'%(bname,rlat,rlon,dfile)
        bufr_decode(dfile,btlatlons,verb=verb)

    # mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
    #
    ioverride=override
    
    # -- clean off previous adecks -- cases where we erroneous did an adeck
    #
    if(ioverride):
        curAdecks=glob.glob("%s/adeck*%s*"%(odir,dtg))
        if(odirS != None):
            curAdecks=curAdecks+glob.glob("%s/adeck*%s*"%(odirS,dtg))
            
        for cura in curAdecks:
            cmd="rm %s"%(cura)
            mf.runcmd(cmd)
            
    dfiles=glob.glob("%s/*ECMF*"%(tdir))
    gfiles=glob.glob("%s/*ECEP*"%(tdir))

    for dfile in gfiles:
        rc=doDfile(dfile,override=ioverride,verb=verb)
                
    for dfile in dfiles:
        rc=doDfile(dfile,override=ioverride,verb=verb)
    
    return    
        
        
def makeAdeckCard(stmid,aid,dtg,tau,ilat,ilon,hemns,hemew,ipmin,ivmax,irmax):
    
    (snum,b1id,year,b2id,tstm2id,tstm1id)=getStmParams(stmid)
    
    adecknum=98
    adeckname=aid
    
    r34ne=r34se=r34sw=r34nw=0
    ipoci=0
    iroci=0

    acard1=''
    acard2=''
    acard3=''

    acard0="%2s, %2s, %10s, %2s, %4s, %3d,"%(b2id,str(snum),dtg,adecknum,adeckname,tau)

    oextra=" %4d, %4d, %3d"%(ipoci,iroci,irmax)

    # add \n at end of card to be consistent with real adecks
    #
    acard1=acard0+" %3d%1s, %4d%1s, %3d, %4d,   ,  34, NEQ, %4d, %4d, %4d, %4d,%s\n"%\
        (ilat,hemns,ilon,hemew,ivmax,ipmin,r34ne,r34se,r34sw,r34nw,oextra)
    
    return(acard1)
    

def doRsync2Hfip(odir,rdir,ropt='',verb=0):
    
    rsyncOpt="-alv"
    cmd="rsync %s %s/ %s/"%(rsyncOpt,odir,rdir)
    mf.runcmd(cmd,ropt)

#llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
# local defs
#

class TcOpsCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv

        self.argopts={
            1:['dtgopt',    'no default'],
            }

        self.defaults={
            }

        self.options={
            'ropt':            ['N','','norun',' norun is norun'],
            'verb':            ['V',0,1,'verb=1 is verbose'],
            'override':        ['O',0,1,'override bufr cracking'],
            'doBufr':          ['B',1,0,'do NOT crack the bufr'],
            'doAD2':           ['A',1,0,'do NOT do adc and ad2'],
            'doWget':          ['W',1,0,'do NOT wget'],
            'doEpsPlots':      ['E',1,0,'do NOT run w2-tc-g-epsanal-dss-ad2.py...'] 
            }

        self.purpose='''
mirror ecmwf wmo essential of tcbufr'''

        self.examples='''
%s 2004010100     : pull from archive dir for 2004'''


MF.sTimer('all')

argv=sys.argv
CL=TcOpsCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main
#

dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)

tbdir=w2.TcpsdRR2DatDir

af=w2.EcmwfWmoFtpserver
al=w2.EcmwfWmoLogin
ap=w2.EcmwfWmoPasswd

tbdir=EcmwfWmoBufrLocalDir
obdir=TcAdecksEcmwfDir
rbdir="%s/tc/ecmwf"%(w2.EsrlHttpIntranetDocRootFiorino)
mf.ChkDir(rbdir)

MF.sTimer('all')

tD=TcData(dtgopt=dtgopt)

for dtg in dtgs:

    rcS=CurShemOverlap(dtg)
    (isShemOver,curyear,curyearp1)=rcS
    sdir="%s0000"%(dtg)
    tdir="%s/%s/%s"%(tbdir,curyear,dtg)
    odir="%s/%s/wmo"%(obdir,curyear)
    rdir="%s/%s/wmo"%(rbdir,curyear)
    
    if(verb):
        print 'SSS',isShemOver

    mf.ChkDir(tdir,diropt='mk')
    mf.ChkDir(odir,diropt='mk')
    mf.ChkDir(rdir,diropt='mk')
    
    odirS=rdirS=None
    if(isShemOver):
        odirS="%s/%s/wmo"%(obdir,curyearp1)
        mf.ChkDir(odirS,diropt='mk')

        rdirS="%s/%s/wmo"%(rbdir,curyearp1)
        mf.ChkDir(rdirS,diropt='mk')
    
    if(doWget):
        MF.sTimer('get-wmo-tc: %s'%(dtg))
        mf.ChangeDir(tdir)
        logpath="%s/db.wget.%s.txt"%(tdir,dtg)
        cmd="wget -nv -m -nd -T 180 -t 2 \"ftp://%s:%s@%s/%s/*tropical_cyclone*\""%(al,ap,af,sdir)
        mf.runcmd(cmd,ropt)
        MF.dTimer('get-wmo-tc: %s'%(dtg))
        
    if(doBufr):
        
        acards={}
        btlatlons=getBTlatlons(dtg, tD)
        MF.sTimer('get-wmo-tc: %s'%(dtg))
        rc=crackBufr(dtg,btlatlons,tdir,odir,odirS=odirS,
                     override=override,verb=verb)

        # -- uniq the acards lisr
        #
        MF.uniqDict2List(acards)
        
        if(verb):
            for kk in acards.keys():
                print kk
                ss=acards[kk].keys()
                if('EMDT' in ss):
                    ocards=acards[kk]['EMDT']
                    for ocard in ocards:
                        print ocard.strip()
                    print
                    print
                    
        # -- output
        #
        
        kk1=acards.keys()
        
        gotShem=0
        for k1 in kk1:
            allcards=[]
            kk2=acards[k1].keys()
            for k2 in kk2:
                ocards=acards[k1][k2]
                allcards=allcards+ocards
                
            odirCur=odir
            tt=k1.split('.')
            stmyear=tt[-1]
            if(stmyear == curyearp1):
                opath="%s/adeck-ecmwf-wmo.%s.%s"%(odirS,dtg,k1)
                gotShem=1
            else:
                opath="%s/adeck-ecmwf-wmo.%s.%s"%(odir,dtg,k1)
            print 'OOO: ',opath
            MF.WriteList2Path(allcards, opath)
    
        MF.dTimer('get-wmo-tc: %s'%(dtg))
        
# -- rsync over to hfip/fiorino/tc
#
if(doRsync2Hfip):
    rc=doRsync2Hfip(odir,rdir,ropt=ropt)
    if(gotShem):
        rc=doRsync2Hfip(odirS,rdirS,ropt=ropt)

    
# -- do adc and ad2
#
if(doAD2):
    oOpt=''
    if(override): oOpt='-O1'
    MF.sTimer('adc-ad2-update')
    cmd="%s/w2-tc-convert-tm-mftrkN-to-atcf-adeck.py %s -d %s -A %s"%(w2.PrcDirTcdatW2,'ec-wmo',dtgopt,oOpt)
    mf.runcmd(cmd,ropt)
    MF.dTimer('adc-ad2-update')

    MF.sTimer('ad2-9X-update')
    cmd="%s/w2-tc-dss-ad2.py %s -d %s -9"%(w2.PrcDirTcdatW2,'ec-wmo',dtgopt)
    mf.runcmd(cmd,ropt)
    MF.dTimer('ad2-9X-update')

# -- do eps plots
#
if(doEpsPlots):
    MF.sTimer('g.eps-plots')
    cmd="%s/w2-tc-g-epsanal-dss-ad2.py %s ecmb"%(w2.PrcDirTcdatW2,dtgopt)
    mf.runcmd(cmd,ropt)
    MF.dTimer('g.eps-plots')

    # -- rsync to wxmap2.com
    #
    rc=rsync2Wxmap2('tceps',ropt)
    
    
MF.dTimer('all')
sys.exit()
