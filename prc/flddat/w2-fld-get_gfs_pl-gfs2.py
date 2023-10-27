#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from M2 import setModel2

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class WgetCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',    'no default'],
            }

        self.defaults={
            'model':'gfs2',
            }

        self.options={
            'doGfsGet':    ['G',1,0,'do NOT wget...'],
            'doGribMap':   ['M',1,0,'do NOT gribmap...'],
            'doCycle':     ['C',0,1,'cycle by taus...'],
            'override':    ['O',0,1,'override'],
            'verb':        ['V',0,1,'verb=1 is verbose'],
            'ropt':        ['N','','norun',' norun is norun'],
            }

        self.purpose='''
purpose -- wget mirror gfs stb (sat brightness t) goes images
%s cur
'''
        self.examples='''
%s cur
'''

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#


MF.sTimer(tag='wget.gfs.stb')

argstr="pyfile -y 2010 -S w.10 -P"
argv=argstr.split()
argv=sys.argv
CL=WgetCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

model='gfs2'
m2=setModel2(model)

dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)

btau=0
etau=192
dtau=6

taus=range(btau,etau+1,dtau)

getGfss={
    'ua':"get_gfs.pl data %s %d %d %d UGRD:VGRD:HGT:RH:TMP 100_mb:150_mb:200_mb:250_mb:300_mb:400_mb:500_mb:700_mb:850_mb:925_mb:1000_mb %s",
    'uas':"get_gfs.pl data %s %d %d %d UGRD:VGRD 10_m_above %s",
    'tas':"get_gfs.pl data %s %d %d %d TMP:TMAX:TMIN 2_m_above %s",
    'ts':"get_gfs.pl data %s %d %d %d TMP surface %s",
    'sfc':"get_gfs.pl data %s %d %d %d PWAT:MSLET:PRATE:CPRAT:APCP:ACPCP all %s",
}


def anlOlines(olines):
    
    rc=0
    for oline in olines:
        if(mf.find(oline,'error')):
            rc=-1
            return(rc)

    for oline in olines:
        if(mf.find(oline,'finished')):
            ofile=olines[-2:-1]
            gotfile=ofile[0]
            rc=1
            print 'YYY: ',gotfile
            return(rc)
            
            
    return(rc)
        


# -- 20210421 -- throttle at NCEP
# -- 20220409 -- cycle by taus

doDelay=1
delaySec=10

delaySecSleep=1
niterMax=6

ebtaus=[]

# -- cycle one tau at a time

dtauC=0
for tau in range(btau,etau+1,dtau):
    ebtaus.append((tau,tau+dtauC))
    

for dtg in dtgs:

    MF.sTimer('GET-GFS-ALL-%s'%(dtg))
    tdir="%s/%s"%(m2.w2fldsSrcDir,dtg)
    mf.ChkDir(tdir,diropt='mk')


    # -- run get_gfs.pl
    #
    if(doGfsGet):
        MF.sTimer('get_gfs')
        for k in getGfss.keys():
            MF.sTimer('ALL %s  dtg: %s'%(k,dtg))
            tmpdir="%s/%s"%(tdir,k)
            mf.ChkDir(tmpdir,diropt='mk')
            
            if(doCycle):
                    
                for ebtau in ebtaus:

                    btau=ebtau[0]
                    etau=ebtau[1]
                    
                    dtau=6
                    rc=0
                    MF.sTimer('%s tau: %d'%(k,btau))
                    niter=0
                    while(rc != 1):
                        cmd=getGfss[k]%(dtg,btau,etau,dtau,tmpdir)
                        olines=MF.runcmdLog(cmd,ropt)
                        rc=anlOlines(olines)
                        niter=niter+1
                        if(niter > niterMax):
                            print 'failed on %s tau: %d niterMax: %d'%(k,btau,niter)
                            sys.exit()
                        if(niter > 1):
                            print 'redoing...niter: ',niter
                            
                        MF.dTimer('%s tau: %d'%(k,btau))
                        sleep(delaySecSleep)
                    
            else:
                cmd=getGfss[k]%(dtg,btau,etau,dtau,tmpdir)
                mf.runcmd(cmd,ropt)
                    
                    
            MF.dTimer('ALL %s  dtg: %s'%(k,dtg))
            
            if(doDelay): sleep(delaySec)
            
        MF.dTimer('get_gfs')
            
    
    # -- cat tmp files by tau
    #

    kk=getGfss.keys()
    kk.sort()
    nkk=len(kk)

    for tau in taus:
        fldstau=[]
        tpath="%s/gfs2.w2flds.%s.f%03d.grb2"%(tdir,dtg,tau)
        
        for k in kk:
            tmpdir="%s/%s"%(tdir,k)
            flds=glob.glob("%s/gfs*f%03d"%(tmpdir,tau))
            if(len(flds) > 0):
                fldstau.append(flds[0])
            
        if(len(fldstau) == nkk):
            
            for n in range(0,len(fldstau)):
            
                fldtau=fldstau[n]

                if(n == 0):
                    cmd="cat %s > %s"%(fldtau,tpath)
                    mf.runcmd(cmd,ropt)
                else:
                    cmd="cat %s >> %s"%(fldtau,tpath)
                    mf.runcmd(cmd,ropt)
                    
                # -- kill off tmp file
                #
                cmd="rm %s"%(fldtau)
                mf.runcmd(cmd,ropt)
                
            
            
    # -- do the gribmap
    #
    if(doGribMap):
        wgribFilterOpt='-C'
        cmd="w2-fld-wgrib-filter.py %s %s %s"%(dtg,model,wgribFilterOpt)
        mf.runcmd(cmd,ropt)        

        
    MF.dTimer('GET-GFS-ALL-%s'%(dtg))
