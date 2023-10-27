from TCdiag import *
from tcCL import TcPrcMonitor
from M import *
from tcbase import *
import numpy as np
import matplotlib.pyplot as plot
import matplotlib.dates as datespy
from datetime import datetime

class stormAnl(MFbase):

    """ class for analyzing the diag card output """

    def __init__(self,
                 cards):

        for i in range(len(cards)):
            cards[i]=cards[i].rstrip() # strips the newline character out of the strings

        label=cards[0]
        data=cards[1:-2]
        diags={}
        dtgs=[]
        i=0
        rmiss=-999.

# puts the data into a dicionary called diags
        for dat in data:
            line=dat.split()
            dtgs.append(line[1])
            diags[dtgs[i]]=line
            i=i+1

# creates the dictionary by variable containing the time series of that variable
        varss=['stmid','dtg','btwnd','mdwnd','shrmag','tpw','vtan','dvg','vort','rh700','rh500','sst','ssta','cpsb','cpsvtl','cpsvtu']
        varlablong=['Storm ID', 'Date/Time Group', 'Best Track Wind (kt)','Model Wind (kt)','Magnitude of Shear (kt)','Total Precipitable Water (mm)','850mb Tangential Wind (kt)','200mb Divergence (s^-1)','850mb Vorticity (s^-1)','700mb Relative Humidity (%)','500mb Relative Humidity (%)','Sea Surface Temperature (K)','Sea Surface Temperature Anomaly (K)','Cyclone Phase: Baroclinicity','Cyclone Lower Trop Thermal Wind','Cyclone Upper Trop Thermal Wind']
        
        tmseries={}
        ptcmean={}
        count={}
        datadictionary={}

        for var in varss:
            ptcmean[var]=0.
            count[var]=0
            for dtg in dtgs:
                if varss.index(var)>1:
                    if float(diags[dtg][varss.index(var)])!=rmiss and float(diags[dtg][varss.index(var)])!=999.9 and float(diags[dtg][varss.index(var)])!=9999.:
                        datadictionary[dtg,var]=float(diags[dtg][varss.index(var)])
                        ptcmean[var]=ptcmean[var]+datadictionary[dtg,var]
                        count[var]=count[var]+1
                    else:
                        datadictionary[dtg,var]=None
                else:
                    datadictionary[dtg,var]=diags[dtg][varss.index(var)]

        for j in range(len(varss)):
            lst=[]
            for dtg in dtgs:
                if j > 1:
                    if float(diags[dtg][j])!=rmiss and float(diags[dtg][j])!=999.9 and float(diags[dtg][j])!=9999:

                        if datadictionary[dtg,'stmid'][2] == 'S' and (j == 6 or j == 8):
                            lst.append(float(diags[dtg][j])*(-1))
                        else:
                            lst.append(float(diags[dtg][j]))
                    else:
                        lst.append(None)
                else:
                    lst.append(diags[dtg][j])
                    #                lst.append(diags[dtg][j])
            #print 'SSS:',varss[j],lst
            tmseries[varss[j]]=lst
            
        for var in varss:
            if count[var]>0:
                ptcmean[var]=ptcmean[var]/count[var]
            else:
                ptcmean[var]=rmiss

# gets the time of development for the system, or death time
        devtime=cards[-1].split()[1]
        idev=dtgs.index(devtime)

# find if the storm developed
        pTCdev=cards[-2].split()[1]
        self.pTCdev=int(pTCdev)


# get the storm id
        stmid=tmseries['stmid'][-1]

        self.cards=cards
        self.tmseries=tmseries
        self.diags=diags
        self.devtime=devtime
        self.idev=idev
        self.dtgs=dtgs
        self.stmid=stmid
        self.label=label
        self.vars=varss
        self.longvar=varlablong
        self.basin={'W':'West Pacific', 'E': 'East Pacific', 'C': 'Central Pacific', 'L': 'Atlantic','S': 'Southern Hemisphere'}
        self.ptcmean=ptcmean
        self.year=dtgs[-1][0:4]

# set default mins and maxes for options
        maxes={}
        mins={}
        
        mins['btwnd']=0.
        maxes['btwnd']=50.

        mins['mdwnd']=0.
        maxes['mdwnd']=50.
        
        mins['shrmag']=0.
        maxes['shrmag']=50.

        mins['tpw']=45.
        maxes['tpw']=80.

        mins['vtan']=-25
        maxes['vtan']=175

        mins['dvg']=-80
        maxes['dvg']=200

        mins['vort']=-50
        maxes['vort']=250

        mins['rh700']=30
        maxes['rh700']=90

        mins['rh500']=30
        maxes['rh500']=90

        mins['sst']=25
        maxes['sst']=32

        mins['ssta']=-0.3
        maxes['ssta']=2.0

        mins['cpsb']=-12
        maxes['cpsb']=20

        mins['cpsvtl']=-75
        maxes['cpsvtl']=150

        mins['cpsvtu']=-150
        maxes['cpsvtu']=100

        self.mins=mins

        self.maxes=maxes

    def plotVar(self,var,dosmooth=0):
        if self.pTCdev == 1:
            col='g-'
        else:
            col='r-'

        idev=self.idev

        self.xlabel='Hours before Genesis/Dissipation'
        self.ylabel=self.longvar[self.vars.index(var)]
        self.title=self.basin[self.stmid[2]]

        xs=np.arange((idev)*6,-1,-6)
        ys=np.array(self.tmseries[var][0:idev+1]).astype(np.double)
        if(dosmooth):   ys=smooth(ys)
            
        mask=np.isfinite(ys)

        plot.plot(xs[mask],ys[mask],col,linewidth=1.0)
        
        ax=plot.gca()
        self.ax=ax


    def plotScaledVar(self,var):
        if self.pTCdev == 1:
            col='g-'
        else:
            col='r-'

        self.xlabel='Portion of pTC Lifetime'
        self.ylabel=self.longvar[self.vars.index(var)]
        self.title=self.basin[self.stmid[2]]

        rdev=float(self.idev)
        if(rdev<1):
            rdev=1

        print '*****',rdev


        ys=np.array(self.tmseries[var][0:self.idev+1]).astype(np.double)
        xs=np.arange(0,1.5,(1/rdev))
        print xs

        mask=np.isfinite(ys)
        
        plot.plot(xs[mask],ys[mask],col,linewidth=1.0)
        ax=plot.gca()
        self.ax=ax


    def plotDTG(self,var):
        dates=[]
        for dtg in self.dtgs:
            year=int(dtg[:4])
            month=int(dtg[4:6])
            day=int(dtg[6:8])
            hour=int(dtg[8:])
            print dtg
            print year, month, day, hour
            date=datetime(year,month,day,hour)
            dates.append(date)

        dates=datespy.date2num(dates)
        print dates

        plot.plot_date(dates,self.tmseries[var],'b-')

        ax=plot.gca()
        self.ax=ax
        self.xlabel='Date'
        self.ylabel=self.longvar[self.vars.index(var)]
        self.title=self.basin[self.stmid[2]]
    
    def getIdev(self):
        return self.idev

    def setXaxis(self,xmin,xmax):
        self.ax.set_xlim(xmin,xmax)
        self.ax.set_xticks(range(0,xmax,24))
        self.ax.set_xticks(range(0,xmax,6),minor=True)
    
    def setYaxis(self,ymin,ymax):
        self.ax.set_ylim(ymin,ymax)
        
    def labelPlot(self):
        plot.xlabel(self.xlabel)
        plot.ylabel(self.ylabel)
        plot.title(self.year+' '+self.title+' pTCs Before Genesis')

    def showPlot(self):
        plot.show()

    def printCard(self):
        print '********************************************************'
        for card in self.cards:
            print card

    def getMeanLabel(self):
        meanlabel="\nMeanFields:\n    SYSTEM.ID   START.TIME      DEVELOP" + self.label[24:]
        return(meanlabel)

    def getPtcMean(self):
        meanstring="{0:>13}{1:>13}{2:>13}".format(self.stmid,self.dtgs[0],self.devtime)
        for var in self.vars:
            if var != 'stmid' and var != 'dtg':
                meanstring=meanstring+"{0:>12}".format(round(self.ptcmean[var],2))
        return(meanstring)

    def getXaxis(self):
        return(plot.gca().get_xlim())

    def getYaxis(self):
        return(plot.gca().get_ylim())

    def getMin(self,var):
        dat=[]

        for v in range(self.idev+1):
            dat.append(self.tmseries[var][v])

        return(min(dat))

    def getMax(self,var):
        dat=[]

        for v in range(self.idev+1):
            dat.append(self.tmseries[var][v])

        return(max(dat))

class TCdiag9X0X(MFbase):
 
    """analyze tau 0 diagfile and output one card per storm/dtg
"""
    def __init__(self,
                 dtg,
                 model,
                 stmid,
                 status,
                 lsdiagPath,
                 tGa,
                 verb,
                 ):

        self.dtg=dtg
        self.model=model
        self.stmid=status.split()[1]
        rmiss=-999.
        self.rmiss=rmiss
        dats=[]

        if (lsdiagPath == None):

            cpsB=rmiss
            cpsVTl=rmiss
            cpsVTu=rmiss
                
            vmax=rmiss
            vtan850=rmiss
            tpw=rmiss
            shrmag=rmiss
            dvg200=rmiss
            vrt850=rmiss
            
            r700=rmiss
            r500=rmiss
            sst=rmiss
            ssta=rmiss
            wndBT=rmiss

        else:            
            tGa.parseDiag(stmid,lsdiagpath=lsdiagPath)
            
            cData=tGa.customData
            cLabels=tGa.customLabels
            
            sData=tGa.stmData
            sLabels=tGa.stmLabels
            
            sndData=tGa.sndData
            sndLabels=tGa.sndLabels

            wndBT=status.split()[2]

            otau=0
            cpsB=cData[otau,11]
            cpsVTl=cData[otau,12]
            cpsVTu=cData[otau,13]
                
            vmax=sData[otau,3]
            vtan850=sData[otau,14]
            tpw=sData[otau,12]
            shrmag=sData[otau,6]
            dvg200=sData[otau,16]
            vrt850=sData[otau,15]
            lat=sData[otau,1]
            lon=sData[otau,2]

            r700=sndData[otau,2,5]
            r500=sndData[otau,2,6]

            sst=float(sData[otau,10])/10
            ssta=float(cData[otau,5])/10


            if(verb):
                cLndx=cLabels.keys()
                cLndx.sort()
                
                sLndx=sLabels.keys()
                sLndx.sort()
                for cL in cLndx:
                    print 'CCC',cL,cLabels[cL],cData[otau,cL]
                    
                    for sL in sLndx:
                        print 'SSS',sL,sLabels[sL],sData[otau,sL]
                        
                        print 'CPS: ',cpsB,cpsVTl,cpsVTu
                        print 'Stm: ',vmax,vtan850
                        tGa.ls()

        dats.append(self.stmid)
        dats.append(dtg)
        dats.append(wndBT)
        dats.append(vmax)
        dats.append(shrmag)
        dats.append(tpw)
        dats.append(vtan850)
        dats.append(dvg200)
        dats.append(vrt850)
        dats.append(r700)
        dats.append(r500)
        dats.append(sst)
        dats.append(ssta)
        dats.append(cpsB)
        dats.append(cpsVTl)
        dats.append(cpsVTu)
        
        self.dats=dats
        
    def getDiagCard(self):

        """ prints out the card with all of the wanted variables for analysis purposes. The flag shows if the tcdiag file ran, 1 for yes, 0 for no. prints out rmiss if tcdiag didn't run """

        # card="{0:>12}{1:>12}{2:>12}{3:>12}{4:>12}{5:>12}{6:>12}{7:>12}{8:>12}{9:>12}{10:>12}{11:>12}{12:>12}{13:>12}{14:>12}{15:>12}".format(self.stmid,self.dtg,self.wndBT,self.vmax,self.shrmag,self.tpw,self.vtan850,self.dvg200,self.vrt850,self.r700,self.r500,self.sst,self.ssta,self.cpsB,self.cpsVTl,self.cpsVTu)
        
        card=""

        for l in range(len(self.dats)):
            card=card+"{0:>12}".format(self.dats[l])

        return(card)

class Labels():
    """Some methods allowing for the printing of labels for card output in the TCdiag"""

    def getLabel(self):
        cardlabel="   SYSTEM ID   DATE/TIME   BTWIND(KT)  MAXWND(KT)  SHRMAG(KT)     TPW(MM) VTAN850(KT)  200DVG(/S)  850VRT(/S)     RH700MB     RH500MB      SST(K)  SSTANOM(C)       CPSB      CPSVTL      CPSVTU"
        self.cardlabel=cardlabel
        return(cardlabel)

    def getMeanLabel(self):
        meanlabel="\nMeanFields:\n    SYSTEM.ID   START.TIME      DEVELOP" + self.cardlabel[24:]
        return(meanlabel)


class stmlife(MFbase):
    """ includes several methods that track diagnosics of the storm throughout its lifetime """
    def __init__(self,model,stmid,dtgs,
                 tD,
                 status,
                 lspaths,
                 pTCdev,
                 verb=0,
                 ):

        self.starttime=dtgs[0]
        self.endtime=dtgs[-1]

        self.devtime=None #***************************

        if pTCdev == 1:
            self.devtime=self.endtime

        self.model=model
        self.dtgs=dtgs
        self.stmid=stmid
        self.tD=tD
        self.lspaths=lspaths
        self.rmiss=-999
        self.pTCdev=pTCdev
        self.numvars=14

        label=Labels()
        self.label=label

        count=[]
        cards={}
        ptcmean=[]



        for i in range(self.numvars):
            ptcmean.append(0.0)
            count.append(0)

        for dtg in self.dtgs:

            lsdiagPaths=lspaths[stmid,dtg][2]

            if(len(lsdiagPaths) == 0):
                lsdiagPath=None
            else:
                lsdiagPath=lsdiagPaths[-1]

            tGa=TcDiagAnl(dtg,model,stmids=[stmid],tD=tD,verb=verb) 
            tGa.tD=tD
            tG9=TCdiag9X0X(dtg,model,stmid,status[dtg],lsdiagPath,tGa,verb=verb)
            card=tG9.getDiagCard()
            cards[dtg]=card

            tt=card.split()
            sid=getStmParams(tt[0],convert9x=1)[-1]

            if int(sid[:2])>=90:
                for i in range(self.numvars):
                    if float(tt[i+2]) != self.rmiss and float(tt[i+2]) != 999.9:
                        ptcmean[i]=ptcmean[i]+float(tt[i+2])
                        count[i]=count[i]+1
            elif self.devtime == self.endtime:
                self.devtime=dtg

        for i in range(self.numvars):
            if count[i] > 0:
                ptcmean[i]=ptcmean[i]/count[i]
            else:
                ptcmean[i]=self.rmiss

        self.ptcmean=ptcmean

        self.diagcards=cards

    def printCards(self):

        print self.label.getLabel()

        for dtg in self.dtgs:
            print self.diagcards[dtg]

    def printPtcMean(self):
        print self.label.getMeanLabel()
        print "{0:>13}{1:>13}{2:>13}".format(self.stmid,self.starttime,self.devtime),
        for i in range(self.numvars):
            print "{0:>11}".format(round(self.ptcmean[i],2)),
        print '\n'

    def toFile(self,path):
        f=open(path,'w')
        f.write(self.label.getLabel()+'\n')
        for dtg in self.dtgs:
            f.write(self.diagcards[dtg]+'\n')
        f.write('Developed: '+str(self.pTCdev)+'\n')
        if self.pTCdev == 1:
            f.write('At: '+self.devtime)
        else:
            f.write('Dissipated: '+self.endtime)
    def getStart(self):
        return self.starttime

    def getDevelopDeath(self):
        return self.devtime






#Old class here so that old versions of the code still work
class TCdiag9X(MFbase):
 
    """analyze tau 0 diagfile and output one card per storm/dtg
"""
    def __init__(self,
                 dtg,
                 model,
                 stmid,
                 tGa,
                 verb):

        self.dtg=dtg
        self.model=model
        self.stmid=stmid

#        print 'oooooooooooo',Dtstmids,dtg,fstmid,lsdiagPath
        (otstmids,olsdiagPaths)=tGa.getLsdiagPathsStmids(model)
#        stmid=getStmParams(stmid,convert9x=1)[-1]
            
        lsdiagPath=olsdiagPaths[stmid]
            #        tGa.lsDiag(ostmid,lsdiagpath=lsdiagPath)
        tGa.parseDiag(stmid,lsdiagpath=lsdiagPath)
        
            #        tGa.ls()
        
        cData=tGa.customData
        cLabels=tGa.customLabels
        
        sData=tGa.stmData
        sLabels=tGa.stmLabels
        
        
        cLndx=cLabels.keys()
        cLndx.sort()
        
        sLndx=sLabels.keys()
        sLndx.sort()
        
        otau=0
        cpsB=cData[otau,11]
        cpsVTl=cData[otau,12]
        cpsVTu=cData[otau,13]
        
        vmax=sData[otau,3]
        vtan850=sData[otau,14]
        tpw=sData[otau,12]
        shrmag=sData[otau,6]
        dvg200=sData[otau,16]
        vrt850=sData[otau,15]
        
            
        if(verb):
            for cL in cLndx:
                print 'CCC',cL,cLabels[cL],cData[otau,cL]
                
                for sL in sLndx:
                    print 'SSS',sL,sLabels[sL],sData[otau,sL]
                    
                    print 'CPS: ',cpsB,cpsVTl,cpsVTu
                    print 'Stm: ',vmax,vtan850
                    tGa.ls()

        # else:
        #     rmiss=-999
        #     cpsB=rmiss
        #     cpsVTl=rmiss
        #     cpsVTu=rmiss
                
        #     vmax=rmiss
        #     vtan850=rmiss
        #     tpw=47
        #     shrmag=rmiss
        #     dvg200=rmiss
        #     vrt850=rmiss

        self.stmid=stmid
            
        self.cpsB=cpsB
        self.cpsVTl=cpsVTl
        self.cpsVTu=cpsVTu
        
        self.vmax=vmax
        self.vtan850=vtan850
        self.tpw=tpw
        self.shrmag=shrmag
        self.dvg200=dvg200
        self.vrt850=vrt850

#        rc=(cpsB,cpsVTl)

#        return(rc)
        
        
    def getDiagCard(self, flag):

        """ prints out the card with all of the wanted variables for analysis purposes. The flag shows if the tcdiag file ran, 1 for yes, 0 for no. prints out rmiss if tcdiag didn't run """

        card="{0:>12}{1:>12}{2:>12}{3:>12}{4:>12}{5:>12}{6:>12}{7:>12}{8:>12}{9:>12}{10:>12}".format(self.stmid,self.dtg,self.vmax,self.shrmag,self.tpw,self.vtan850,self.dvg200,self.vrt850,self.cpsB,self.cpsVTl,self.cpsVTu)
        
        return(card)

