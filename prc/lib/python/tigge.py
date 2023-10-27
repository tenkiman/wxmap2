from tcbase import *
import const
from math import sqrt

def XmlTime2Dtg(xtime,domin=0):

    dtg=None
    yyyy=xtime[0:4]
    mm=xtime[5:7]
    dd=xtime[8:10]
    hh=xtime[11:13]
    mn=xtime[14:16]

    dtg=yyyy+mm+dd+hh
    if(domin):
        dtg=dtg+':'+mn
    return(dtg)
    


def ParseHeader(h,verb=0):

    hc=h[0].childNodes

    pcenter=btime=ctime=product=genapp=None
    
    for i in range(0,hc.length):
        hh=hc[i]
        if(hh.nodeType == 1):
            nname=str(hh.nodeName)
            if(nname == 'productionCenter'):
                pcenter=str(hh.firstChild.data)

            elif(nname == 'baseTime'):
                btime=str(hh.firstChild.data)
                
            elif(nname == 'creationTime'):
                ctime=str(hh.firstChild.data)

            elif(nname == 'product'):
                product=str(hh.firstChild.data)

            elif(nname == 'generatingApplication'):
                h2=hh.childNodes
                
                genapp=str(h2[1].firstChild.data)

    
    bdtg=XmlTime2Dtg(btime)
    cdtg=XmlTime2Dtg(ctime,domin=1)

    if(verb):
        print 'HHH pcenter:   ',pcenter
        print 'HHH product:   ',product
        print 'HHH genapp:    ',genapp
        print 'HHH bdtg:      ',bdtg
        print 'HHH cdtg:      ',cdtg
        
    return(bdtg,cdtg,pcenter,product,genapp)
                
def ParseForecastId(adata):

    ftype=None
    fmember=None
    
    for i in range(0,len(adata)):
        akey=str(adata[i][0])
        aval=str(adata[i][1])
        #print 'aaaaa ',i,akey,aval

        if(akey == 'type'):
            ftype=aval
        elif(akey == 'member'):
            fmember=aval

    return(ftype,fmember)


def MakeAdeckCard(bdtg,stmid,atcfaid,itau,clat,clon,rpmin,rvmax):

    
    if(len(stmid.split('.')) == 2):
        b2id=Basin1toBasin2[stmid[2]]
        stmnum=stmid[0:2]

    elif(len(stmid.split('_')) == 2):
        clat=stmid.split('_')[0]
        clon=stmid.split('_')[1]
        (rlat,rlon)=Clatlon2Rlatlon(clat,clon)
        b1id=tcbasinb1id(rlat,rlon,b3id='')
        b2id=Basin1toBasin2[b1id]
        stmnum=stmid

    else:
        (rlat,rlon)=Clatlon2Rlatlon(clat,clon)
        b1id=tcbasinb1id(rlat,rlon,b3id='')
        b2id=Basin1toBasin2[b1id]
        stmnum=stmid
        
    if(rvmax == None):
        rvmax=0.0
    
    if(rpmin == None):
        ipmin=0
    else:
        ipmin=int(rpmin+0.5)
        
    ivmax=int(rvmax*const.ms2knots+0.5)

    #AL, 02, 2008072006, 03, AVNO,  96, 699N,  253W,  19, 1002, XX,  34, NEQ,    0,    0,    0,    0, 
    acard="%2s, %s, %10s, 22, %4s, %3d, %4s, %5s, %3d, %4d, XX,  34, NEQ,    0,    0,    0,    0,"%(b2id,stmnum,bdtg,atcfaid,itau,clat,clon,ivmax,ipmin)

    if(clat == '999X'): acard=None

    return(acard)




def ConvertRlatlon2Clatlon(rlat,rlon,alat,alon):

    nshemi=None
    ewhemi=None
    
    for i in range(0,len(alat)):
        akey=str(alat[i][0])
        aval=str(alat[i][1])
        if(akey == 'units'):
            nshemi=aval[-1]

    for i in range(0,len(alon)):
        akey=str(alon[i][0])
        aval=str(alon[i][1])
        if(akey == 'units'):
            ewhemi=aval[-1]

    if(nshemi == 'S'):
        rlat=rlat*(-1.0)
    if(ewhemi == 'W'):
        rlon=360.0-rlon

    (clat,clon)=Rlatlon2Clatlon(rlat,rlon)

    return(clat,clon)



def ForecastId2AtcfModel(ftype,fmember):

    if(ftype == 'ensembleForecast' and fmember != None):
        if(int(fmember) == 0):
            aid='ECNT'
            aid='EP00'
        else:
            aid='EP%02d'%(int(fmember))
    elif(ftype == 'forecast'):
        aid='EDET'
    elif(ftype == 'analysis'):
        aid='EANL'
    else:
        aid='XXXX'

    return(aid)
        

def GetStmidFromTcBts(clat,clon,btcs,atcfaid='uuuu',distmax=4.0,verb=0):

    (rlat,rlon)=Clatlon2Rlatlon(clat,clon)

    hitids=[]
    
    mindist=99999.9
    stmid=None
    
    stmids=btcs.keys()
    stmids.sort()
    
    for stmid in stmids:
        vmax=btcs[stmid][2]
        pmin=btcs[stmid][3]
        btlat=btcs[stmid][0]
        btlon=btcs[stmid][1]

        dist=sqrt((btlat-rlat)*(btlat-rlat)+(btlon-rlon)*(btlon-rlon))

        if(dist < distmax):
            hitids.append([dist,stmid,btlat,btlon])

        if(verb): print 'SSSS: ',stmid,atcfaid,clat,clon,btlat,btlon,vmax,pmin,dist,distmax,len(hitids)


    #
    # multiple stmids -- go for non 9X
    #
        
    if(len(hitids) > 1):
        stmid=None
        for hitid in hitids:
            snum=int(hitid[1][0:2])
            if(snum < 50):
                print 'HHHHHHHHHHHHH mulitple hits: ',hitid[1],atcfaid
                stmid=hitid[1]
                btlat00=hitid[2]
                btlon00=hitid[3]
        #
        # no storms in warnning -- go for nearest
        #
        if(stmid == None):
            mindist=9999999.9
            for hitid in hitids:
                dist=hitid[0]
                if(dist < mindist):
                    mindist=dist
                    minstmid=hitid[1]
                    btlat00=hitid[2]
                    btlon00=hitid[3]

            
            stmid=minstmid
            
    elif(len(hitids) == 1):
        stmid=hitids[0][1]
        btlat00=hitids[0][2]
        btlon00=hitids[0][3]
                
    else:
        stmid='99X.9999'
        btlat00=999.9
        btlon00=999.9

    return(stmid,btlat00,btlon00)
        


def GetEpsStmid(trkdata,trkdataAnl,btcs,atcfaid,ddname,verb=0,warn=0,verbbt=0):


    kk=trkdata.keys()
    kk.sort()

    gottau00=0
    gottau12=0
    gotstmid=0
    
    for k in kk:
        itau=int(k)

        if(itau <= 12 and verb):
            print 'tigge.GetEpsStmid: ',ddname,itau,atcfaid,trkdata[k],gottau00
            
        if(itau > 12):
            break
        
        if(itau == 0):
            (clat,clon,rpmin,rvmax)=trkdata[k]
            (stmid,btlat00,btlon00)=GetStmidFromTcBts(clat,clon,btcs,atcfaid,verb=verbbt)
            if(stmid != '99X.9999'):
                gotstmid=1
                gottau00=1

        if(itau > 0 and itau <= 12 and gottau00 == 0):
            
            gotanl=0
            (clat,clon,rpmin,rvmax)=trkdata[k]
            try:
                (clat,clon,rpmin,rvmax)=trkdataAnl[ddname]
                warncard='IIII-GetEpsStmid() tracker has no tau0'
                clat=clat.strip()
                if(len(clat) == 2 and clat[0] == '0'):
                    (clat,clon,rpmin,rvmax)=trkdata[k]
                    gotanl=0
                    if(warn): print warncard,'-- anl posit is 0N 0W, gotanl=0 using btcs for: ',k,clat,clon
                else:
                    if(warn): print warncard,'-- using EANL tau0 ddname: %',ddname,'clat/clon/rpmin/rvmax: ',clat,clon,rpmin,rvmax
                    gotanl=1
            except:
                if(warn): print warncard,' a TCgenesis track -- either first tau > 12 h or could not find tau=0 posit...'
                continue
                
            (stmid,btlat00,btlon00)=GetStmidFromTcBts(clat,clon,btcs,atcfaid,verb=verbbt)

            if(stmid != '99X.9999'):
                gotstmid=1
                if(not(gotanl)):
                    (clat,clon)=Rlatlon2Clatlon(btlat00,btlon00)
                trkdata[0]=(clat,clon,rpmin,rvmax)
    
    if(not(gotstmid)):
        tt=ddname.split('_')
        elat=tt[1]
        elon=tt[2]
        estmid="%s_%s"%(elat,elon)
        stmid=estmid
        
    if(verb): print 'gotstmid: ',gotstmid,gottau00,gottau12,stmid,'dddddd'

    return(stmid)
        
        
def ParseData(data,trkdataAnl,bdtg,btcs,adecks,adtaus,adstmids,adaids,verb=0):

    def dumpacard(acard,itau):

        #print 'FFFFFF===== , %03d %6s %6s'%(itau,clat,clon),rpmin,rvmax
        
        try:
            adtaus[stmid,atcfaid].append(itau)
        except:
            adtaus[stmid,atcfaid]=[]
            adtaus[stmid,atcfaid].append(itau)
            
        adecks[stmid,atcfaid,itau]=acard
                

    dd=data.getElementsByTagName('disturbance')
    adata=data.attributes.items()

    (ftype,fmember)=ParseForecastId(adata)
    (atcfaid)=ForecastId2AtcfModel(ftype,fmember)

    if(verb):
        print 'TTT ftype:     ',ftype
        print 'TTT fmember:   ',fmember
        print 'TTT atcfaid:   ',atcfaid


    
        
    for j in range(0,dd.length):

        gotstmid=0

        dds=dd[j]
        try:
            ddname=dds.getAttribute('ID')
        except:
            ddname=None
        ddname=ddname.replace(' ','')

        ddsfs=dds.getElementsByTagName('fix')

        gottau00=0
        gottau12=0

        trkdata={}

        nfixes=ddsfs.length
        if(verb): print 'NNNNNNNNNNNNNNN ',ddname,' nfixes: ',nfixes

        if(nfixes == 0):
            if(verb): print '00000000000000 posits for ',ddname
            continue
            

        for k in range(0,nfixes):

            tau=None
            fix=ddsfs[k]
            fixa=fix.attributes
            for l in range(0,fixa.length):
                fixai=fixa.items()
                fixakey=str(fixai[l][0])
                fixaval=str(fixai[l][1])
                if(fixakey == 'hour'):
                    tau=fixaval

            
            fixc=fix.childNodes

            lat=lon=tcparms=None
            for l in range(0,fixc.length):
                fixtau=fixc[l]
                if(fixtau.nodeType == 1):
                    nname=str(fixtau.nodeName)
                    if(nname == 'latitude'):
                        lat=fixtau
                    elif(nname == 'longitude'):
                        lon=fixtau
                    elif(nname == 'cycloneData'):
                        tcparms=fixtau

            if(lat != None and lon != None):
                try:
                    rlat=float(lat.firstChild.data)
                    rlon=float(lon.firstChild.data)
                    alat=lat.attributes.items()
                    alon=lon.attributes.items()
                except:
                    print 'WWW(tigge.ParseData) lat/lon: ',lat.firstChild.data,lon.firstChild.data,'; continue...'
                    rlat=None
                    None

            #if(verb): print 'fff k: ',k,tau,rlat,rlon,alat,alon

            pmin=vmax=rpmin=rvmax=None
            if(tcparms != None):

                tcparmsc=tcparms.childNodes

                for l in range(0,tcparmsc.length):
                    tcc=tcparmsc[l]
                    if(tcc.nodeType == 1):
                        nname=str(tcc.nodeName)
                
                        if(nname == 'minimumPressure'):
                            pmin=tcc
                        elif(nname == 'maximumWind'):
                            vmax=tcc

                if(pmin != None):
                    cpmin=None
                    pc=pmin.childNodes
                    for i in range(0,pc.length):
                        pcc=pc[i]
                        nname=str(pcc.nodeName)
                        if(nname == 'pressure'):
                            pmin=pcc
                        
                if(vmax != None):
                    vc=vmax.childNodes
                    for i in range(0,vc.length):
                        vcc=vc[i]
                        nname=str(vcc.nodeName)
                        if(nname == 'speed'):
                            vmax=vcc


            #print 'TTTTTTTTTTTTTTTTTTT ',pmin,vmax
            
            if(pmin != None):
                try:
                    rpmin=float(pmin.firstChild.data)
                    apmin=pmin.attributes.items()
                    #print 'ppppp ',apmin[0],apmin[1]
                except:
                    print 'WWW(tigge.ParseData) pmin: ',pmin.firstChild.data,'; continue...'
                    None

            if(vmax != None):
                try:
                    rvmax=float(vmax.firstChild.data)
                    avmax=vmax.attributes.items()
                except:
                    print 'WWW(tigge.ParseData) vmax: ',vmax.firstChild.data,'; continue...'
                    None
                    
            if(rlat == None): continue
                
            (clat,clon)=ConvertRlatlon2Clatlon(rlat,rlon,alat,alon)
            if(tau == None):
                itau=0
            else:
                itau=int(tau)

            #
            # dump to trk hash
            #
            trkdata[itau]=(clat,clon,rpmin,rvmax)
            if(ftype == 'analysis'): trkdataAnl[ddname]=(clat,clon,rpmin,rvmax)


        stmid=GetEpsStmid(trkdata,trkdataAnl,btcs,atcfaid,ddname,verb=verb)
        
        kk=trkdata.keys()
        kk.sort()

        for k in kk:
            itau=int(k)
            (clat,clon,rpmin,rvmax)=trkdata[k]
            acard=MakeAdeckCard(bdtg,stmid,atcfaid,itau,clat,clon,rpmin,rvmax)
            if(acard != None):  dumpacard(acard,itau)

        try:
            adstmids[atcfaid].append(stmid)
        except:
            adstmids[atcfaid]=[]
            adstmids[atcfaid].append(stmid)

        adaids.append(atcfaid)
            
        if(verb): print 'AAA ',stmid,atcfaid,acard
            
                         





