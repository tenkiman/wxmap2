#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

class TcOpsCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv

        self.argopts={
            1:['dtgopt',    'dtgopt'],
            2:['model',     'model'],
        }

        self.defaults={
        }

        self.options={
            'ropt':            ['N','','norun',' norun is norun'],
            'override':        ['O',0,1,' redo wget'],
            'verb':            ['V',0,1,'verb=1 is verbose'],
            'useJpeng':        ['J',0,1,'use Jpeng vice ops for source of TC eps xml vice ncep'],
        }

        self.purpose='''
mirror adecks from ecmwf tigge xml tracker server to local'''

        self.examples='''
%s ops ecmwf'''


MF.sTimer('all')

argv=sys.argv
CL=TcOpsCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

idtgopt=dtgopt
if(dtgopt == 'ops'): idtgopt='cur'
dtgs=mf.dtg_dtgopt_prc(idtgopt)

w2.setNcepTCepsSource(useJpeng=useJpeng)

if(model == 'all'):

    models=['ecmwf','ukmo','ncep','cmc']

    for model in models:
        cmd="%s %s %s"%(pyfile,dtgopt,model)
        for o,a in CL.opts:
            cmd="%s %s %s"%(cmd,o,a)
        mf.runcmd(cmd,ropt)

    sys.exit()



if(mf.find(model,'ecm')):
    model='ecmwf'
elif(mf.find(model,'ukm')):
    model='ukmo'
elif(mf.find(model,'ncep')):
    model='ncep'
elif(mf.find(model,'cmc')):
    model='cmc'
else:
    print "EEEE invalid model in: %s  model: %s"%(pyfile,model)
    sys.exit()


dtgs=mf.dtg_dtgopt_prc(dtgopt)

#
# increase time for finding 12z -- maybe very late at ecmwf web site
#
if(dtgopt == 'ops12' and mf.find(model,'ecm') ):
    dtg=mf.dtg_command_prc(dtgopt,opsfhr=8.0)
    dtgs=[dtg]

for dtg in dtgs:

    yyyy=dtg[0:4]
    yyyymmdd=dtg[0:8]
    hh=dtg[8:10]

    dmasks=None
    print model
    if(mf.find(model,'ecm')):
        af=w2.EcmwfTiggeFtpserver
        al=w2.EcmwfTiggeLogin
        ap=w2.EcmwfTiggePasswd
        sbdir=w2.EcmwfTiggeDatDir
        dtype='z_tigge_c_ecmf_'
        dmask="*%s*%s*"%(dtype,dtg)

    elif(mf.find(model,'ukm')):
        af=w2.uKmoTiggeFtpserver
        al=None
        ap=None
        sbdir=w2.uKmoTiggeDatDir
        dtype='z_tigge_c_egrr_'
        dmask="*%s*%s*"%(dtype,dtg)
        
        dmasks=[
            "z_tigge_c_egrr_%s0000_mogreps_glob_prod_etctr_glo.xml.gz"%(dtg),
            "z_tigge_c_egrr_%s0000_mogm_glob_prod_tctr_glo.xml"%(dtg),
        ]

    elif(model == 'ncep'):
        af=w2.NcepTiggeFtpserver
        al=w2.NcepTiggeLogin
        ap=w2.NcepTiggePasswd
        sbdir="%s/%s"%(w2.NcepTiggeDatDir,yyyymmdd)
        if(w2.useJpeng):
            sbdir=sbdir
        else:
            sbdir="%s/gefs.%s/%s/tctrack"%(w2.NcepTiggeDatDir,yyyymmdd,hh)
            
        dtype='GEFS_glob_prod_etctr_glo'

        if(w2.useJpeng):
            dtype='G*FS_glob_prod_*tr_glo'
            dmask="*%s*%s*"%(dtg,dtype)
        else:
            dmasks=["*%s*GFS_glob_prod_sttr_glo.xml"%(dtg),
                    "*%s*GEFS_glob_prod_esttr_glo.xml"%(dtg),
                    ]

    elif(model == 'cmc'):
        af=w2.CmcTiggeFtpserver
        al=w2.CmcTiggeLogin
        ap=w2.CmcTiggePasswd
        sbdir="%s/%s"%(w2.CmcTiggeDatDir,yyyymmdd)
        
        if(w2.useJpeng):
            sbdir=sbdir
        else:
            sbdir="%s/cmce.%s/%s/tctrack"%(w2.CmcTiggeDatDir,yyyymmdd,hh)

        if(w2.useJpeng):
            dtype='C*_glob_prod_*tr_glo'
            dmask="*%s*%s*"%(dtg,dtype)
        else:
            
            dmasks=["*%s*CMC_glob_prod_sttr_glo.xml"%(dtg),
                    "*%s*CENS_glob_prod_esttr_glo.xml"%(dtg),
                    ]

    tbdir=w2.TcTiggeDatDir

    #ftp://ftp.emc.ncep.noaa.gov/gc_wmb/mcharles/tigge/beta/cxml/20090625/kwbc_20090625000000_GEFS_glob_prod_etctr_glo.xml
    #wget -m ftp://tigge:tigge@tigge-ldm.ecmwf.int/cxml/z_tigge_c_ecmf_20090428000000_ifs_glob_prod_all_glo.xml
    #ftp://ftp.emc.ncep.noaa.gov/gc_wmb/mcharles/tigge/beta/cxml/20090625/kwbc_20090625060000_GFS_glob_prod_tctr_glo.xml

    tdir="%s/%s/tigge/%s"%(tbdir,model,yyyy)
    mf.ChkDir(tdir,diropt='mk')
    mf.ChangeDir(tdir)

    logdir="%s/%s"%(tdir,dtg)
    mf.ChkDir(logdir,diropt='mk')
    logpath="%s/db.wget.%s.%s.txt"%(logdir,model,dtg)

    # output wget (stderr) to logpath
    #
    if(dmasks == None and ap != None):
        ftpurl="\"ftp://%s:%s@%s/%s/%s\""%(al,ap,af,sbdir,dmask)
    
    if(ap == None):
        ftpurl="\"ftp://%s/%s/%s\""%(af,sbdir,dmask)
        
    wgetOpt='-nv -m -nd -T 30 -t 2'

    if(dmasks != None):

        for dmask in dmasks:
            filesdone=glob.glob("%s/%s*"%(tdir,dmask))
            if(ap != None):
                ftpurl="\"ftp://%s:%s@%s/%s/%s\""%(al,ap,af,sbdir,dmask)

            if(len(filesdone) == 0 or override):
                cmd="wget %s -t 2 -a %s %s"%(wgetOpt,logpath,ftpurl)
                mf.runcmd(cmd,ropt)

                # -- check if got an .xml; if so gzip
                #
                filesdone=glob.glob("%s/%s*"%(tdir,dmask))
                if(len(filesdone) == 1 and not(mf.find(filesdone[0],'gz')) and model == 'ukmo'):
                    cmd="gzip %s"%(filesdone[0])
                    mf.runcmd(cmd,ropt)
                    print 'III(doing 1111111111111st gzip) for file: ',filesdone[0]
                    
            if(len(filesdone) == 1 and mf.find(filesdone[0],'gz') and model != 'ukmo'):
                # -- if the above check failed, do the gzip now
                #
                cmd="gunzip %s"%(filesdone[0])
                mf.runcmd(cmd,ropt)
                print 'III(doing 222222222222222nd gunzip) for file: ',filesdone[0]
            elif(model == 'ukmo'):
                #print 'III(gzip done) for dmask: ',dmask,' for non-ukmo model'
                continue
            else:
                print 'III(gzip done) for dmask: ',dmask

    else:

        cmd="wget %s -a %s %s"%(wgetOpt,logpath,ftpurl)
        mf.runcmd(cmd,ropt)


sys.exit()
