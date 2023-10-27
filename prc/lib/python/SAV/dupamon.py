import rlcompleter
import readline
readline.parse_and_bind("tab: complete")

import os
import sys
from math import sqrt

import struct
import array

import mf

from sakimon import upamon

class dupamon(upamon):

    dlatmax=2.0
    distmin=1.5
    distprob=0.25

    def __init__(self,yyyymm=None,var='t',tsynhour='00',tsubtype='101',initopt=None):

        self.tsynhour=tsynhour
        self.tsubtype=tsubtype
        
        self.uPaDir=self.BaseDir+'/upa'
        
        self.dotesting=0

        donoload=0

        if(yyyymm == None):
            
            yyyymm='198001'
            yyyymm='197607'
            
            #
            # if testing use tmp
            #
            self.ObsDir=self.BaseDir+'/tmp'
            self.uPaDir=self.BaseDir+'/tmp'
            self.dotesting=1

            
        self.yyyymm=yyyymm
            

        self.upath="%s/%s"%(self.uPaDir,'sakimon.t.%s.txt'%(self.yyyymm))

        try:
            self.fu=open(self.upath)
            print 'uPamon opening: ',self.upath
        except:
            print "EEE unable to open: %s"%(self.upath)
            print "EEE do a noload"
            donoload=1

            
        #
        # set the physical variable 
        #
        self.upavar=var

        #
        # set the stat and .ctl variables
        #
        if(var == 't'):
            self.statvars=self.StatVariablesTa
        elif(var == 'w'):
            self.statvars=self.StatVariablesWind
        else:
            self.statvars=self.StatVariables

        __opath="%s/era40.upamon.%s.%s.%s.%s.obs"%\
                 (self.ObsDir,self.upavar,self.yyyymm[0:6],self.tsynhour,self.tsubtype)
        print 'stnobs opening: ',__opath
        
        try:
            self.Ofo=open(__opath,'wb')
        except:
            raise IOError('unable to open: %s'%(__opath))


        self.openstatus=1
    
        if(donoload):
            print "WWWWWWWW no upamon stats, doing noload for: %s"%(self.yyyymm)
            stnid='alldone '
            stnrec=struct.pack('8sfffii',stnid,0.0,0.0,0.0,0,0)
            self.Ofo.write(stnrec)
            self.Ofo.close()
            self.openstatus=0


            

    def ParseStnCard(self,card):

        tt=card.split()

        stnid=tt[1]
        rlat=tt[5]
        rlon=tt[7]
        elv=tt[9]
        wmoid=tt[15]
        subtype=tt[17]
        src=tt[19]
        ndtgs=tt[21]

        nlat=len(rlat)
        nshem=rlat[nlat-1]
        rlat=float(rlat[0:nlat-1])
        if(nshem == 'S'): rlat=-rlat

        nlon=len(rlon)
        ewhem=rlon[nlon-1]
        rlon=float(rlon[0:nlon-1])
        if(ewhem == 'W'): rlon=360.0-rlon

        return(stnid,rlat,rlon,elv,wmoid,subtype,src,ndtgs)

    def LoadStnArray(self,cards,verb=0):

        stn={}
        
        for card in cards:
            (stnid,rlat,rlon,elv,wmoid,subtype,src,ndtgs)=self.ParseStnCard(card)
            
            #print len(card),card
            #print stnid,rlat,rlon,elv,wmoid,subtype,src,ndtgs
            stn[rlat]=[stnid,rlat,rlon,wmoid,subtype,src,ndtgs]

        return(stn)

    def FiltStnStats(self,ucards):

        test=0
        
        nlevs=len(self.MandatoryPressureLevels)
        nstn=0
        nsynhours=4

        fstns={}
        fdata={}

        #
        # local function to load up cards
        #
        
        def loadcards(ucards,i):
            
            dcards=[]

            datathere=0
            syncard=ucards[i]
            syntime=syncard.split()[2]
            i=i+1
            #
            #  skip title
            #
            i=i+1
            for j in range(0,nlevs):
                dcards.append(ucards[i])
                tt=ucards[i].split()
                #
                # output only if there are some count, even if none are good (tt[7])
                #
                dtest=int(tt[6])
                if(dtest > 0): datathere=1
                #print j,ucards[i]
                #if(tt[0] == '500' and datathere): print tt
                i=i+1

            i=i+1
            return(syntime,dcards,datathere,i)


        i=0
        while(1):
            
            try:
                (stnid,rlat,rlon,elv,wmoid,subtype,src,ndtgs)=self.ParseStnCard(ucards[i])
            except:
                return(fstns,fdata)

            i=i+1

            for j in range(0,nsynhours):
                (synhour,dcards,datathere,i)=loadcards(ucards,i)
                if(synhour == self.tsynhour and subtype == self.tsubtype and datathere):
                    fstns[rlat,stnid]=[stnid,rlat,rlon,elv,wmoid,subtype,src,ndtgs]
                    fdata[rlat,stnid]=[]
                    flist=[]
                    for dcard in dcards:
                        flist=[]
                        dd=dcard.split()
                        ff=[]
                        for d in dd:
                            try:
                                fd=float(d)
                            except:
                                fd=self.stnundef
                            flist.append(fd)
                            
                        fdata[rlat,stnid].append(flist)
                            
                    nstn=nstn+1
                    #print 'iiiiiiii ',rlat,nstn,stnid,subtype,datathere,synhour,i
                    #print rlat,fstns[rlat]

            if(test and nstn > 10):
                return(fstns,fdata)

    def DupCheck(self,stns,verb=0):

        keys=stns.keys()
        keys.sort()

        
        imax=100

        prcflg={}

        for k in keys:
            prcflg[k]=[0]
        
        i=0
        for k in keys:

            curflg=prcflg[k][0]

            #
            # if the flag has been set by an earlier check; skip
            #
            if(curflg != 0):
                #print 'qqqqqqqqqqqqqqqqqqqq ',i,k[1],curflg
                i=i+1
                continue
            
            rlat0=stns[k][1]
            rlon0=stns[k][2]

            #print 'qqqqqqqqqqqqqqqqqq ',i,k[1],len(prcflg[k]),curflg
            dndx={}
            for j in range(i+1,i+imax):
                try:
                    rlat1=stns[keys[j]][1]
                    rlon1=stns[keys[j]][2]
                    dlat=abs(rlat1-rlat0)
                    dlon=rlon1-rlon0
                    dd=sqrt(dlat*dlat + dlon*dlon)
                    if(dlat > self.dlatmax): break
                    #print i,j,dlat,dlon,dd
                    dndx[dd]=j
                except:
                    continue

            ndndx=len(dndx)
            if(ndndx > 0):
                dkeys=dndx.keys()
                dkeys.sort()
                for dk in dkeys:
                    #print 'kkkkkkkkkk ',k,i,ndndx,dk,dndx[dk]
                    #print dk,self.distmin
                    if(dk < self.distmin):
                        idx=dndx[dk]
                        kd=keys[idx]

                        wmoid0=stns[k][4]
                        wmoid1=stns[kd][4]

                        st0=stns[k][5]
                        st1=stns[kd][5]

                        src0=stns[k][6]
                        src1=stns[kd][6]

                        ndtg0=stns[k][7]
                        ndtg1=stns[kd][7]

                        if(wmoid0 == wmoid1):
                            code='DEFINATE Dup'
                            dupcode0='D'
                            dupcode1='d'
                                
                        elif(dk<self.distprob):
                            code='Probable Dup'
                            dupcode0='P'
                            dupcode1='p'
                                
                        else:
                            code='maybe.......'
                            dupcode0='M'
                            dupcode1='m'

                        prcflg[k]=[dupcode0,kd]
                        prcflg[kd]=[dupcode1,k]
                        if(verb):
                            print "%5d :: %s: %4.2f :: %s %s :: %s %s :: %s %s :: %s %s :: %s %s"%\
                                  (i,code,dk,k[1],kd[1],wmoid0,wmoid1,st0,st1,src0,src1,ndtg0,ndtg1)

                        break
                        #print 'ddddddddddddddddddddddd ',i,stns[k]
                        #print 'ddddddddddddddddddddddd ',idx,stns[skey]

            i=i+1

        return(prcflg)

    def StatNdx(self):

        if(self.upavar == 't'):
            ncg=7
            na0=1
            na1=5
            nc0=6
            nc1=10
            nbc0=11
            nbc1=12
            ncbc=13
        elif(self.upavar == 'w'):
            ncg=7
            na0=1
            na1=5
            nc0=6
            nc1=10
            nbc0=-1
            nbc1=-1
            ncbc=-1

        return(ncg,na0,na1,nc0,nc1,nbc0,nbc1,ncbc)


    def StnHeaderSfc(self,dupflag,stn,verb=0):

        nlevs=len(self.MandatoryPressureLevels)
        nvars=len(self.statvars)
        svars=self.statvars

        stndt=0.0
        stnlev=nlevs+1
        stnflag=1

        longid=stn[0]

        rlat=stn[1]
        rlon=stn[2]
        
        elevation=float(stn[3])
        wmoid=stn[4]
        subtype=float(stn[5])
        source=float(stn[6])

        try:
            iwmoid=int(wmoid)
        except:
            iwmoid=-999
            
        if(wmoid[0:1] == 'p'):
            if(verb): print 'pppppppppp wmoid: ',wmoid
            iwmoid=-int(wmoid[1:6])
        elif(iwmoid <0):
            iwmoid=99999

        hemns='n'
        if(rlat < 0): hemns='s'

        stnid="%s%03.0f%04.0f"%(hemns,(abs(rlat)*10.0),(rlon*10))
            
        stnhead=struct.pack('8sfffii',stnid,rlat,rlon,stndt,stnlev,stnflag)

        fdupflag=-1.0
        if(dupflag == 'D'): fdupflag=10.0
        if(dupflag == 'P'): fdupflag=1.0
        if(dupflag == 'M'): fdupflag=0.5
        if(dupflag == 0): fdupflag=0.0
        
        if(elevation == -999): elevation=self.undef
        stnsfc=struct.pack('%df'%(self.Nsfcvar+1),float(iwmoid),subtype,source,elevation,fdupflag,rlat,rlon)

        if(verb): print 'sssssssssss ',stnid,rlat,rlon,stndt,stnlev,stnflag,float(iwmoid),subtype,source,elevation,fdupflag

        stnpart1=stnhead+stnsfc

        self.Ofo.write(stnpart1)

        


        

    def MergeObs(self,dupflag,fdata,fstns,k0,k1,opt='merge',verb=0):

        nlevs=len(self.MandatoryPressureLevels)
        nvars=len(self.statvars)
        svars=self.statvars

        ncg,na0,na1,nc0,nc1,nbc0,nbc1,ncbc=self.StatNdx()


        def printcard(title,flist,n):
            ocard='%s: '%(title)
            for j in range(0,n+1):
                fo=flist[j]
                if(fo == self.stnundef):
                    ocard="%s%s "%(ocard,'******')
                else:
                    ocard="%s%6.2f "%(ocard,fo)
            print ocard

        #
        # clean up and output
        #

        if(opt=='cleanonly'):

            #
            # write out the station header and sfc vars including the duplicate flag
            #
            
            self.StnHeaderSfc(dupflag,fstns[k0],verb=verb)

            dlist=[]
            
            for i in range(0,nlevs):

                f0=fdata[k0][i]
                doprint=0
                if(f0[0] == 500 and verb): doprint=1
                
                #if(doprint): printcard('---  k',f0,nvars)
                cg0=f0[ncg]
                odata=f0
                    
                if(odata[ncbc] == 0.0):
                    for j in range(nbc0,nbc1+1):
                        odata[j]=self.stnundef
                        ####odata[ncbc]=self.stnundef
                        
                    if(doprint): printcard('FFF  k',odata,nvars)

                dlist=dlist+odata

            stndata=array.array('f')
            stndata.fromlist(dlist)
            stndata.write(self.Ofo)
            
            return

        #
        # merging of dups and output
        #

        nobs0=0
        nobs1=0
        
        dlist=[]
        
        for i in range(0,nlevs):

            doprint=0
            if(fdata[k0][i][0] == 500.0 and verb): doprint=1

            if(doprint):
                print self.statvars
                printcard('qqq  k0',fdata[k0][i],nvars)
                printcard('qqq  k1',fdata[k1][i],nvars)
                
            f0=fdata[k0][i]
            f1=fdata[k1][i]
            cg0=f0[ncg]
            cg1=f1[ncg]

            if(cg0 == self.stnundef): cg0=0.0
            if(cg1 == self.stnundef): cg1=0.0

            nobs0=nobs0+cg0
            nobs1=nobs1+cg1
                
            #
            # initialize to first
            #
                
            odata=f0

            #
            # if one dup has zero good count, set the merge to the other
            #

            if( cg0 > 0.0 and cg1 == 0.0 ):
                odata=f0

            if( cg1 > 0.0 and cg0 == 0.0 ):
                odata=f1

            #
            # merge
            #

            if( (cg0 != 0.0 and cg0 != self.stnundef) and (cg1 != 0.0 and cg1 != self.stnundef) ):

                #
                # ob,fg,an + rms
                #
                for j in range(na0,na1+1):
                    dobar=1
                    if(svars[j-1][0] == 'r'):
                        if(cg0 == 1):
                            bar=f1[j]
                            dobar=0
                        elif(cg1 == 1):
                            bar=f0[j]
                            dobar=0
                        else:
                            dobar=1
                    if(dobar):
                        bar=(f0[j]*cg0+f1[j]*cg1)/(cg0+cg1)

                    odata[j]=bar

                    #print svars[j-1],j,f0[j],cg0,f1[j],cg1,cg0+cg1,bar,dobar
                #
                # counts
                #
                for j in range(nc0,nc1+1):
                    sum=f0[j]+f1[j]
                    odata[j]=sum

            #
            # bias correction
            #

            if(ncbc > 0):

                cbc0=f0[ncbc]
                cbc1=f1[ncbc]

                if(cbc0 == self.stnundef): cbc0=0.0
                if(cbc1 == self.stnundef): cbc1=0.0

                if(cbc0 > 0.0 or cbc1 > 0.0):

                    for j in range(nbc0,nbc1+1):

                        bar=(f0[j]*cbc0+f1[j]*cbc1)/(cbc0+cbc1)
                        odata[j]=bar

                    odata[ncbc]=cbc0+cbc1

                #
                # undef bias correction
                #

                if(odata[ncbc] == 0.0):

                    for j in range(nbc0,nbc1+1):
                        odata[j]=self.stnundef
                    ### let it stay at 0: odata[ncbc]=self.stnundef

            dlist=dlist+odata
            
            if(doprint): printcard('qqq bar',odata,nvars)

        #
        # set the meta data based on the dup with the most obs
        #
        stndup=fstns[k0]
        if(nobs0 >= nobs1): stndup=fstns[k0]
        if(nobs1 > nobs0): stndup=fstns[k1]


        self.StnHeaderSfc(dupflag,stndup,verb=verb)

        stndata=array.array('f')
        stndata.fromlist(dlist)
        stndata.write(self.Ofo)
        
        

    def MergeStns(self,fstns,fdata,prcflg,verb=0):

        kk=prcflg.keys()
        kk.sort()

        ntot=0
        nout=0
        for k in kk:

            lf=len(prcflg[k])
            dupflag=prcflg[k][0]

            #print 'bbbb dupd: ',ntot,nout
            if(lf == 2):
                k0=k
                k1=prcflg[k][1]
                f0=fdata[k0][3][1]
                f1=fdata[k1][3][1]

                c0=fdata[k0][3][6]
                c1=fdata[k1][3][6]

                #
                # merge D and P
                #

                if(dupflag == 'D' or dupflag == 'P'):
                    
                    if(verb): print "DP dupd: %6.2f %s :: %s ::  %6.2f %s :: %8.2f %8.2f : %8.2f %8.2f "%\
                              (k0[0],k0[1],dupflag,k1[0],k1[1],f0,f1,c0,c1)
                    
                    self.MergeObs(dupflag,fdata,fstns,k0,k1)
                    nout=nout+1

                #
                # skip the stations second station in "definite" or "probable" dups 
                #
                elif(dupflag == 'd' or dupflag == 'p'):
                    
                    if(verb): print "dp dupd: %6.2f %s :: %s ::  %6.2f %s :: %8.2f %8.2f : %8.2f %8.2f "%\
                              (k0[0],k0[1],dupflag,k1[0],k1[1],f0,f1,c0,c1)
                    
                #
                # do a 'cleanonly' merge of the "maybe" dups
                #
                else:
                    
                    if(verb): print "Mm dupd: %6.2f %s :: %s ::  %6.2f %s :: %8.2f %8.2f : %8.2f %8.2f "%\
                              (k0[0],k0[1],dupflag,k1[0],k1[1],f0,f1,c0,c1)
                    
                    self.MergeObs(dupflag,fdata,fstns,k0,k0,'cleanonly')
                    nout=nout+1

            else:
                
                if(dupflag==0):
                    if(verb): print "NO dupd: %6.2f %s :: %s"%(k[0],k[1],prcflg[k][0])
                    self.MergeObs(dupflag,fdata,fstns,k,k,'cleanonly')
                    nout=nout+1

            ntot=ntot+1
            #print 'aaaa dupd: ',ntot,nout



        stnid='alldone '
        stnrec=struct.pack('8sfffii',stnid,0.0,0.0,0.0,0,0)
        self.Ofo.write(stnrec)
        self.Ofo.close()

        print "Counts for: %s  ntot: %4d  nout: %d"%(self.yyyymm,ntot,nout)

    

        
    
        
if (__name__ == "__main__"):

    import sys
    import time

    import mf

    verb=0

    #
    # instantiate the upamon object which opens a file
    #

    d=dupamon(var='t')

    #
    # read in upamon cards with stats
    #
    
    stime=time.time()
    ucards=d.ReadCards(d.fu)
    mf.Timer('read:   ',stime)

    #
    # filter out syntime and subtype 
    #
     
    stime=time.time()
    (fstns,fdata)=d.FiltStnStats(ucards)
    mf.Timer('filter: ',stime)

    #
    # find the dups
    #
    stime=time.time()
    prcflg=d.DupCheck(fstns)
    mf.Timer('dupchk: ',stime)

    #
    # merge and output
    #
    stime=time.time()
    d.MergeStns(fstns,fdata,prcflg)
    mf.Timer('dupchk: ',stime)


