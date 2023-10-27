#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class WgetCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            #1:['dtgopt',    'no default'],
            }

        self.defaults={
            'model':'gfs2',
            }

        self.options={
            'dtgopt':           ['d:',None,'a','dtgopt for rsync of w2flds'],
            'dow2fldsonly':     ['W',0,1,'override'],
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'doit':             ['X','','norun',' norun is norun'],
            'noRunChk':         ['R',0,1,"""if 1 -- don't if running"""],
            'dryrun':           ['D',0,1,'1 - '],
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


MF.sTimer(tag='kaze2kishou')

CL=WgetCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

MF.sTimer(tag='chkifrunning')
rc=w2.ChkIfRunningNWP(dtg=None,pyfile=pyfile,model=None)
if(rc > 1 and not(noRunChk)):
    print 'AAA allready running...'
    sys.exit()
    

doit=1
prcdir=w2.PrcDirFlddatW2
expath="%s/ex-kaze2kishou.txt"%(prcdir)

# -- do update for case when I'm change files on kishou
#
rsyncoptDry='-alvun  --protocol=29 --exclude-from=%s '%(expath)
rsyncoptDo='-aluv  --protocol=29 --exclude-from=%s '%(expath)

rsyncopt=rsyncoptDry
if(doit and ropt == ''):
    rsyncopt=rsyncoptDo

if(dryrun):
    ropt=''
    rsyncopt=rsyncoptDry


mf.ChangeDir(w2.DatBdirW2data)

if(dow2fldsonly and dtgopt != None):

    dtgs=mf.dtg_dtgopt_prc(dtgopt)

    mmask="%s/w2flds/dat/*"%(w2.Nwp2DataBdir)
    mdirs=glob.glob(mmask)
    models=[]
    for mdir in mdirs:
        model=mdir.split('/')[-1]
        models.append(model)

    for model in models:
        for dtg in dtgs:
            cmd='rsync %s nwp2/w2flds/dat/%s/%s fiorino@kishou.fsl.noaa.gov:/w21/dat/nwp2/w2flds/dat/%s'%(rsyncopt,model,dtg,model)
            mf.runcmd(cmd,ropt)


    sys.exit()







dir2s=['cmc',
# - interferes with local inv on kishou#
#       'DSs',
       'ecmwf',
       'esrl',
       'fnmoc',
       'jma',
       'ncep',
       'ukmo',
       ]

dirDats=[
       'pr',
       'ocean',
       ]

dir4s=['w2flds']

for dirD in dirDats:
    cmd='rsync %s %s/ fiorino@kishou.fsl.noaa.gov:/w21/dat/%s/'%(rsyncopt,dirD,dirD)
    mf.runcmd(cmd,ropt)

for dir4 in dir4s:
    cmd='rsync %s nwp2/%s/ fiorino@kishou.fsl.noaa.gov:/w21/dat/nwp2/%s/'%(rsyncopt,dir4,dir4)
    mf.runcmd(cmd,ropt)

for dir2 in dir2s:
    cmd='rsync %s nwp2/%s/ fiorino@kishou.fsl.noaa.gov:/w21/dat/nwp2/%s/'%(rsyncopt,dir2,dir2)
    mf.runcmd(cmd,ropt)


MF.dTimer(tag='kaze2kishou')
