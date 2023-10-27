# --- new fim

from WxMAP2 import Model,MFutils,mf

class FIM(Model,MFutils):


    def __init__(self,stdoutPath,
                 override=0,
                 verb=0,
                 ):

        self.stdoutPath=stdoutPath
        self.override=override
        self.verb=verb

        self.ParseStdOut()


    def ParseStdOut(self):

        # precip - total/nonconv/conv=  0.0000000E+00  0.0000000E+00  0.0000000E+00
        # Global 3D mass          =  5.1274939E+18  at time step=           1
        # Global 3D water vapor   =  1.3496351E+16  at time step=           1
        # Global 3D cloud water   =  3.5297962E+13  at time step=           1
        # Global integ acc precip =  6.9420607E+12  at time step=           1
        # Global integ evaporation=  6.7022252E+12  at time step=           1


        totalRuntime=-999.

        rundate=None
        rundtg=None
        timestep=None
        timestepunits=None
        Ntimesteps=None
        dtau=None
        dtauunits=None

        modtimers=[]

        gwnoise={}
        gpr={}
        gprc={}
        gprl={}
        gmass={}
        gh2o={}
        gclh2o={}
        gpraccum={}
        gevap={}

        cards=[]
        if(self.ChkPath(self.stdoutPath)):
            cards=open(self.stdoutPath).readlines()

        if(len(cards) == 0):
            self.stdout=None
            del self.tStdOutPath
            return


        ntimer=0
        for n in range(0,len(cards)):

            card=cards[n][:-1]

            if(mf.find(card,'Timeout during client startup')):
                print 'WWWWWWWWWWWWWWWWWWW Timeout in stdout'

            if(mf.find(card,'(pvsurf)')): 
                continue

            if(mf.find(card,'DATE-TIME: ')):
                rundate=card[12:-1].strip()
                if(self.verb): print 'TTTTT rundate',rundate,'ddd'

                #Default time step:                         101 seconds
                #Time step reduced to                        90 seconds


            if(mf.find(card,'Length of time step:')):

                tt=card.split(':')
                ltt=len(tt)
                tt=tt[ltt-1].split()
                timestep=float(tt[0])
                timestepunits=tt[1]
                if(self.verb): print 'TTTTTTTTT ',timestep,timestepunits

            if(mf.find(card,'Time step reduced to')):

                tt=card.split()
                timestep=float(tt[-2])
                timestepunits=tt[-1]
                if(self.verb): print 'TTTTTTTTT ',timestep,timestepunits

            if(mf.find(card,'Number of time steps')):

                #Number of time steps:                    6000 timesteps
                tt=card.split()
                Ntimesteps=tt[-2]
                if(self.verb): print 'TTTTTTTTT Ntimesteps: ',Ntimesteps

            if(mf.find(card,'Forecast initial time')):

                tt=card.split()
                rundtg=tt[3][0:10]
                if(self.verb): print 'TTTTTTTTT ',rundtg

            if(mf.find(card,'Output every  ')):
                tt=card.split()
                dtau=tt[2]
                dtauunits=tt[3]
                if(self.verb): print 'TTTTTTTTT ',dtau,dtauunits

            if(mf.find(card,'Total time =  ')):
                tt=card.split()
                totalRuntime=float(tt[3])
                if(self.verb): print 'TTTTTTTTT ',dtau,dtauunits

            #
            # time series
            #
            bd=28
            if(mf.find(card,' rms-d(psfc)**2/d**2t) = ')):

                # rms-d(psfc)**2/d**2t) =          10   23.05441    
                tt=card.split()
                its=int(tt[2])
                val=float(tt[3])
                #print 'mmmmmmmmmmmmmmmmmmmmmmmmmmm noise',tt,its,val
                if(self.verb): print 'noise ',its,val
                gwnoise[its]=val

            if(mf.find(card,'precip - total/nonconv/conv=')):

                #precip - total/nonconv/conv=  0.0000000E+00  0.0000000E+00  0.0000000E+00

                # -- latest format
                #

                gotits=0
                cardp1=cards[n+1]
                if(mf.find(cardp1,'time step')):
                    tt2=cardp1.split()
                    its=int(tt2[-1])
                    gotits=1

                if(gotits == 0):

                    # -- go back for its -- new code to handle extra lines and possible (pvsurf) diag
                    #
                    nbmax=n-10
                    nb=n-1
                    while(not(mf.find(cards[nb],'MAXMIN')) or (mf.find(cards[nb],'(pvsurf)')) and nb >= nbmax):
                        nb=nb-1
                        
                    tt2=cards[nb]
                    tt2=tt2.split()
                    its=int(tt2[1])
                    print '000000000000000000000000 precip its: ',its

                tt=card.split()

                pr=float(tt[3])
                prl=float(tt[4])
                prc=float(tt[5])
                #print 'mmmmmmmmmmmmmmmmmmmmmmmmmmm gmass',tt,its,pr,prl,prc
                if(self.verb): print 'pr     ',its,pr,prl,prc
                gpr[its]=pr
                gprl[its]=prl
                gprc[its]=prc

            if(mf.find(card,'Global 3D mass          =')):

                #Global 3D mass          = 5.1249919E+18 at   0.1 hr, time step=       1
                tt=card[bd:].split()
                tt=card.split()
                its=int(tt[-1])
                val=float(tt[4])
                #print 'mmmmmmmmmmmmmmmmmmmmmmmmmmm gmass',tt,its,val
                if(self.verb): print 'gmass  ',its,val
                gmass[its]=val

            if(mf.find(card,'Global 3D water vapor   =')):

                #Global 3D water vapor   = 1.3939858E+16 at   0.1 hr, time step=       1
                tt=card.split()
                its=int(tt[-1])
                val=float(tt[5])
                #print 'mmmmmmmmmmmmmmmmmmmmmmmmmmm   h2o',tt,its,val
                if(self.verb): print 'gh2o     ',its,val
                gh2o[its]=val

            if(mf.find(card,'Global 3D cloud water   =')):

                #Global 3D cloud water   = 3.6389756E+13 at   0.1 hr, time step=       1
                tt=card.split()
                its=int(tt[-1])
                val=float(tt[5])
                #print 'mmmmmmmmmmmmmmmmmmmmmmmmmmm clh2o ',tt,its,val
                if(self.verb): print 'gclh2o    ',its,val
                gclh2o[its]=val

            if(mf.find(card,'Global integ acc precip =')):

                #Global integ acc precip = 1.9118372E+13 at   0.1 hr, time step=       1
                tt=card.split()
                val=float(tt[5])
                #print 'mmmmmmmmmmmmmmmmmmmmmmmmmmm praccum ',tt,its,val
                if(self.verb): print 'gpraccum ',its,val
                gpraccum[its]=val

            if(mf.find(card,'Global integ evaporation=')):

                # Global integ evaporation=  6.1587870E+12  at time step=           1
                tt=card.split()
                # -- 2015010500 -- change in evap for fim9?  negative? 
                if(mf.find(tt[2],'=')):
                    tt3=tt[2].split('=')
                    val=tt3[1]
                else:
                    val=float(tt[3])
                #print 'mmmmmmmmmmmmmmmmmmmmmmmmmmm evap ',tt,its,val
                if(self.verb): print 'gevap   ',its,val
                gevap[its]=val

            if(mf.find(card,'MODULE TIME (sec)')):

                ntimer=ntimer+1

                if(ntimer == 2):
                    nstart=n+2
                    nend=nstart+11
                    for nn in range(nstart,nend+1):
                        card=cards[nn][:-1]
                        tt=card.split()

                        try:
                            prcname=tt[0]
                        except:
                            continue
                        bd=1
                        if(prcname == 'Main'):  bd=2

                        try:
                            prcmin=float(tt[bd])
                            prcmax=float(tt[bd+1])

                            modtimers.append((prcname,prcmin,prcmax))
                            if(self.verb) : print 'modtimers: ',prcname,prcmin,prcmax
                        except:
                            continue


        rec=(
            rundate,
            rundtg,
            timestep,
            timestepunits,
            Ntimesteps,
            dtau,
            dtauunits,
            gwnoise,
            gpr,
            gprl,
            gprc,
            gmass,
            gh2o,
            gclh2o,
            gpraccum,
            gevap,
            modtimers,
        )

        self.totalRuntime=totalRuntime

        self.setStdOutParams(rec)


    def setStdOutParams(self,rec):

        TS={}
        vardesc={}

        (
            rundate,
            rundtg,
            timestep,
            timestepunits,
            Ntimesteps,
            dtau,
            dtauunits,
            gwnoise,
            gpr,
            gprl,
            gprc,
            gmass,
            gh2o,
            gclh2o,
            gpraccum,
            gevap,
            modtimers,
            )=rec


        self.rundate=rundate
        self.rundtg=rundtg
        self.timestep=timestep
        self.timestepunits=timestepunits
        self.Ntimesteps=Ntimesteps
        self.dtau=dtau
        self.dtauunits=dtauunits
        self.modtimers=modtimers

        TS['gwnoise']=gwnoise
        TS['gpr']=gpr
        TS['gprl']=gprl
        TS['gprc']=gprc
        TS['gmass']=gmass
        TS['gh2o']=gh2o
        TS['gclh2o']=gclh2o
        TS['gpraccum']=gpraccum
        TS['gevap']=gevap

        self.TS=TS

        vardesc['gwnoise']='Gravity Wave Noise rms(dp*2/dt*2)'
        vardesc['gpr']='Global Total Precip'
        vardesc['gprl']='Global Large-Scale Precip'
        vardesc['gprc']='Global Convective Precip'
        vardesc['gmass']='Global 3D mass'
        vardesc['gh2o']='Global 3D water vapor'
        vardesc['gclh2o']='Global 3D cloud water'
        vardesc['gpraccum']='Global integ acc precip'
        vardesc['gevap']='Global integ evaporation'

        self.vardesc=vardesc



    def lsStdOut(self):


        print
        print 'rundate:       ',self.rundate
        print 'rundtg:        ',self.rundtg
        print 'timestep:      ',self.timestep
        print 'Ntimesteps:    ',self.Ntimesteps
        print 'timestepunits: ',self.timestepunits
        print 'dtau:          ',self.dtau
        print 'dtauunits:     ',self.dtauunits
        print

        if(hasattr(self,'modtimers')):

            print 'Module timer:'
            for modtimer in self.modtimers:
                print '%-12s: min: %7.2f  max: %7.2f'%(modtimer[0],modtimer[1],modtimer[2])

        print '                  --------'
        print 'totalRuntime:      %7.2f'%(self.totalRuntime)
        print

        kk=self.TS.keys()
        print 'TimeSeries vars:'
        for k  in kk:
            print k


        print