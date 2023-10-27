#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

#llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
#
#  local defs
#
            
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
            'prcopt':'all',
            'doHiFreqChk':0,
            'dogribmap':1,
            }

        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'source':           ['S:','qmorph','a',' [qmorph]|cmorph'],
            'ropt':             ['N','','norun',' norun is norun'],
            'doRm':             ['R',0,1,'do os.unlink'],
            }

        self.purpose='''
clean off cpc c|qmorph products on kaze'''

        self.examples="""
%s cur-d5 # remove all data <= cur-d5"""

argv=sys.argv
CL=WgetCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

dtgs=mf.dtg_dtgopt_prc(dtgopt)


MF.sTimer('all')
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
#   main loop
#

if(not(w2.onKaze)):
    print 'EEE only run this on Kaze!!!'
    sys.exit()

pdir=w2.PrcDirFlddatW2

if(source == 'qmorph'):
    sdir=w2.NhcQmorphFinalLocal
    sdirl=w2.NhcFtpTargetDirQmorph
    grbdir=w2.NhcQmorphProductsGrib
    prodpre="pr%s"%(source[0])
    
elif(source == 'cmorph'):
    sdir=w2.NhcCmorphFinalLocal
    sdirl=w2.NhcFtpTargetDirCmorph
    grbdir=w2.NhcCmorphProductsGrib
    prodpre="pr%s"%(source[0])




MF.sTimer('glob')
grbPrdPaths=glob.glob("%s/*"%(grbdir))
grbSrcPaths=glob.glob("%s/*"%(sdir))
grbIncPaths=glob.glob("%s/*"%(sdirl))
MF.dTimer('glob')

basedtg=dtgs[-1]

for gpath in grbPrdPaths:
    (dir,file)=os.path.split(gpath)
    (base,ext)=os.path.splitext(file)
    tt=base.split('_')
    if(tt[-1] == 'global' or len(tt) == 2): continue
    dtg=tt[-1]
    ddiff=mf.dtgdiff(basedtg,dtg)
    if(ddiff <= 0.0 and doRm):
        if(ropt != 'norun'): 
            os.unlink(gpath)
            print 'KKKill grbPrdPath:',gpath
        else:
            print 'Will KKKill grbPrdPath: ',gpath
            
for gpath in grbSrcPaths:
    (dir,file)=os.path.split(gpath)
    (base,ext)=os.path.splitext(file)
    if(mf.find(gpath,'.idx')): continue
    tt=base.split('.')
    if(len(tt) == 1): continue
    dtg=tt[-1]
    ddiff=mf.dtgdiff(basedtg,dtg)
    
    if(ddiff <= 0.0 and doRm):
        if(ropt != 'norun'): 
            os.unlink(gpath)
            print 'KKKill grbSrcPath:',gpath
        else:
            print 'Will KKKill grbSrcPath: ',gpath
            
for gpath in grbIncPaths:
    (dir,file)=os.path.split(gpath)
    (base,ext)=os.path.splitext(file)
    tt=base.split('_')
    if(len(tt) != 3): continue
    dtg=tt[-1]
    ddiff=mf.dtgdiff(basedtg,dtg)
    
    if(ddiff <= 0.0 and doRm):
        if(ropt != 'norun'): 
            os.unlink(gpath)
            print 'KKKill grbIncPath:',gpath
        else:
            print 'Will KKKill grbIncPath: ',gpath
            
            

MF.dTimer('all')
sys.exit()    

