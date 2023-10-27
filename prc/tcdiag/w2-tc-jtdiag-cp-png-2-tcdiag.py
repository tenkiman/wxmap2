#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

prcdir=w2.PrcDirTcdiagW2

#llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
# local defs
#
class JTdiagCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv

        self.argopts={
            1:['dtgopt',    'no default'],
            }

        self.defaults={
            }

        self.options={
            'ropt':            ['N','','norun',' norun is norun'],
            'verb':            ['V',0,1,'verb=1 is verbose'],
            'doClean':         ['K',0,1,'clean off target dir with rm -r'],
            'override':        ['O',0,1,'do cp -p vice cp -p -n'],
            'doJsInv':         ['J',1,0,'do NOT make 10-d .js inventory'],
            'doDiagOnly':      ['D',0,1,'only do the diagnostic file'],
            'stmopt':          ['S:',None,'a','stmopt'],
            'modelopt':        ['m:',None,'a','modelopt'],
            'ndayback':        ['n:',10,'i','nday back to do inventory'],
            'dochkIfRunning':  ['o',1,0,'do NOT chkifrunning in MFutils.chkIfJobIsRunning'],
            }

        self.purpose='''
cp -p png from tcdiag to jtdiag web'''

        self.examples='''
%s cur12-12     : pull from archive dir for 2004'''


MF.sTimer('all')

argv=sys.argv
CL=JTdiagCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

if(ropt == 'norun'): dochkIfRunning=0

# -- since running in crontab...
#
MF.ChangeDir(prcdir)


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# main
#

models={
    'gfs2':6,
    'ecm5':12,
    'cgd2':12,
    'navg':6,     # added 2019062400
    'jgsm':6,     # added 2019062400
    #'ecm4':12,
    #'ukm2':12,
    #    'fv3g':12,  # not running after hfip reservations
}
    

# -- from TCdiag.py
getVars=['shr_mag','max_wind','sst','200dvrg','tpw','850vort',
         'precip', # -- includes psl and roci/poci
         'trkplt'] # -- add track plot

ttaus=[0,6,12,18,24,30,36,42,48,60,72,84,96,108,120]

phrP06={
    6:0,
    12:6,
    18:12,
    24:18,
    30:24,
    36:30,
    42:36,
    48:42,
    60:48,
    72:60,
    84:72,
    96:84,
    108:96,
    120:108,
    132:120,
}

phrP12={
    12:0,
    18:6,
    24:12,
    30:18,
    36:24,
    42:30,
    48:36.42,
    60:48,
    72:60,
    84:72,
    96:84,
    108:96,
    120:108,
    132:120,
}

if(modelopt != None): 
    omodels=modelopt.split(',')
    imodels=models.keys()
    nmodels={}
    for omodel in omodels:
        if(omodel in imodels):
            nmodels[omodel]=models[omodel]
            
    models=nmodels
    

MF.sTimer('ALL-cp-js-inv')
dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)

if(w2.onKaze or w2.onTenki or w2.onGmu):
    sbdir='%s/tcdiag'%(w2.HfipProducts)
    tbdir='%s/jtdiag'%(w2.HfipProducts)
else:
    sbdir='/w21/dat/tc/tcdiag'
    tbdir='/w21/web/jtdiag'
    
# use symbolic links vice cp
#
cpopt='-p -f -s'
cpopt='-p -f'  # -- do actual file for rsync purpose
if(override): doClean=1

for dtg in dtgs:

    dtgm6=mf.dtginc(dtg,-6)
    dtgm12=mf.dtginc(dtg,-12)
    
    MF.sTimer('cp-tcdiag-2-jtdiag-%s'%(dtg))
    yyyy=dtg[0:4]
    tdir="%s/%s/%s"%(tbdir,yyyy,dtg)
    
    if(doClean):
        cmd="rm -r %s"%(tdir)
        mf.runcmd(cmd,ropt)

    MF.ChkDir(tdir,'mk')

    for model in models.keys():

        # -- bypass cp to only do diagnostic files
        #
        if(ropt == 'norun'):
            print 'III-%s will do dtg: %s model: %s'%(pyfile,dtg,model)
            continue
            
            
        if(doDiagOnly): continue
        
        phr=models[model]
        if(MF.is0618Z(dtg)): phr=6

        if(phr == 6):
            sdir="%s/%s/%s"%(sbdir,yyyy,dtgm6)
            phrs=phrP06
            
        elif(phr == 12):
            sdir="%s/%s/%s"%(sbdir,yyyy,dtgm12)
            phrs=phrP12

        staus=phrs.keys()
        vtaus=phrs.values()
        vtaus.sort()
        staus.sort()

        for gvar in getVars:
     
            gmask="%s/%s/%s.*.png"%(sdir,model,gvar)
            pngs=glob.glob(gmask)
            pngs.sort()
            if(verb): print 'ggg',gmask,pngs

            if(gvar == 'trkplt'):

                for spng in pngs:
                    (pdir,png)=os.path.split(spng)
                    cmd="cp %s %s %s/%s"%(cpopt,spng,tdir,png)
                    mf.runcmd(cmd,ropt)

            else:
                
            
                for spng in pngs:

                    (pdir,png)=os.path.split(spng)
                    tt=png.split('.')
                    stau=int(tt[-2])
                    syear=tt[-3]
                    snum=tt[-4]
                    prod=tt[-5]

                    if(stau in staus):
                        ttau=phrs[stau]
                        tt=str(ttau).split('.')
                        # -- check for double use
                        #
                        if(len(tt) == 2):
                            ttau1=int(tt[0])
                            tpng="%s-%s.%s-%s-%s-%03d.png"%(model,snum,syear,dtg,prod,ttau1)
                            cmd="cp %s %s %s/%s"%(cpopt,spng,tdir,tpng)
                            mf.runcmd(cmd,ropt)
                            ttau2=int(tt[1])
                            tpng="%s-%s.%s-%s-%s-%03d.png"%(model,snum,syear,dtg,prod,ttau2)
                            cmd="cp %s %s %s/%s"%(cpopt,spng,tdir,tpng)
                            mf.runcmd(cmd,ropt)

                        else:
                            tpng="%s-%s.%s-%s-%s-%03d.png"%(model,snum,syear,dtg,prod,ttau)
                            cmd="cp %s %s %s/%s"%(cpopt,spng,tdir,tpng)
                            mf.runcmd(cmd,ropt)
                            

            
    # -- diagfiles
    #
    tdirdiag="%s/DIAGFILES"%(tdir)
    MF.ChkDir(tdirdiag,'mk')

    for model in models.keys():
        
        phr=models[model]
        if(MF.is0618Z(dtg)): phr=6
        if(phr == 6):
            sdir="%s/%s/%s"%(sbdir,yyyy,dtgm6)
            sdtg=dtgm6
            
        elif(phr == 12):
            sdir="%s/%s/%s"%(sbdir,yyyy,dtgm12)
            sdtg=dtgm12
        
        dmask="%s/DIAGFILES/*%s*.txt"%(sdir,model)
        diags=glob.glob(dmask)
        for diag in diags:
            
            (ddiag,fdiag)=os.path.split(diag)
            odiag=fdiag.replace(sdtg,dtg)
            #print 'ddd',fdiag
            #print 'ooo',odiag
    
            cmd="cp %s %s %s/%s"%(cpopt,diag,tdirdiag,odiag)
            #mf.runcmd(cmd,ropt)
            mf.runcmd(cmd,'quiet')
    
    MF.dTimer('cp-tcdiag-2-jtdiag-%s'%(dtg))

if(doJsInv):
    
    cmd="w2-tc-jtdiag-inv.py cur-d%d.cur alljt"%(ndayback)
    mf.runcmd(cmd,ropt)
    
    
MF.sTimer('ALL-cp-js-inv')

sys.exit()
