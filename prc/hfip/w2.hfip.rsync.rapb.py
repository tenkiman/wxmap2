#!/usr/bin/env python

from WxMAP2 import *
w2=W2()


class MdeckCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv

        self.argopts={
            1:['dtgopt',    'no default'],
        }

        self.defaults={
            'lsopt':'s',
            'doupdate':0,
        }

        self.options={
            'dorm':            ['R',0,1,'kill sdir'],
            'reverse':         ['r',0,1,'reverse rsync target -> source'],
            'datSource':       ['d:','all','a','datSource: tcdiag,tcgen,tceps, or all'],
            'override':        ['O',0,1,'override'],
            'verb':            ['V',0,1,'verb=1 is verbose'],
            'ropt':            ['N','','norun',' norun is norun'],
            'doDataHfip':      ['H',0,1,'make /data/amb/hfip target dir'],
            'stm3id':          ['S:',None,'a','only get stm3id'],

        }

        self.purpose=''' of %s
rsync/archive data from /data/rapb/projecst/hfip'''

        self.examples='''
%s 2014010312.2014011418.6 -S 07p -r -d tcdiag # put back tcdiag for 07p'''


class ArchiveHfip(MFbase):

    sbdir='/data/rapb/projects/hfip'
    tbdir='/FWV2/rapb:projects:hfip'

    datdirs=['tcdiagDAT','tcgenDAT','tcepsDAT']

    def __init__(self,dtgopt=None,year=None,datSource='all',
                 ropt='norun',stm3id=None,dorm=0,doDataHfip=0):

        self.year=year
        self.ropt=ropt
        self.dtgopt=dtgopt
        self.stm3id=stm3id
        self.dorm=dorm

        if(doDataHfip):
            self.tbdir='/data/amb/hfip/fiorino/w21/dat'
            
        
        if(mf.find(datSource,'tcd')):
            self.datdirs=['tcdiagDAT']
        elif(mf.find(datSource,'tcg')):
            self.datdirs=['tcgenDAT']
        elif(mf.find(datSource,'tce')):
            self.datdirs=['tcepsDAT']
        else:
            self.datdirs=['tcdiagDAT','tcgenDAT','tcepsDAT']


    def doRsync(self,reverse=0,ropt='norun'):

        dtgs=[]
        if(self.dtgopt != None): dtgs=mf.dtg_dtgopt_prc(self.dtgopt)


        for datdir in self.datdirs:

            if(len(dtgs) > 0):

                for dtg in dtgs:
                    year=dtg[0:4]
                    tdir="%s/%s/%s"%(self.tbdir,datdir,year)
                    MF.ChkDir(tdir,'mk')
                    sdir="%s/%s/%s"%(self.sbdir,datdir,year)
                    dtgsdir="%s/%s"%(sdir,dtg)

                    isthere=MF.ChkDir(dtgsdir,'quiet')

                    if(reverse):
                        isthere=MF.ChkDir(tdir,'quiet')
                        tt=dtgsdir
                        dtgsdir="%s/%s/"%(tdir,dtg)
                        tdir=tt
                        self.dorm=0
                        
                        # -- restore a specific storm
                        #
                        if(self.stm3id != None):

                            mask="%s*%s*"%(dtgsdir,stm3id.upper())
                            print 'mask: ',mask
                            paths=glob.glob(mask)

                            if(len(paths) > 0):
                                MF.ChkDir(tdir,'mk')
                                cmd="cp -n %s*%s* %s/."%(dtgsdir,stm3id.upper(),tdir)
                                mf.runcmd(cmd,ropt)
                            
                            tdirsModel=[]
                            sdirsModel=[]
                            paths=glob.glob("%s/*/*%s*"%(dtgsdir,stm3id.upper()))
                            for path in paths:
                                (sdir,sfile)=os.path.split(path)
                                tdirStm=sdir.replace(dtgsdir,tdir+'/')
                                tdirsModel.append(tdirStm)
                                sdirsModel.append(sdir)
                                
                            tdirsModel=mf.uniq(tdirsModel)
                            sdirsModel=mf.uniq(sdirsModel)
                            
                            for tdirM in tdirsModel:
                                sdirM=sdirsModel[tdirsModel.index(tdirM)]
                                MF.ChkDir(tdirM,'mk')
                                cmd="cp -n %s/*%s* %s/."%(sdirM,stm3id.upper(),tdirM)
                                mf.runcmd(cmd,ropt)
                            
                    if(isthere and stm3id == None):
                        rsyncopt='-alv'
                        if(self.dorm):	rsyncopt="%s --remove-source-files"%(rsyncopt)
                        cmd="rsync %s %s %s/"%(rsyncopt,dtgsdir,tdir)
                        mf.runcmd(cmd,self.ropt)

                        if(self.dorm and self.ropt != 'norun' and not(reverse)):
                            cmd='rm -r %s'%(dtgsdir)
                            mf.runcmd(cmd,self.ropt)

            elif(year != None):

                tdir="%s/%s/%s"%(self.tbdir,datdir,year)
                MF.ChkDir(tdir,'mk')
                sdir="%s/%s/%s"%(self.sbdir,datdir,year)
                cmd="rsync -alv %s/ %s/"%(sdir,tdir)
                mf.runcmd(cmd,self.ropt)

                if(self.dorm and self.ropt != 'norun' and not(reverse)):
                    cmd='rm -r %s'%(sdir)
                    mf.runcmd(cmd,self.ropt)






#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# -- main
#

MF.sTimer('all')

CL=MdeckCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

year='2011'
aR=ArchiveHfip(dtgopt,ropt=ropt,dorm=dorm,datSource=datSource,stm3id=stm3id,
               doDataHfip=doDataHfip)
aR.doRsync(reverse=reverse,ropt=ropt)
