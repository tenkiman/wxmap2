#!/usr/bin/env python

from WxMAP2 import *
w2=W2()
MF=MFutils()

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

def runUD(cmd,sdir,year=None,dozip=0,docp=0,verb=0):

    sdir=sdir.replace('//','/')

    if(mf.find(sdir,'usb2')): 
        if(doMike3):
            sdir=sdir.replace('/tc/','/tc-mike3/')
        else:
            sdir=sdir.replace('/tc/','/tc-mike2/')

    if(year != None):
        udir="%s/%s"%(sdir,year)
        zpath="%s/%s.zip"%(sdir,year)
        if(mf.find(zpath,'mtcswa')): zpath="%s/???-%s.zip"%(sdir,year)
        zpath=zpath.replace('//','/')
        if(docp):
            udir=sdir
            zpath="%s/*%s*"%(sdir,year)
            zpath=zpath.replace('//','/')
    else:
        udir=sdir
        
    if(dozip or docp):
        cmd="du %s"%(zpath)
    else:
        udir=udir.replace('//','/')
        cmd="usage.py %s"%(udir)

    siz='-999'
    rc=mf.runcmd2(cmd, ropt='', verb=0, lsopt='q', prefix='', 
                  postfix='', 
                  ostdout=1)
    
    if(dozip or docp):
        if(rc[0]):
            #print 'ZZZ',cmd,len(rc[1])
            if(len(rc[1]) > 2):
                asiz=0
                mcards=rc[1]
                for mcard in mcards:
                    if(len(mcard) <= 1): continue
                    siz=mcard.split('\t')[0]
                    mpath=mcard.split('\t')[1]
                    asiz=asiz+int(siz)
                    #print 'mtcswa: ',siz,'path: ',mpath
                siz=asiz
                
            else:
                siz=rc[1][0].split('\t')[0]
                if(len(siz) == 0):
                    #print 'WWW000--',zpath
                    siz=-999
                else:
                    #print 'zzzsiz ',rc,siz,cmd
                    siz=int(siz)
            
            if(docp):
                print 'Cdir: %-60s   siz: %10d'%(zpath,siz)
            else:
                print 'Zdir: %-60s   siz: %10d'%(zpath,siz)
                
                
            
        return(siz)

    if(rc[0]): 
        cards=rc[1]
        if(verb): print
        for card in cards:
            card=str(card)
            if(mf.find(card,'Total...')): siz=card.split()[-1]

            if(verb):
                if(mf.find(card,'Total...') or mf.find(card,'Files...') or mf.find(card,'Dirs...')):
                    print card
                
        if(siz > 0):
            siz=siz.replace(',','')
        siz=int(siz)
        odir=sdir
        if(year != None): odir="%s/%s"%(sdir,year)
        
        odir=odir.replace('//','/')
        print ' dir: %-60s   siz: %10d'%(odir,siz)
        return(siz)
                


class MssCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            #1:['yearOpt',    'no default'],
            }

        self.defaults={
            }

        self.options={
            'verb':          ['V',0,1,'verb=1 is verbose'],
            'ropt':          ['N','','norun',' norun is norun'],
            'doit':          ['X',0,1,'run it...'],
            'doGmu':         ['G',0,1,'push to GMU...'],
            'doReverse':     ['R',0,1,'rsync from usb2 to local'],
            'doWx2Reverse':  ['r',0,1,'rsync from wx2 to local'],
            'doCurrent':     ['C',0,1,'only do dirs in CURRENT.txt'],
            'doDryRun':      ['D',0,1,'do dryrun rsyncf'],
            'doMike2':       ['2',0,1,'Mike2 if doWx2Reverse...'],
            'doMike3':       ['3',0,1,'Mike3 or on Mike3 if doWx2Reverse...'],
            'doMike4':       ['4',0,1,'Mike4...'],
            'doArgo':        ['A',0,1,'go to argo.orc.edu...'],
            'doud':          ['U',0,1,'use ud to find total siz...'],
            'doUsb2':        ['2',0,1,'find total siz...'],
            'doWxmap2':      ['W',0,1,'push to wxmap2...'],
            'yearOpt':       ['Y:',None,'a','set year...'],
            'sourceOpt':     ['S:',None,'a',"""source: 'tmtrkN' | 'mftrkN' | 'trk-tmtrkN'"""],
            'doByParts':     ['P:',0,'i',"""do by sections"""],
            }

        self.purpose='''
convert tmtrkN adecks to zip archive
'''
        self.examples='''
%s year'''

MF.sTimer(tag='all')

argv=sys.argv
CL=MssCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

prcdir=w2.PrcDirTcdatW2

# -- set the active path
#
actPath='%s/active-tc-dirs-20200506.txt'%(prcdir)

if(doCurrent):
    actPath='%s/active-tc-dirs-CURRENT.txt'%(prcdir)
    
if(doWxmap2):
    actPath='%s/active-tc-dirs-CURRENT-2021-WX2.txt'%(prcdir)
    
if(doGmu):
    actPath='%s/active-tc-dirs-CURRENT-2021-GMU.txt'%(prcdir)
    
    
nSecSleepWx2=0

cards=MF.ReadFile2List(actPath)

sbdir='/dat1'
tbdir='/usb2/dat'
if(doMike3):
    if(doWx2Reverse):
        sbdir='/w21/dat'
        sbdir='/mnt/USB3Ext4-13/dat'
        sbdir='/w21/dat'
        tbdir='/w21/dat'
    else:
        sbdir='/w21/dat'
        tbdir='/usb2/dat'

if(doUsb2 and doud):
    sbdir=tbdir
    
if(doReverse):
    sbdir='/usb2/dat'
    tbdir='/w21/dat'
    
    
if(doDryRun):
    rsyncOpt='-alvn'
else:
    rsyncOpt='-alv'
    
# -- do to wxmap2.com
#
if(doWxmap2):
    tbdir='''mfiorino@wxmap2.com:/home3/mfiorino'''
    rsyncOpt='''%s --rsh="ssh -p2222" --size-only'''%(rsyncOpt)
    
    
if(doMike4):
    sbdir='/w21/dat'
    if(doReverse):
        ss=sbdir
        tt=tbdir
        sbdir=tt
        tbdir=ss
        
        if(doWxmap2):
            sbdir='''mfiorino@wxmap2.com:/home3/mfiorino'''
            

if(doArgo):
    sbdir='/home/mfiorino/w22/dat'
    

if(doGmu):
    sbdir='/w21/dat'
    tbdir='mfiorino@hopper1.orc.gmu.edu:/scratch/mfiorino/dat'
    rsyncOpt='-alv --timeout=120'

if(doit == 0 or doud == 0): ropt='norun'

if(doit and doud == 0): ropt=''
MF.sTimer('ALL-tc-active')
allCommands=[]

allSiz=0
for card in cards:
    # -- comment cards
    #
    if(card[0] == '#'): continue
    if(verb): print card[0:-1]
    if(len(card) <= 2): continue
    tt=card.split()
    ttt=tt[0].split(':')
    dtype=ttt[0]
    ddir=ttt[-1]
    
    sdir="%s/%s"%(sbdir,ddir)
    
    if(doWxmap2):

        if(doReverse):
            tdir="%s/%s"%(tbdir,ddir)
            ddir=ddir.replace('tc/','tcdat/')
            sdir='''%s/%s'''%(sbdir,ddir)
        else:
            ddir=ddir.replace('tc/','tcdat/')
            tdir='''%s/%s'''%(tbdir,ddir)
            
    else:
        tdir="%s/%s"%(tbdir,ddir)
    
    
    if(not(doReverse) and (doMike3 or doMike4)):
        if(doMike3):
            tdir=tdir.replace('/tc/','/tc-mike3/')
        elif(doMike2):
            tdir=tdir.replace('/tc/','/tc-mike2/')
            
    if(verb):
        print
        print 'SSSSS: ',sdir,'TTTTTT: ',tdir
        print
    if(doit and not(doud) and not(doWxmap2 and doReverse)):
        MF.ChangeDir(sdir)
        
    didsub=0
    if(len(tt) > 1):
        didsub=1
        #if(verb == 0):
            #print 'SSSSSSS:',tt,'sss: ',sdir,'ttt: ',tdir
        for t1 in tt[1:]:
            dozip=0 ; docp=0 
            t2=t1.split('/')
            t2=t2[0:-1]
            moddir=''
            if(len(t2) == 2): 
                moddir=t2[0]
                if(moddir[0] == 'Z' or moddir[0] == 'C'): moddir=moddir[1:]

            if(t1[0] == 'Z'): dozip=1
            if(t1[0] == 'C'): docp=1
            ydir=t1
            if(docp or dozip): ydir=t1[1:]

            year=ydir[0:4]
            
            if(docp):
                # -- if doing DS...only do mdecks so ad2 always local
                #
                if(dtype == 'DS'):
                    maskOpt='''m*%s*'''%(year)
                else:
                    maskOpt='''*%s*'''%(year)
                    
                if(doWxmap2):
                    if(doWx2Reverse):
                        cmd='''rsync %s --include="%s" --exclude="*" "%s/" "%s/"'''%(rsyncOpt,maskOpt,tdir,sdir)
                    else:
                        cmd='''rsync %s --include="%s" --exclude="*" "%s/" "%s/"'''%(rsyncOpt,maskOpt,sdir,tdir)
                else:
                    cmd='''rsync %s --include="%s" --exclude="*" "%s/" "%s/"'''%(rsyncOpt,maskOpt,sdir,tdir)
                cmd=cmd.replace('//','/')
                if(doud):
                    siz=runUD(cmd,sdir,year,docp=1)
                    allSiz=allSiz+siz
                else:
                    allCommands.append(cmd)
                    if(not(doWxmap2)):
                        mf.runcmd(cmd,ropt)
                    
                    
                if(verb): print 'CP--t1: ',sdir,ydir

            # -- zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzip
            #
            elif(dozip):
                ssdir="%s/%s"%(sdir,ydir)
                ssdir=ssdir.replace('//','/')
                ssdir=ssdir[0:-1]
                #print 'zzzzzzzzzzzz-ssdir',ssdir,' moddir:',moddir
                if(moddir != '' and doit and not(doud)):
                    MF.ChangeDir(moddir)
                (ssdir,year)=os.path.split(ssdir)
                zips=glob.glob("%s/*zip"%(ssdir))
                if(verb):
                    print 'ZZ--t1: ',ydir,'ss: ',ssdir,'#zips: ',len(zips),'year: ',year,'MMMM: ',moddir
                    if(len(zips) > 0):
                        for zip in zips:
                            siz=MF.GetPathSiz(zip)
                            siz=siz/(1024*1024)
                            print 'zip: ',zip,'siz: ',siz,' MB'
                            
                #ropt='norun'
                if(len(zips) == 0 and doit and not(doud)):
                    cmd="zip -r -m -u %s.zip %s/"%(year,year)
                    allCommands.append(cmd)
                    if(not(doWxmap2)):
                        mf.runcmd(cmd,ropt)
                    
                if(moddir != '' and doit and not(doud)):
                    MF.ChangeDir(ssdir)

                #tdir="%s/%s"%(tbdir,sdir)
                if(doWxmap2):
                    tdir='''%s/%s'''%(tbdir,tdir)
                    print 'not ready to do zip to wxmap2...sayounara'
                    sys.exit()
                else:
                    tdir=tdir.replace('/tc/','/tc-mike2/')
                
                cmd='''rsync %s --include="*%s*" --exclude="*" "%s/" "%s/"'''%(rsyncOpt,year,sdir,tdir)
                cmd=cmd.replace('//','/')

                if(doud): 
                    siz=runUD(cmd,sdir,year,dozip=1)
                    allSiz=allSiz+siz
                else:
                    allCommands.append(cmd)
                    if(not(doWxmap2)):
                        mf.runcmd(cmd,ropt)
                
            else:
                if(doWxmap2):
                    if(doWx2Reverse):
                        cmd='''rsync %s "%s/%s/" "%s/%s/"'''%(rsyncOpt,tdir,year,sdir,year)
                    else:
                        cmd='''rsync %s "%s/%s/" "%s/%s/"'''%(rsyncOpt,sdir,year,tdir,year)
                else:
                    cmd='''rsync %s "%s/%s/" "%s/%s/"'''%(rsyncOpt,sdir,year,tdir,year)
                cmd=cmd.replace('//','/')
                if(doud):
                    siz=-999.0
                    try:
                        iyear=int(year)
                        if(iyear < 2020): siz=0.0
                    except:
                        None
                        
                    #print 'sdir',sdir,year,'siz: ',siz
                    if(siz != 0.0):
                        siz=runUD(cmd,sdir,year)
                    allSiz=allSiz+siz
                    
                else:
                    allCommands.append(cmd)
                    if(not(doWxmap2)):
                        mf.runcmd(cmd,ropt)
                
    if(didsub == 0):
        #if(verb == 0): print 'AAAAAAA: ',sdir,'ttt: ',tdir
        if(doWxmap2):
            if(doWx2Reverse):
                cmd='''rsync %s "%s/" "%s/"'''%(rsyncOpt,tdir,sdir)
            else:
                cmd='''rsync %s "%s/" "%s/"'''%(rsyncOpt,sdir,tdir)
        else:
            cmd='''rsync %s "%s/" "%s/"'''%(rsyncOpt,sdir,tdir)
        cmd=cmd.replace('//','/')
        if(doud): 
            siz=runUD(cmd,sdir)
            allSiz=allSiz+siz
        else:
            allCommands.append(cmd)
            if(not(doWxmap2)):
                mf.runcmd(cmd,ropt)

if(doud):
    fallSiz=allSiz/(1024*1024)
    fallSiz=float(fallSiz)
    print 
    print 'allSiz: %10d KB %5.1f GB'%(allSiz,fallSiz)
               
               
MF.dTimer('ALL-tc-active')
     
nCmds=len(allCommands)
doCommands=[]

# -- don't do .dat in tcdat/tmtrkN
#
nallCommands=[]

for acmd in allCommands:
    if(mf.find(acmd,'tcdat/tmtrkN') or mf.find(acmd,'tc/tcanal')):
        nacmd=acmd.replace('''size-only''','''size-only --exclude="*.dat"''')
        nallCommands.append(nacmd)
    else:
        nallCommands.append(acmd)
        
allCommands=nallCommands

if(doByParts > 0 and doWxmap2):
    if(doByParts == 1):
        doCommands=allCommands[0:8]
    elif(doByParts == 2):
        doCommands=allCommands[8:16]
    elif(doByParts == 3):
        doCommands=allCommands[16:24]
    elif(doByParts == 4):
        doCommands=allCommands[24:nCmds]

    for cmd in doCommands:
        mf.runcmd(cmd,ropt)
                
sys.exit()
