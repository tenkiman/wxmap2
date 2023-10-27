import rlcompleter
import readline
readline.parse_and_bind("tab: complete")

import os
import sys
from math import sqrt

import struct
import array

import mf

class upamon:

    BaseDir='/pcmdi/reanal/ecmwf/era40/ob/upamon'
    BaseDir='/mfw_backup1/mfw_home1/ecmwf/era40/ob/upamon'
    BaseDir='/pcmdi/upamon'
    #BaseDir='/pcmdi/tenki_dat1/reanal/ecmwf/era40/upamon'
    
    InputDir=BaseDir+'/txt'
    ObsDir=BaseDir+'/obs'
    uPaDir=BaseDir+'/upa'  # similar to txt version of upamon
    
    MandatoryPressureLevels=[1000,925,850,700,500,400,300,250,200,150,100,70,50,30,20,10]
    SynopticTimes=['00','06','12','18']

    stnundef=-9999.0

    StatVariables=['ob','of','oa','rf','ra','ct','cg','cr','cbl','cd']

    VarDesc={'t':'Temperature',
             'w':'Wind Speed',
             'u':'u comp wind',
             'v':'v comp wind',
             'r':'RH',
             'q':'specific humidity',
             'z':'geopential height',
             }
             
    VaruNits={'t':'[k]',
             'w':'[m/s]',
             'u':'[m/s]',
             'v':'[m/s]',
             'r':'[%]',
             'q':'[g/kg]',
             'z':'[m]',
             }
             
             

    StatVar2Ctl={'ob':'ob',
                 'of':'fc',
                 'oa':'an',
                 'rf':'mf',
                 'ra':'ma',
                 'ct':'cn',
                 'cg':'ct',
                 'cr':'cx',
                 'cbl':'cb',
                 'cd':'cd',
                 'obuc':'obuc',
                 'obbc':'obbc',
                 'cbc':'cbc',
                 }
    
    
    StatVariablesCtlDesc={'ob':'Observation',
                          'fc':'Background',
                          'an':'Analysis',
                          'mf':'RMS o-f',
                          'ma':'RMS o-a',
                          'cn':'Count total',
                          'ct':'Count good',
                          'cx':'Count reject',
                          'cb':'Count blacklist',
                          'cd':'Count Dups',
                          'obuc':'Ob un biascorrected',
                          'obbc':'Ob BIASCORRECTED',
                          'cbc':'Count biascorrected',
                          }

    SubTypeDesc={
        101:'TEMP land',
        102:'TEMP ship',
        103:'TEMP dropsond/tcbog',
        104:'TEMP ROCOB',
        105:'TEMP ROCOB',
        106:'TEMP mobile',
        }
              
    
    StatVariablesTa=StatVariables + ['obuc','obbc','cbc']

    undef=1e20
    
    SizNoload=28

    #
    # __ "hides" these variables (mangles then to non obvious for)
    #
    
    __wvar=['wob','wof','woa','wrf','wra']
    __uvar=['uob','uof','uoa','urf','ura']
    __vvar=['vob','vof','voa','vrf','vra']
    
    StatVariablesWind=__wvar + __uvar + __vvar + ['ct','cg','cr','cbl','cd']

    __wvar=['wob','wfc','wan','wmf','wma']
    __uvar=['uob','ufc','uan','umf','uma']
    __vvar=['vob','vfc','van','vmf','vma']
    
    StatVariablesWindCtl=__wvar + __uvar + __vvar + ['wcn','wct','wcx','wcb','wcd']

    Nsfcvar=6
    NsfcvarStn=4

    def __init__(self,yyyymm=None,var='t',initopt=None):

        self.dogzip=0
        self.dogunzip=1
        
        #
        # open input data
        #
        
        if(yyyymm == None):
            
            #self.BaseDir='/pcmdi/reanal/ecmwf/era40/ob/upamon'
            self.BaseDir='/pcmdi/tenki_dat1/reanal/ecmwf/era40/upamon'
            self.BaseDir='/pcmdi/upamon'
            self.InputDir=self.BaseDir+'/txt'

            self.dpath="%s/%s"%(self.InputDir,'fb.test.txt')
            self.dpath="%s/%s"%(self.InputDir,'fb.19580101.txt')
            #self.dpath="%s/%s"%(self.InputDir,'fb.1958010200.txt') ; self.yyyymm='19580102'
            self.dpath="%s/%s"%(self.InputDir,'fb.197301.big.txt') ; self.yyyymm='197301'
            
            self.dpath="%s/%s"%(self.InputDir,'feedbackglob197301') ; self.yyyymm='197301'
            self.dpath="%s/%s"%(self.InputDir,'fb.93722.txt') ; self.yyyymm='195801'
            self.dpath="%s/%s"%(self.InputDir,'fb.dupcheck.txt') ; self.yyyymm='195801'
            self.dpath="%s/%s"%(self.InputDir,'fb.dup.prob.txt')
            self.dpath="%s/%s"%(self.InputDir,'fb.43192.199209.txt') ; self.yyyymm='199209'
            self.dpath="%s/%s"%(self.InputDir,'fb.big.195801.txt') ; self.yyyymm='195801'
            self.dpath="%s/%s"%(self.InputDir,'fb.94374.txt') ; self.yyyymm='195802'
            self.dpath="%s/%s"%(self.InputDir,'fb.91285.199009.txt') ; self.yyyymm='199009'

            try:
                self.fd=open(self.dpath)
                print 'GGGGGGG opening: ',self.dpath
            except:
                raise IOError('unable to open: %s'%(self.dpath))
            #
            # if testing use tmp
            #
            self.ObsDir=self.BaseDir+'/tmp'
            self.uPaDir=self.BaseDir+'/tmp'
            self.dotesting=1

        elif(yyyymm == 'test'):

            print 'just testing'
            return
            
            
        else:

            self.yyyymm=yyyymm

            self.dpath="%s/%s%s"%(self.InputDir,'feedbackglob',yyyymm)
            self.gzdpath="%s/%s%s.gz"%(self.InputDir,'feedbackglob',yyyymm)
            dpaththere=os.path.exists(self.dpath)
            gzdpaththere=os.path.exists(self.gzdpath)

            if(initopt == 'noload'):
                
                if(dpaththere):
                    self.fd=111
                elif(gzdpaththere):
                    self.fd=999
                else:
                    self.fd=-999
                self.dotesting=0
                    
            else:
                
                if(dpaththere):
                    self.dogunzip=0
                
                elif(gzdpaththere):
                    self.dogunzip=1
                    cmd="gunzip %s"%(self.gzdpath)
                    mf.runcmd(cmd)

                try:
                    self.fd=open(self.dpath)
                    print 'GGGGGGG opening: ',self.dpath
                except:
                    self.fd=None
            
                self.dotesting=0

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

        if(var == 'w'):
            self.statvarsctl=self.StatVariablesWindCtl
        else:
            ss=[]
            for s in self.statvars:
                s2c=self.StatVar2Ctl[s]
                ss.append(self.upavar+s2c)
            self.statvarsctl=ss



        #OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
        #
        # open output obs files
        #

        noloadtest=(initopt == 'noload' and self.fd == -999)

        if(noloadtest or self.fd != -999):
            
            self.Ofo={}
            for __stime in self.SynopticTimes:
                __opath="%s/sakimon.%s.%s.%s.obs"%(self.ObsDir,self.upavar,self.yyyymm[0:6],__stime)

                try:
                    self.Ofo[__stime]=open(__opath,'wb')
                except:
                    raise IOError('unable to open: %s'%(__opath))

        #
        # bail if doing noload
        #

        if(noloadtest): return



        #OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
        #
        # open upa output txt similar to txt version of upamon
        #

        __opath="%s/sakimon.%s.%s.txt"%(self.uPaDir,self.upavar,self.yyyymm[0:6])

        try:
            self.Ofu=open(__opath,'w')
        except:
            raise IOError('unable to open: %s'%(__opath))

        #OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
        #
        # create .ctl
        #
        
        for __stime in self.SynopticTimes:
            __opath="%s/sakimon.%s.%s.ctl"%(self.ObsDir,self.upavar,__stime)
            self.CtlFile(__opath,__stime)
        
        

        #
        # set the slices of the big card to pull out vars and flags
        #

        self.td1=52  ;  self.td2=84  ;  self.tf1=84  ; self.tf2=96
        self.qd1=96  ;  self.qd2=120 ;  self.qf1=120 ; self.qf2=130
        self.rd1=130 ;  self.rd2=154 ;  self.rf1=154 ; self.rf2=164
        self.wd1=164 ;  self.wd2=220 ;  self.wf1=220 ; self.wf2=230
        self.zd1=230 ;  self.zd2=270 ;  self.zf1=270 ; self.zf2=278



    def CtlFile(self,cpath,stime):

        try:
            Octl=open(cpath,'w')
        except:
            raise IOError('unable to open: %s'%(cpath))
            
        (dir,file)=os.path.split(cpath)
        (bfile,bext)=os.path.splitext(file)
        #dfile=bfile+'.obs'
        #sfile=bfile+'.smp'

        bdtg='19480101'+stime
        gtime=mf.dtg2gtime(bdtg)

        nvar=len(self.statvarsctl)+self.NsfcvarStn

        vars=[]
        vars.append('wmo     0 0 integer wmoid if less than 0 then was undef and set to n undef wmo')
        vars.append('st      0 0 subtype')
        vars.append('src     0 0 source code')
        vars.append('elv     0 0 station elevation [m]')

        for s in self.statvarsctl:
            desc="%s %s %s"%(self.VarDesc[s[0]],self.StatVariablesCtlDesc[s[1:len(s)]],self.VaruNits[s[0]])
            vars.append("%-7s 1 0 %s"%(s,desc))
        

        if(self.dotesting):
            ntimes=1
            gtime=mf.dtg2gtime(self.yyyymm+'01'+stime)
        else:
            ntimes=660
            
        dfilemask="sakimon.%s.%%y4%%m2.%s.obs"%(self.upavar,stime)
        sfile="sakimon.%s.%s.smp"%(self.upavar,stime)

        ctl="""dset ^%s
title test
dtype station
index %s
undef %s
options template
tdef %s linear %s 1mo
vars %d
"""%(dfilemask,sfile,self.undef,ntimes,gtime,nvar)

        for v in vars:
            ctl=ctl+"%s\n"%(v)

        ctl=ctl+'endvars\n'

        #print ctl

        Octl.writelines(ctl)

        

    def BinSynopticTime(self,hh):

        if((hh>=22 and hh<=24) or (hh>=0 and hh<=3) ): ohh='00'
        if( hh>= 4 and hh<=9  ): ohh='06'
        if( hh>=10 and hh<=15 ): ohh='12'
        if( hh>=16 and hh<=21 ): ohh='18'

        return(ohh)


    def CheckFlags(self,flags):
        
        lf=len(flags)
        
        iok=1
        ibc=0
        ibl=0
        
        for l in range(0,lf):
            if(flags[l] == '3'): iok=0

        if(flags[4] == '3'): ibl=1
        if(lf == 6):
            if(flags[lf-1] == '2'): ibc=1


        return(iok,ibc,ibl)
            


    def ParseDataDic(self,dtg,syntime,stat,cntdic,datadic):

        plevs=cntdic.keys()

        for plev in plevs:

            vardata=datadic[plev]
            var=vardata[0]

            # 20040427 - output to detect multiple data in a 6-h window
            #
            #if(plev == 1000):
            #    print 'vvvv ',plev,dtg,syntime,cntdic[plev],vardata[1:5] 

            if(var == 't'):
                flags=vardata[len(vardata)-6:len(vardata)]
                obuc=float(vardata[1])
                ob=float(vardata[2])
                of=float(vardata[3])
                oa=float(vardata[4])

            elif(var == 'w'):
                flags=vardata[len(vardata)-5:len(vardata)]
                wob=float(vardata[1])
                uob=float(vardata[2])
                uof=float(vardata[3])
                uoa=float(vardata[4])
                vob=float(vardata[5])
                vof=float(vardata[6])
                voa=float(vardata[7])
                wof=wob-sqrt( (uob-uof)*(uob-uof) + (vob-vof)*(vob-vof) )
                woa=wob-sqrt( (uob-uoa)*(uob-uoa) + (vob-voa)*(vob-voa) )
                ob=wob

            elif(var == 'q'):
                flags=vardata[len(vardata)-5:len(vardata)]
                #
                #  check for bad q data...
                #
                try:
                    ob=float(vardata[1])
                except:
                    print 'WWWWWWWWW bad q ob:  ',vardata
                    ob=-999.0
                    continue
                
                of=float(vardata[2])
                oa=float(vardata[3])
                #
                # rescale fro 0.1 g/kg to g/kg
                #
                if(ob != -999.0):
                    ob=float(vardata[1])*0.1
                    of=float(vardata[2])*0.1
                    oa=float(vardata[3])*0.1


            elif(var == 'z'):
                flags=vardata[len(vardata)-5:len(vardata)]
                obzg=float(vardata[1])
                ob=float(vardata[2])
                of=float(vardata[3])
                try:
                    oa=float(vardata[4])
                except:
                    print vardata[4]
                    print vardata
                    print plev
                    sys.exit()

            else:
                flags=vardata[len(vardata)-5:len(vardata)]
                ob=float(vardata[1])
                of=float(vardata[2])
                oa=float(vardata[3])

            (iok,ibc,ibl)=self.CheckFlags(flags)

            if(ob != -999.0):

                stat[plev][syntime]['ct']=stat[plev][syntime]['ct']+1
                stat[plev][syntime]['cd']=stat[plev][syntime]['cd']+cntdic[plev]-1

                if(iok):

                    if(var == 'w'):

                        stat[plev][syntime]['wob']=stat[plev][syntime]['wob']+wob
                        stat[plev][syntime]['wof']=stat[plev][syntime]['wof']+wof
                        stat[plev][syntime]['woa']=stat[plev][syntime]['woa']+woa
                        stat[plev][syntime]['wrf']=stat[plev][syntime]['wrf']+wof*wof
                        stat[plev][syntime]['wra']=stat[plev][syntime]['wra']+woa*woa

                        stat[plev][syntime]['uob']=stat[plev][syntime]['uob']+uob
                        stat[plev][syntime]['uof']=stat[plev][syntime]['uof']+uof
                        stat[plev][syntime]['uoa']=stat[plev][syntime]['uoa']+uoa
                        stat[plev][syntime]['urf']=stat[plev][syntime]['urf']+uof*uof
                        stat[plev][syntime]['ura']=stat[plev][syntime]['ura']+uoa*uoa

                        stat[plev][syntime]['vob']=stat[plev][syntime]['vob']+vob
                        stat[plev][syntime]['vof']=stat[plev][syntime]['vof']+vof
                        stat[plev][syntime]['voa']=stat[plev][syntime]['voa']+voa
                        stat[plev][syntime]['vrf']=stat[plev][syntime]['vrf']+vof*vof
                        stat[plev][syntime]['vra']=stat[plev][syntime]['vra']+voa*voa

                        stat[plev][syntime]['cg']=stat[plev][syntime]['cg']+1


                    else:

                        stat[plev][syntime]['cg']=stat[plev][syntime]['cg']+1
                        stat[plev][syntime]['ob']=stat[plev][syntime]['ob']+ob
                        stat[plev][syntime]['of']=stat[plev][syntime]['of']+of
                        stat[plev][syntime]['oa']=stat[plev][syntime]['oa']+oa
                        stat[plev][syntime]['rf']=stat[plev][syntime]['rf']+of*of
                        stat[plev][syntime]['ra']=stat[plev][syntime]['ra']+oa*oa

                        if(var == 't' and ibc):
                            stat[plev][syntime]['obuc']=stat[plev][syntime]['obuc']+obuc
                            stat[plev][syntime]['obbc']=stat[plev][syntime]['obbc']+ob
                            stat[plev][syntime]['cbc']=stat[plev][syntime]['cbc']+1

                else:

                    stat[plev][syntime]['cr']=stat[plev][syntime]['cr']+1

                    if(ibl):
                        stat[plev][syntime]['cbl']=stat[plev][syntime]['cbl']+1





    def FinaliseStats(self,stats):

        plevs=self.MandatoryPressureLevels
        stimes=self.SynopticTimes
        

        def rms(stats,p,s,rf,of):

            #
            # the sums have ALREADY been divided by N!!!
            #
            epsilon=1e-10
            sum1=stats[p][s][rf]
            sum2=stats[p][s][of]
            sum=sum1-(sum2*sum2)
            
            try:
                rms=sqrt(sum)
            except:
                #
                # check for small number
                # 
                if(abs(sum) <epsilon):
                    rms=0.0
                else:
                    print 'EEE in rms sqrt',rf,of,sum1,sum2,p,s,ngood,sum
                    sys.exit()

            #print 'qqq ',p,s,sum1,sum2,sum,"%2i %6.3f"%(ngood,rms)

            stats[p][s][rf]=rms

            
        for p in plevs:

            for s in stimes:

                ngood=stats[p][s]['cg']
                nbl=stats[p][s]['cbl']
                
                if( ngood > 0.0):

                    slist=['ob','of','oa','rf','ra']
                    rlist=[('rf','of'),('ra','oa')]

                    if(self.upavar == 't'):
                        
                        nbc=stats[p][s]['cbc']
                        slistbc=['obuc','obbc']

                        if(nbc > 0.0):
                            for sl in slistbc:
                                stats[p][s][sl]=stats[p][s][sl]/nbc
                            
                    if(self.upavar == 'w'):
                        
                        slist=['wob','wof','woa','wrf','wra',
                               'uob','uof','uoa','urf','ura',
                               'vob','vof','voa','vrf','vra']
                        
                        rlist=[('wrf','wof'),('wra','woa'),
                               ('urf','uof'),('ura','uoa'),
                               ('vrf','vof'),('vra','voa')]

                    
                    for sl in slist:
                        stats[p][s][sl]=stats[p][s][sl]/ngood
                            
                    for rl in rlist:
                        rms(stats,p,s,rl[0],rl[1])
                    


    def InitStats(self):
        
        plevs=self.MandatoryPressureLevels
        stimes=self.SynopticTimes
        vars=self.statvars

        stats={}

        for p in plevs:
            stats[p]={}

            for s in stimes:
                stats[p][s]={}

                for v in vars:
                    stats[p][s][v]=0.0

        return(stats)
                    
    

    def ReadCard(self):
        card=self.fd.readline()
        return(card)

    def ReadCards(self,filehandle=None):
        if(filehandle == None):
            filehandle=self.fd
        cards=filehandle.readlines()
        return(cards)

    def ParseCard(self,ncard,verb=1):

        #ncard=card[0:230]+' '+card[230:-1]
        #ncard=card

        docard=0

        if(docard):
            cardc=''
            for i in range(1,11):
                cardc=cardc+'0000_0000%1d'%(i)
            ocard=cardc+cardc+cardc[0:80]
            
            print ocard[0:100]
            print ncard[0:100]
            
            print ocard[90:200]
            print ncard[90:200]

            print ocard[190:280]
            print ncard[190:280]

        dosplit=0
        
        if(dosplit):

            tt=ncard[0:53].split()
            meta=tt[0:7]
            (dtg,csubtype,source,wmoid,clat,clon,stnheight)=meta
            p=tt[7]
            

        else:

            dtg=ncard[0:10]
            csubtype=ncard[11:15]
            source=ncard[15:17]
            wmoid=ncard[17:25].strip()
            clat=ncard[25:31]
            clon=ncard[31:39]
            stnheight=ncard[39:44]
            p=ncard[45:53]


        #print dtg,csubtype,source,wmoid,clat,clon,stnheight

        
        meta=(dtg,csubtype,source,wmoid,clat,clon,stnheight)

        isubtype=int(csubtype)
        rlon=float(clon)
        rlat=float(clat)

        if(rlon<0.0):
            rlon=360.0+rlon
        
        if(rlat<0.0):
            nshem='S'
            rlat=abs(rlat)
        else:
            nshem='N'
        
        rlat=rlat*100.0
        rlon=rlon*100.0

        ostnid="stn_%s%04.0f_%05.0fE"%(nshem,rlat,rlon)

        data=[]
        data.append(self.upavar)


        if(self.upavar == 't'):

            dsplit=ncard[self.td1:self.td2].split()
            fsplit=ncard[self.tf1:self.tf2].split()
            data=data+dsplit+fsplit

        if(self.upavar == 'w'):

            dsplit=ncard[self.wd1:self.wd2].split()
            fsplit=ncard[self.wf1:self.wf2].split()
            data=data+dsplit+fsplit

        if(self.upavar == 'q'):

            dsplit=ncard[self.qd1:self.qd2].split()
            fsplit=ncard[self.qf1:self.qf2].split()
            data=data+dsplit+fsplit
        #
        # use q flags vice r flags which are always blacklisted
        #

        if(self.upavar == 'r'):

            dsplit=ncard[self.rd1:self.rd2].split()
            fsplit=ncard[self.qf1:self.qf2].split()
            data=data+dsplit+fsplit

        #
        # use temperature vice height flags
        #
    
        if(self.upavar == 'z'):
            
            dsplit=ncard[self.zd1:self.zd2].split()
            fsplit=ncard[self.tf1:self.tf2].split()
            data=data+dsplit+fsplit

        
        #(tob,toba,tobafg,tobaan,tflgfinal,tflgfg,tflgobfg,tflgan,tflgoban,tflgdatum)=tt[8:18]
        #print 'ttt ',dtg,subtype,source,wmoid,rlat,rlon
        #print 'ttt ',ostnid,stnheight
        #if(isubtype >= 101 and isubtype <= 150):
        #    if(verb):
        #        print 'ttt ',ostind,dtg,wmoid,isubtype,p,tob,toba,tobafg,tobaan

        return(ostnid,meta,p,data)
    

    def LoadDataArrays(self,cards,verb=0):

        ostnidOld='asdfasdf'
        ostnidundef='adsfasdf'
        

        umeta={}
        udata={}

        nundef=1
        n=1
        for card in cards:

            ncard=len(card)
            if(ncard == 0): break
            n=n+1

            (ostnid,meta,p,data)=self.ParseCard(card,verb=0)
            (dtg,csubtype,source,wmoid,clat,clon,stnheight)=meta
            
            if(wmoid == '-999'):
                wmoid="p%04d"%(nundef)
                if(ostnid != ostnidundef):
                    ostnidundef=ostnid
                    nundef=nundef+1
                    if(nundef > 9999): nundef=1

            isubtype=int(csubtype)

            if(isubtype < 101): continue
            if(verb): print 'cccccccccccc ',n,ncard,card[0:50]

            odata=[p,data]
            ometa=[wmoid,isubtype,source,stnheight]

            if(ostnid != ostnidOld):

                ostnidOld=ostnid

                #
                # meta data
                #

                try:
                    umeta[ostnidOld][dtg].append(ometa)
                    if(verb): print 'nnnnnnnnnnnn got it ',ostnidOld,wmoid,dtg
                except:
                    try:
                        umeta[ostnidOld][dtg]=[]
                        umeta[ostnidOld][dtg].append(ometa)
                    except:
                        umeta[ostnidOld]={}
                        umeta[ostnidOld][dtg]=[]
                        umeta[ostnidOld][dtg].append(ometa)
                    if(verb): print 'nnnnnnnnnnnn ssssssss ',ostnidOld,wmoid,dtg


                #
                # feedback
                #

                try:
                    udata[ostnidOld][dtg].append(odata)
                    if(verb): print 'nnnnnnnnnnnn got it ',ostnidOld,wmoid,dtg
                except:
                    try:
                        udata[ostnidOld][dtg]=[]
                        udata[ostnidOld][dtg].append(odata)
                    except:
                        udata[ostnidOld]={}
                        udata[ostnidOld][dtg]=[]
                        udata[ostnidOld][dtg].append(odata)
                    if(verb): print 'nnnnnnnnnnnn ssssssss ',ostnidOld,wmoid,dtg


            else:

                if(verb): print 'oooooooooooo ',ostnidOld,dtg

                try:
                    udata[ostnidOld][dtg].append(odata)
                    if(verb): print 'nnnnnnnnnnnn got it ',ostnidOld,wmoid,dtg
                except:
                    udata[ostnidOld][dtg]=[]
                    udata[ostnidOld][dtg].append(odata)
                    if(verb): print 'nnnnnnnnnnnn ssssssss ',ostnidOld,wmoid,dtg

        print 'NNNNNNNN cards loaded: ',n

        return(umeta,udata)


    def RunStats(self,stat,data):
            
        #
        # collect stats by cycling  through dtgs
        #
        dtgs=data.keys()
        dtgs.sort()
        
        for dtg in dtgs:
            dd1=data[dtg]
            syntime=self.BinSynopticTime(int(dtg[8:10]))
            (cntdic,datadic)=self.DataByLevel(dd1)
            self.ParseDataDic(dtg,syntime,stat,cntdic,datadic)

        return(dtgs)


    def DataByLevel(self,datalist):
        datadic={}
        cntdic={}
        for l in range(0,len(datalist)):
            (lev,data)=(datalist[l][0],datalist[l][1])
            plev=int(float(lev))
            datadic[plev]=data
            try:
                cntdic[plev]=cntdic[plev]+1
            except:
                cntdic[plev]=1

        return(cntdic,datadic)


    def PrintCards(self,card):
        self.Ofu.writelines(card+'\n')
        

    def FinaliseOutput(self):

        stnid='alldone '
        for stime in self.SynopticTimes:
            stnrec=struct.pack('8sfffii',stnid,0.0,0.0,0.0,0,0)
            self.Ofo[stime].write(stnrec)
            self.Ofo[stime].close()


        if(self.fd != None and self.fd != -999):
            self.fd.close()
            
        try:
            self.Ofu.close()
        except:
            None

        if(self.dogzip == 1):
            cmd="gzip %s"%(self.dpath)
            mf.runcmd(cmd)
        
    def PrintStats(self,stat,basemeta,dtgs,s,doprintterm=0):

        doupafile=1
        doobsfile=1

        verb=0
        
        if(doprintterm): verb=1
      
        stimes=self.SynopticTimes
        plevs=[850,500,100,10]
        plevs=self.MandatoryPressureLevels
        slist=self.statvars

        stndt=0.0
        stnlev=len(plevs)+1
        stnflag=1

        wmoid=basemeta[0]
        subtype=basemeta[1]
        source=basemeta[2]
        elevation=float(basemeta[3])

        if(wmoid[0:1] == 'p'):
            if(verb): print 'pppppppppp wmoid: ',wmoid
            iwmoid=-int(wmoid[1:6])
        elif(int(wmoid) <0):
            iwmoid=99999
        else:
            iwmoid=int(wmoid)

        ndtgs=len(dtgs)

        slat=float(s[5:9])*0.01
        hemns=s[4:5]
        ihemns=0
        rlat=slat
        if(hemns == 'S'):
            rlat=-slat
            ihemns=9

        slon=float(s[10:15])*0.01
        rlon=slon
        hemew='E'
        if(slon>=180.0):
            slon=360.0-slon
            hemew='W'

        #stnid="%s%03.0f%03.0f%s"%(hemns,(slat*10.0),(rlon),'\0')
        #stnid="%s%03.0f%03.0f%1s"%(hemns.lower(),(slat*10.0),(rlon),'\0')
        #
        # bug in grads; couldn't hand ids > 6 chars, plus lower to be consistent since can't match on upper
        #
        stnid="%s%03.0f%04.0f"%(hemns.lower(),(slat*10.0),(rlon*10))

            
        stncard="Stn: %s Var: %s Lat: %5.2f%s Lon: %6.2f%s Elv: %4.0f Yr: %4s Mo: %2s "%\
                 (s,self.upavar,slat,hemns,slon,hemew,elevation,self.yyyymm[0:4],self.yyyymm[4:6])
        stncard=stncard+"WMO: %-5s Sub: %-3s Src: %-3s Ndtgs: %3d"%\
                 (wmoid,subtype,source,ndtgs)

        if(doobsfile):
            stnhead=struct.pack('8sfffii',stnid,rlat,rlon,stndt,stnlev,stnflag)
            if(elevation == -999): elevation=self.undef
            stnsfc=struct.pack('%df'%(self.NsfcvarStn),float(iwmoid),float(subtype),float(source),elevation)

        if(verb): print stncard
        self.PrintCards(stncard)
        
        for stime in stimes:

            if(doobsfile):
                self.Ofo[stime].write(stnhead)
                self.Ofo[stime].write(stnsfc)

                stnlist=[]
                stndata=array.array('f')

            card="Synoptic Time: %s Z"%(stime)
            if(doprintterm): print card
            if(doupafile): self.PrintCards(card)

            card="plev  "
            for sl in slist:
                format=" %+6s"
                if(sl[0] == 'c'): format="%+4s"
                if(self.upavar == 'w' and sl[0] != 'c'): format=" %-6s"
                if(self.upavar == 'z' and sl[0] != 'c'): format=" %-8s"
                card=card + format%(sl)
            if(doprintterm): print card
            if(doupafile): self.PrintCards(card)

            for plev in plevs:

                card= "%4d  "%(plev)
                if(doobsfile): stnlist.append(float(plev))
                for sl in slist:
                    format=" %6.2f"
                    if(self.upavar == 'w'): format=" %6.2f"
                    if(self.upavar == 'z'): format=" %8.2f"
                    if(sl[0] == 'c'): format="  %2.0f"

                    if(stat[plev][stime]['cg'] == 0.0):
                        ovalp=9999.9
                        if(sl[0] == 'c'):
                            ovalc='   *'
                            ovalp=stat[plev][stime][sl]
                            ovalc=format%(ovalp)
                        else:
                            ovalc=' ******'
                            if(self.upavar == 'z'): ovalc=' ********'
                    else:
                        ovalp=stat[plev][stime][sl]
                        if(sl[0:2] == 'of'):
                            ovalp=stat[plev][stime]['ob'] - ovalp
                        elif(sl[0:2] == 'oa'):
                            ovalp=stat[plev][stime]['ob'] - ovalp
                        ovalc=format%(ovalp)

                    card=card + ovalc

                    if(ovalp == 9999.9):
                        oval=self.undef
                    else:
                        oval=ovalp
                        
                    if(doobsfile): stnlist.append(oval)
                    
                if(doprintterm): print card
                if(doupafile): self.PrintCards(card)

            if(doprintterm): print
            if(doupafile): self.PrintCards(' ')

            if(doobsfile):
                stndata.fromlist(stnlist)
                stndata.write(self.Ofo[stime])


    def MakeNoloadStats(self):

        N=open('/tmp/noload.stn.obs','wb')
      
        stimes=self.SynopticTimes
        plevs=self.MandatoryPressureLevels
        slist=self.statvars

        stnid='mrnload\0'
        rlat=0.0
        rlon=0.0
        stndt=0.0
        stnlev=len(plevs)+1
        stnflag=1

        iwmoid=0
        subtype=0
        source=0
        elevation=self.undef

        stnhead=struct.pack('8sfffii',stnid,rlat,rlon,stndt,stnlev,stnflag)
        stnsfc=struct.pack('%df'%(self.NsfcvarStn),float(iwmoid),float(subtype),float(source),elevation)

        N.write(stnhead)
        N.write(stnsfc)
        
        stnlist=[]
        stndata=array.array('f')

        for plev in plevs:

            stnlist.append(float(plev))
            for sl in slist:
                oval=self.undef
                stnlist.append(oval)

        stndata.fromlist(stnlist)
        stndata.write(N)

        stnid='alldone '
        stnrec=struct.pack('8sfffii',stnid,0.0,0.0,0.0,0,0)
        N.write(stnrec)



    def RmNoloads(self):

        from glob import glob

        apaths=[self.ObsDir,self.uPaDir]

        for apath in apaths:

            paths=glob(apath+"/*")

            for path in paths:
                try:
                    siz=os.path.getsize(path)
                except:
                    siz=-999
                if(siz == self.SizNoload or siz == 0):
                    print "Killing (%d): %s"%(siz,path)
                    os.unlink(path)

        
    def RmZeros(self):

        from glob import glob

        apaths=[self.ObsDir,self.uPaDir]

        for apath in apaths:

            paths=glob(apath+"/*")

            for path in paths:
                try:
                    siz=os.path.getsize(path)
                except:
                    siz=-999
                if(siz == 0):
                    print "Killing (%d): %s"%(siz,path)
                    os.unlink(path)

        
            



        
if (__name__ == "__main__"):

    import sys
    import time

    import mf

    verb=0

    #
    # instantiate the upamon object which opens a file
    #

    u=upamon(var='t')
    #u=upamon(var='w')


    #
    # read the cards; all at once
    #
    
    stime=time.time()
    cards=u.ReadCards()
    mf.Timer('read cards',stime)


    #
    # load the meta and data arrays from the cards
    #
    
    stime=time.time()
    (umeta,udata)=u.LoadDataArrays(cards)
    mf.Timer('loaded the data',stime)

    stns=umeta.keys()
    stns.sort()

    stimer=time.time()
    for s in stns:

        dd=umeta[s].keys()
        basemeta=umeta[s][dd[0]][0]

        #
        # get the station data and do stats
        #

        dd=udata[s]
        stat=u.InitStats()
        dtgs=u.RunStats(stat,dd)

        #
        # finalize, e.g,  /N and RMS() 
        #
        u.FinaliseStats(stat)

        #
        # output
        #
        u.PrintStats(stat,basemeta,dtgs,s,doprintterm=1)

    u.FinaliseOutput()

    mf.Timer('stat calc',stimer)

    
