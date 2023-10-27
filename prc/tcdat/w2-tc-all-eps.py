#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

class TcOpsCmdLine(CmdLine):

    EpsModels=['ecmwf','ukmo','ncep','cmc']
    
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
            'model':           ['m:',None,'a',' set model to process, for -T ncep: geps*cmc; cmc - just cmc'],
            'verb':            ['V',0,1,'verb=1 is verbose'],
            'override':        ['O',0,1,'override'],
            'doncEpOnly':      ['E',0,1,'only do ncep...'],
            'doNcepTigge':     ['T',0,1,'wget of ncep/cmc tigge cxml -- broken as of 2018022'],
            'doNcepAD2':       ['2',0,1,'use ncep ad2 only'],
            'useJpeng':        ['J',0,1,'useJpeng source of TC eps xml vice ncep'],
            }

        self.purpose='''
run all eps .py for a dtg...
'''
        self.examples='''
%s ops
'''


MF.sTimer('all')

argv=sys.argv
CL=TcOpsCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

dtgs=mf.dtg_dtgopt_prc(dtgopt)
ncepAdeckOpt='-A'
if(doNcepTigge or doncEpOnly): ncepAdeckOpt=''
prcdir=os.getenv('W2_PRC_DIR')

tiggeMirrorCmd='%s/tcdat/w2-tc-wget-mirror-tigge-2-local.py'%(prcdir)
tiggeAdeckCmd='%s/tcdat/w2-tc-tigge-xml-2-wxmap-adecks.py'%(prcdir)
epsAD2Cmd='%s/tcdat/w2-tc-g-epsanal-dss-ad2.py'%(prcdir)
adcCmd='%s/tcdat/w2-tc-convert-tm-mftrkN-to-atcf-adeck.py'%(prcdir)
ad2Cmd='%s/tcdat/w2-tc-dss-ad2.py'%(prcdir)

jOpt=''
if(useJpeng): jOpt='-J'

for dtg in dtgs:
    
    if(doNcepAD2):
        
        if(doncEpOnly):
            oopt=''
            if(override): oopt='-O'
            cmd="%s %s ncep,cmc %s"%(epsAD2Cmd,dtg,oopt)
            mf.runcmd(cmd,ropt)

        else:
            # -- do the ukmo from tigge -- this puts trackers in /dat/tc/adeck/ukmo -> atcf-form -> ad2
            #
            if(model == None or model == 'ukmo'):
                cmd="%s %s ukmo all"%(tiggeMirrorCmd,dtg)
                mf.runcmd(cmd,ropt)
                
                # -- just get the det aid ...
                cmd="%s %s ukmo det -G"%(tiggeAdeckCmd,dtg)
                mf.runcmd(cmd,ropt)
                
                cmd="%s %s ukmo all -G"%(tiggeAdeckCmd,dtg)
                mf.runcmd(cmd,ropt)
                
                cmd="%s ukmo -d %s -A"%(adcCmd,dtg)
                mf.runcmd(cmd,ropt)
                
            # -- graphics using ad2
            #
            oopt=''
            if(override): oopt='-O'

            if(model == None or model == 'ukmo'):
                cmd="%s %s ukmo %s"%(epsAD2Cmd,dtg,oopt)
                mf.runcmd(cmd,ropt)
                
            if(model == None or (model == 'ncep')):
                cmd="%s %s ncep,cmc %s"%(epsAD2Cmd,dtg,oopt)
                mf.runcmd(cmd,ropt)
                
            if(model == None or (model == 'cmc')):
                cmd="%s %s cmc %s"%(epsAD2Cmd,dtg,oopt)
                mf.runcmd(cmd,ropt)
        
        
    else:
    
        if(not(doncEpOnly)):
        
            if(model == None or model == 'ecmwf'):
                cmd="%s %s ecmwf"%(tiggeMirrorCmd,dtg)
                mf.runcmd(cmd,ropt)
        
            if(model == None or model == 'ukmo'):
                cmd="%s %s ukmo"%(tiggeMirrorCmd,dtg)
                mf.runcmd(cmd,ropt)
        
        if(doNcepTigge or doncEpOnly):
            
            if(model == None or (model == 'cmc')):
                cmd="%s %s cmc %s"%(tiggeMirrorCmd,dtg,jOpt)
                mf.runcmd(cmd,ropt)
                
            if(model == None or (model == 'ncep')):
                
                cmd="%s %s cmc %s"%(tiggeMirrorCmd,dtg,jOpt)
                mf.runcmd(cmd,ropt)
        
                cmd="%s %s ncep %s"%(tiggeMirrorCmd,dtg,jOpt)
                mf.runcmd(cmd,ropt)
        
        if(not(doncEpOnly)):
            
            if(model == None or model == 'ecmwf'):
            
                cmd="%s %s ecmwf ecmt"%(tiggeAdeckCmd,dtg)
                mf.runcmd(cmd,ropt)
            
                cmd="%s %s ecmwf all"%(tiggeAdeckCmd,dtg)
                mf.runcmd(cmd,ropt)
                
            if(model == None or model == 'ukmo'):
                cmd="%s %s ukmo all"%(tiggeAdeckCmd,dtg)
                mf.runcmd(cmd,ropt)
        
                
        if(model == None or (model == 'ncep')):

            cmd="%s %s ncep gfst"%(tiggeAdeckCmd,dtg)
            mf.runcmd(cmd,ropt)
        
            cmd="%s %s ncep all %s"%(tiggeAdeckCmd,dtg,ncepAdeckOpt)
            mf.runcmd(cmd,ropt)
            
            # -- do adc to put cmc and gefs in atcf-form and in the AD2
            #
            cmd="%s gefs -d %s -A"%(adcCmd,dtg)
            mf.runcmd(cmd,ropt)

            cmd="%s %s cmc cmct"%(tiggeAdeckCmd,dtg)
            mf.runcmd(cmd,ropt)
    
            cmd="%s %s cmc all %s"%(tiggeAdeckCmd,dtg,ncepAdeckOpt)
            mf.runcmd(cmd,ropt)

            # -- do adc to put cmc and gefs in atcf-form and in the AD2
            #
            cmd="%s cmc -d %s -A"%(adcCmd,dtg)
            mf.runcmd(cmd,ropt)
            
        if(model == None or (model == 'cmc')):

            cmd="%s %s cmc cmct"%(tiggeAdeckCmd,dtg)
            mf.runcmd(cmd,ropt)
    
            cmd="%s %s cmc all %s"%(tiggeAdeckCmd,dtg,ncepAdeckOpt)
            mf.runcmd(cmd,ropt)
        

    
        if(not(doNcepTigge)):
            
            if(model == None or model == 'ukmo'):
            
                cmd="%s %s ukmo all"%(tiggeMirrorCmd,dtg)
                mf.runcmd(cmd,ropt)
                
                cmd="%s %s ukmo all"%(tiggeAdeckCmd,dtg)
                mf.runcmd(cmd,ropt)

# -- rsync to wxmap2.com
#
if(ropt != 'norun'):
    rc=rsync2Wxmap2('tceps',ropt)

    
MF.dTimer('all')
