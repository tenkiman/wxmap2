#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

from M2 import setModel2

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# command line setup
#
class w2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
        }

        self.options={
            'verb':         ['V',0,1,'verb=1 is verbose'],
            'doAll':        ['A',0,1,'do ALL dirs in tc/'],
            'ropt':         ['N','norun','norun','must use -X to run'],
            'doIt':         ['X',0,1,'run it norun is norun'],
            }


        self.purpose='''
rsync from tenki7 to argo.orc.gmu.edu
(c) 2009-2021 Michael Fiorino,wxmap2.com'''

        self.examples='''
%s -X # doit '''

CL=w2CmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

tcdirs={
    'DSs':'a',
    'adeck':'j',
    'adeck/atcf-form':'n',
    'adeck/cmc':'n',
    'adeck/ecmwf':'n',
    'adeck/esrl':'n',
    'adeck/jtwc':'j',
    'adeck/mftrkN':'n',
    'adeck/tmtrkN':'n',
    'adeck/ncep':'n',
    'adeck/nhc':'n',
    'bdeck/jtwc':'j',
    'bdeck/nhc':'n',
    'bdeck2':'n',
    'bt':'n',
    'carq':'n',
    'cira/mtcswa':'n',
    'cira/mtcswa2':'n',
    'cmc':'n',
    'com/nhc':'n',
    'dis/nhc':'n',
    'ecmwf/wmo-essential':'n',
    'edeck/jtwc':'j',
    'edeck/nhc':'n',
    'fdeck/jtwc':'j',
    'fdeck/nhc':'n',
    'jtwc':'a',
    'mdeck':'j',
    'nhc':'n',
    'names':'a',
    'ncep/tigge':'n',
    'reftrk':'a',
    'stext/jtwc':'j',
    'tcdiag':'n',
    'tceps':'n',
    'ukmo/tigge':'n',
}


#tcdirs=['bdeck']
#print 'curdtg',curdtg
yy=curdtg[0:4]
yyp1=int(yy)+1
yyp1=str(yyp1)
mm=curdtg[4:6]
dd=curdtg[6:8]

# -- logic to change day to touch from earliest mod 3(ddd)
#
idd=int(dd)
ddd=3
ddc=(idd%ddd+0)*ddd
cddc="%02d"%(ddc)
touchDate='%s-%s-%s'%(yy,mm,cddc)
print 'ttt',touchDate

if(doAll):
    tcdirs={'.':'a'}

if(doIt):
    ropt='quiet'
    
MF.sTimer('hopper-TC-touch')
tcdirKeys=tcdirs.keys()
tcdirKeys.sort()
for tcdir in tcdirKeys:
    bdir='/scratch/mfiorino/dat/tc/%s/'%(tcdir)
    tctype=tcdirs[tcdir]

    if(tctype == 'a'):
        wdirs=[bdir]
    elif(tctype == 'n'):
        wdirs=["%s/%s"%(bdir,yy)]
    elif(tctype == 'j'):
        wdirs=[
    '%s/%s'%(bdir,yy),
    '%s/%s'%(bdir,yyp1),
        ]
        
    for wdir in wdirs:
        wdir=wdir.replace('//','/')
        wdir=wdir.replace('/./','/')
        print
        print wdir
        print
        for dirpath, dirs, files in os.walk(wdir):
    
            for filename in files:
                fname = os.path.join(dirpath,filename)
                cmd="ls -lHa %s"%(fname)
                mf.runcmd(cmd,ropt)
                cmd="""touch -d '%s' %s"""%(touchDate,fname)
                mf.runcmd(cmd,ropt)
                cmd="ls -lHa %s"%(fname)
                mf.runcmd(cmd,ropt)
                print
            
MF.dTimer('hopper-TC-touch')
    
sys.exit()



#rsyncOpt='-aluv --timeout=120'
#if(reverse): rsyncOpt='-aluv --timeout=120'
#if(ropt == 'norun'): rsyncOpt='-alvn'


#sdir='/data/w22/dat/tc'
#tdir='mfiorino@argo.orc.gmu.edu:/scratch/mfiorino/dat/tc'
#tdir='mfiorino@hopper1.orc.gmu.edu:/scratch/mfiorino/dat/tc'

#tcdirs=['tmtrkN','adeck/tmtrkN']
#dssdirs={
    #'DSs/*bd2*2021*':'DSs/',
    #'DSs/*ad2*2021*':'DSs/',
#}
        

#if(reverse):
    #MF.sTimer('GMU tc pull')
    #cmd="time rsync %s %s/ %s/"%(rsyncOpt,tdir,sdir)
    #mf.runcmd(cmd,ropt)
    #MF.dTimer('GMU tc pull')
    
#else:
    
    #if(doAll):
        #tcanalEx='''--exclude "tcanal"'''
        #cmd="time rsync %s %s %s/ %s/"%(rsyncOpt,tcanalEx,sdir,tdir)
        #mf.runcmd(cmd,ropt)

        #tcanalEx='''--exclude "*.dat"'''
        #sdirt="%s/tcanal"%(sdir)
        #tdirt="%s/tcanal"%(tdir)
        #cmd="time rsync %s %s %s/ %s/"%(rsyncOpt,tcanalEx,sdirt,tdirt)
        #mf.runcmd(cmd,ropt)
        
    #else:
        #for sdirds in dssdirs.keys():
            #tdirds=dssdirs[sdirds]
            #sdirtc="%s/%s"%(sdir,sdirds)
            #tdirtc="%s/%s"%(tdir,tdirds)
            #cmd="time rsync %s %s %s"%(rsyncOpt,sdirtc,tdirtc)
            #mf.runcmd(cmd,ropt)
        
        #for tcdir in tcdirs:
            #sdirtc="%s/%s/%s"%(sdir,tcdir,curyear)
            #tdirtc="%s/%s/%s"%(tdir,tcdir,curyear)
            #cmd="time rsync %s %s/ %s/"%(rsyncOpt,sdirtc,tdirtc)
            #mf.runcmd(cmd,ropt)
    

