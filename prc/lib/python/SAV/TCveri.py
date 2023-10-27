"""
config for TC verification processing

"""

import os
import sys
import string
import posixpath
import glob
import copy

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

import cPickle as pickle

import time

import w2
import mf
import atcf
import TCtdos
import TCw2 as TC


from const import  *


dTau12=12


def VdeckVitals(stmids,imodels,tdoopt,ruleopt,phr,verb):

    printall=1

    if(ruleopt == None):
        oruleopt='ops'
    else:
        oruleopt=ruleopt

    
    nmodels=len(imodels)

    if(nmodels > 2):
        print 'EEE(TCveri.VdeckVitals): too many models ',nmodels,imodels
        sys.exit()



    #
    # cycle through 1-2 models
    #

    filt0012=filt0618=0

    nmodel=1
    for imodel in imodels:

        vdmodel=imodel

        limod=len(imodel)
        cphr=imodel[limod-2:limod]

        if(cphr == '00' or cphr == '06' or cphr == '12'):
            phr=int(cphr)
            imodel=imodel[0:limod-2]
        else:
            phr=None

        if(verb): print 'mmmmmmmmmmm imodel,vdmodel,phr: ',imodel,vdmodel,phr

        if(atcf.DtauModel[imodel] == 12):
            
            if(phr == None and atcf.StartSynHourModel[imodel] == 6):
                filt0012=0
                filt0618=1
            elif(phr != None and int(phr) == 6 and atcf.StartSynHourModel[imodel] == 6):
                filt0012=1
                filt0618=0
            elif(phr != None and int(phr) == 0 and atcf.StartSynHourModel[imodel] == 6):
                filt0012=0
                filt0618=1
            elif(phr != None and int(phr) == 6):
                filt0012=0
                filt0618=1
            else:
                filt0012=1
                filt0618=0

        for stmid in stmids:

            (stm3id,year)=stmid.split('.')
            b1id=stm3id[2]
            b3id=TC.Basin1toBasin3[b1id]
            
            vddir=TC.BaseDirDataTc+"/vdeck/%s"%(year)

            vdmask="%s/vdeck.%s.%s.%s.%s.*.txt"%(vddir,b3id,year,stm3id,vdmodel)
            
            ls=glob.glob(vdmask)
            if(len(ls) == 1):
                vdpath=ls[0]
            else:
                print 'EEE no vdecks for: ',stmid,' and vdmask: ',vdmask
                return(None,None,None,None,None,None,None)

            if(verb): print 'vdmask ',vdmask,ls,vdmodel
            
            tt=vdpath.split('.')
            b3id=tt[1]
            year=tt[2]
            stm3id=tt[3]
            b1id=stm3id[2:3]
            bdtg=tt[5]
            edtg=tt[6]

            vdcards=open(vdpath,'r').readlines()

            if(nmodel == 1):
                vdmodel1=vdmodel
                (idtgs,fcs1)=TC.ParseVdeck2Fcs(vdcards)
                rclist=TC.SetBtVdeck(stm3id,imodel,idtgs,fcs1,ruleopt,verb=verb)
            elif(nmodel == 2):
                vdmodel2=vdmodel
                (idtgs,fcs2)=TC.ParseVdeck2Fcs(vdcards)
                rclist=TC.SetBtVdeck(stm3id,imodel,idtgs,fcs2,ruleopt,verb=verb)

            taus=rclist[0]
            dtgs=rclist[1]
            btvflg=rclist[2]
            btgcards=rclist[3]
            edtgplot=rclist[4]
            blatmin=rclist[5]
            blatmax=rclist[6]
            blonmin=rclist[7]
            blonmax=rclist[8]
            ruleflg=rclist[9]
            bttime2carq=rclist[10]
            bttime2warn=rclist[11]
            bttime2end=rclist[12]
            blatminall=rclist[13]
            blatmaxall=rclist[14]
            blonminall=rclist[15]
            blonmaxall=rclist[16]



        nmodel=nmodel+1

    if(nmodels == 1):
        fcs2=copy.deepcopy(fcs1)
        vdmodel2=vdmodel1
        



    btpycards=[]
    dfepycards=[]
    pycards=[]
    scards=[]

    #
    #
    #

    cntbt={}
    cntfc={}
    cnthit={}  
    cntmiss={}  
    cntmissfc={}  
    cntover={}  
    cntoverfc={}  

    def FCconsistency():

        mod1consist={}

        for dtg in dtgs:

            if(btvflg[dtg] == 1):

                i=0
                for tau in taus:

                    try:
                        [vdtg,flat1,flon1,fvmax,flf,ffe,fcte,fate,ffcte,ffate,fewe,fnse]=fcs1[dtg,tau]
                        [blat1,blon1,bvmax1,blf1]=fcs1[dtg,tau,'bt']

                        [vdtg2,flat2,flon2,fvmax2,flf2,ffe2,fcte2,fate2,ffcte2,ffate2,fewe2,fnse2]=fcs2[dtg,tau]
                        [bvmax2,fvmax2,fve2,fveu2,fver2]=fcs2[dtg,tau,'vmax']
                        [blat2,blon2,bvmax2,blf2]=fcs1[dtg,tau,'bt']

                    except:
                        if(verb): print 'fail1111 ',tau
                        mod1consist[dtg,tau]=[-999.0]
                        i=i+1
                        continue

                    if(tau == 0):
                        blat0=blat1
                        blon0=blon1
                        flat0=flat1
                        flon0=flon1
                        blat1m1=blat1
                        blon1m1=blon1
                        flat1m1=flat1
                        flon1m1=flon1
                        taum1=0
                        dtau=0


                    elif(i> 0):

                        taum1=taus[i-1]
                        dtau=tau-taum1

                        try:
                            [vdtg,flat1m1,flon1m1,fvmaxm1,flfm1,ffem1,fctem1,fatem1,ffctem1,ffatem1,fewem1,fnsem1]=fcs1[dtg,taum1]
                            [blat1m1,blon1m1,bvmax1m1,blf1m1]=fcs1[dtg,taum1,'bt']
                        except:
                            #
                            # go back to early tau for ofc (no 60, 84, ...) 
                            #
                            taum1=taus[i-2]
                            dtau=tau-taum1
                            try:
                                [vdtg,flat1m1,flon1m1,fvmaxm1,flfm1,ffem1,fctem1,fatem1,ffctem1,ffatem1,fewem1,fnsem1]=fcs1[dtg,taum1]
                                [blat1m1,blon1m1,bvmax1m1,blf1m1]=fcs1[dtg,taum1,'bt']
                            except:
                                print 'EEEEEEEEE no tau-2 fc ........',dtg,tau,i,taum1,taus
                                #sys.exit()



                    if( blat1 > -90.0 and blat1 < 88.0 and flat1 > -90.0 and flat1 < 88.0 ):

                        #print 
                        #print '0000000000000bbbbbb %s tau %03d'%(dtg,tau),blat0,blon0
                        #print '1111111111111bbbbbb %s tau %03d'%(dtg,tau),blat1,blon1
                        #print 'm1m1m1m1m1m1mbbbbbb %s tau %03d'%(dtg,tau),blat1m1,blon1m1
                        #print 
                        #print '0000000000000ffffff %s tau %03d'%(dtg,tau),flat0,flon0
                        #print '1111111111111ffffff %s tau %03d'%(dtg,tau),flat1,flon1
                        #print 'm1m1m1m1m1m1mffffff %s tau %03d'%(dtg,tau),flat1m1,flon1m1

                        if(dtau == 0):
                            (fccourse,fcspeed,fciumotion,fcivmotion)=(0.0,0.0,0.0,0.0)
                            (btcourse,btspeed,btiumotion,btivmotion)=(0.0,0.0,0.0,0.0)
                        else:
                            (fccourse,fcspeed,fciumotion,fcivmotion)=TC.rumhdsp(flat1m1,flon1m1,flat1,flon1,dtau)
                            (btcourse,btspeed,btiumotion,btivmotion)=TC.rumhdsp(blat1m1,blon1m1,blat1,blon1,dtau)

                        #print 'bbbbbbbbbbbbbffffff %s tau %03d'%(dtg,tau),btcourse,btspeed
                        #print 'rrrrrrrrrrrrrffffff %s tau %03d'%(dtg,tau),fccourse,fcspeed

                        fe=gc_dist(blat1,blon1,flat1,flon1)
                        gc0=gc_dist(blat0,blon0,flat1,flon1)
                        bgc0=gc_dist(blat0,blon0,blat1,blon1)

                        (difx,dify,theta)=gc_theta(blat1,blon1,flat1,flon1)
                        (difx0,dify0,theta0)=gc_theta(blat0,blon0,flat1,flon1)
                        (bdifx0,bdify0,btheta0)=gc_theta(blat0,blon0,blat1,blon1)

                        #print '1111111111111 tau %03d'%(tau),blat0,blon0,blat1,blon1,flat1,flon1
                        #print '111 tau %03d %s fe: %6.1f Th: %5.1f x,y: %5.0f %5.0f'%(tau,dtg,fe,theta,difx,dify)
                        #print '111 tau %03d %s gc0: %6.1f Th: %5.1f x,y: %5.0f %5.0f'%(tau,dtg,gc0,theta0,difx0,dify0)
                        #print '111 tau %03d %s gc0: %6.1f Th: %5.1f x,y: %5.0f %5.0f'%(tau,dtg,bgc0,btheta0,bdifx0,bdify0)

                        mod1consist[dtg,tau]=[fe,theta,difx,dify,gc0,theta0,difx0,dify0,bgc0,btheta0,bdifx0,bdify0,
                                              flat1,flon1,blat1,blon1,fccourse,fcspeed,btcourse,btspeed]
                    else:
                        mod1consist[dtg,tau]=[-888.0]

                    i=i+1


            else:

                for tau in taus:
                    mod1consist[dtg,tau]=[-789.0]

            
        for tau in taus:

            if(verb): print
            ndtgs=len(dtgs)
            for i in range(0,ndtgs):

                rcp0=mod1consist[dtgs[i],tau]
                if(i<ndtgs-1):
                    try:
                        rcp1=mod1consist[dtgs[i+1],tau]
                    except:
                        rcp1=rcp0
                else:
                    rcp1=rcp0

                if(i<ndtgs-2):
                    try:
                        rcp2=mod1consist[dtgs[i+2],tau]
                    except:
                        rcp2=rcp0
            else:
                rcp2=rcp0
                
            if(i<ndtgs-3):
                try:
                    rcp3=mod1consist[dtgs[i+3],tau]
                except:
                    rcp3=rcp0
            else:
                rcp3=rcp0
                
            fep0=rcp0[0]
            fep1=rcp1[0]
            fep2=rcp2[0]
            fep3=rcp3[0]

            if(fep0 >= 0.0 and fep1 >= 0.0):
                ConsistAnal(rcp0,rcp1,i,tau,dtgs,dtrun=6.0)
            elif(fep0 >= 0.0 and fep2 >= 0.0):
                ConsistAnal(rcp0,rcp2,i,tau,dtgs,dtrun=12.0)
                #print "yyy222: i: %2d t: %03d %s fes: %5.0f %5.0f"%(i,tau,dtgs[i],fep0,fep2)
            elif(fep0 >= 0.0 and fep3 >= 0.0):
                ConsistAnal(rcp0,rcp3,i,tau,dtgs,dtrun=18.0)
                #print "yyy222: i: %2d t: %03d %s fes: %5.0f %5.0f"%(i,tau,dtgs[i],fep0,fep2)
            else:
                continue
                #print "nnn: i: %2d t: %03d %s"%(i,tau,dtgs[i])



    def SimpleTauStat(stat,var,varname,tau):

        var2=var*var
        
        try:
            stat[varname,tau,'n']=stat[varname,tau,'n']+1
        except:
            stat[varname,tau,'n']=1

        try:
            stat[varname,tau,'sum']=stat[varname,tau,'sum']+var
        except:
            stat[varname,tau,'sum']=var

        try:
            stat[varname,tau,'abssum']=stat[varname,tau,'abssum']+math.fabs(var)
        except:
            stat[varname,tau,'abssum']=math.fabs(var)

        try:
            stat[varname,tau,'sum2']=stat[varname,tau,'sum2']+var2
        except:
            stat[varname,tau,'sum2']=var2
            


    def FinalizeStat(TauStats,ic):

        (vfe,
        vcte,vate,vctef,vatef,veweb,vnseb,
        vfve,vfveu,vfver,
        vbv,vfv)=ic

        try:
            mfe=TauStats[vfe,tau,'sum']/TauStats[vfe,tau,'n']
        except:
            mfe=-999.0

        try:
            mcte=TauStats[vcte,tau,'sum']/TauStats[vcte,tau,'n']
            mate=TauStats[vate,tau,'sum']/TauStats[vate,tau,'n']
        except:
            mcte=-999.0
            mate=-999.0

        try:
            mctef=TauStats[vctef,tau,'sum']/TauStats[vctef,tau,'n']
            matef=TauStats[vatef,tau,'sum']/TauStats[vatef,tau,'n']
        except:
            mctef=-999.0
            matef=-999.0

        try:
            meweb=TauStats[veweb,tau,'sum']/TauStats[veweb,tau,'n']
            mnseb=TauStats[vnseb,tau,'sum']/TauStats[vnseb,tau,'n']
        except:
            meweb=-999.0
            mnseb=-999.0

        try:
            mave=TauStats[vfve,tau,'abssum']/TauStats[vfve,tau,'n']
            mbve=TauStats[vfve,tau,'sum']/TauStats[vfve,tau,'n']
        except:
            mave=-999.0
            mbve=-999.0

        try:
            maveu=TauStats[vfveu,tau,'abssum']/TauStats[vfveu,tau,'n']
            mbveu=TauStats[vfveu,tau,'sum']/TauStats[vfveu,tau,'n']
        except:
            maveu=-999.0
            mbveu=-999.0

        try:
            maver=TauStats[vfver,tau,'abssum']/TauStats[vfver,tau,'n']
            mbver=TauStats[vfver,tau,'sum']/TauStats[vfver,tau,'n']
        except:
            maver=-999.0
            mbver=-999.0

        try:
            mbv=TauStats[vbv,tau,'abssum']/TauStats[vbv,tau,'n']
            mfv=TauStats[vfv,tau,'sum']/TauStats[vfv,tau,'n']
        except:
            mbv=-999.0
            mfv=-999.0


        rc=(mfe,mcte,mate,mctef,matef,meweb,mnseb,
            mave,mbve,maveu,mbveu,maver,mbver,
            mbv,mfv)

        return(rc)




    TauStats={}

    for tau in taus:

        cntbt[tau]=0
        cntfc[tau]=0
        cnthit[tau]=0
        cntmiss[tau]=0
        cntover[tau]=0
        cntmissfc[tau]=0
        cntoverfc[tau]=0



    doFCconsistchk=0
    #
    # run-to-run forecast consistency check
    #

    if(doFCconsistchk): FCconsistency()
        

    tdos=[]
    fcgcards=[]
    for dtg in dtgs:

        hh=dtg[8:10]

        if(filt0012 and (hh == '06' or hh == '18')):
            continue
        elif(filt0618 and (hh == '00' or hh == '12')):
            continue

        if(btvflg[dtg] == 1):

            fcgcard="%s %s :: "%(imodel,dtg)

            ihitbt00=0
            ihitfc00=0

            for tau in taus:

                if(tau == 0): ihitbt00=1

                try:
                    [vdtg,flat,flon,fvmax,flf,ffe,fcte,fate,fctef,fatef,feweb,fnseb]=fcs1[dtg,tau]
                    [bvmax,fvmax,fve,fveu,fver]=fcs1[dtg,tau,'vmax']
                    tdo=fcs1[dtg,tau,'tdo']

                    [vdtg2,flat2,flon2,fvmax2,flf2,ffe2,fcte2,fate2,fctef2,fatef2,feweb2,fnseb2]=fcs2[dtg,tau]
                    [bvmax2,fvmax2,fve2,fveu2,fver2]=fcs2[dtg,tau,'vmax']
                    tdo2=fcs2[dtg,tau,'tdo']
                except:
                    if(verb): print 'fail2222',tau
                    continue

                tdos.append(tdo)

                if(tdoopt != None and tdo != tdoopt): continue 

                ihitbt=0
                try:
                    if(btvflg[vdtg] == 1):
                        ihitbt=1
                        cntbt[tau]=cntbt[tau]+1
                except:
                    continue

                #
                # forecast made
                #
                fctest1=( (flat > -90.0 and flat < 88.0) or (flat == 97.9 and fvmax > 0.0) )
                fctest2=( (flat2 > -90.0 and flat2 < 88.0) or (flat2 == 97.9 and fvmax2 > 0.0) )
                
                fctest=( fctest1 and fctest2 )

                if(fctest):
                    try:
                        if(btvflg[vdtg] == 1):
                            ihitfc=1
                            cntfc[tau]=cntfc[tau]+1
                            if(tau == 0): ihitfc00=1
                    except:
                        ihitfc=-999

                #
                # no forecast ........
                #
                else:
                    try:
                        if(btvflg[vdtg] == 1):
                            ihitfc=-1
                        else:
                            ihitfc=0
                    except:
                        continue


                if(verb): print 'fffffffff ',"%03d %2d %2d %2d %2d"%(tau,ihitbt,ihitfc,ihitbt00,ihitfc00),dtg,vdtg,flat,tdo,fctest


                if(ihitbt == 1 and ihitfc == 1): cnthit[tau]=cnthit[tau]+1
                if(ihitbt == 1 and ihitfc == -1):
                    cntmiss[tau]=cntmiss[tau]+1
                    if(ihitfc00 == 1): cntmissfc[tau]=cntmissfc[tau]+1

                if(ihitbt == 0 and ihitfc == 1):
                    cntover[tau]=cntover[tau]+1
                    if(ihitfc00 ==1): cntoverfc[tau]=cntoverfc[tau]+1


                if(vdtg <= edtgplot and fctest):

                    offe=-999
#                    try:
                    if(btvflg[vdtg] == 1):
                        
                        offe=ffe

                        SimpleTauStat(TauStats,ffe,'ffe',tau)
                        SimpleTauStat(TauStats,fcte,'fcte',tau)
                        SimpleTauStat(TauStats,fate,'fate',tau)
                        SimpleTauStat(TauStats,fctef,'fctef',tau)
                        SimpleTauStat(TauStats,fatef,'fatef',tau)
                        SimpleTauStat(TauStats,feweb,'feweb',tau)
                        SimpleTauStat(TauStats,fnseb,'fnseb',tau)
                       
                        if(fve != -999.0):
                            SimpleTauStat(TauStats,fve,'fve',tau)
                            SimpleTauStat(TauStats,bvmax,'bvm',tau)
                            SimpleTauStat(TauStats,fvmax,'fvm',tau)

                        if(fveu != -999.0):
                            SimpleTauStat(TauStats,fveu,'fveu',tau)

                        if(fver != -999.0):
                            SimpleTauStat(TauStats,fver,'fver',tau)

#
# 2nd aid
#
                        SimpleTauStat(TauStats,ffe2,'ffe2',tau)
                        SimpleTauStat(TauStats,fcte2,'fcte2',tau)
                        SimpleTauStat(TauStats,fate2,'fate2',tau)
                        SimpleTauStat(TauStats,fctef2,'fctef2',tau)
                        SimpleTauStat(TauStats,fatef2,'fatef2',tau)
                        SimpleTauStat(TauStats,feweb2,'feweb2',tau)
                        SimpleTauStat(TauStats,fnseb2,'fnseb2',tau)
                       
                        if(fve2 != -999.0):
                            SimpleTauStat(TauStats,fve2,'fve2',tau)
                            SimpleTauStat(TauStats,bvmax2,'bvm2',tau)
                            SimpleTauStat(TauStats,fvmax2,'fvm2',tau)

                        if(fveu != -999.0):
                            SimpleTauStat(TauStats,fveu2,'fveu2',tau)

                        if(fver != -999.0):
                            SimpleTauStat(TauStats,fver2,'fver2',tau)



                        if(tau == 36 or tau == 72):
                            dfe=ffe2-ffe
                            if(tau == 36): fenorm=75.0
                            if(tau == 72): fenorm=150.0

                            if(ffe2 == 0.0):
                                dfep=-999.9
                                dfeppacflt=-999.9
                            else:
                                dfep=(dfe/ffe2)*100.0
                                dfeppacflt=(dfe/fenorm)*100.0


                            dfepycard="""DfeVitals['%s','%s','%s','%s',%d] = [%6.1f,%6.1f,%6.1f,%4.0f,%4.0f,'%s']"""%\
                                      (stmid,vdtg,imodel,oruleopt,tau,ffe,ffe2,dfe,dfep,dfeppacflt,tdo)
                            if(verb): print 'dfe: ',dfepycard
                            dfepycards.append(dfepycard)


#                    except:
#                        if(verb): print 'fail2: ',tau,vdtg
#                        continue

                    #print 'fcs1 ',tau,dtg,vdtg,flat,offe,flf
                    fcgcard="%s %03d %5.1f %5.1f %3d %4d :"%(fcgcard,tau,flat,flon,int(fvmax),int(offe))


            fcgcards.append(fcgcard)


    for tau in taus:

#
# 11111111111 aid 1
#

        vfe='ffe'; vcte='fcte'; vate='fate'; vctef='fctef'; vatef='fatef'
        veweb='feweb'; vnseb='fnseb'; vfve='fve'; vfveu='fveu'; vfver='fver'; vbv='bvm'; vfv='fvm'

        ic1=(vfe,
            vcte,vate,vctef,vatef,veweb,vnseb,
            vfve,vfveu,vfver,
            vbv,vfv)

        (mfe1,
         mcte1,mate1,mctef1,matef1,meweb1,mnseb1,
         mave1,mbve1,maveu1,mbveu1,maver1,mbver1,
         mbv1,mfv1)=FinalizeStat(TauStats,ic1)

#
# 2222222222 aid 2
#

        vfe2='ffe2'; vcte2='fcte2'; vate2='fate2'; vctef2='fctef2'; vatef2='fatef2'
        veweb2='feweb2'; vnseb2='fnseb2'; vfve2='fve2'; vfveu2='fveu2'; vfver2='fver2'; vbv2='bvm2'; vfv2='fvm2'
                      
        ic2=(vfe2,
            vcte2,vate2,vctef2,vatef2,veweb2,vnseb2,
            vfve2,vfveu2,vfver2,
            vbv2,vfv2)
        
        (mfe2,
         mcte2,mate2,mctef2,matef2,meweb2,mnseb2,
         mave2,mbve2,maveu2,mbveu2,maver2,mbver2,
         mbv2,mfv2)=FinalizeStat(TauStats,ic2)


        if(verb and cntfc > 0):
            print
            print "      cntbt : %03d %3d"%(tau,cntbt[tau])
            print "      cntfc : %03d %3d"%(tau,cntfc[tau])
            print "     cnthit : %03d %3d"%(tau,cnthit[tau])
            print "    cntmiss : %03d %3d"%(tau,cntmiss[tau])
            print "    cntover : %03d %3d"%(tau,cntover[tau])
            print "  cntmissfc : %03d %3d"%(tau,cntmissfc[tau])
            print "  cntoverfc : %03d %3d"%(tau,cntoverfc[tau])
            print "       mfe1 : %03d %4.0f %2d"%(tau,mfe1,mfe1)
            print "      mcte1 : %03d %4.0f %2d"%(tau,mcte1,mcte1)
            print "      mate1 : %03d %4.0f %2d"%(tau,mate1,mate1)

            print "      mave1 : %03d %4.0f %2d"%(tau,mave1,mave1)
            print "      mbve1 : %03d %4.0f %2d"%(tau,mbve1,mbve1)
            print "     maveu1 : %03d %4.0f %2d"%(tau,maveu1,maveu1)
            print "     mbveu1 : %03d %4.0f %2d"%(tau,mbveu1,mbveu1)
            print "     maver1 : %03d %4.0f %2d"%(tau,maver1,maver1)
            print "     mbver1 : %03d %4.0f %2d"%(tau,mbver1,mbver1)
            print "       mbv1 : %03d %4.0f %2d"%(tau,mbv1,mbv1)
            print "       mfv1 : %03d %4.0f %2d"%(tau,mfv1,mfv1)


        scard1="%03d C %2d %2d %2d %2d fc %2d %2d"%(tau,cntbt[tau],cntfc[tau],
                                              cntmiss[tau],cntover[tau],
                                              cntmissfc[tau],cntoverfc[tau]
                                              )

        pycard1="C %2d %2d %2d %2d fc %2d %2d"%(cntbt[tau],cntfc[tau],
                                              cntmiss[tau],cntover[tau],
                                              cntmissfc[tau],cntoverfc[tau]
                                              )
        pycard1=pycard1

        ovdmodel1=vdmodel1
        if(tdoopt != None):
            ovdmodel1=vdmodel1+tdoopt

        ovdmodel2=vdmodel2
        if(tdoopt != None):
            ovdmodel2=vdmodel2+tdoopt

        def scardout(ovdmodel1,
                     mfe1,mcte1,mate1,
                     mctef1,matef1,
                     meweb1,mnseb1,
                     mbv1,mfv1,mave1,mbve1,
                     maveu1,mbveu1,maver1,mbver1):
        

            scard="%9s FE %4.0f  CT/Ab: %4.0f %4.0f CT/Av: %4.0f %4.0f CT/AeN: %4.0f %4.0f"%\
                    (ovdmodel1,mfe1,mcte1,mate1,
                     mctef1,matef1,
                     meweb1,mnseb1)

            scard="%s VmB/Fc: %3.0f %3.0f VeCA/b: %3.0f %3.0f"%\
                    (scard,mbv1,mfv1,mave1,mbve1)
            
            scard="%s  VeUA/b: %5.1f %5.1f VeRA/b: %5.1f %5.1f"%\
                    (scard,maveu1,mbveu1,maver1,mbver1)

            return(scard)



        scard2=scardout(ovdmodel1,
                        mfe1,mcte1,mate1,
                        mctef1,matef1,
                        meweb1,mnseb1,
                        mbv1,mfv1,mave1,mbve1,
                        maveu1,mbveu1,maver1,mbver1)
        

        scard3=scardout(ovdmodel2,
                        mfe2,mcte2,mate2,
                        mctef2,matef2,
                        meweb2,mnseb2,
                        mbv2,mfv2,mave2,mbve2,
                        maveu2,mbveu2,maver2,mbver2)
        

        scard="%s %s %s"%(scard1,scard2,scard3)




        if(mfe1 != -999.0 or printall):
            scards.append(scard)


        if(tdoopt != None):
            otdoopt=tdoopt
        else:
            otdoopt='ALL'


    return(scards)


#--------------------------------------------------
#
#  load w2 adecks into dic
#
#--------------------------------------------------

def LoadW2TcFcCards(stmopt,year,phr,imodel,amodel,verb=0):

    ftmfcards=None
    ftcards=None
    
    ftdir=TC.AdeckDirW2
    ftype='adeck'

    if(phr != None):
        omodel="%s%02d"%(imodel,int(phr))
        tamodel="%s%02d"%(amodel,int(phr))
    else:
        omodel=imodel
        tamodel=amodel
        
    ftmask='%s/%s/w2.adeck.%s.%s.*'%(ftdir,year,omodel,stmopt)
    if(verb): print 'W2 ADECK ftmask: ',ftmask
    ftpaths=glob.glob(ftmask)
    
    if(verb):
        print 'adeck data for : ',imodel,' ftpaths: ',ftpaths
        for ftpath in ftpaths:
            print 'ffff ',ftpath

    ftcards=[]    
    for ftpath in ftpaths:
        (d,f)=os.path.split(ftpath)
        cards=open(ftpath).readlines()
        for card in cards:
            ftcards.append(card)

    aftcards={}

    for ftcard in ftcards:
        tt=ftcard.split(',')
        dtg=tt[2].strip()
        iamodel=tt[4].strip()
        if(iamodel == tamodel):
            try:
                aftcards[dtg].append(ftcard)
            except:
                aftcards[dtg]=[]
                aftcards[dtg].append(ftcard)

    return(aftcards)



def ParseFtCards(dtg,cards,taumax=144,verb=0):

    verb=0
    
    stms=[]
    ftcs={}
    ftcs2={}

    #
    # for older tracking files check if cyclones
    #
    if(cards[0].find('NO CY') != -1):
        print 'WWWW \'NO CYCLONES TO TRACK\' message in track file...'
        return(ftcs,ftcs2)

    
    nstms=int(cards[0].split()[0])

    if(verb):
        print 'nnnn ',nstms,cards[nstms+2]

    n=-1
    for card in cards:
        
        n=n+1
        if(n < nstms+2): continue
        if(verb): print card[:-1]
        tt=card.split()

        if( ( tt[0] == '***') or ( tt[0] != 'LOST' and tt[0] != 'FINISHED') ):

            #
            # new style storm from tracker SSS.YYYY
            #

            try:
                ss=tt[1].split('.')
                stm=ss[0]
            except:
                stm=tt[1]
            
            stms.append(stm)
            
            if( tt[0] == '***'):
                latwarn=float(tt[2])
                lonwarn=float(tt[3])
                ftcs[stm]=[(latwarn,lonwarn)]
                ftcs2[stm]=[(latwarn,lonwarn)]
            
            else:
                tau=int(tt[0])
                sdtgm12=mf.dtginc(dtg,tau-12);
                sdtgp12=mf.dtginc(dtg,tau+12);
                sdtg=mf.dtginc(dtg,tau);
                lat=float(tt[2])
                lon=float(tt[3])
                ccirc='CC'
                if(float(tt[6]) < 0): ccirc='VM'

                ft=(tau,sdtg,sdtgm12,sdtgp12,lat,lon,ccirc)

                try:
                    ftcs[stm].append(ft)
                except:
                    print 'EEEEEEEEE no warning posit for: ',stm
                    sys.exit()

   
    #
    # extend fc track to taumax (120) with 999 to for force detection of
    # bt for POD purposes
    #

    
    stms=mf.uniq(stms)
    #
    # check for an fc with no posits
    # add a noload
    #
    donoload=0
    for stm in stms:
        
        np=len(ftcs[stm])
        if(np == 1):
            ft=(0,dtg,dtg,dtg,99.9,999.9,'CC')
            ftcs[stm].append(ft)
            
        if(donoload):
            (latwarn,lonwarn)=ftcs[stm][0]
            ftcs[stm]=[(latwarn,lonwarn)]
            ft=(0,dtg,dtg,dtg,99.9,999.9,'CC')
            ftcs[stm].append(ft)

    
    for stm in stms:
        np=len(ftcs[stm])-1
        (ftau,fsdtg,sdtgm12,sdtgp12,lat,lon,ccirc)=ftcs[stm][np]

        if(ftau < taumax):
            npall=taumax/dTau12+1
            sdtg=fsdtg
            tau=ftau+dTau12
            for i in range(np+1,npall+1):
                sdtg=mf.dtginc(sdtg,dTau12)
                sdtgm12=mf.dtginc(sdtg,-dTau12)
                sdtgp12=mf.dtginc(sdtg,+dTau12)
                alat=99.9
                alon=999.9
                accirc='CC'
                ftadd=(tau,sdtg,sdtgm12,sdtgp12,alat,alon,accirc)
                ftcs[stm].append(ftadd)
                tau=tau+dTau12
                

    return(ftcs)

def ParseFtMfCards(dtg,cards):


    #
    # 20041007: handle bad data
    #
    
    def splitfc(cards,i,undef):

        try:
            scard=cards[i]
        except:
            scard='undef '

        try:
            tt=scard.split()
            tlon=float(tt[1])
            tlat=float(tt[2])
            tval=float(tt[3])
            tdist=TC.gc_dist(flat,flon,tlat,tlon)
        except:
            tdist=tval=tlon=tlat=undef
            
        return(tdist,tval,tlon,tlat)

    def splittau(cards,i):
        tt=cards[i].split()
        type=tt[0]
        tau=int(float(tt[2]))
        stmid=tt[4]
        flon=float(tt[5])
        flat=float(tt[6])
        #print type,tau,stmid,flon,flat
        i=i+1

        tt=cards[i].split()
        #print i,tt
        nhi=int(tt[0])
        nlo=int(tt[1])
        i=i+1

        return(type,tau,stmid,flon,flat,nhi,nlo,i)


    verb=0

    undef=1e20
    
    dcrit={}
    dcrit['SPD','H']=400.0
    dcrit['SPD','L']=200.0
    dcrit['VRT','H']=400.0
    dcrit['VRT','L']=200.0

    ftcstruct={}

    stms=[]
    ftcs={}

    ncards=len(cards)

    for i in range(0,ncards):

        if(mf.find(cards[i],'tau:')):
           
           (type,tau,stmid,flon,flat,nhi,nlo,i)=splittau(cards,i)

           tdcrit=dcrit[type,'H']
           tdmin=undef
           for j in range(0,nhi):
               (tdist,tval,tlon,tlat)=splitfc(cards,i,undef)
               if(tdist < tdcrit and tdist < tdmin):
                   tdmin=tdist
                   tvalcrit=tval
               if(verb): print 'hi ',i,tdcrit,tdist,tlon,tlat,tval,ncards
               i=i+1

           if(type == 'SPD'): typeout='spdmax'
           if(type == 'VRT'): typeout='vrtmax'
           if(tdmin == undef):
               tdmin=-888.8
               tvalcrit=-88.8
           ftcstruct[stmid,tau,typeout,'dist']=tdmin
           ftcstruct[stmid,tau,typeout,'val']=tvalcrit
         
           if(verb):
               print "hhhhhhhhhhh stm: %s tau: %03d type: %s ::  %7.1f  %7.2f"%\
                     (stmid,tau,type,tdmin,tvalcrit)


           tdcrit=dcrit[type,'L']
           tdmin=undef
           for j in range(0,nlo):
               (tdist,tval,tlon,tlat)=splitfc(cards,i,undef)
               if(tdist < tdcrit and tdist < tdmin):
                   tdmin=tdist
                   tvalcrit=tval
               if(verb): print 'lo ',i,tdist,tlon,tlat,tval
               i=i+1
               
           if(type == 'SPD'): typeout='spdmin'
           if(type == 'VRT'): typeout='vrtmin'
           if(tdmin == undef):
               tdmin=-888.8
               tvalcrit=-88.8
           ftcstruct[stmid,tau,typeout,'dist']=tdmin
           ftcstruct[stmid,tau,typeout,'val']=tvalcrit
         

           if(verb):
               print "lllllllllll stm: %s tau: %03d type: %s ::  %7.1f  %7.2f"%\
                     (stmid,tau,type,tdmin,tvalcrit)

           #print 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee ',i

    return(ftcstruct)



def LoadItrkTaus(dtg,taus,fcs):

    itrk={}
    
    nt=0
    for tau in taus:
        try:
            itrk[tau]=fcs[dtg,tau]
            flat=itrk[tau][1]
            if(flat > -88 and flat < 88.0):
                nt=nt+1
        except:
            #itrk[tau]=[-99.9,-999.9,-99.9]
            vdtg99='1776122613'
            flat99=-99.9
            flon99=-999.9
            fvmax99=-99.9
            flf99=-0.99
            ffe99=-999.9
            fcte99=-999.9
            fate99=-999.9
            ffcte99=-999.9
            ffate99=-999.9
            fewe99=-999.9
            fens99=-999.9
            fr34quad99=[-77,-77,-77,-77]
            fr50quad99=[-77,-77,-77,-77]

            itrk[tau]=[vdtg99,flat99,flon99,fvmax99,flf99,ffe99,
                       fcte99,fate99,ffcte99,ffate99,fewe99,fens99,fr34quad99,fr50quad99]

    return(itrk,nt)


def LoadItrk(dtg,fcs,dtau=6,dtaumax=144):

    itrk={}

    tau=0
    dtau=6
    nt=0

    while(tau <= dtaumax):
        
        try:
            itrk[tau]=fcs[dtg,tau]
            flat=itrk[tau][1]
            if(flat > -88 and flat < 88.0):
                nt=nt+1
        except:
            pass

        tau=tau+dtau


    return(itrk,nt)

def CheckJtrkPhr(jtrk,phr):
    #
    # in using the the 3-h interp track, the lat is in the 0 posit vice 1 position in itrk
    # use try for case of initial position only
    #
    
    iok=0
    try:
        flat=jtrk[phr][0]
        if(flat > -88.0 and flat < 88.0): iok=1
    except:
        iok=0
    return(iok)
    


#----------------------------------------------------------------------
#
# routine to smooth input track in lat,lon
# doextrap -- extrap from last point using previous motion to add
# taus  -- similar to nhc_interp.f except done on INuPT to rumterp
#
#----------------------------------------------------------------------

def FcTrackInterpFill(itrk,dtx,npass,verb=0):

    def dic2list(dic,ne):
        kk=dic.keys()
        kk.sort()

        list=[]
        for k in kk:
            list.append(dic[k][ne])

        return(list)
        
    
    def list2dic(dic,list,ne):

        kk=dic.keys()
        kk.sort()

        for i in range(0,len(kk)):
            dic[kk[i]][ne]=list[i]

        return
    

    def smth121(data,npass=0):
        
        nd=len(data)

        if(npass == 0):
            tdata=copy.deepcopy(data)
            return(tdata)

        odata=copy.deepcopy(data)
        tdata=copy.deepcopy(data)
        
        for n in range(0,npass+1):

            for i in range(0,nd):
                if(i == 0 or i == nd-1):
                    tdata[i]=odata[i]
                else:
                    tdata[i]=0.25*odata[i-1]+0.5*odata[i]+0.25*odata[i+1]
                    
            for i in range(0,nd):
                odata[i]=tdata[i]

        return(tdata)

    itaus=itrk.keys()
    itaus.sort()

    deftrk={}
    mottrk={}
    jtrk={}

    xtrk=copy.deepcopy(itrk)

    #
    # loaded defined track
    #
    for tau in itaus:

        flat=itrk[tau][1]
        flon=itrk[tau][2]
        fvmax=itrk[tau][3]
        r34quad=itrk[tau][12]
        r50quad=itrk[tau][13]

        if(flat < 85.0 and flat > -85.0):
            deftrk[tau]=[flat,flon,fvmax,r34quad,r50quad]

    deftaus=deftrk.keys()
    deftaus=deftrk.keys()
    deftaus.sort()

    ntaus=len(deftaus)

    etau=0
    if(ntaus>1): etau=deftaus[ntaus-1]

    #
    # bail if no forecasts
    #
    if(etau == 0):
        
        #
        # case of initial position only, return for phr=0...
        #
        jtrk[etau]=deftrk[etau]
        return(jtrk,itrk,deftaus)
        
    #
    # get motion of defined track
    #

    for i in range(0,ntaus):

        tau=deftaus[i]
        
        i0=i
        ip1=i+1

        if(ntaus > 1):
            
            if(i0 < ntaus-1):
                i0=i
                ip1=i+1

            elif(i0 == ntaus-1):
                i0=i-1
                ip1=i

            dtau=deftaus[ip1]-deftaus[i0]
            
        else:

            dtau=0.0
        
        if(dtau == 0.0):
            edir=270.0
            espd=0.0
            dvmax=0.0
            
        else:

            tau0=deftaus[i0]
            tau1=deftaus[ip1]
                        
            flat0=deftrk[tau0][0]
            flon0=deftrk[tau0][1]
            fvmax0=deftrk[tau0][2]

            flat1=deftrk[tau1][0]
            flon1=deftrk[tau1][1]
            fvmax1=deftrk[tau1][2]
            dvmax=fvmax1-fvmax0

            (course,speed,eiu,eiv)=TC.rumhdsp(flat0,flon0,flat1,flon1,dtau)

        #
        # use penultimate motion for end motion
        #
        
        if(i == ip1):
            otau=deftaus[ip1]
        else:
            otau=deftaus[i0]

        mottrk[otau]=[course,speed,dvmax]

    taus=mottrk.keys()
    taus.sort()

    #
    # only go out +dtx(3) h at the end for the smoother only
    # extrap after bias corr + smoothing
    #
    
    etau=taus[-1]
    etaux=etau+dtx

    otaus=range(0,etaux+1,dtx)
    
    nt=len(taus)

    n=0
    tau0=taus[n]
    if(nt >= 1): tau1=taus[n+1]

    #
    # rumterp to the dtx track (0,3,6,9,12), nhc_interpfcst.f uses linear
    #
    
    for otau in otaus:
        
        if(otau == tau0):
            dtau=0

        elif(otau >= tau1):

            atend=0
            n=n+1
            if(n == nt-1):
                n=n-1
                atend=1
            
            tau0=taus[n]
            if(nt >= 1): tau1=taus[n+1]
            
            dtau=0
            #
            # correct handling of extrap point
            #
            if(atend):
                tau0=tau1
                tau1=otaus[-1]
                dtau=otau-tau0

        else:
            dtau=otau-tau0

        rlat0=deftrk[tau0][0]
        rlon0=deftrk[tau0][1]
        vmax0=deftrk[tau0][2]
        r34quad0=deftrk[tau0][3]
        r50quad0=deftrk[tau0][4]

        course=mottrk[tau0][0]
        speed=mottrk[tau0][1]
        dvmax=mottrk[tau0][2]
        
        if(dtau > 0):
            (rlat1,rlon1)=TC.rumltlg(course,speed,dtau,rlat0,rlon0)
            vfact=float(dtau)/float((tau1-tau0))
            vmax1=vmax0+vfact*dvmax
        else:
            rlat1=rlat0
            rlon1=rlon0
            vmax1=vmax0
            vfact=0.0
            
        jtrk[otau]=[rlat1,rlon1,vmax1,r34quad0,r50quad0]

            

    rlats=dic2list(jtrk,0)
    srlats=smth121(rlats,npass)
    
    rlons=dic2list(jtrk,1)
    srlons=smth121(rlons,npass)
    
    vmaxs=dic2list(jtrk,2)
    svmaxs=smth121(vmaxs,npass)
    
    list2dic(jtrk,srlats,0)
    list2dic(jtrk,srlons,1)
    list2dic(jtrk,svmaxs,2)


    #
    # load to the input taus + extrap posits
    #
    for tau in itaus:
        
        if(tau <= etau):
            flat0=itrk[tau][1]
            flon0=itrk[tau][2]
            fvmax0=itrk[tau][3]
        
            xtrk[tau][1]=jtrk[tau][0]
            xtrk[tau][2]=jtrk[tau][1]
            xtrk[tau][3]=jtrk[tau][2]

            flat1=xtrk[tau][1]
            flon1=xtrk[tau][2]
            fvmax1=xtrk[tau][3]
            
        elif(tau <= etaux):
            
            xtrk[tau]=itrk[etau]
            
            flat0=itrk[tau][1]
            flon0=itrk[tau][2]
            fvmax0=itrk[tau][3]

            xtrk[tau][1]=jtrk[tau][0]
            xtrk[tau][2]=jtrk[tau][1]
            xtrk[tau][3]=jtrk[tau][2]

            flat1=xtrk[tau][1]
            flon1=xtrk[tau][2]
            fvmax1=xtrk[tau][3]
            
        if(tau >= etau and tau <= etaux and verb):
            print 'eeee %03d  LAT0: %5.2f  10: %5.2f LON0: %5.2f  10: %5.2f VMAX: %5.2f  10: %5.2f'%(tau,flat0,flat1,flon0,flon1,fvmax0,fvmax1)


    return(jtrk,xtrk,deftaus)



def SelectBestBtCqTau0(bdir0,bspd0,bvmax0,
                       cqdir0,cqspd0,cqvmax0,
                       blat0,blon0,
                       cqlat0,cqlon0,verb):
    
    #
    # bt/cq dir,spd init posit
    #
    
    if(cqspd0 > 0.0):
        btspd=cqspd0
        btdir=cqdir0
    else:
        btspd=bspd0
        btdir=bdir0
    
    if(cqvmax0 > 0.0):
        bvmax=cqvmax0
    else:
        bvmax=bvmax0
        
    if(cqlat0 > -88.0 and cqlat0 < 88.0):
        btlat=cqlat0
        btlon=cqlon0
    else:
        btlat=blat0
        btlon=blon0
        
    if(verb):
        print 'CCCCCCCCCCCiiiQQQ ',cqdir0,cqspd0,cqlat0,cqlon0
        print 'CCCCCCCCCCCiiibbb ',bdir0,bspd0,blat0,blon0
        print 'CCCCCCCCCCCoooooo ',btdir,btspd,btlat,btlon
        
    return(btlat,btlon,btdir,btspd,bvmax)


def selectvmaxcorrparms(vmaxcorrtype):

    if(vmaxcorrtype == 'none'):
        vmaxtaucut=0.0
        vmaxtaumin=-999.0
        vmaxcorrmin=0.0
        
    elif(vmaxcorrtype == 'light'):
        vmaxtaucut=12.0
        vmaxtaumin=120.0
        vmaxcorrmin=0.25
        
    elif(vmaxcorrtype == 'moderate'):
        vmaxtaucut=48.0
        vmaxtaumin=120.0
        vmaxcorrmin=0.5
        
    elif(vmaxcorrtype == 'heavy'):
        vmaxtaucut=48.0
        vmaxtaumin=72.0
        vmaxcorrmin=0.75
        
    elif(vmaxcorrtype == 'full'):
        vmaxtaumin=0.0
        vmaxtaucut=0.0
        vmaxcorrmin=1.0
    else:
        print 'EEEEEEEEEEEEEEE invalid vmaxcorrtype: ',vmaxcorrtype
        sys.exit()

    return(vmaxtaumin,vmaxtaucut,vmaxcorrmin)


def setfvmaxoffact(tau,atend,
                   vmaxtaumin,vmaxtaucut,vmaxcorrmin):

    ftau=float(tau)
    if(vmaxtaumin  > 0.0):

        if((ftau >= vmaxtaucut and ftau <= vmaxtaumin) ):
            fvmaxofffact=((vmaxtaumin-ftau)/(vmaxtaumin-vmaxtaucut))*(1.0-vmaxcorrmin) + vmaxcorrmin
        
        elif(ftau > vmaxtaumin or atend):
            fvmaxofffact=vmaxcorrmin

        elif((ftau < 0) or (ftau >= 0 and ftau < vmaxtaucut) ):
            fvmaxofffact=1.0

        else:
            print 'EEEEEEEEEEEEEEEE setfvmaxoffact error'
            sys.exit()


    else:
        
        fvmaxofffact=1.0

    if(fvmaxofffact < 0.0): fvmaxofffact=0.0

    if(vmaxtaumin == 0.0):  fvmaxofffact=1.0

    return(fvmaxofffact)

#bbbbbbbbbbbbbbbbbbbcccccccccccccccccccccccccccccc
#
# bias correct and 3-h interp track from above 
#
#bbbbbbbbbbbbbbbbbbbcccccccccccccccccccccccccccccc

def BiasCorrFcTrackInterpFill(jtrk,itrk,deftaus,phr,dtx,
                              btlat,btlon,btdir,btspd,bvmax,
                              model,dtg,stm3id,
                              dopc=1,vmaxmin=20.0,verb=0):


    #------------------------------------------------------------------------------------

    def PersistCorr(tau,lat0,lon0,course,speed,
                    latfc,lonfc,
                    pctauend=12,pcmin=0.33):
    
        (latp,lonp)=TC.rumltlg(course,speed,tau,lat0,lon0)

        if(tau <= pctauend):
            pcorr=pcmin+(1.0-(float(tau)/pctauend))*(1.0-pcmin)
            latpc=(1.0-pcorr)*latfc + pcorr*latp
            lonpc=(1.0-pcorr)*lonfc + pcorr*lonp
            #print 'qqqqqqqqq------------------ ',tau,pcmin,pcorr,' lat: ',latfc,latp,latpc,' lon: ',lonfc,lonp,lonpc

        
            
        return(latpc,lonpc)


    #
    # hard-wired from nhc_interp.f for dt=3
    #

    def fiextrap(t,a,b,c):
        x=(2.0*a + t*(4.0*b - c - 3.0*a + t*(c - 2.0*b + a)))/2.0
        return(x)

    #------------------------------------------------------------------------------------


    itaus=itrk.keys()
    itaus.sort()

    otrk=copy.deepcopy(itrk)

    vmaxcorrtype=atcf.VmaxCorrType[model]

    (vmaxtaumin,vmaxtaucut,vmaxcorrmin)=selectvmaxcorrparms(vmaxcorrtype)
    
    taus=jtrk.keys()
    taus.sort()

    #
    #
    #
    try:
        latoff=btlat-jtrk[phr][0]
        lonoff=btlon-jtrk[phr][1]
        fvmaxoff=bvmax-jtrk[phr][2]

    except:
        print 'WWWWW no jtrk for: ',stm3id,'  dtg: ',dtg,'  phr: ',phr
        return(otrk)

    

    #print 'OO11111 latoff,lonoff %02f %5.1f %5.1f %6.1f %6.1f :: %6.1f %6.1f '%(phr,btlat,jtrk[phr][0],btlon,jtrk[phr][1],latoff,lonoff)
    
    if(verb):
        itaus=itrk.keys()
        itaus.sort()
        for tau in itaus:
            # ['2008061806', 9.5, 132.1, 21.0, 0.0, 42.3, 0.100001, 42.3, -16.3001, -38.9, -29.6, 30.0, [-999, -999, -999, -999], [-999, -999, -999, -999]]
            print 'III tau: %03d'%(tau)," %5.1f %6.1f %3.0f"%(itrk[tau][1],itrk[tau][2],itrk[tau][3]),itrk[tau][12],itrk[tau][13]
        for tau in taus:
            print 'JJJ tau: %03d'%(tau)," %5.1f %6.1f %3.0f"%(jtrk[tau][0],jtrk[tau][1],jtrk[tau][2]),jtrk[tau][3],jtrk[tau][4]


    
    jtrknopc={}
    
    for tau in taus:

        atend=0
        if(tau == taus[-1]): atend=1

        vmoff=0.0
        dtau=tau-phr
        
        vmoff=setfvmaxoffact(dtau,atend,
                             vmaxtaumin,vmaxtaucut,vmaxcorrmin)


        latbc=jtrk[tau][0]+latoff
        lonbc=jtrk[tau][1]+lonoff
        vmaxbc=jtrk[tau][2]+fvmaxoff*vmoff

        #
        # undef
        #
        if(jtrk[tau][2] == 0.0):
            vmaxbc=0.0

        jtrknopc[tau]=[latbc,lonbc,vmaxbc]
        
        latcur=loncur=-999.
        if(dtau >= 3 and dtau <= 12 and dopc):
            (latpc,lonpc)=PersistCorr(dtau,btlat,btlon,btdir,btspd,
                                      latbc,lonbc
                                      )
            latbc=latpc
            lonbc=lonpc
            
        jtrk[tau][0]=latbc
        jtrk[tau][1]=lonbc
        jtrk[tau][2]=vmaxbc




    #
    # do the extrap
    #

    xtaus=range(taus[-1],taus[-1]+phr,dtx)

    try:
        etaum1=taus[-2]
    except:
        etaum1=taus[0]


    for xtau in xtaus:
        tm2=xtau-3*dtx
        tm1=xtau-2*dtx
        tm0=xtau-dtx
        jtrknopc[xtau]=[0,0,0]
        jtrk[xtau]=[0,0,0,[],[]]
        for j in range(0,3):
            a=jtrk[tm2][j]
            b=jtrk[tm1][j]
            c=jtrk[tm0][j]
            jtrk[xtau][j]=fiextrap(3,a,b,c)

##             try:
##                 if(j == 0):  print 'try',xtau
##             except:
##                 if(j == 0): print 'except',xtau
##                 jtrk[xtau]=jtrk[taus[-1]]
##                 jtrk[xtau][j]=fiextrap(3,a,b,c)
                
            jtrknopc[xtau][j]=jtrk[xtau][j]

        #
        # set radii constant from etau -> last xtau
        #
        for j in range(3,5):
            jtrk[xtau][j]=jtrk[etaum1][j]
            

    taus=jtrk.keys()
    taus.sort()

    if(verb):
        for tau in taus:
            print 'FFF tau: %03d'%(tau)," %5.1f PC: %5.1f | %6.1f PC: %6.1f |  %3.0f"%(jtrk[tau][0],jtrknopc[tau][0],\
                                                                                       jtrk[tau][1],jtrknopc[tau][1],jtrk[tau][2]),\
                                                                                       jtrk[tau][3],jtrk[tau][4]

    #
    # put out final track; shift radii to phr from tau=0, i.e., do not interpolate but assume forecast unchange
    #

    for tau in deftaus:

        otrk[tau][1]=jtrk[tau+phr][0]
        otrk[tau][2]=jtrk[tau+phr][1]
        #
        # max sure intensity does not fall below vmaxmin
        #
        ovmax=jtrk[tau+phr][2]
        if(ovmax < vmaxmin):
            ovmax=vmaxmin
        otrk[tau][3]=ovmax
        
        #
        # do not use interpolated radii; assume the forecast is the constant  
        #
        otrk[tau][12]=jtrk[tau][3]
        otrk[tau][13]=jtrk[tau][4]

        if(verb):
            print 'OOO tau: %03d'%(tau)," %5.1f | %6.1f |  %3.0f"%(otrk[tau][1],otrk[tau][2],otrk[tau][3]),\
                  otrk[tau][12],otrk[tau][13]
                            

    return(otrk)

    


        

        
def ParseAdeckCards(dtg,cards,dtautracker,verb=0,taumax=144):

    def ParseTcs(tcs,stm):
        
        olat=-99.9
        olon=-999.9
        odir=-999.9
        ospd=-99.9
        otype=None
        ovmax=-99


        for tc in tcs:
            tt=tc.split()
            
            #for i in range(0,len(tt)):
            #    print 'mmmm ',i,tt[i]
                
            stmid=tt[1]
            stmid3=stmid.split('.')[0]

            if(stm == stmid3):

                bvmax=float(tt[2])
                blat=float(tt[4])
                blon=float(tt[5])
                bdir=float(tt[8])
                bspd=float(tt[9])

                clat=float(tt[21])
                clon=float(tt[22])
                cvmax=float(tt[23])
                cdir=float(tt[24])
                cspd=float(tt[25])

                if(clat > -89.0):
                    olat=clat
                    olon=clon
                    odir=cdir
                    ospd=cspd
                    ovmax=cvmax
                    otype='carq'
                else:
                    olat=blat
                    olon=blon
                    odir=bdir
                    ospd=bspd
                    ovmax=bvmax
                    otype='bt'



        return(olat,olon,odir,ospd,ovmax,otype)


    stms=[]
    ftcs={}
    ftcsf={}
    ftcs2={}
    ftcstruct={}

    ostm=None
    settau0=0

    for card in cards:

        tt=card.split(',')
        bid2=tt[0][0:2]
        bid1=TC.Basin2toBasin1[bid2]
        try:
            stmnum=int(tt[1])
        except:
            stmnum=99
            
        stm="%02d%s"%(stmnum,bid1)

        if(ostm != None and stm != ostm):
            settau0=0
            ostm=stm
        
        #for n in range(0,len(tt)):
        #    print "tttt %-2d %s"%(n,tt[n].strip())


        stms.append(stm)

        tau=int(tt[5])

        clat=tt[6]
        clon=tt[7]
        
        try:
            vmax=int(tt[8])
        except:
            vmax=-88.8
            
        try:
            pmin=int(tt[9])
        except:
            pmin=-888.8

        #
        # 20070620 -- code to handle wind radii
        #
        
        wrad34ne=wrad34se=wrad34sw=wrad34nw=-999
        
        iw=11
        try:
            wrad34=int(tt[iw])
        except:
            wrad34=-999
            wrad34ne=wrad34se=wrad34sw=wrad34nw=-999

        iw=iw+2
        if(wrad34 == 34):
            try:
                wrad34ne=int(tt[iw]) ; iw=iw+1
                wrad34se=int(tt[iw]) ; iw=iw+1
                wrad34sw=int(tt[iw]) ; iw=iw+1
                wrad34nw=int(tt[iw]) ; iw=iw+1
            except:
                wrad34ne=wrad34se=wrad34sw=wrad34nw=-999
            

        #
        # ofcl adeck is special because extra info that breaks the append 50/64 radii to end of card for one card / tau
        # work backwards
        # 
        ntt=len(tt)


        if(ntt == 28 or ntt == 34 or ntt == 40):
            iw=27
        elif(ntt == 35):
            iw=30
        else:
            iw=17


        wrad50ne=wrad50se=wrad50sw=wrad50nw=-999

        iw=ntt-7
        
        try:
            wrad50=int(tt[iw])
        except:
            wrad50=-999


        #
        # if 64 kt, back up and try again
        #
        if(wrad50 == 64):
            iw=iw-6
            
        try:
            wrad50=int(tt[iw])
        except:
            wrad50=-999
        
        iw=iw+2
        if(wrad50 == 50):
            try:
                wrad50ne=int(tt[iw]) ; iw=iw+1
                wrad50se=int(tt[iw]) ; iw=iw+1
                wrad50sw=int(tt[iw]) ; iw=iw+1
                wrad50nw=int(tt[iw]) ; iw=iw+1
            except:
                wrad50ne=wrad50se=wrad50sw=wrad50nw=-999

        #
        # set to undef if ALL rad are 0
        #
        if(wrad34ne == 0 and wrad34se == 0 and wrad34sw == 0 and wrad34nw == 0):
            wrad34ne=wrad34se=wrad34sw=wrad34nw=-999
            

        if(wrad50ne == 0 and wrad50se == 0 and wrad50sw == 0 and wrad50nw == 0):
            wrad50ne=wrad50se=wrad50sw=wrad34nw=-999
            

        #print '33333333333333 ',tau,wrad34ne,wrad34se,wrad34sw,wrad34nw
        #print '55555555555555 ',tau,wrad50ne,wrad50se,wrad50sw,wrad50nw

        #
        # 20070620 -- hwrf is the first model tracker i've hit that outputs wind radii
        # until we add wind radii to the ft=() detect dup and fill only one ft / tau
        #
        
        if(verb):
            print 'CC: ',card[:-1]

        (rlat,rlon,ilat,ilon,hemns,hemew)=TC.Clatlon2Rlatlon(clat,clon)
        #print 'bbb ',bid2,bid1,stmnum,stm,tau,clat,clon,rlat,rlon


        sdtgm12=mf.dtginc(dtg,tau-12)
        sdtgp12=mf.dtginc(dtg,tau+12)
        sdtg=mf.dtginc(dtg,tau)
        
        lat=rlat
        lon=rlon
        ccirc='CC'

        if(pmin > 0.0 and vmax <= 0.0):
            vmax=TC.HolidayAtkinsonPsl2Vmax(pmin)


        ftcstruct[stm,tau,'r34quad','vals']=[wrad34ne,wrad34se,wrad34sw,wrad34nw]
        ftcstruct[stm,tau,'r50quad','vals']=[wrad50ne,wrad50se,wrad50sw,wrad50nw]
        ftcstruct[stm,tau,'spdmax','val']=vmax

        ft=(tau,sdtg,sdtgm12,sdtgp12,lat,lon,ccirc)

        if(tau == 0 and settau0 == 0):
            
            wlat=rlat
            wlon=rlon
            ftcs[stm]=[(wlat,wlon)]
            
            # put warning position in tau -1
            ftcs2[stm,-1]=[(wlat,wlon)]

            settau0=1
            ostm=stm
        
        elif( (tau == 6 or tau == 12 or tau == 24) and settau0 == 0):
            
            
            tcs=TC.findtcs(dtg)
            (olat,olon,odir,ospd,ovmax,otype)=ParseTcs(tcs,stm)

            print 'WWWWW no initial posit: ',stm,dtg,tau,' adding: ',olat,olon,ovmax
            tau0=0
            sdtgm12=mf.dtginc(dtg,tau0-12);
            sdtgp12=mf.dtginc(dtg,tau0+12);
            sdtg=mf.dtginc(dtg,tau0);
            
            ft00=(tau0,sdtg,sdtgm12,sdtgp12,olat,olon,ccirc)
            ftcs[stm]=[(olat,olon)]
            ftcs[stm].append(ft00)

            ftcs2[stm,-1]=[(olat,olon)]
            ftcs2[stm,tau0]=ft00
            

            #
            # set the initial wind for intensity verification
            #
            ftcstruct[stm,tau0,'spdmax','val']=ovmax

            settau0=1

        if(tau > 0 and settau0 == 0):
            print 'WWWWWW--- fcst with no tau 0, 6, or 12 define as error and return None tau: ',tau
            return(None,None,None)


 
        try:
            ftcs[stm].append(ft)
            ftcs2[stm,tau]=ft
        except:
            print 'EEE---- bad ft in ftcs',stm,tau,' ft: ',stm,tau,ft
            sys.exit()


    stms=mf.uniq(stms)

    
    for stm in stms:
        
        np=len(ftcs[stm])

        #dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
        #
        # dup tau 0 check
        #
        #0000000000000000000000000000000000000000000000000000000000000000000000
        
        if(np == 3):

            nftc=[]
            tauold=ftcs[stm][1][0]
            nftc.append(ftcs[stm][0])
            nftc.append(ftcs[stm][1])
            isdup=0
            for n in range(2,np):
                tau=ftcs[stm][n][0]
                if(tau == tauold):
                    print 'asdfasdfasdf dup',dtg
                    isdup=1
                    tauold=tau
                else:
                    nftc.append(ftcs[stm][n])

            if(isdup):
                ftcs[stm]=nftc
                np=len(ftcs[stm])
                print 'WWWWW tau0 dup in adeck, resetting... ',dtg

                
        if(np == 1):
            ft=(0,dtg,dtg,dtg,99.9,999.9,'CC')
            ftcs[stm].append(ft)
            ftcs2[stm,0]=ft



    #
    # add noloads at end of forecast
    #
    
    for stm in stms:

        np=len(ftcs[stm])-1

        (ftau,fsdtg,sdtgm12,sdtgp12,lat,lon,ccirc)=ftcs[stm][np]

        if(ftau < taumax):

            extrataus=range(ftau+dtautracker,taumax+1,dtautracker)
            sdtg=fsdtg

            for etau in extrataus:
                sdtg=mf.dtginc(sdtg,dtautracker)
                sdtgm12=mf.dtginc(sdtg,-dTau12)
                sdtgp12=mf.dtginc(sdtg,+dTau12)
                alat=99.9
                alon=999.9
                accirc='CC'
                ftadd=(etau,sdtg,sdtgm12,sdtgp12,alat,alon,accirc)
                ftcs[stm].append(ftadd)
                ftcs2[stm,etau]=ftadd
                
                wrad34ne=wrad34se=wrad34sw=wrad34nw=-999
                wrad50ne=wrad50se=wrad50sw=wrad34nw=-999
                vmax=-88.8

                ftcstruct[stm,etau,'r34quad','vals']=[wrad34ne,wrad34se,wrad34sw,wrad34nw]
                ftcstruct[stm,etau,'r50quad','vals']=[wrad50ne,wrad50se,wrad50sw,wrad50nw]
                ftcstruct[stm,etau,'spdmax','val']=vmax

            
                
    #
    # final check make sure there is data in the hash if model changes the frequency of output
    # e.g., in egrr could have 0,12,24,36 and then 0,24,48 so missing 12 and 36 and this fouls
    # up the vdeck process:
    #
    
    taus=range(0,taumax+1,dtautracker)
    sdtg=dtg
    
    for stm in stms:

        
        sdtg=dtg

        [(olat,olon)]=ftcs2[stm,-1]
        ftcsf[stm]=[(olat,olon)]

        n=0
        m=0
        for tau in taus:

            try:
                ft=ftcs2[stm,tau]
                ftcsf[stm].append(ft)
                n=n+1
                m=m+1

            except:
                
                sdtg=mf.dtginc(dtg,tau)
                sdtgm12=mf.dtginc(sdtg,-dTau12)
                sdtgp12=mf.dtginc(sdtg,+dTau12)
                
                alat=99.9
                alon=999.9
                accirc='CC'
                ftadd=(tau,sdtg,sdtgm12,sdtgp12,alat,alon,accirc)
                ftcsf[stm].append(ftadd)
                ftcs2[stm,tau]=ftadd

                wrad34ne=wrad34se=wrad34sw=wrad34nw=-999
                wrad50ne=wrad50se=wrad50sw=wrad34nw=-999
                vmax=-88.8

                ftcstruct[stm,tau,'r34quad','vals']=[wrad34ne,wrad34se,wrad34sw,wrad34nw]
                ftcstruct[stm,tau,'r50quad','vals']=[wrad50ne,wrad50se,wrad50sw,wrad50nw]
                ftcstruct[stm,tau,'spdmax','val']=vmax

                
                m=m+1

            if(verb):
                print '00000000000 ',sdtg,n,m,tau
                print '11111111111 ',ftcs[stm][n]
                print 'fffffffffff ',ftcsf[stm][m]
                print '22222222222 ',ftcs2[stm,tau]
                print 'VVVVVVVVVVV ',ftcstruct[stm,tau,'spdmax','val']



    return(ftcsf,ftcs2,ftcstruct)




def GetftcstrucParms(ftcstruct,fcid,tau):
    
    try:
        fmaxspd=ftcstruct[fcid,tau,'spdmax','val']
    except:
        fmaxspd=-88.8

    try:
        ftr34quad=ftcstruct[fcid,tau,'r34quad','vals']
    except:
        ftr34quad=[-888,-888,-888,-888]
        
    try:
        ftr50quad=ftcstruct[fcid,tau,'r50quad','vals']
    except:
        ftr50quad=[-888,-888,-888,-888]
        
    try:
        fminspd=ftcstruct[fcid,tau,'spdmin','val']
    except:
        fminspd=-88.8

    try:
        fmaxvrt=ftcstruct[fcid,tau,'vrtmax','val']
    except:
        fmaxvrt=-88.8

    try:
        fminvrt=ftcstruct[fcid,tau,'vrtmin','val']
    except:
        fminvrt=-88.8

    try:
        fmaxspddist=ftcstruct[fcid,tau,'spdmax','dist']
    except:
        fmaxspddist=-888.8

    try:
        fminspddist=ftcstruct[fcid,tau,'spdmin','dist']
    except:
        fminspddist=-888.8

    try:
        fmaxvrtdist=ftcstruct[fcid,tau,'vrtmax','dist']
    except:
        fmaxvrtdist=-888.8

    try:
        fminvrtdist=ftcstruct[fcid,tau,'vrtmin','dist']
    except:
        fminvrtdist=-888.8

    return(fmaxspddist,fminspd,fminspddist,fmaxvrt,fmaxvrtdist,fmaxspd,ftr34quad,ftr50quad)



def NoLoadFtCards(dtg,tcs,dtautracker,opt='noload',taumax=144):

    ftcs={}
    stms=[]
    btlat={}
    btlon={}

    for tc in tcs:
        stmid=tc.split()[1]
        stmid=stmid.split('.')[0]

        btlat[stmid]=float(tc.split()[4])
        btlon[stmid]=float(tc.split()[5])
        
        stms.append(stmid)
        
    for stm in stms:

        wtlat=btlat[stm]
        wtlon=btlon[stm]
        
        ftcs[stm]=[(wtlat,wtlon)]
        if(opt == 'noshow'):
            ft=(0,dtg,dtg,dtg,95.9,955.9,'CC')
        elif(opt == 'noload'):
            ft=(0,dtg,dtg,dtg,91.9,911.9,'CC')

        ftcs[stm].append(ft)

    
    for stm in stms:
        np=len(ftcs[stm])-1
        (ftau,fsdtg,sdtgm12,sdtgp12,lat,lon,ccirc)=ftcs[stm][np]

        if(ftau < taumax):
            npall=taumax/dtautracker+1
            sdtg=fsdtg
            tau=ftau+dtautracker
            for i in range(np+1,npall+1):
                sdtg=mf.dtginc(sdtg,dtautracker)
                sdtgm12=mf.dtginc(sdtg,-dTau12)
                sdtgp12=mf.dtginc(sdtg,+dTau12)
                if(opt == 'noshow'):
                    alat=95.9
                    alon=955.9
                elif(opt == 'noload'):
                    alat=91.9
                    alon=911.9

                accirc='CC'
                ftadd=(tau,sdtg,sdtgm12,sdtgp12,alat,alon,accirc)
                ftcs[stm].append(ftadd)
                tau=tau+dtautracker

    return(ftcs)



def add2000(y):
    if(len(y) == 1):
        yyyy=str(2000+int(y))
    elif(len(y) == 2):
        if(int(y) > 25):
            yyyy=str(1900+int(y))
        else:
            yyyy=str(2000+int(y))
            
    else:
        yyyy=y
    return(yyyy)



def MakeStmList(stmopt,dofilt9x=0,verb=0):


    def getyears(yyy):

        if(yyy == 'cur'):
            curdtg=mf.dtg()
            yyy=curdtg[0:4]
            
        years=[]
        n1=0
        n2=0
        
        tt0=yyy.split('-')
        tt1=yyy.split(',')

        if(len(tt1) > 1):
            for tt in tt1:
                yyyy=add2000(tt)
                years.append(yyyy)
            return(years)
        
        if(len(tt0) > 1):
            y1=tt0[0]
            y2=tt0[1]
            yyyy1=add2000(y1)
            yyyy2=add2000(y2)
            
            if(len(yyyy1) != 4 or len(yyyy2) != 4):
                print 'EEEE getyears tt:',tt
                return(None)

            else:
                n1=int(yyyy1)
                n2=int(yyyy2)
                for n in range(n1,n2+1):
                    years.append(str(n))

        else:
            if(len(yyy) <= 2): yyy=add2000(yyy)
            years=[yyy]

        return(years)
        

    def getstmids(sss,year):
        
        sids=[]
        n1=0
        n2=0
        tt=sss.split('-')

        if(len(tt) > 1):
            if(len(tt[0]) != 2 or len(tt[1]) != 3):
                print 'EEEE getstmids tt:',tt
                return(None)

            else:
                n1=int(tt[0])
                n2=int(tt[1][0:2])
                bid=tt[1][2].upper()

                for n in range(n1,n2+1):
                    sid="%02d%1s.%s"%(n,bid,year)
                    sids.append(sid)
                    
        elif(len(sss) == 1):
            tcnames=TC.GetTCnamesHash(year)
            bchk=sss.upper()
            for tcname in tcnames:
                if(tcname[1][2:3] == bchk):
                    sid="%s.%s"%(tcname[1],tcname[0])
                    sids.append(sid)
                else:
                    sid=None

            if(sid != None):
                sids.append(sid)
            
            
        elif(len(tt) == 1):

            if(len(sss) == 3):

                if(sss[0].upper() == 'M'):
                    nback=int(sss[1])
                    bchk=sss[2].upper()
                    tcnames=TC.GetTCnamesHash(year)
                    for tcname in tcnames:
                        if(tcname[1][2:3] == bchk):
                            sid="%s.%s"%(tcname[1],tcname[0])
                            sids.append(sid)
                        else:
                            sid=None

                    sids.sort()
                    osids=[]
                    
                    nsids=len(sids)
                    for n in range(nsids-nback,nsids):
                        osids.append(sids[n])

                    return(osids)


                else:
                    
                    sid="%s.%s"%(sss.upper(),year)
                    sids.append(sid)
                


        else:
            print 'EEEE getstmids sss:',sss
            return(None)
            

        sids.sort()
        return(sids)

    #
    # start.......................
    #
    
    ttt=stmopt.split('-')
    ttc=stmopt.split(',')
    tt=stmopt.split('.')
    
    curdtg=mf.dtg()
    curyear=curdtg[0:4]

    #
    # single storm
    #
    
    if(len(tt) == 1 and len(ttt) == 1 and len(ttc) == 1):
        if(len(tt[0]) == 3):
            stmid=tt[0][2]
        elif(len(tt[0]) != 1):
            print 'EEEE bad stm3id: ',tt[0],tt
            sys.exit()
        else:
            stmid=tt[0]
            
        if(TC.IsShemBasinStm(stmid)):
            stmyear=TC.GetShemYear(curdtg)
        else:
            stmyear=curyear
        stmyear=add2000(stmyear)
        
        stmopt=stmopt+'.'+stmyear
        tt=stmopt.split('.')

    #
    # stm spanning using current year
    #
    elif(len(ttt) > 1 and len(ttc) == 1 and len(tt) == 1):

        stmids=getstmids(stmopt,curyear)
        return(stmids)
        
        


    #
    # list of individual stmid (sss.y)
    #

    if(len(ttc) > 1):

        stmids=[]
        for stmopt in ttc:
            stmids=stmids+MakeStmList(stmopt,dofilt9x,verb)

        return(stmids)
            
            
    if(len(ttc) > 1 and len(tt) > 2):
        
        stmids=[]

        for stmid in ttc:
            ss1=stmid.split('.')
            if(len(ss1) != 2):
                print 'EEE invalid individual stm: ',stmmid
                sys.exit()

            sid=ss1[0]
            yid=ss1[1]
            if(len(yid) >= 1): yid=add2000(yid)
            rc=getstmids(sid,yid)
            stmids=stmids+rc
            
        return(stmids)
        

    
    
    sopt=tt[0]
    yopt=tt[1]

    years=getyears(yopt)

    if(verb):
        print 'ssssssssssss sopt: ',sopt
        print 'yyyyyyyyyyyy yopt: ',yopt,years
    

    stmids=[]

    for year in years:

        ss=sopt.split(',')
        if(len(ss) > 1):
            for sss in ss:
                rc=getstmids(sss,year)
                if(rc != None):
                    stmids=stmids+rc

        else:
            rc=getstmids(sopt,year)
            if(rc != None):
                stmids=stmids+rc

    #
    # filter out 9X
    #
    
    if(dofilt9x):
        nstmids=[]
        for stmid in stmids:
            num=int(stmid[0:2])
            if(num < 80):
                nstmids.append(stmid)

        stmids=nstmids
                


        

    if(verb):
        for stmid in stmids:
            print 'ssxsssssssss ',stmid

    return(stmids)


def TrackBtBiasCorr(itrk,taus,model,
                    bdir0,bspd0,bvmax0,
                    cqdir0,cqspd0,cqvmax0,
                    blat0,blon0,
                    cqlat0,cqlon0,
                    phr,verb=0):


    def radiiterp(rval,radquad0,radquad1,vmax0,vmax1,dtau,phrint):

        #
        # the physically minimum r34 for vmax=35 would be???  my guess: 20 nm
        # for r50 and vmax=50? would be ? rmax?               my guess: 15 nm
        #
        r34min=20.0
        r50min=15.0
    
        oradquad=copy.deepcopy(radquad0)

        dtaum1=1.0/float(dtau)

        dvmax=(vmax1-vmax0)*dtaum1
        vmaxi=vmax0+dvmax*phrint
        
        nr=len(radquad1)
        for n in range(0,nr):

            r1=float(radquad1[n])
            r0=float(radquad0[n])
            
            if(r1 < 0.0 and vmaxi >= rval and rval == 34.0): r1=r34min
            if(r1 < 0.0 and vmaxi >= rval and rval == 50.0): r1=r50min
            
            if(r0 < 0.0 and vmaxi >= rval and rval == 34.0): r0=r34min
            if(r0 < 0.0 and vmaxi >= rval and rval == 50.0): r0=r50min
            
            drad=(r1-r0)*dtaum1

            if(vmaxi >= rval):
                radi=r0+drad*phrint
            else:
                radi=-999.0

            #
            # final qc r < rmin
            #
            if(rval == 34.0 and radi > 0.0 and radi <= r34min): radi=r34min
            if(rval == 50.0 and radi > 0.0 and radi <= r50min): radi=r50min
            
            oradquad[n]=mf.nint(radi)


        return(oradquad)



    def rumterp(itrk,otrk,etrk,model,
                btlat,btlon,bvmax,
                flatoff,flonoff,fvmaxoff,
                tau0,tau1,phr,atend,verb=0):

        dtau=tau1-tau0
        if(tau1 == tau0): dtau=12
        
        
        if(atend):
            phrint=phr+dtau
        else:
            phrint=phr

        flat0=itrk[tau0][1]
        flon0=itrk[tau0][2]
        fvmax0=itrk[tau0][3]
        r34quad0=itrk[tau0][12]
        r50quad0=itrk[tau0][13]

        flat1=itrk[tau1][1]
        flon1=itrk[tau1][2]
        fvmax1=itrk[tau1][3]
        r34quad1=itrk[tau1][12]
        r50quad1=itrk[tau1][13]

        flat0x=etrk[tau0][1]
        flon0x=etrk[tau0][2]


        r34val=34.0
        r50val=50.0
        or34quad=radiiterp(r34val,r34quad0,r34quad1,fvmax0,fvmax1,dtau,phrint)
        or50quad=radiiterp(r50val,r50quad0,r50quad1,fvmax0,fvmax1,dtau,phrint)


        dvmax=(fvmax1-fvmax0)/dtau

        (edir,espd,eiu,eiv)=TC.rumhdsp(flat0,flon0,flat1,flon1,dtau)
        (flate,flone)=TC.rumltlg(edir,espd,phrint,flat0,flon0)
        
        fvmaxe=fvmax0+dvmax*phrint

        if(tau0 == 0 and flatoff == None):
            flatoff=flate-btlat
            flonoff=flone-btlon
            fvmaxoff=bvmax-fvmaxe
            (flatx,flonx)=TC.rumltlg(edir,espd,dtau,btlat,btlon)
        else:
            #
            # 20071023 -- bug set the offset to 0 for e
            #
            #flatoff=0.0
            #flonoff=0.0
            #fvmaxoff=0.0
            (flatx,flonx)=TC.rumltlg(edir,espd,dtau,flat0x,flon0x)


        flate=flate-flatoff
        flone=flone-flonoff

        vmaxcorrtype=atcf.VmaxCorrType[model]


        if(vmaxcorrtype == 'none'):
            taucut=0
            taumin=-999.0
            vmaxcorrmin=0.0

        elif(vmaxcorrtype == 'light'):
            taucut=12.0
            taumin=120.0
            vmaxcorrmin=0.25
        
        elif(vmaxcorrtype == 'moderate'):
            taucut=48
            taumin=120.0
            vmaxcorrmin=0.5

        elif(vmaxcorrtype == 'heavy'):
            taucut=48
            taumin=72.0
            vmaxcorrmin=0.75

        elif(vmaxcorrtype == 'full'):
            taumin=0
            taucut=0.0
            vmaxcorrmin=1.0

        if(tau0 >= taucut and taumin > 0.0):
            fvmaxofffact=(taumin-tau0)/taumin
        elif(atend and tau1 >= taucut and taumin > 0.0):
            fvmaxofffact=(taumin-tau1)/taumin
        else:
            fvmaxofffact=1.0

        if(fvmaxofffact < 0.0): fvmaxofffact=0.0
        
        if(taumin == 0.0):
            fvmaxofffact=1.0
        elif(taumin < 0.0):
            fvmaxofffact=vmaxcorrmin

        if(fvmaxofffact < vmaxcorrmin): fvmaxofffact=vmaxcorrmin
             
        
        if(verb):
            pcard="%4d %4d %2d  0: %6.1f %6.1f %3d  "%(tau0,tau1,phrint,flat0,flon0,fvmax0)
            pcard="%s 1: %6.1f %6.1f %3d"%(pcard,flat1,flon1,fvmax1)
            pcard="%s i: %6.1f %6.1f %3d"%(pcard,flate,flone,fvmaxe)
            print 'rumterp: ',pcard

        if(tau0 == 0):
            etrk[tau0][1]=btlat
            etrk[tau0][2]=btlon

        etrk[tau1][1]=flatx
        etrk[tau1][2]=flonx


        #
        # otrk -- rum interp
        # etrk -- rum extrap 
        #

        if(atend):
            otrk[tau1][1]=flate
            otrk[tau1][2]=flone
            otrk[tau1][3]=fvmaxe+fvmaxoff*fvmaxofffact
            etrk[tau1][3]=fvmaxe+fvmaxoff*fvmaxofffact

            otrk[tau1][12]=or34quad
            otrk[tau1][13]=or50quad
            etrk[tau1][12]=or34quad
            etrk[tau1][13]=or50quad
            
            
        else:
            otrk[tau0][1]=flate
            otrk[tau0][2]=flone
            otrk[tau0][3]=fvmaxe+fvmaxoff*fvmaxofffact
            etrk[tau0][3]=fvmaxe+fvmaxoff*fvmaxofffact

            otrk[tau0][12]=or34quad
            otrk[tau0][13]=or50quad
            etrk[tau0][12]=or34quad
            etrk[tau0][13]=or50quad
            
        #print "pppppppp----- %3i %4.0f %3.0f : %6.1f %6.1f %3i  X: %6.1f  %6.1f %3i"%(tau0,edir,espd,
        #                                                                              otrk[tau0][1],otrk[tau0][2],otrk[tau0][3],
        #                                                                              etrk[tau0][1],etrk[tau0][2],etrk[tau0][3])

        return(flatoff,flonoff,fvmaxoff)



    #
    #------------------------------------
    #
    
    otrk=copy.deepcopy(itrk)
    etrk=copy.deepcopy(itrk)
                   
    #
    # find fc taus
    #
    
    ftaus=[]

    for tau in taus:
        flat=itrk[tau][1]
        if(flat > -90.0 and flat < 88.0):
            ftaus.append(tau)

    #
    # check for noshow/noload
    #
    ntaus=len(ftaus)

    ###if(ntaus == 0 or ntaus == 1): return(otrk)
    #
    # 20071129 -- handle initial position only trackers
    #
    if(ntaus == 0): return(otrk)

    #
    # save target taus and replace input taus with forecast taus
    #
    
    itaus=taus
    taus=ftaus
    
    ntau=len(taus)
    etau=taus[ntau-1]

    #
    # check if 36-h fc; if not the set to 24 and then 12 ... because # taus handled below
    #

    if(etau >= 36):
        taubc=36
        taubc=12
    elif(etau == 24):
        taubc=24
        taubc=12
    elif(etau == 12):
        taubc=12

    if(verb): print 'EEEEEEEEEEE etau: ',etau

    #
    # bt/cq dir,spd init posit
    #

    if(cqspd0 > 0.0):
        btspd=cqspd0
        btdir=cqdir0
    else:
        btspd=bspd0
        btdir=bdir0

    if(cqvmax0 > 0.0):
        bvmax=cqvmax0
    else:
        bvmax=bvmax0

    if(cqlat0 > -88.0 and cqlat0 < 88.0):
        btlat=cqlat0
        btlon=cqlon0
    else:
        btlat=blat0
        btlon=blon0

    if(verb):
        print 'CCCCCCCCCCCiiiQQQ ',cqdir0,cqspd0,cqlat0,cqlon0
        print 'CCCCCCCCCCCiiibbb ',bdir0,bspd0,blat0,blon0
        print 'CCCCCCCCCCCoooooo ',btdir,btspd,btlat,btlon

        
    i=0
    flatoff=flonoff=fvmaxoff=None
    atend=0
    while(i< ntau):
        tau0=taus[i]
        if(i < ntau-1):
            tau1=taus[i+1]
        elif(i == ntau-1):
            tau0=taus[i-1]
            tau1=taus[i]
            atend=1

        flat0=itrk[tau0][1]
        flat1=itrk[tau1][1]

        (flatoff,flonoff,fvmaxoff)=rumterp(itrk,otrk,etrk,model,
                                           btlat,btlon,bvmax,
                                           flatoff,flonoff,fvmaxoff,
                                           tau0,tau1,phr,atend,verb)

        i=i+1
        if(i == ntau): break

    
    try:
        tau00=taus[0]
        flat00=otrk[0][1]
        flon00=otrk[0][2]
        flat36=otrk[taubc][1]
        flon36=otrk[taubc][2]
        (fdir36,fspd36,fiumot36,fivmot36)=TC.rumhdsp(flat00,flon00,flat36,flon36,taubc)
    except:
        fspd36=-99.9


    if(fspd36 > 0.0 and verb):
        print '36  ',flat00,flon00,flat36,flon36,taubc
        print '36  ',fdir36,fspd36
        
            
    bc12hr=0
    bc24hr=0

    
    i=0
    while(i< ntau):

        tau0=taus[i]
        if(ntau == 1):
            tau1=tau0
        else:
            tau1=taus[i+1]

        if(tau0 == etau and ntau == 1 ):
            tau0=taus[i]
            tau1=taus[i]
        elif(tau0 == etau):
            tau0=taus[i-1]
            tau1=taus[i]
            
        dtau=tau1-tau0
        if(tau1 == tau0): dtau=12

        flat0=otrk[tau0][1]
        flon0=otrk[tau0][2]
        fvmax0=otrk[tau0][3]

        flat1=otrk[tau1][1]
        flon1=otrk[tau1][2]
        fvmax1=otrk[tau1][3]


        (fdir,fspd,fiumot,fivmot)=TC.rumhdsp(flat0,flon0,flat1,flon1,dtau)

        
        if(verb):
            print
            print '--- ',i,tau0,tau1,dtau,fspd36
            print '000 ',flat0,flon0,fvmax0
            print '111 ',flat1,flon1,fvmax1
            print 'bc: ',btdir,btspd,' fc: ',fdir,fspd,fiumot,fivmot
            print 'cq: ',cqdir0,cqspd0,' fc: ',fdir,fspd,fiumot,fivmot

        if(fspd36 > 0.0 and tau1 == taubc):
            dtau36=tau1-tau00
            (flat36bc,flon36bc)=TC.rumltlg(fdir36,fspd36,dtau36,flat00,flon00)

            if(tau1 == 12):
                perwght12=0.67
                (flatbt,flonbt)=TC.rumltlg(btdir,btspd,dtau36,flat00,flon00)
                flat1bc=flat36bc*(1.0-perwght12) + flatbt*perwght12
                flon1bc=flon36bc*(1.0-perwght12) + flonbt*perwght12
                otrk[tau1][1]=flat1bc
                otrk[tau1][2]=flon1bc
                bc12hr=1

            if(tau1 == 24):
                perwght24=0.50
                (flatbt,flonbt)=TC.rumltlg(fdir,fspd,dtau,flat0,flon0)
                flat1bc=flat36bc*(1.0-perwght24) + flatbt*perwght24
                flon1bc=flon36bc*(1.0-perwght24) + flonbt*perwght24
                otrk[tau1][1]=flat1bc
                otrk[tau1][2]=flon1bc
                bc24hr=1

        else:
            flat36bc=-99.9
            flon36bc=-999.9
            flatbt=-99.9
            flonbt=-999.9
            dtau36=-99.9

        if(flat36bc > -90 and verb):
            print 'b36 -- ',flat36bc,flon36bc,dtau36
            print 'b36 bt ',flatbt,flonbt,dtau,flat00,flon00
            
        i=i+1

        #
        # use xtrap for tau > 72 h
        #
        # 20071023 -- just do interp generally works better
        #
        doxtrptaugt72=1
        doxtrptaugt72=0

        if(doxtrptaugt72):
            if(tau0 == 72):
                #print 'tttteq84 ',model,tau0,otrk[tau0][1],etrk[tau0][1]
                otrk[tau0][1]=0.5*(otrk[tau0][1]+etrk[tau0][1])
                otrk[tau0][2]=0.5*(otrk[tau0][2]+etrk[tau0][2])
                otrk[tau0][3]=0.5*(otrk[tau0][3]+etrk[tau0][3])
            elif(tau0 > 72):
                #print 'ttttgt84 ',model,tau0,otrk[tau0][1],etrk[tau0][1]
                otrk[tau0][1]=etrk[tau0][1]
                otrk[tau0][2]=etrk[tau0][2]
                otrk[tau0][3]=etrk[tau0][3]
            

        if(i == ntau-1): break

    if(verb):
        i=0
        while(i< ntau):
            tau0=taus[i]
            olat0=otrk[tau0][1]
            olon0=otrk[tau0][2]
            ilat0=itrk[tau0][1]
            ilon0=itrk[tau0][2]
            print "AAA----BCBC phr: %3d  %03i in: %5.1f %6.1f  out: %5.1f %6.1f"%(phr,tau0,ilat0,ilon0,olat0,olon0)
            i=i+1
            if(i == ntau): break


    return(otrk)


def VitalsAllStats(mod1s,taus,vstmids,vhash,verb=0):

    allstats=[]

    for mod1 in mod1s:

        mfe1s={}
        mfe2s={}
        mcte1s={}
        mcte2s={}
        mate1s={}
        mate2s={}
        gainxys={}
        gaine6xs={}
        nfe1s={}
        mfe2m1s={}
        pof1s={}
        pod1s={}

        mvear1s={}
        mvebr1s={}
        mvear2s={}
        mvebr2s={}
        
        nrun1s={}
        nrunmiss1s={}
        nbt1s={}
        nfc1s={}
        nfcmiss1s={}
        nfcover1s={}
        
        isVmaxOnlyModel1=mf.find(mod1,'icon')

        for tau in taus:

            mfe1=0.0
            mfe2=0.0
            mcte1=0.0
            mcte2=0.0
            mate1=0.0
            mate2=0.0
            nfe1=0
            nfe2=0
            if(tau == 0):
               nrun1=0
               nrunmiss1=0
               nrunover1=0
            nbt1=0
            nfc1=0
            nfcmiss1=0
            nfcover1=0

            mvear1=0.0
            mvebr1=0.0
            mvear2=0.0
            mvebr2=0.0
            
            nvear1=0
            nvebr1=0
            nvear2=0
            nvebr2=0
            
            for stmid in vstmids:

                if(verb): print 'SSSSSSSSS ',stmid

                try:
                    if(vhash[mod1,tau,stmid][0][0] == None):
                        continue
                except: 
                    continue
                
                for vh in vhash[mod1,tau,stmid]:
                    tt=vh[0].split()
                    if(tau == 0):
                        nfc=int(tt[2])
                        nrun=int(tt[1])
                        nrunmiss=int(tt[3])
                        nrunover=int(tt[4])
                        nbt=nrun
                    else:
                        nbt=int(tt[1])
                        nfc=int(tt[2])

                    nfcmiss=int(tt[6])
                    nfcover=int(tt[7])

                    if(verb):
                        print 'nnn',tau,'       nr,nrm,nro',nrun,nrunmiss,nrunover
                        print 'nnn',tau,'nbt,nfc,nfcm,nfco',nbt,nfc,nfcmiss,nfcover

                    tt=vh[1].split()

                    fe1=float(tt[2])
                    vear1=float(tt[22])
                    vebr1=float(tt[23])

                    #print 'vvvvvvvvvvvvvvv ',vear1
                    if(vear1 > -900.0):
                        mvear1=mvear1+nfc*vear1
                        nvear1=nvear1+nfc
                        mvebr1=mvebr1+nfc*vebr1
                        nvebr1=nvebr1+nfc
                    #print 'vvvvvvvvvvvv ',mvear1,nvear1

                    nbt1=nbt1+nbt
                    if(verb): print "bbbbbbbbbbbbb %s tau: %3d  %3d %3d"%(stmid,tau,nbt,nbt1)

                    if(tau == 0):
                        nrun1=nrun1+nrun
                        nrunmiss1=nrunmiss1+nrunmiss
                        nrunover1=nrunover1+nrunover

                    #
                    # 20061016 -- new structure for the vitals
                    #

                    if(fe1 >= 0.0):
                        cte1=float(tt[4])
                        ate1=float(tt[5])
                        mfe1=mfe1+nfc*fe1
                        mcte1=mcte1+nfc*cte1
                        mate1=mate1+nfc*ate1
                        nfe1=nfe1+nfc
                        nfc1=nfc1+nfc
                        nfcmiss1=nfcmiss1+nfcmiss
                        nfcover1=nfcover1+nfcover

                        if(verb): print 'nnnnnnnnnnn ',fe1,nfc,mfe1,nfe1


                    tt=vh[2].split()
                    fe2=float(tt[2])
                    if(fe2 >= 0.0):
                        cte2=float(tt[4])
                        ate2=float(tt[5])
                        mfe2=mfe2+nfc*fe2
                        mcte2=mcte2+nfc*cte2
                        mate2=mate2+nfc*ate2
                        nfe2=nfe2+nfc

                    vear2=float(tt[22])
                    vebr2=float(tt[23])
                    if(vear2 > -900.0):
                        mvear2=mvear2+nfc*vear2
                        nvear2=nvear2+nfc
                        mvebr2=mvebr2+nfc*vebr2
                        nvebr2=nvebr2+nfc


            if(nfe1 >= 0):

                if(nbt1 > 0):
                    pod1=float(nfc1)/float(nbt1)*100.0
                else:
                    pod1=0.0

                nof1=float(nfc1+nfcmiss1)

                if(nof1 > 0.0):
                    pof1=(1.0-(float(nfcmiss1)/nof1))*100.0
                else:
                    pof1=0.0

                if(nvear1 > 0):
                    mvear1=mvear1/nvear1
                    mvebr1=mvebr1/nvear1


                if(nfe1 > 0):
                    mfe1=mfe1/nfe1
                    mcte1=mcte1/nfe1
                    mate1=mate1/nfe1
                else:
                    mfe1=0.0
                    mcte1=0.0
                    mate1=0.0
                    gainxy=0.0

                if(nvear2 > 0):
                    mvear2=mvear2/nvear2
                    mvebr2=mvebr2/nvear2

                if(nfe2 > 0):
                    mfe2=mfe2/nfe2
                    mcte2=mcte2/nfe2
                    mate2=mate2/nfe2
                else:
                    mfe2=0.0
                    mcte2=0.0
                    mate2=0.0
                    gainxy=0.0

                if(mfe2 > 0.0):
                    gainxy=((mfe2-mfe1)/mfe2)*100.0
                else:
                    gainxy=0.0

                if(gainxy == 100.0): gainxy=0.0

                mfe2m1=(mfe2-mfe1)
                
                #
                # turn off track stats for vmax only aids
                #
                if(isVmaxOnlyModel1):
                    gainxy=0.0
                    mfe2m1=0.0
                    mfe2=0.0
                    mcte2=0.0
                    mate2=0.0
                    


                mfe1s[tau]=mfe1
                mfe2s[tau]=mfe2
                mcte1s[tau]=mcte1
                mcte2s[tau]=mcte2
                mate1s[tau]=mate1
                mate2s[tau]=mate2
                mvear1s[tau]=mvear1
                mvebr1s[tau]=mvebr1
                mvear2s[tau]=mvear2
                mvebr2s[tau]=mvebr2

                nrun1s[tau]=nrun1
                nrunmiss1s[tau]=nrunmiss1
                nbt1s[tau]=nbt1
                nfc1s[tau]=nfc1
                nfcmiss1s[tau]=nfcmiss1
                nfcover1s[tau]=nfcover1

                gainxys[tau]=gainxy
                nfe1s[tau]=nfe1
                mfe2m1s[tau]=mfe2m1
                pof1s[tau]=pof1
                pod1s[tau]=pod1


        #
        # do more processing and report
        #

        ntaus=len(taus)

        i=0
        for tau in taus:

            mfe1=mfe1s[tau]
            mfe2=mfe2s[tau]
            mcte1=mcte1s[tau]
            mcte2=mcte2s[tau]
            mate1=mate1s[tau]
            mate2=mate2s[tau]
            mfe2m1=mfe2m1s[tau]

            if(i == 0):
                tau1=taus[i+1]
                tau0=taus[i]
                dtau=float(tau1-tau0)
            elif(i == (ntaus-1)):
                tau1=taus[i]
                tau0=taus[i-1]
                dtau=float(tau1-tau0)

            elif(i < (ntaus-1) and i == 0):
                tau1=taus[i+1]
                tau0=taus[i]
                dtau=float(tau1-tau0)

            elif(i < (ntaus-1) and i > 0):
                tau1=taus[i+1]
                tau0=taus[i-1]
                dtau=float(tau1-tau0)

            dfe1=(mfe1s[tau1]-mfe1s[tau0])/dtau
            dfe2=(mfe2s[tau1]-mfe2s[tau0])/dtau


            dfetau=6.0
            #
            # make it always 6h growth
            #
            #if(int(hh1) == 6 or int(hh2) == 6):
            #    dfetau=6.0
            #elif(int(hh1) == 12 or int(hh2) == 12):
            #     dfetau=12.0

            gain1err06=dfe1*dfetau
            gain2err06=dfe2*dfetau

            #
            # turn off track stats for vmax only aids
            #
            if(isVmaxOnlyModel1):
                gain1err06=0.0
                gain2err06=0.0
                
            gaine6xs[tau]=gain1err06
            gainxy=gainxys[tau]
            nfe1=nfe1s[tau]
            pof1=pof1s[tau]
            pod1=pod1s[tau]

            nrun1=nrun1s[tau]
            nrunmiss1=nrunmiss1s[tau]
            nbt1=nbt1s[tau]
            nfc1=nfc1s[tau]
            nfcmiss1=nfcmiss1s[tau]
            nfcover1=nfcover1s[tau]

            i=i+1


        statlist=(mod1,mfe1s,mfe2s,mcte1s,mcte2s,
                  mate1s,mate2s,
                  mvear1s,mvear2s,mvebr1s,mvebr2s,
                  gainxys,gaine6xs,nfe1s,
                  mfe2m1s,pof1s,pod1s,nrun1s,
                  nrunmiss1s,nbt1s,nfc1s,
                  nfcmiss1s,nfcover1s)

        allstats.append(statlist)

    return(allstats)


def stmlistcard(stmids,nmax=15):

    if(len(stmids) > nmax):
        return(None)

    rptcard='Storms: '
    for stmid in stmids:
        rptcard=rptcard+"%s "%(stmid)

    return(rptcard)
        

def stmyearscard(stmids):
    years=[]
    for stmid in stmids:
        year=stmid.split('.')[1]
        years.append(year)

    years=mf.uniq(years)

    oyear=''
    ny=len(years)
    for n in range(0,ny):
        if(n < ny-1):
            oyear=oyear+"%s, "%(years[n])
        else:
            oyear=oyear+"%s"%(years[n])

    return(oyear)


def PrintVitalsAllStats(allstats,taus,
                        stmids,vstmids,models,
                        verb,lsopt,vopts,
                        print0fc=0):

    (veriopts,tau00filtopt,stmopt,stmoptall,tauls,dohomo)=vopts

    try:
        nstms=len(vstmids[models[0]])
    except:
        nstms=0
        print'NNNN no stms with stats: ',stmids,vstmids
        rc=(None,None,None,None,None)
        return(rc)
        
    #
    # single storm
    #
    if(nstms == 1):
        ostmopt=stmids[0]
    else:
        ostmopt=stmopt
        
    basinshort='Bsss'
        
    nmodels=len(models)
    if(nmodels == 1):
        mod1=models[nmodels-1]
        mod2=mod1
    elif(nmodels >= 2):
        mod2=models[nmodels-1]


    #
    # collect lists for ploting/printing
    #

    pmodels=[]
    plstats=[]
    pstats=[]
    pns=[]

    report=[]
    rptcards=[]



    nstats=len(allstats)

    #
    # get last model
    #

    if(nstats > 1):

        allstatlast=allstats[nstats-1]

        (lmod1,lmfe1s,lmfe2s,lmcte1s,lmcte2s,
         mate1s,mate2s,
         mvear1s,mvear2s,mvebr1s,mvebr2s,
         gainxys,gaine6xs,nfe1s,
         mfe2m1s,pof1s,pod1s,nrun1s,
         nrunmiss1s,nbt1s,nfc1s,
         nfcmiss1s,nfcover1s)=allstatlast

    else:
        lmod1=None


    for n in range(0,nstats):

        allstat=allstats[n]

        (mod1,mfe1s,mfe2s,mcte1s,mcte2s,
         mate1s,mate2s,
         mvear1s,mvear2s,mvebr1s,mvebr2s,
         gainxys,gaine6xs,nfe1s,
         mfe2m1s,pof1s,pod1s,nrun1s,
         nrunmiss1s,nbt1s,nfc1s,
         nfcmiss1s,nfcover1s)=allstat


        if(lmod1 == None):
            lmod1=mod1

        isVmaxOnlyModel1=(mf.find(mod1,'icon'))


        if(dohomo):

            omod1=mod1.split('.')[0]
            omod2=mod1.split('.')[1]

            pmodels.append(omod1)
            plstats.append([mcte1s,mate1s])
            pstats.append([mfe1s,gainxys,pod1s,pof1s])
            pns.append(nfe1s)

            if(n == nstats-1):
                pmodels.append(omod2)
                plstats.append([mcte2s,mate2s])
                pstats.append([mfe2s,gainxys,pod1s,pof1s])
                pns.append(nfe1s)

        else:

            pmodels.append(mod1)
            plstats.append([mcte1s,mate1s])
            pstats.append([mfe1s,gainxys,pod1s,pof1s])
            pns.append(nfe1s)


        #
        # the allstats is now loaded correctly with the mfe2 model so just use it...
        #

        if(nstats > 1):

            for tau in taus:

                try:
                    lmfe2=mfe2s[tau]
                    mfe1=mfe1s[tau]
                except:
                    continue

                if(lmfe2 > 0.0):
                    gainxy=((lmfe2-mfe1)/lmfe2)*100.0
                else:
                    gainxy=0.0

                if(gainxy == 100): gainxy=0.0
                
                #
                # turn off track stats for vmax only aids
                #
                
                if(isVmaxOnlyModel1):
                    gainxy=0.0
                
                gainxys[tau]=gainxy

        else:

            lmfe2s=mfe2s

            for tau in taus:

                try:
                    lmfe2=mfe2s[tau]
                except:
                    continue
                mfe1=mfe1s[tau]

                if(lmfe2 > 0.0):
                    gainxy=((lmfe2-mfe1)/lmfe2)*100.0
                else:
                    gainxy=0.0

                if(gainxy == 100): gainxy=0.0

                if(isVmaxOnlyModel1):
                    gainxy=0.0

                gainxys[tau]=gainxy

            
        if(dohomo):
            dohetero=0
            nstms=len(vstmids[omod1])
            print
            oyear=stmyearscard(stmids)
            rptcard="Homogeneous Comp of Model: %s  against: %s  N: %d TCs in: %s for: %s"%(omod1,omod2,nstms,basinshort,oyear)
            print rptcard
            rptcards.append(rptcard)

            vcard=stmlistcard(vstmids[omod1])
            if(vcard != None and lsopt == 1):
                print vcard
                rptcards.append(vcard)

            omod1=mod1

        else:
            dohetero=1
            oyear=stmyearscard(stmids)
            rptcard="Hetero Comp Tau00FiltOpt: %s   Model: %s  against: %s  N: %d TCs in: %s for %s"%\
                     (tau00filtopt,mod1,mod2,nstms,basinshort,oyear)
            print rptcard
            rptcards.append(rptcard)
            
            vcard=stmlistcard(vstmids[mod1])
            if(vcard != None and lsopt == 1):
                print vcard
                rptcards.append(vcard)

            omod1="%s_%s"%(mod1,lmod1)
            omod1=mod1


        h1card=" tau   mfe1 cte1/ate1    mfe2 cte2/ate2 VeA1/Vb1 A2/b2   GNxy%   2m1 E6x    "
        if(dohomo):
            h2card="POD%  POF%     Nr NrM  Nbt  Nfc NfM NfO Mod1.Mod2"
        else:
            h2card="POD%  POF%     Nr NrM  Nbt  Nfc NfM NfO Mod1_Mod2"
        rptcard=h1card+h2card

        if(lsopt == 1):
            print
            print rptcard
            
        rptcards.append(rptcard)

        for tau in taus:

            try:
                lmfe2=lmfe2s[tau]
                mfe1=mfe1s[tau]
                mfe2=mfe2s[tau]
            except:
                continue

            mvear1=mvear1s[tau]
            mvebr1=mvebr1s[tau]
            
            mvear2=mvear2s[tau]
            mvebr2=mvebr2s[tau]

            mcte1=mcte1s[tau]
            mcte2=mcte2s[tau]
            mate1=mate1s[tau]
            mate2=mate2s[tau]
            mfe2m1=mfe2m1s[tau]

            gain1err06=gaine6xs[tau]
            gainxy=gainxys[tau]
            nfe1=nfe1s[tau]
            pof1=pof1s[tau]
            pod1=pod1s[tau]


            nrun1=nrun1s[tau]
            nrunmiss1=nrunmiss1s[tau]
            nbt1=nbt1s[tau]
            nfc1=nfc1s[tau]
            nfcmiss1=nfcmiss1s[tau]
            nfcover1=nfcover1s[tau]

            #
            # bail if no forcast
            #
            if(not(print0fc) and nfc1 == 0):
                continue
            
            
            if(nfc1 == 0):
                gain1err06=0.0
                
            if(isVmaxOnlyModel1):
                gain1err06=0.0

            vmaxlim=70
            cmvear1="%3.0f"%(mvear1)
            if(mvear1 > vmaxlim): cmvear1=' **'
            cmvear2="%3.0f"%(mvear2)
            if(mvear2 > vmaxlim): cmvear2=' **'
            cmvebr1="%-3.0f"%(mvebr1)
            if(mvebr1 < -vmaxlim): cmvebr1='** '
            cmvebr2="%-3.0f"%(mvebr2)
            if(mvebr2 < -vmaxlim): cmvebr2='** '

            rptcard1="%3dh  %5.1f %4.0f/%-4.0f : %5.1f %4.0f/%-4.0f :"%(tau,mfe1,mcte1,mate1,mfe2,mcte2,mate2)
            rptcard1b="%s/%-3.0f%s/%s :"%(cmvear1,mvebr1,cmvear2,cmvebr2)
            rptcard1a=" %4.0f %5.0f %3.0f : %5.1f %5.1f : "%(gainxy,mfe2m1,gain1err06,pod1,pof1)
            rptcard2="%4d %3d %4d %4d %3d %3d %s %s"%(nrun1,nrunmiss1,nbt1,nfc1,nfcmiss1,nfcover1,omod1,ostmopt)
            rptcard=rptcard1+rptcard1b+rptcard1a+rptcard2
            rptcards.append(rptcard)
            if(lsopt == 1):
                print rptcard


    return(rptcards,pmodels,pstats,plstats,pns)

def StatFigureTable(models,stats,lstats,ns,taus,dohomo,stmopt,verb=0):

    table={}

    ctaus=[]
    colLabels=[]
    rowLabels=[]
    rowLabelsCtAt=[]
    rowColors=[]
    legLabels=[]
    topTitles=[]
    topTitlesCtAt=[]
    modColors=[]
    yLabels={}
    yLims={}
    
    topTitlesGainxy=[]
    rowLabelsGainxy=[]
    rowColorsGainxy=[]
    
    topTitlesPodxy=[]
    rowLabelsPodxy=[]
    rowColorsPodxy=[]
    
    topTitlesPofxy=[]
    rowLabelsPofxy=[]
    rowColorsPofxy=[]
    
    (tdocolor,Color2Hex)=TCtdos.TdoColors()

    gainxy=[]
    cgainxy=[]
    podxy=[]
    cpodxy=[]
    pofxy=[]
    cpofxy=[]
    
    mfe=[]
    ctxt=[]
    ctxtctat=[]

    Nxy=[]

    nstats=len(stats)
    
    for i in range(0,nstats):

        stat=stats[i]

        s1=lstats[i][0]
        s2=lstats[i][1]

        n=ns[i]
        ctxtrow=[]
        cgainxyrow=[]
        cctatrow=[]
        cpodxyrow=[]
        cpofxyrow=[]
        
        gainxyrow=[]
        Nxyrow=[]
        podxyrow=[]
        pofxyrow=[]
        mferow=[]
        
        for tau in taus:

            #ctxtrow.append("%3.0f|%3d|%2.0f/%-2.0f"%(stat[0][tau],n[tau],s1[tau],s2[tau]))
            #ctxtrow.append("%3.0f[%3d] (%3.0f/%-3.0f)"%(stat[0][tau],n[tau],s1[tau],s2[tau]))
            #ctxtrow.append("%3.0f(%3.0f/%-3.0f)"%(stat[0][tau],s1[tau],s2[tau]))
            #ctatrow.append("%4.0f/%-4.0f"%(s1[tau],s2[tau]))

            cstring=" %3.0f|%3d "%(stat[0][tau],n[tau])
            ctxtrow.append(cstring)

            cstring="%2.0f/%-2.0f|%3d "%(s1[tau],s2[tau],n[tau])
            cctatrow.append(cstring)

            cgainxyrow.append("%4.0f [%d]"%(stat[1][tau],n[tau]))
            cpodxyrow.append("%4.0f [%d]"%(stat[2][tau],n[tau]))
            cpofxyrow.append("%4.0f [%d]"%(stat[3][tau],n[tau]))
            
            mferow.append(stat[0][tau])
            gainxyrow.append(stat[1][tau])
            Nxyrow.append(float(n[tau]))
            podxyrow.append(stat[2][tau])
            pofxyrow.append(stat[3][tau])

            
        ctxt.append(ctxtrow)
        ctxtctat.append(cctatrow)
        mfe.append(mferow)

        if( i < nstats - 1):
            cpodxy.append(cpodxyrow)
            podxy.append(podxyrow)
            cpofxy.append(cpofxyrow)
            pofxy.append(pofxyrow)
            cgainxy.append(cgainxyrow)
            gainxy.append(gainxyrow)

        elif(not(dohomo)):
            
            cpodxy.append(cpodxyrow)
            podxy.append(podxyrow)
            cpofxy.append(cpofxyrow)
            pofxy.append(pofxyrow)
            
        Nxy.append(Nxyrow)

    
    yLabels['mfe']='MFE [nm]'
    yLabels['gainxy']='Gain [%]'
    yLabels['pod']='Prob of Detection [%]'
    yLabels['pof']='Prob of Forecast [%]'

    yLims['mfe']=(0,600,50)
    yLims['gainxy']=(-70,70,10)
    yLims['gainxy']=(-20,20,5)
    yLims['sgainxy']=(-100,100,10)
    yLims['pod']=(0,140,10)
    yLims['pof']=(0,140,10)



    nmodels=len(models)

    if(dohomo):
        comptype='Homogeneous'
    else:
        comptype='Heterogeneous'
        
    t1mod='Models: '
    t1gain="Gain [%%] against: %s   TCs: %s"%(models[nmodels-1],stmopt)
    t1pod="POD [%%] TCs: %s"%(stmopt)
    t1pof="POF [%%] TCs: %s"%(stmopt)
    if(dohomo):
        t1pod="POD [%%] against: %s  TCs: %s"%(models[nmodels-1],stmopt)
        t1pof="POF [%%] against: %s  TCs: %s"%(models[nmodels-1],stmopt)
        
    
    for n in range(0,nmodels):

        model=models[n]

        #m3=model[0:3]
        lm=len(model)
        suf2=model[lm-2:lm]
        if(suf2 == '00' or suf2 == '06' or suf2 == '12'):
            m3=model[0:lm-2]
        else:
            m3=model

        matts=atcf.TrkModeltoBattributes[m3]
        mcol=matts[2]
        mcol=Color2Hex[mcol]
        modColors.append(mcol)
        
        if(verb): print 'model ',m3,matts,mcol
        legLabels.append("%s"%(model))

        rowColors.append(mcol)
        #rowLabels.append("FE|N|CT/AT")
        #rowLabels.append("%s FE|N|CT/AT"%(model))

        rowLabels.append("%s FE|N"%(model))
        rowLabelsCtAt.append("%s CT/AT|N"%(model))

        #rowColors.append(mcol)
        #rowLabels.append("%s CT/AT"%(model))


        gxycol=Color2Hex['usafblue']

        if(n < nmodels-1):
            rowColorsPodxy.append(gxycol)
            rowLabelsPodxy.append("%s Pod|N"%(model))

            rowColorsPofxy.append(gxycol)
            rowLabelsPofxy.append("%s Pof|N"%(model))

        elif(not(dohomo)):
            rowColorsPodxy.append(gxycol)
            rowLabelsPodxy.append("%s Pod|N"%(model))

            rowColorsPofxy.append(gxycol)
            rowLabelsPofxy.append("%s Pof|N"%(model))


        if(n < nmodels-1):
            t1mod="%s %s,"%(t1mod,model)
        else:
            t1mod="%s %s"%(t1mod,model)

    #
    # gainxy
    #
    

    for n in range(0,nmodels-1):

        model=models[n]

        lm=len(model)
        suf2=model[lm-2:lm]
        if(suf2 == '00' or suf2 == '06' or suf2 == '12'):
            m3=model[0:lm-2]
        else:
            m3=model
        matts=atcf.TrkModeltoBattributes[m3]
        mcol=matts[2]
        mcol=Color2Hex[mcol]
        modColors.append(mcol)

        gxycol=Color2Hex['usafblue']
        rowColorsGainxy.append(gxycol)
        rowLabelsGainxy.append("%s [N]"%(model))



    t1mfe="%s TCs: %s\n%s Comp FE|N in table"%(t1mod,stmopt,comptype)
    t1ctat="%s TCs: %s\n%s Comp CT/AT|N in table"%(t1mod,stmopt,comptype)
    t1gain="%s\n%s Comp [> 0 better ; < 0 worse]"%(t1gain,comptype)
    t1pod="%s\n%s"%(t1pod,comptype)
    t1pof="%s\n%s Comp"%(t1pof,comptype)
    
    for tau in taus:
        colLabels.append("%dh"%(tau))


    topTitles.append(t1mfe)
    topTitlesCtAt.append(t1ctat)
    topTitlesGainxy.append(t1gain)
    topTitlesPodxy.append(t1pod)
    topTitlesPofxy.append(t1pof)
    
    table['clab']=colLabels
    table['rcol']=rowColors
    table['rlab']=rowLabels
    table['rlabctat']=rowLabelsCtAt
    table['ylab']=yLabels
    table['ylims']=yLims

    table['llab']=legLabels
    table['mfe']=mfe
    table['ctxt']=ctxt
    table['ctxtctat']=ctxtctat
    table['toptitles']=topTitles
    table['toptitlesctat']=topTitlesCtAt
    table['modcolors']=modColors
    
    table['toptitlesgainxy']=topTitlesGainxy
    table['rcolgainxy']=rowColorsGainxy
    table['rlabgainxy']=rowLabelsGainxy
    table['gainxy']=gainxy
    table['cgainxy']=cgainxy
    
    
    table['toptitlespodxy']=topTitlesPodxy
    table['rcolpodxy']=rowColorsPodxy
    table['rlabpodxy']=rowLabelsPodxy
    table['podxy']=podxy
    table['cpodxy']=cpodxy
    
    table['toptitlespofxy']=topTitlesPofxy
    table['rcolpofxy']=rowColorsPofxy
    table['rlabpofxy']=rowLabelsPofxy
    table['pofxy']=pofxy
    table['cpofxy']=cpofxy
    
    
    return(table)



def GetVitalsHomoStats(vstmids,vtype,dfeonly,models,resetcache=0,verb=0):

    taus=[0,12,24,36,48,60,72,84,96,108,120]
    taus=[0,12,24,36,48,72,96,120]

    vhash={}

    for vstmid in vstmids:

        (stmid,year)=vstmid.split('.')
        b1id=stmid[2:3]

        if(b1id == 'L' or b1id == 'E' or b1id == 'C'):
            rulebase='NhcOps'
            tccenter='NHC'
        else:
            rulebase='JtwcOps'
            tccenter='JTWC'

        VTC=GetTcVitalsHomoHash(stmid,year,models,resetcache,verb=0)

        if(VTC == None): continue


        vits=VTC.Vitals

        vks=w2.GetKeys(vits,'vits',verb=0)
        
        for tau in taus:

            for mod1 in models:
                vmodopt=mod1

                try:
                    vkey=(vstmid,vmodopt,rulebase,'ALL',tau)
                    vl=vits[vkey]
                    if(verb): print 'vvvvvvvvvvvvvv ',vkey,vl
                except:
                    vl=None

                if(vl != None):
                    cnts=vl[0]
                    statmod1=vl[1]
                    statmod2=vl[2]
                else:
                    cnts=statmod1=statmod2=None

                if(verb):
                    print 'cnts ',tau,cnts
                    print 'statmod1 ',tau,statmod1
                    print 'statmod2 ',tau,statmod2

                try:
                    vhash[mod1,tau,vstmid].append([cnts,statmod1,statmod2])
                    if(verb): print 'ttt ',tau,vstmid
                except:
                    vhash[mod1,tau,vstmid]=[]
                    vhash[mod1,tau,vstmid].append([cnts,statmod1,statmod2])
                    if(verb): print 'bbbbbbbbbbbbbbbb ',tau,vstmid


    return(taus,vstmids,vhash)




def GetVitalsAllStats(vstmids,vtype,dfeonly,models,verb=0):


    taus=[0,12,24,36,48,60,72,84,96,108,120]
    taus=[0,12,24,36,48,72,96,120]

    vhash={}

    for vstmid in vstmids:

        (stmid,year)=vstmid.split('.')
        b1id=stmid[2:3]

        if(b1id == 'L' or b1id == 'E' or b1id == 'C'):
            rulebase='NhcOps'
            tccenter='NHC'
        else:
            rulebase='JtwcOps'
            tccenter='JTWC'

        VTC=GetTcVitalsHash(stmid,year,vtype,verb)

        if(VTC == None): continue

        if(dfeonly):

            dfes=VTC.DfeVitals
            dks=w2.GetKeys(dfes,'dfes',verb=0)

        else:

            vits=VTC.Vitals
            bts=VTC.BtGcards
            fcs=VTC.FcGcards
            gsfs=VTC.GsfGcards
            dfes=VTC.DfeVitals

            vks=w2.GetKeys(vits,'vits',verb=0)
            bks=w2.GetKeys(bts,'bts',verb=0)
            fks=w2.GetKeys(fcs,'fcs',verb=0)
            gks=w2.GetKeys(gsfs,'gsfs',verb=0)
            dks=w2.GetKeys(dfes,'dfes',verb=0)

        for tau in taus:

            for mod1 in models:
                vmodopt=mod1

                try:
                    vkey=(vstmid,vmodopt,rulebase,'ALL',tau)
                    vl=vits[vkey]
                    if(verb): print 'vvvvvvvvvvvvvv ',vkey,vl
                except:
                    vl=None
                    print 'NNNNNNNNNNNNNNNNnnno data for ',vstmid,vmodopt,rulebase,'ALL',tau

                if(vl != None):
                    cnts=vl[0]
                    statmod1=vl[1]
                    statmod2=vl[2]
                else:
                    cnts=statmod1=statmod2=None

                if(verb):
                    print 'cnts ',tau,cnts
                    print 'statmod1 ',tau,statmod1
                    print 'statmod2 ',tau,statmod2

                try:
                    vhash[mod1,tau,vstmid].append([cnts,statmod1,statmod2])
                    if(verb): print 'ttt ',tau,vstmid
                except:
                    vhash[mod1,tau,vstmid]=[]
                    vhash[mod1,tau,vstmid].append([cnts,statmod1,statmod2])
                    if(verb): print 'bbbbbbbbbbbbbbbb ',tau,vstmid


    return(taus,vstmids,vhash)



def StmPrintVitalsAllStats(vstmids,stmstats,allstmstats,stmmeta,obasin,dohomo,taus,year,stmopt,models,veritau,
                           verb,lsopt,vopts):


    def model2m3(model):
        lm=len(model)
        if(lm == 5):
            m3=model[0:3]
        elif(lm >= 4):
            m3=model[0:4]
        else:
            m3=model[0:3]
        return(m3)

    nallstmstats=len(allstmstats)
    print 'nstats ',nallstmstats

    nstmfcs=[]

    for n in range(0,nallstmstats):

        allstat=allstmstats[n]
        
        (mod1,mfe1s,mfe2s,mcte1s,mcte2s,
         mate1s,mate2s,
         mvear1s,mvear2s,mvebr1s,mvebr2s,
         gainxys,gaine6xs,nfe1s,
         mfe2m1s,pof1s,pod1s,nrun1s,
         nrunmiss1s,nbt1s,nfc1s,
         nfcmiss1s,nfcover1s)=allstat

        nstmfcs.append(nfc1s)

    
    nstms=len(vstmids)

    nmodels=len(models)
    if(nmodels == 1):
        mod1=models[nmodels-1]
        mod2=mod1
    elif(nmodels >= 2):
        mod2=models[nmodels-1]

    #
    # collect lists for ploting/printing
    #

    pnsfracmax=-999.0
    pnsfracmin=999.0

    rptcards=[]
    
    pmodels=[]
    pstats={}
    pns={}
    pnsfrac={}

    nstmid=0
    for stmid in vstmids:

        ostmname="%s %s"%(stmmeta[stmid][1],stmmeta[stmid][0])
        
        allstats=stmstats[stmid]
        nstats=len(allstats)
        ostmopt="%s.%s"%(stmid,year)

        #
        # get last model
        #

        if(nstats > 1):

            allstatlast=allstats[nstats-1]

            (lmod1,lmfe1s,lmfe2s,lmcte1s,lmcte2s,
             mate1s,mate2s,
             mvear1s,mvear2s,mvebr1s,mvebr2s,
             gainxys,gaine6xs,nfe1s,
             mfe2m1s,pof1s,pod1s,nrun1s,
             nrunmiss1s,nbt1s,nfc1s,
             nfcmiss1s,nfcover1s)=allstatlast

        else:
            lmod1=None


        if(nstmid > 0):
            if(dohomo):
                h1card=" tau   mfe1 cte1/ate1    mfe2 cte2/ate2   GNxy%   "
                h2card="2m1 E6x    POD%  POF%     Nr NrM  Nbt  Nfc NfM NfO Mod1.Mod2"
                rptcard=h1card+h2card
            else:
                h1card=" tau   mfe1 cte1/ate1    mfe2 cte2/ate2   GNxy%   "
                h2card="2m1 E6x    POD%  POF%     Nr NrM  Nbt  Nfc NfM NfO Mod1_Mod2"
                rptcard=h1card+h2card

            if(lsopt == 1):
                print
                print rptcard
            
            rptcards.append(rptcard)
        
        for n in range(0,nstats):

            allstat=allstats[n]

            (mod1,mfe1s,mfe2s,mcte1s,mcte2s,
             mate1s,mate2s,
             mvear1s,mvear2s,mvebr1s,mvebr2s,
             gainxys,gaine6xs,nfe1s,
             mfe2m1s,pof1s,pod1s,nrun1s,
             nrunmiss1s,nbt1s,nfc1s,
             nfcmiss1s,nfcover1s)=allstat

            if(lmod1 == None):
                lmod1=mod1

            if(nstats > 1):
                for tau in taus:
                    lmfe2=lmfe2s[tau]
                    mfe1=mfe1s[tau]
                    if(lmfe2 > 0.0):
                        gainxy=((lmfe2-mfe1)/lmfe2)*100.0
                    else:
                        gainxy=0.0
                    
                    isVmaxOnlyModel1=(mod1 == 'icon')
                    if(isVmaxOnlyModel1): gainxy=0

                    gainxys[tau]=gainxy
            else:
                lmfe2s=mfe2s
                for tau in taus:
                    try:
                        lmfe2=mfe2s[tau]
                        mfe1=mfe1s[tau]
                    except:
                        gainxy=0.0
                        continue

                    if(lmfe2 > 0.0):
                        gainxy=((lmfe2-mfe1)/lmfe2)*100.0
                    else:
                        gainxy=0.0
                    isVmaxOnlyModel2=(mod2 == 'icon')
                    if(isVmaxOnlyModel2): gainxy=0

                    gainxys[tau]=gainxy


            if(nstmid == 0):
                if(dohomo):
                    omod1=mod1.split('.')[0]
                    omod2=mod1.split('.')[1]
                    pmodels.append(omod1)
                    if(n == nstats-1):
                        pmodels.append(omod2)
                else:
                    omod1=mod1
                    pmodels.append(omod1)
                    omod2=mod2
                    

            else:
                if(dohomo):
                    omod1=mod1.split('.')[0]
                    omod2=mod1.split('.')[1]
                else:
                    omod1=mod1
                    omod2=mod2

            if(nstmid == 0 and n == 0):
                print
                h2card=" N: %d TCs in: %s for: %s"%(nstms,obasin,year)
                if(dohomo):
                    dohetero=0
                    h1card="Homogeneous Comp of Model: %s  against: %s"%(omod1,omod2)
                    rptcard=h1card+h2card
                    if(lsopt == 1):
                        print rptcard
                    rptcards.append(rptcard)
                    #omod1=mod1
                else:
                    dohetero=1
                    h1card="Heterogeneous Comp of Model: %s  against: %s"%(omod1,omod2)
                    rptcard=h1card+h2card
                    if(lsopt == 1):
                        print rptcard
                    rptcards.append(rptcard)
                    #omod1=mod1
                    
                if(dohomo):
                    h1card=" tau   mfe1 cte1/ate1    mfe2 cte2/ate2   GNxy%   "
                    h2card="2m1 E6x    POD%  POF%     Nr NrM  Nbt  Nfc NfM NfO Mod1.Mod2"
                    rptcard=h1card+h2card
                else:
                    h1card=" tau   mfe1 cte1/ate1    mfe2 cte2/ate2   GNxy%   "
                    h2card="2m1 E6x    POD%  POF%     Nr NrM  Nbt  Nfc NfM NfO Mod1_Mod2"
                    rptcard=h1card+h2card

                if(lsopt == 1):
                    print
                    print rptcard
                rptcards.append(rptcard)



            otaus=[veritau]

            for tau in otaus:

                try:
                    lmfe2=lmfe2s[tau]
                    
                except:

                    lmfe2s[tau]=0.0
                    mfe1s[tau]=0.0
                    mfe2s[tau]=0.0
                    mcte1s[tau]=0.0
                    mcte2s[tau]=0.0
                    mate1s[tau]=0.0
                    mate2s[tau]=0.0
                    mfe2m1s[tau]=0.0

                    gaine6xs[tau]=0.0
                    gainxys[tau]=0.0
                    nfe1s[tau]=0.0
                    pof1s[tau]=0.0
                    pod1s[tau]=0.0

                    nrun1s[tau]=0
                    nrunmiss1s[tau]=0
                    nbt1s[tau]=0
                    nfc1s[tau]=0
                    nfcmiss1s[tau]=0
                    nfcover1s[tau]=0

                    
                mfe1=mfe1s[tau]
                mfe2=mfe2s[tau]
                mcte1=mcte1s[tau]
                mcte2=mcte2s[tau]
                mate1=mate1s[tau]
                mate2=mate2s[tau]
                mfe2m1=mfe2m1s[tau]

                gain1err06=gaine6xs[tau]
                gainxy=gainxys[tau]
                nfe1=nfe1s[tau]
                pof1=pof1s[tau]
                pod1=pod1s[tau]

                nrun1=nrun1s[tau]
                nrunmiss1=nrunmiss1s[tau]
                nbt1=nbt1s[tau]
                nfc1=nfc1s[tau]
                nfcmiss1=nfcmiss1s[tau]
                nfcover1=nfcover1s[tau]

                if(nfe1 == 0): gainxy=0.0


                nstmfc=nstmfcs[n][tau]
                
                if(nfc1 == 0):
                    gain1err06=0.0

                if(dohomo):
                    pstats[stmid,omod1]=[mfe1,mcte1,mate1,gainxy,pod1,pof1]
                    pns[stmid,omod1]=nfe1
                    if(nstmfc > 0):
                        pnsfrac[stmid,omod1]=float(nfe1)/float(nstmfc)
                    else:
                        pnsfrac[stmid,omod1]=0
                        
                    if(pnsfrac[stmid,omod1] > pnsfracmax): pnsfracmax=pnsfrac[stmid,omod1]
                    if(pnsfrac[stmid,omod1] < pnsfracmin): pnsfracmin=pnsfrac[stmid,omod1]
                    
                    if(n == nstats-1):
                        pstats[stmid,omod2]=[mfe2,mcte2,mate2,gainxy,pod1,pof1]
                        pns[stmid,omod2]=nfe1
                        if(nstmfc > 0):
                            pnsfrac[stmid,omod2]=float(nfe1)/float(nstmfc)
                        else:
                            pnsfrac[stmid,omod2]=0.0
                        if(pnsfrac[stmid,omod1] > pnsfracmax): pnsfracmax=pnsfrac[stmid,omod1]
                        if(pnsfrac[stmid,omod1] < pnsfracmin): pnsfracmin=pnsfrac[stmid,omod1]
                else:
                    pstats[stmid,omod1]=[mfe1,mcte1,mate1,gainxy,pod1,pof1]
                    pns[stmid,omod1]=nfe1
                    pnsfrac[stmid,omod1]=float(nfe1)/float(nstmfc)
                    if(pnsfrac[stmid,omod1] > pnsfracmax): pnsfracmax=pnsfrac[stmid,omod1]
                    if(pnsfrac[stmid,omod1] < pnsfracmin): pnsfracmin=pnsfrac[stmid,omod1]


            
            rptcard1="%3dh  %5.1f %4.0f/%-4.0f : %5.1f %4.0f/%-4.0f :"%(tau,mfe1,mcte1,mate1,mfe2,mcte2,mate2)
            rptcard1a="  %4.0f %5.0f %3.0f : %5.1f %5.1f : "%(gainxy,mfe2m1,gain1err06,pod1,pof1)
            rptcard2="%4d %3d %4d %4d %3d %3d "%(nrun1,nrunmiss1,nbt1,nfc1,nfcmiss1,nfcover1)
            rptcard2a="%s %s %s"%(omod1,ostmopt,ostmname)
            rptcard=rptcard1+rptcard1a+rptcard2+rptcard2a
            rptcards.append(rptcard)
            if(lsopt == 1):
                print rptcard

        nstmid=nstmid+1


    table={}

    ctaus=[]
    colLabels=[]
    rowLabels=[]
    rowLabelsCtAt=[]
    rowColors=[]
    legLabels=[]
    topTitles=[]
    topTitlesCtAt=[]
    modColors=[]
    yLabels={}
    yLims={}
    
    topTitlessGainxy=[]
    rowLabelssGainxy=[]
    rowColorssGainxy=[]
    
    topTitlesGainxy=[]
    rowLabelsGainxy=[]
    rowColorsGainxy=[]
    
    topTitlesPodxy=[]
    rowLabelsPodxy=[]
    rowColorsPodxy=[]
    
    topTitlesPofxy=[]
    rowLabelsPofxy=[]
    rowColorsPofxy=[]
    
    topTitlesNfracxy=[]
    rowLabelsNfracxy=[]
    rowColorsNfracxy=[]
    
    (tdocolor,Color2Hex)=TCtdos.TdoColors()

    gainxy=[]
    cgainxy=[]
    sgainxy=[]
    csgainxy=[]

    podxy=[]
    cpodxy=[]
    pofxy=[]
    cpofxy=[]
    nfracxy=[]
    cnfracxy=[]
    
    mfe=[]
    ctxt=[]
    ctxtctat=[]

    nxy=[]

    npmodels=len(pmodels)
    
    i=0
    j=0
    for model in pmodels:
        
        ctxtrow=[]
        cgainxyrow=[]
        csgainxyrow=[]
        cctatrow=[]
        cpodxyrow=[]
        cpofxyrow=[]
        cnfracxyrow=[]

        gainxyrow=[]
        sgainxyrow=[]
        nxyrow=[]
        podxyrow=[]
        pofxyrow=[]
        nfracxyrow=[]
        mferow=[]

        nstms=len(vstmids)

        for stmid in vstmids:

            stat=pstats[stmid,model]

            n=pns[stmid,model]
            nfrac=pnsfrac[stmid,model]*100.0

            tau=otaus[0]
            
            cstring=" %3.0f|%3d "%(stat[0],n)
            cstring="%d"%(n)
            ctxtrow.append(cstring)

            cstring="%2.0f/%-2.0f|%3d "%(stat[1],stat[2],n)
            cstring="%d"%(n)
            cctatrow.append(cstring)

            cstring="%4.0f [%d]"%(stat[3],n)
            cstring="%d"%(n)
            cgainxyrow.append(cstring)

            cstring="%d"%(n)
            csgainxyrow.append(cstring)

            cstring="%4.0f [%d]"%(stat[4],n)
            cstring="%d"%(n)
            cpodxyrow.append(cstring)
            
            cstring="%4.0f [%d]"%(stat[5],n)
            cstring="%d"%(n)
            cpofxyrow.append(cstring)
            
            cstring="%2.0f"%(nfrac)
            cnfracxyrow.append(cstring)
            
            mferow.append(stat[0])
            gainxyrow.append(stat[3])
            sgainxystat=(stat[3]*nfrac)*0.1
            sgainxyrow.append(sgainxystat)
            nxyrow.append(float(n))
            podxyrow.append(stat[4])
            pofxyrow.append(stat[5])
            nfracxyrow.append(nfrac)

            i=i+1

            
        ctxt.append(ctxtrow)
        ctxtctat.append(cctatrow)
        mfe.append(mferow)
        cnfracxy.append(cnfracxyrow)
        nfracxy.append(nfracxyrow)

        if( j < npmodels - 1):
            cpodxy.append(cpodxyrow)
            podxy.append(podxyrow)
            cpofxy.append(cpofxyrow)
            pofxy.append(pofxyrow)
            cgainxy.append(cgainxyrow)
            csgainxy.append(csgainxyrow)
            gainxy.append(gainxyrow)
            sgainxy.append(sgainxyrow)

        elif(not(dohomo)):
            
            cpodxy.append(cpodxyrow)
            podxy.append(podxyrow)
            cpofxy.append(cpofxyrow)
            pofxy.append(pofxyrow)
            
        nxy.append(nxyrow)

        j=j+1



    npmodels=len(pmodels)

    if(dohomo):
        comptype="Homogeneous against: %s"%(pmodels[npmodels-1])
    else:
        comptype="Heterogeneous"
        
    t1mod="Tau: %sh  Models: "%(otaus[0])
    t1gain="Tau: %sh Gain [%%] against: %s   TCs: %s"%(otaus[0],pmodels[npmodels-1],stmopt)
    t1sgain="Tau: %sh Scaled Gain [%%*%%] against: %s   TCs: %s"%(otaus[0],pmodels[npmodels-1],stmopt)
    t1pod="POD [%%] TCs: %s"%(stmopt)
    t1pof="POF [%%] TCs: %s"%(stmopt)
    t1nfrac="N frac [%%] TCs: %s"%(stmopt)

    if(dohomo):
        t1pod="POD [%%] against: %s  TCs: %s"%(pmodels[npmodels-1],stmopt)
        t1pof="POF [%%] against: %s  TCs: %s"%(pmodels[npmodels-1],stmopt)
        t1nfrac="N frac [%%] against: %s  TCs: %s"%(pmodels[npmodels-1],stmopt)
        
    
    for n in range(0,npmodels):

        model=pmodels[n]
        m3=model2m3(model)

        matts=atcf.TrkModeltoBattributes[m3]
        mcol=matts[2]
        mcol=Color2Hex[mcol]
        modColors.append(mcol)
        
        if(verb): print 'model ',m3,matts,mcol
        legLabels.append("%s"%(model))

        rowColors.append(mcol)

        rlstring="%s FE|N"%(model)
        rlstring="%s N"%(model)
        rowLabels.append(rlstring)

        rowLabelsCtAt.append("%s CT/AT|N"%(model))

        rowColorsNfracxy.append(mcol)
        rowLabelsNfracxy.append("%s N%%"%(model))

        gxycol=Color2Hex['usafblue']

        if(n < npmodels-1):
            rowColorsPodxy.append(gxycol)
            rowLabelsPodxy.append("%s N"%(model))

            rowColorsPofxy.append(gxycol)
            rowLabelsPofxy.append("%s N"%(model))

        elif(not(dohomo)):

            rowColorsPodxy.append(gxycol)
            rowLabelsPodxy.append("%s N"%(model))

            rowColorsPofxy.append(gxycol)
            rowLabelsPofxy.append("%s N"%(model))


        if(n < npmodels-1):
            t1mod="%s %s,"%(t1mod,model)
        else:
            t1mod="%s %s"%(t1mod,model)

    yLabels['mfe']='MFE [nm]'
    yLabels['gainxy']='Gain [%]'
    yLabels['sgainxy']='Scaled Gain [%*%]*0.1'
    yLabels['pod']='Prob of Detection [%]'
    yLabels['pof']='Prob of Forecast [%]'
    yLabels['nfrac']='N frac [%]'

    yLims['mfe']=(0,600,50)
    yLims['gainxy']=(-100,100,10)
    yLims['gainxy']=(-50,50,10)
    yLims['sgainxy']=yLims['gainxy']
    
    yLims['pod']=(0,140,10)
    yLims['pof']=(0,140,10)

    ylint=5.0
    ymaxnfrac=float(int(pnsfracmax*100.0/ylint)+1.0)*ylint
    if(ymaxnfrac < 20.0): ymaxnfrac=20.0
    yLims['nfrac']=(0,ymaxnfrac,ylint)

    #
    # gainxy
    #

    for n in range(0,npmodels-1):

        model=pmodels[n]

        m3=model2m3(model)
        matts=atcf.TrkModeltoBattributes[m3]
        mcol=matts[2]
        mcol=Color2Hex[mcol]
        modColors.append(mcol)

        gxycol=Color2Hex['usafblue']
        rowColorsGainxy.append(gxycol)
        rowLabelsGainxy.append("%s [N]"%(model))
        rowColorssGainxy.append(gxycol)
        rowLabelssGainxy.append("%s [N]"%(model))


    t1mfe="%s TCs: %s\n%s Comp N in table"%(t1mod,stmopt,comptype)
    t1ctat="%s TCs: %s\n%s Comp CT/AT|N in table"%(t1mod,stmopt,comptype)
    t1gain="%s\n%s Comp [> 0 better ; < 0 worse]"%(t1gain,comptype)
    t1sgain="%s\n%s Comp [> 0 better ; < 0 worse]"%(t1sgain,comptype)
    t1pod="%s\n%s"%(t1pod,comptype)
    t1pof="%s\n%s Comp"%(t1pof,comptype)
    t1nfrac="%s TCs: %s\n%s Comp"%(t1mod,stmopt,comptype)

    for stmid in vstmids:
        colLabels.append("%s"%(stmid))

    topTitles.append(t1mfe)
    topTitlesCtAt.append(t1ctat)
    topTitlesGainxy.append(t1gain)
    topTitlessGainxy.append(t1sgain)
    topTitlesPodxy.append(t1pod)
    topTitlesPofxy.append(t1pof)
    topTitlesNfracxy.append(t1nfrac)
    
    table['clab']=colLabels
    table['rcol']=rowColors
    table['rlab']=rowLabels
    table['rlabctat']=rowLabelsCtAt
    table['ylab']=yLabels
    table['ylims']=yLims

    table['llab']=legLabels
    table['mfe']=mfe
    table['ctxt']=ctxt
    table['ctxtctat']=ctxtctat
    table['toptitles']=topTitles
    table['toptitlesctat']=topTitlesCtAt
    table['modcolors']=modColors
    
    table['toptitlesgainxy']=topTitlesGainxy
    table['rcolgainxy']=rowColorsGainxy
    table['rlabgainxy']=rowLabelsGainxy
    table['gainxy']=gainxy
    table['cgainxy']=cgainxy
    
    table['toptitlessgainxy']=topTitlessGainxy
    table['rcolsgainxy']=rowColorssGainxy
    table['rlabsgainxy']=rowLabelssGainxy
    table['sgainxy']=sgainxy
    table['csgainxy']=csgainxy
    
    table['toptitlespodxy']=topTitlesPodxy
    table['rcolpodxy']=rowColorsPodxy
    table['rlabpodxy']=rowLabelsPodxy
    table['podxy']=podxy
    table['cpodxy']=cpodxy
    
    table['toptitlespofxy']=topTitlesPofxy
    table['rcolpofxy']=rowColorsPofxy
    table['rlabpofxy']=rowLabelsPofxy
    table['pofxy']=pofxy
    table['cpofxy']=cpofxy
    
    table['toptitlesnfracxy']=topTitlesNfracxy
    table['rcolnfracxy']=rowColorsNfracxy
    table['rlabnfracxy']=rowLabelsNfracxy
    table['nfracxy']=nfracxy
    table['cnfracxy']=cnfracxy
    

    return(rptcards,table,pmodels,vstmids)







def PlotVitalsAllStats(ptype,stattable,xdata,ydata,dohomo,doshow,pltdir,pltfile,verb=0,doxv=0,bargap=0.1,xtype='taus'):
    
    stimec=time.time()
    from pylab import *
    mf.Timer('import pylab: ',stimec)

    stimec=time.time()
    
    plotpaths=[]
 
    nx=len(xdata)
    ny=len(ydata)

    if(ptype == 'gainxy'):
        ny=ny-1
        (ymin,ymax,ylint)=stattable['ylims']['gainxy']
        ylab=stattable['ylab']['gainxy']
        coll=stattable['clab']
        rowl=stattable['rlabgainxy']
        rowc=stattable['rcolgainxy']
        ctxt=stattable['cgainxy']
        t1=stattable['toptitlesgainxy'][0]
        pdata=stattable['gainxy']

        #
        # set tau=0 gainxy to zero
        #
        if(xtype == 'taus'):
            for n in range(0,len(pdata)):
                pdata[n][0]=0.0
                
    elif(ptype == 'sgainxy'):
        ny=ny-1
        (ymin,ymax,ylint)=stattable['ylims']['sgainxy']
        ylab=stattable['ylab']['sgainxy']
        coll=stattable['clab']
        rowl=stattable['rlabsgainxy']
        rowc=stattable['rcolsgainxy']
        ctxt=stattable['csgainxy']
        t1=stattable['toptitlessgainxy'][0]
        pdata=stattable['sgainxy']

    elif(ptype == 'pod'):
        (ymin,ymax,ylint)=stattable['ylims']['pod']
        ylab=stattable['ylab']['pod']
        if(dohomo):   ny=ny-1
        ylab=stattable['ylab']['pod']
        coll=stattable['clab']
        rowl=stattable['rlabpodxy']
        rowc=stattable['rcolpodxy']
        ctxt=stattable['cpodxy']
        t1=stattable['toptitlespodxy'][0]
        pdata=stattable['podxy']


    elif(ptype == 'pof'):
        (ymin,ymax,ylint)=stattable['ylims']['pof']
        ylab=stattable['ylab']['pof']
        if(dohomo):  ny=ny-1
        coll=stattable['clab']
        rowl=stattable['rlabpofxy']
        rowc=stattable['rcolpofxy']
        ctxt=stattable['cpofxy']
        t1=stattable['toptitlespofxy'][0]
        pdata=stattable['pofxy']


    elif(ptype == 'nfrac'):
        (ymin,ymax,ylint)=stattable['ylims']['nfrac']
        ylab=stattable['ylab']['nfrac']
        if(dohomo):  ny=ny-1
        coll=stattable['clab']
        rowl=stattable['rlabnfracxy']
        rowc=stattable['rcolnfracxy']
        ctxt=stattable['cnfracxy']
        t1=stattable['toptitlesnfracxy'][0]
        pdata=stattable['nfracxy']


    elif(mf.find(ptype,'mfe') == 1):
        (ymin,ymax,ylint)=stattable['ylims']['mfe']
        ylab=stattable['ylab']['mfe']
        coll=stattable['clab']
        rowc=stattable['rcol']

        if(ptype == 'mfe'):
            rowl=stattable['rlab']
            ctxt=stattable['ctxt']
            t1=stattable['toptitles'][0]
        elif(ptype == 'mfectat'):
            rowl=stattable['rlabctat']
            ctxt=stattable['ctxtctat']
            t1=stattable['toptitlesctat'][0]

        pdata=stattable['mfe']


    ind = arange(0.0,nx+0.0,1.0)  # the x locations for the groups
    indp5 = arange(0.5,nx+0.5,1.0)  # the x locations for the groups

    width = (1.0-bargap)/float(ny)

    axes([0.125, 0.175, 0.775, 0.700])

    pbars=[]

    for n in range(0,ny):

        pdy=width*n
        py=ind+pdy+bargap*0.5
        pcol=stattable['modcolors'][n]

        if(verb):
            l=0
            for y1 in py:
                if(l == 0): print
                print 'ppppppppppp ',n,l,y1,pdata[n][0],pdy,width,pcol
                l=l+1
        p1 = bar(py, pdata[n], width , color=pcol, yerr=None)
        pbars.append(p1)

    ylabel(ylab)

    xl1=-width
    xl1=0.0
    xl2=len(ind)
    yl1=ymin
    yl2=ymax

    xlim(xl1,xl2)
    ylim(yl1,yl2)

    ticsy = arange(ymin,ymax+1,ylint)     
    yticks(ticsy)
    

    legcols=[]
    leglabs=[]

    for i in range(0,ny):
        leglabs.append(stattable['llab'][i])
        legcols.append(pbars[i][0])

    rc=legend( legcols, leglabs, shadow=True, loc=0, markerscale = 0.4 )

    dotable=1

    if(dotable):

        xticks([])

        if(verb):
            print 'ctxt ',len(ctxt),ctxt
            print 'rowl ',rowl
            print 'rowc ',rowc
            print 'coll ',coll

        rc = table(cellText=ctxt,loc='bottom',
                   rowLabels=rowl,rowColours=rowc,
                   colLabels=coll)

        rc.set_fontsize(8)
        rc.scale(1.0,0.8)

    else:
        coll=stattable['clab']
        xticks(indp5, coll )


    #
    # draw 0 line
    #

    (tdocolor,Color2Hex)=TCtdos.TdoColors()
    if(ptype == 'gainxy' or ptype == 'sgainxy'):
        lcol=Color2Hex['teal']
        x=arange(0.0,nx+1.0,1.0)
        y=x*0.0
        plot(x,y,color=lcol,linewidth=2.00)
    elif(ptype == 'pod' or ptype == 'pof'):
        lcol=Color2Hex['teal']
        x=arange(0.0,nx+1.0,1.0)
        y=x*0.0+100.0
        plot(x,y,color=lcol,linewidth=2.00)

    ylim(ymin,ymax)

    #
    # do top title
    #
    title(t1,size=12)

    pngpath="%s/%s.png"%(pltdir,pltfile)
    plotpaths.append(pngpath)
    savefig(pngpath,orientation='landscape')

    mf.Timer('plot1a: ',stimec)

    if(doxv):
        cmd="xv %s"%(pngpath)
        mf.runcmd(cmd)

    epspath="%s/%s.eps"%(pltdir,pltfile)
    savefig(epspath,orientation='landscape')
    plotpaths.append(epspath)

    if(doshow): show()
    
    clf()

    return(plotpaths)

    
def GetBtCq(dtg,fcs):
    
    try:
        bdir=fcs[dtg,'mot'][0]
        bspd=fcs[dtg,'mot'][1]
        blat=fcs[dtg,'bt'][0]
        blon=fcs[dtg,'bt'][1]
        bvmax=fcs[dtg,'bt'][2]

        cqlat=fcs[dtg,'cq'][0]
        cqlon=fcs[dtg,'cq'][1]
        cqvmax=fcs[dtg,'cq'][2]
        cqdir=fcs[dtg,'cq'][3]
        cqspd=fcs[dtg,'cq'][4]

    except:
        bdir=-999.9
        bspd=-99.9
        blat=-99.9
        bvmax=-99.9
        blon=-999.9
        cqlat=-99.9
        cqlon=-999.9
        cqvmax=-99.9
        cqdir=-999.9
        cqspd=-99.9
        
    return(blat,blon,cqlat,cqlon,bdir,bspd,bvmax,cqdir,cqspd,cqvmax)

def GetTcVitalsHomoHash(stmid,year,models,resetcache=0,verb=0):

    pyfile="Vitals_%s_%s_HomoCache.py"%(stmid,year)
    hdir="%s/%s"%(TC.VdeckDir,year)
    pypath="%s/%s"%(hdir,pyfile)

    if(resetcache and os.path.exists(pypath)):
        cmd="rm  %s"%(pypath)
        mf.runcmd(cmd)

    #
    # defaults to drive VdeckVitlas
    #
    stmopt="%s.%s"%(stmid,year)
    tdoopt=None
    ruleopt=None
    phr=None
    
    #
    # if homocache file there...
    #
    if(os.path.exists(pypath)):
        #print 'YYYYYPPPPP: path there...',pypath
        #
        # check if already done...
        #
        for modopt in models:
            vdlist='VitalsDone'
            vd=GetTCVitalsDoneList(pypath,vdlist)
            if(vd.count(modopt) == 0):
                #print 'not done, create and append...',

                (btgcards,fcgcards,
                 vpycards,scards,gsf1,
                 dfepycards,btpycards)=VdeckVitals(stmopt,modopt,tdoopt,ruleopt,phr,verb)

                if(vpycards != None):
                    vpycards.append("VitalsDone.append('%s')"%(modopt))
                    AppendList2File(pypath,vpycards)
                    AppendList2File(pypath,dfepycards)
            #else:
            #    print 'DONE already, do NOT append'

    #
    # create homocache
    #
    else:

        print 'NNNNNPPPPP: path not there...',pypath,modopt
        allpy=[]
        pycard="""
Vitals = {}
VitalsDone=[]
DfeVitals={}

"""
        allpy.append(pycard)
        for modopt in models:

            (btgcards,fcgcards,
             vpycards,scards,gsf1,
             dfepycards,btpycards)=VdeckVitals(stmopt,modopt,tdoopt,ruleopt,phr,verb)
            
            allpy=allpy+vpycards+dfepycards
            allpy.append("VitalsDone.append('%s')"%(modopt))
            
        sys.path.append(hdir)
        w2.WriteList2File(pypath,allpy)

    #
    #
    #
    try:
        sys.path.append(hdir)
        (vfile,ext)=os.path.splitext(pyfile)
        impcmd="import %s as vtc"%(vfile)
        exec(impcmd)
        if(verb):
            print "Opening TcVitals: %s/%s"%(hdir,pyfile)
    except:
        vtc=None
        if(verb):
            print "FAILED to TcVitals: %s/%s"%(hdir,pyfile)

    return(vtc)


def GetTcVitalsHash(stmid,year,vtype='all',verb=1):

    hdir="%s/%s"%(TC.VdeckDir,year)
    sys.path.append(hdir)
    vfile="Vitals_%s_%s_%s"%(stmid,year,vtype)
    try:
        impcmd="import %s as vtc"%(vfile)
        exec(impcmd)
        if(verb):
            print "Opening TcVitals: %s/%s"%(hdir,vfile)
    except:
        vtc=None
        if(verb):
            print "FAILED to TcVitals: %s/%s"%(hdir,vfile)

    return(vtc)



def GetTCVitalsDoneList(pypath,list):

    (dir,file)=os.path.split(pypath)
    (py,ext)=os.path.splitext(file)
    
    sys.path.append(dir)

    try:
        impcmd="from %s import %s"%(py,list)
        exec(impcmd)
    except:
        print "IIII failed to import list: %s from: %s"%(list,file)

    cmd="olist=copy.copy(%s)"%(list)
    exec(cmd)
    return(olist)


def GetTcVdeckHash(stmid,model,verb=0,dtglatest='2008022920',ropt=''):

    (stmid,year)=stmid.split('.')
    b1id=stmid[2]
    stmnum=stmid[0:2]
    b2id=TC.Basin1toBasin2[b1id].lower()
    
    hdir="%s/%s"%(TC.VdeckDir,year)
    sys.path.append(hdir)

    vfile="v%s%s%s_%s"%(b2id,stmnum,year,model)
    vpath="%s/%s.py"%(hdir,vfile)
    if(verb): print vpath

    if(os.path.exists(vpath)):

        timei=os.path.getctime(vpath)
        ltimei=time.localtime(timei)
        gtimei=time.gmtime(timei)
        gdtimei=time.strftime("%Y%m%d%H%M",gtimei)

        dtgmn=dtglatest +'00'
        (isphr,modelopt)=TC.IsModelPhr(model)
        
        phr=mf.dtgmndiff(gdtimei,dtgmn)
        if(phr > 0):
            mf.ChangeDir(TC.BaseDirPrcTcDat)
            bopt=''
            if(isphr):  bopt='-B'
            cmd="w2.tc.vdeck.py %s.%s  %s %s"%(stmid,year,modelopt,bopt)
            mf.runcmd(cmd,ropt)
    else:

        ###print 'pppppppppppppppppppnnnnnnnnnnnnnnneeeeeeeeeeeeeeeee ',phr
        mf.ChangeDir(BaseDirPrcTcDat)
        bopt=''
        (isphr,modelopt)=IsModelPhr(model)
        print model,modelopt,isphr
        if(isphr): bopt='-B'
        cmd="w2.tc.vdeck.py %s.%s %s %s"%(stmid,year,modelopt,bopt)
        mf.runcmd(cmd,ropt)

    
    try:
        impcmd="import %s as VD"%(vfile)
        exec(impcmd)
        if(verb):
            print "Opening vdecks: %s/%s"%(hdir,vfile)
    except:
        VD=None
        if(verb >= 0):
            print "FAILED to TcVitals: %s/%s.py"%(hdir,vfile)

    return(VD)

def Modopt2Models(modopt,phropt=None):

    mtt1d=modopt.split('.')
    mtt1p=modopt.split(',')
    if(mtt1d != None): mtt1=mtt1d
    if(mtt1p != None): mtt1=mtt1p
    mtt2=modopt.split('_')

    dohomo=0
    if(len(mtt1) > 1):
        dohomo=1
        if(phropt != None):
            models=[]
            for mtt in mtt1:
                models.append("%s%02d"%(mtt,int(phropt)))
        else:
            models=mtt1

    if(len(mtt2) > 1):
        
        if(phropt != None):
            models=[]
            for mtt in mtt2:
                models.append("%s%02d"%(mtt,int(phropt)))
        else:
            models=mtt2

    if(len(mtt1) == 1 and len(mtt2) == 1):
        models=[modopt]
        

    return(models,dohomo)


def Modopt2OpsModels(stmid,modopt,phr=None,bcopt=None):

    models=[]
    
    if(modopt == 'ops'):
        models=models+Modopt2OpsModels(stmid,'obase')+Modopt2OpsModels(stmid,'omod5')
        return(models)
    elif(modopt == 'all'):
        models=models+Modopt2OpsModels(stmid,'base')+Modopt2OpsModels(stmid,'mod5')
        reutrn(models)

    lenmods=len(modopt.split('.'))


    if(
        lenmods > 1 or
        mf.find(modopt,'top5') or
        (modopt == 'mod5') or (modopt == 'omod5') or
        (modopt == 'base') or (modopt == 'obase') or
        (modopt == 'models') or
        (phr != None and mf.find(phr,'all')) or
        (bcopt == 'all')
        ):

        modelsatcf=atcf.modelsadeck

        if(phr != None and mf.find(phr,'all') ):
            phrs=[0,1,6,7,12,13]
        elif(phr == None):
            phrs=[phr]
        else:
            phrs=[int(phr)]

        tt=stmid.split('.')
        bid=tt[0][2:3]
        iyear=int(tt[1])

        if(modopt == 'all'):

            models=atcf.AllModelsAtcfBasin(bid)+atcf.AllModelsLocalBasin(bid)
            models.sort()

        elif(modopt == 'top5'):
            models=atcf.Top5ModelsAtcfBasin(bid)

        elif(modopt == 'mod5' or modopt == 'omod5'):
            models=atcf.Mod5ModelsAtcfBasin(bid,iyear,modopt)

        elif(modopt == 'base' or modopt == 'obase'):
            models=atcf.BaseAidsAtcfBasin(bid,iyear,modopt)

        elif(modopt == 'all.local'):
            models=atcf.AllModelsLocalBasin(bid)

    elif(lenmods > 1):
        models=modopt.split('.')

    else:
        models=[modopt]


    return(models)



def getInvFtcards(inventory,imodel,amodel,stm3id,year,dtg,phr,verb=0,quiet=0):
    
    try:
        inv=inventory[dtg]
    except:
        inv=None

    ifctype=atcf.ModelNametoAdeckType[imodel]


    if(phr != None or ifctype == 2):
        w2ftcards=TC.LoadW2TcFcCards(stm3id,year,phr,imodel,amodel)
        (ftcards,ftmfcards,ftype)=TC.GetTcFcCardsW2(dtg,amodel,phr,w2ftcards)
        oftype=2
    else:
        (ftcards,ftmfcards,ftype)=TC.GetTcFcCards(dtg,imodel,ifctype,stm3id,verb=verb,useallstms=0,quiet=quiet)
        oftype=1

    if(ftcards == None):
        nftcards=0
    else:
        nftcards=len(ftcards)

    return(inv,nftcards,ftcards,ifctype,ftype,oftype)


#
# find vdeck inventory path and calculate age
#
def HowOldIsVdeckInventory(stmid,imodel,phr,verb=1):

    amodel=atcf.ModelAdeckNametoName[imodel]
    filemodel=imodel
    if(phr != None):
        filemodel="%s%02d"%(imodel,int(phr))

    stm3id=stmid.split('.')[0]
    year=stmid.split('.')[1]
    vddir=TC.BaseDirDataTc+"/vdeck/%s/%s"%(year,filemodel)

    invpypofile="vdkinv.%s.%s.pyp"%(stmid,filemodel)
    invpypopath="%s/%s"%(vddir,invpypofile)
    try:
        invage=-w2.PathModifyTimeCurdiff(invpypopath)
    except:
        invage=99999.9

    return(invage)




def IsVdeckup2date(stmid,imodel,phr,verb=1):

    curdtg=mf.dtg()
    rc=0

    mdcards=TC.findtc(stmid,dofilt9x=0)
    if(len(mdcards)== 0):
        return(rc)

    amodel=atcf.ModelAdeckNametoName[imodel]
    filemodel=imodel
    if(phr != None):
        filemodel="%s%02d"%(imodel,int(phr))

    stm3id=stmid.split('.')[0]
    year=stmid.split('.')[1]
    vddir=TC.BaseDirDataTc+"/vdeck/%s/%s"%(year,filemodel)

    dtgs=mdcards.keys()
    dtgs.sort()
    edtg=dtgs[-1]
    try:
        bdtg=dtgs[-3]
    except:
        try:
            bdtg=dtgs[-2]
        except:
            bdtg=dtgs[-1]
    
                    
    lastdtgs=mf.dtgrange(edtg,bdtg,-6)

    invpypofile="vdkinv.%s.%s.pyp"%(stmid,filemodel)
    invpypopath="%s/%s"%(vddir,invpypofile)

    
    if(verb):
        print 'WWWW opening inventory: ',invpypopath
    try:
        OPINV=open(invpypopath)
        chkinv=1
    except:
        chkinv=0
        return(rc)


    if(verb>0):
        print 'cccccc ',invpypopath,chkinv,mf.GetPathSiz(invpypopath)

    if(chkinv and (mf.GetPathSiz(invpypopath) > 0) ):

        (inventory)=pickle.load(OPINV)

        #
        # cycle through previous 12-h of inventory and adecks -- for late trackers
        #
        
        rc=0

        ofe=-999.9
        
        for lastdtg in lastdtgs:

            olastdtg=lastdtg
            
            (inv,nftcards,ftcards,ifctype,ftype,oftype)=getInvFtcards(inventory,imodel,amodel,stm3id,year,lastdtg,phr)
            dtlastdtg=mf.dtgdiff(curdtg,lastdtg)
            ####print 'ffffff oftype',oftype,lastdtg,curdtg,dtlastdtg,'inv: ',inv,' phr:',phr,' nftcards: ',nftcards
            #
            # case 0 -- time interp not run yet
            #
            if(phr != None and inv == None and dtlastdtg == 0.0 and oftype == 2):
                print 'wwwwwwwwwwwwwww will force update because phr not done yet...'
                print 'ffffff oftype',oftype,lastdtg,curdtg,nftcards,inv,dtlastdtg,phr
                return(rc)
            
            if(verb>0):
                oftcard=''
                if(nftcards > 0):
                    oftcard=ftcards[0]
                print 'llllllllllllllllllll ',olastdtg,inv,nftcards,oftcard

            #
            # case 1 no inventory, but a forecast...break out
            #
            if(nftcards > 0 and inv == None):
                break

            if(inv != None):
                (fe,fetime)=inv
                if(verb>0):
                    print 'fffffff11 ',imodel,ifctype,nftcards,ftype,fe
                if(fe >= 0.0 or nftcards == 0):
                    ofe=fe
                    olastdtg=lastdtg
                    if(verb>0):
                        print 'VVVV vdeck up to date: ',imodel,lastdtg,fe,nftcards,ftype
                    rc=1
            #
            # case 1a -- vmaxonly model
            #
                elif(fe == -777.7 and nftcards >= 0):
                    ofe=fe
                    olastdtg=lastdtg
                    if(verb>0):
                        print 'VVVV vdeck up to date: ',imodel,lastdtg,fe,nftcards,ftype
                    rc=1
            #
            # case 2 vdeck had a noload (model was suppose to make a forecast, but there are ntfctards
            #
                elif(fe == -911.9 and nftcards > 0):
                    rc=0
                    break
                
                if(verb>0):
                    print 'rrrrrrrrrrrrrrrrrrrrrrrrr ',rc,lastdtg
                    print

            if(rc):
                break

    if(rc):
        print 'VVVV vdeck up to date... model: %6s  lastdtg: %s  fe: %6.1f'%(imodel,lastdtg,fe)

    OPINV.close()
    return(rc)

