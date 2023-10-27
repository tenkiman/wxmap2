import rlcompleter
import readline
readline.parse_and_bind("tab: complete")

import os
import sys
from math import sqrt

import struct
import array

import mf

#from sakimon import upamon

from dupamon import dupamon

class nupamon(dupamon):

    BaseDir='/pcmdi/tenki_dat1/reanal/ncep/r1/upamon'
    ObsDir=BaseDir+'/obs'
    uPaDir=BaseDir+'/txt'  # txt version of upamon stats
    
    def __init__(self,yyyymm=None,var='t',tsynhour='00',tsubtype='101',initopt=None):

        self.tsynhour=tsynhour
        self.tsubtype=tsubtype
        self.reanal='ncep1'
        
        #
        # open input data
        #
        
        self.BaseDir='/pcmdi/tenki_dat1/reanal/ncep/r1/upamon'
        self.uPaDir=self.BaseDir+'/txt'
        self.ObsDir=self.BaseDir+'/obs'

        if(yyyymm == None):
            yyyymm='197607'
            yyyymm='199112'
            self.ObsDir=self.BaseDir+'/tmp'

        donoload=0
        self.yyyymm=yyyymm
        self.upath="%s/%s"%(self.uPaDir,'upamon.asc.%s'%(self.yyyymm[2:]) )

        try:
            self.fu=open(self.upath)
            print 'GGGGGGG opening: ',self.upath
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


        __opath="%s/ncep1.upamon.%s.%s.%s.%s.obs"%\
                 (self.ObsDir,self.upavar,self.yyyymm[0:6],self.tsynhour,self.tsubtype)
        print 'stnobs opening: ',__opath
        
        try:
            self.Ofo=open(__opath,'wb')
        except:
            raise IOError('unable to open: %s'%(__opath))


        self.openstatus=1
    
        if(donoload):
            print "WWWWWWWW no upamon stats for reanal: %s, doing noload for: %s"%(self.reanal,self.yyyymm)
            stnid='alldone '
            stnrec=struct.pack('8sfffii',stnid,0.0,0.0,0.0,0,0)
            self.Ofo.write(stnrec)
            self.Ofo.close()
            self.openstatus=0

            

#----5----1----5----2----5----3----5----4----5----5----5----6----5----7----5----8
#STATION:03774    ELON:359.78 NLAT:51.08  ELEV:144    YEAR:1979 MNTH:1  HOUR:12

    def ParseStnCard(self,cards,i):

        card=cards[i]
        #print 'pppp ',card[:-1]
        wmoid=card[8:14].strip()
        rlon=float(card[22:29].strip())
        rlat=float(card[34:41].strip())
        elv=card[46:53].strip()
        if(mf.find(elv,'***')): elv=-999
        elv=float(elv)
        synhour=int(card[76:79].strip())
        subtype='101'
        src='14'
        ndtgs='999'

        #print 'pppp ',wmoid,rlon,rlat,elv,synhour
        #print 'pppp ',subtype,src,ndtgs
        
        #
        # calc sakimon stnid
        #

        slat=rlat
        slon=rlon
        
        if(rlat<0.0):
            nshem='S'
            slat=abs(rlat)
        else:
            nshem='N'
        
        slat=slat*100.0
        slon=slon*100.0
        ostnid="stn_%s%04.0f_%05.0fE"%(nshem,slat,slon)

        osynhour=self.BinSynopticTime(synhour)
        
        #
        # advance 2 cards to get on a variable card
        #
        i=i+2

        return(ostnid,osynhour,rlat,rlon,elv,wmoid,subtype,src,ndtgs,i)
    

    def FiltStnStats(self,ucards):

        #
        # local function to load up cards
        #

        plevs=self.MandatoryPressureLevels

        nlevs=len(plevs)
        nvars=len(self.statvars)
        
        nfbvars=7

        def readcard(card,i):
            
            tt=card[:-1].split()

            if(len(tt) == 0):
                type='blank'

            elif(len(tt) >= 7):
                
                if(mf.find(tt[0],'OB')): type='var'
                if(mf.find(tt[0],'STAT')): type='station'
                if(len(tt) == 8): type='data'

            else:
                print 'EEE problem in readcard'
                sys.exit()
            
            i=i+1
            return(type,tt,i)


        def ivar2ovar(ivar):
            if(ivar == 'SP'):
                ovar='q'
            elif(ivar == 'RH'):
                ovar='r'
            elif(ivar == 'S'):
                ovar='w'
            else:
                ovar=ivar.lower()
            return(ovar)

        
        def loadvar(ucards,i):
            
            dlists=[]
            datathere=0
            rc=1

            #
            # first card is the var card
            #
            (type,list,i)=readcard(ucards[i],i)
            #print 'rrrrr ',i,type,list
            if(type == 'var'):
                tt=list[0]
                var=tt[0:len(tt)-2]
                ovar=ivar2ovar(var)
                
                #print 'vvvvvvvvvvvvvvvvvvvvv ',var
                (type,list,i)=readcard(ucards[i],i)
                
                #print 'qqqq ',i,type
                try:
                    (type,list,i)=readcard(ucards[i],i)
                except:
                    rc=0
                    return(rc,ovar,dlists,datathere,i)
                    
                #print 'qqqq ',i,type
                if(type == 'data'):
                    dlists.append(list)
                    #print i,'dddd ',list
                #elif(type == 'blank'):
                #      print i,'non data.......'
                    
                while(type == 'data'):
                    try:
                        (type,list,i)=readcard(ucards[i],i)
                        if(type == 'data'):
                            dlists.append(list)
                    except:
                        rc=0
                        return(rc,ovar,dlists,datathere,i)
                    #print 'vvv ',i,type,list
                #print 'vvvooo ',i,type,list
                
                
            return(rc,ovar,dlists,datathere,i)

        #
        # local routine to convert upamon stat cards to sakimon stat cards
        #

        def upa2saki(var,dlists):
            
            fdata=[]
            flist=[]

            #
            # initialize to stnundef (-9999); nvars+1 to hold pressure
            #
            
            flevlist={}
            for l in range(0,nlevs):
                plev=float(plevs[l])
                tt=[]
                tt.append(plev)
                for i in range(0,nvars):
                    tt.append(self.stnundef)
                    
                flevlist[plev]=tt

            #
            #  load upamon into sakimon list
            #

            for dlist in dlists:
                
                flist=[]
                olist=[]

                #
                # initialize all sakimon vars to undef in the output list: olist
                #
                for i in range(0,nvars+1):
                    olist.append(self.stnundef)

                #
                # turn upamon list floats in the input list: dlist
                #
                for dd in dlist:
                    flist.append(float(dd))


                #
                # rearrange data to sakimon form
                #
                if(var != 'w'):

                    #
                    # if count is 0 then let be undef
                    #
                    if(flist[6] > 0.0):
                        olist[0:6]=flist[0:6]
                    else:
                        olist[0]=flist[0]
                        
                    olist[6]=flist[6]+flist[7]
                    olist[7]=flist[6]
                    olist[8]=flist[7]
                
                flevlist[flist[0]]=olist
                
            for k in plevs:
                fdata.append(flevlist[k])
                
            return(fdata)

            

        test=0
        
        fstns={}
        fdata={}

        nstn=0
        
        i=1

        while(1):
            
            (stnid,synhour,rlat,rlon,elv,wmoid,subtype,src,ndtgs,i)=self.ParseStnCard(ucards,i)

            for j in range(0,nfbvars):
                
                (rc,ovar,dlists,datathere,i)=loadvar(ucards,i)
                if(rc==0):
                    return(fstns,fdata)

                if(synhour == self.tsynhour and ovar == self.upavar):
                    nstn=nstn+1
                    fstns[rlat,stnid]=[stnid,rlat,rlon,elv,wmoid,subtype,src,ndtgs]
                    fdata[rlat,stnid]=upa2saki(self.upavar,dlists)

                #if(nstn > 100):
                #    return(fstns,fdata)
                    

        
if (__name__ == "__main__"):

    import sys
    import time

    import mf

    verb=0

    #
    # instantiate the upamon object which opens a file
    #

    d=nupamon(var='t')

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
    prcflg=d.DupCheck(fstns,verb=1)
    mf.Timer('dupchk: ',stime)

    #
    # merge and output
    #
    stime=time.time()
    d.MergeStns(fstns,fdata,prcflg)
    mf.Timer('dupchk: ',stime)
