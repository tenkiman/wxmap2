#!/usr/bin/env python

from tcbase import *

class AdeckGen2(AdeckGen):


    def __init__(self,dtgopt,modelopt,basinopt,stcgbdir,
                 taids=None,
                 verb=0,warn=1,
                 trktype='tcgen'):

        #from w2 import SetLandFrac
        #from w2 import GetLandFrac

        self.lf=w2.SetLandFrac()
        self.getlf=w2.GetLandFrac

        self.tdtgs=dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)

        if( (taids != None) and (type(taids) is not(ListType)) ):
            taids=[taids]


        self.basins=basinopt.split(',')
        self.models=modelopt.split(',')
        self.stcgbdir=stcgbdir
        self.trktype=trktype

        self.dtgopt=dtgopt
        self.taids=taids
        self.verb=verb
        self.warn=warn

        self.initVars()
        self.initAdeckPathsZip()
        self.initAdeck()

        del self.lf
        del self.getlf


    def initAdeckPathsZip(self):

        bcards={}
        basins=[]

        adpaths=[]
        genprops={}

        for dtg in self.tdtgs:
            yyyy=dtg[0:4]
            yyyymm=dtg[0:6]
            zipPath="%s/%s/tmtrkN-%s.zip"%(self.stcgbdir,yyyy,yyyymm)
            rc=MF.ChkPath(zipPath)
            if(rc == 0):
                print 'EEE-AdeckGen2.initAdeckPathsZip zipPath: ',zipPath,' not there sayounara'
                sys.exit()
                
            AZ=zipfile.ZipFile(zipPath)
            zls=AZ.namelist()

            for model in self.models:
                
                for basin in self.basins:
                
                    adpath="%s/%s.sink.%s.%s.%s.txt"%(dtg,self.trktype,basin,dtg,model)

                    # -- get adeck if in zip archives
                    #
                    if(adpath in zls):
                        
                        (adir,afile)=os.path.split(adpath)
                        tt=afile.split('.')
                        if(len(tt) == 6):
                            prop=(tt[2],tt[3],tt[4])

                        basin=prop[0]
                        basin.lower()
                        basins.append(basin)
            
                        adeck=AZ.open(adpath).readlines()
                        self.addList2DictList(bcards,basin,adeck)

                    else:
                        print 'not there...press...'


            
            basins=self.uniq(basins)
            
            self.basins=basins
            self.bcards=bcards
            self.adecks=oadecks


            sys.exit()

        for adeck in oadecks:


dtgopt='2019120200'
modelopt='gfs2'
basinopt='lant'
stcgbdir='/w21/dat/tc/adeck/tmtrkN'

AG=AdeckGen2(dtgopt, modelopt, basinopt, stcgbdir)

AG.ls()
