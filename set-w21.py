#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# -- command line setup
#

class w2CmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv
        self.argopts={
            1:['computer',    'mike3 | mike5'],
        }

        self.options={
            'verb':                 ['V',0,1,'verb=1 is verbose'],
            'override':             ['O',0,1,'override for models'],
            'doIt':                 ['X','','norun',' norun is norun'],
        }

        self.defaults={

        }

        self.purpose='''
set the links in for web web-config and dat on mike3 and mike5
(c) 2009-%s Michael Fiorino,NOAA ESRL CIRES'''%(w2.curyear)

        self.examples='''
%s mike3 '''

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
# -- cmdline
#

argv=sys.argv

CL=w2CmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr
 
isC=(computer == 'mike3' or computer == 'mike5')

if(not(isC)):
    print 'EEE invalid computer:',computer,' only mike3 and mike5...'
    sys.exit()
    
ssdS={
'mike3':'ssd4',
'mike5':'ssd5',
}

is3=(computer == 'mike3')
is5=(computer == 'mike5')

rootLinks={
    'mike3':('/',{'w21':'/ssd4/wxmap2',
             }),
    
    'mike5':('/',{'w21':'ssd5/wxmap2',
             }),
    
}

datLinks={
    'mike3':('/w21/dat',{'nwp2':'/dat2/dat/nwp2',
             'ocean':'/ssd4/dat/ocean',
             'pr':'/dat16/dat/pr',
             'pr_era5':'/dat2/dat/pr/pr_era5',
             'tc':'/ssd4/dat/tc',
             'tc-dat13':'/dat13/dat/tc',
             }),
    
    'mike5':('/w21/dat',{'nwp2':'/dat9/dat/nwp2',
             'ocean':'/dat3/dat/ocean',
             'pr':'/dat3/dat/pr',
             'sBT':'/dat3/dat/sbt-v03',
             'tc':'/dat17/dat/tc',
             'tc-dat17':'/dat17/dat/tc',
             }),
    
}

webLinks={
    'mike3':('/w21',{
        'web':'/ssd4/products/wxmap2',
        'web-config':'/ssd4/web-config',
        })
}

webConfigLinks={
    'mike3':('/w21/web-config',{
        'jtdiag':'/ssd4/products/jtdiag',
        'tcact':'/ssd4/products/tcact',
        'tcdiag':'/ssd4/products/tcdiag',
        'tceps':'/ssd4/products/tceps',
        'tcgen':'/ssd4/products/tcgen',
        'tctrkveri':'/ssd4/products/tctrkveri',
    })
}

prodLinks={
    'mike3':('/w21/web-config',{
        'jtdiag':'/dat16/products/jtdiag',
        'tcact':'/dat16/products/tcact',
        'tcdiag':'/dat16/products/tcdiag',
        'tceps':'/dat16/products/tceps',
        'tctrkveri':'/dat16/products/tctrkveri',
    })
}    

prodDATLinks={
    'mike3':('/ssd4/products',{
        'jtdiagDAT':'/dat16/products/jtdiagDAT',
        'tcactDAT':'/dat16/products/tcactDAT',
        'tcdiagDAT':'/dat16/products/tcdiagDAT',
        'tcepsDAT':'/dat16/products/tcepsDAT',
        'tctrkveriDAT':'/dat16/products/tctrkveriDAT',
    })
}

allLinks={
    'mike3':(datLinks,webLinks,webConfigLinks,prodLinks,prodDATLinks),
    'mike5':(datLinks),
}


print 'ccc',computer,is3,is5
doRoot=0
switchSsd=1
ropt='norun'
if(doIt):
    ropt=''
    

if(is3):
    print '333'
    
    # -- first do the root of w21
    #
    if(doRoot):
        alink=rootLinks[computer]
        rootDir=alink[0]
        lnLinks=alink[1]
        MF.ChangeDir(rootDir)
        for lnl in lnLinks.keys():
            if((MF.ChkPath(lnl,verb=1) and os.path.islink(lnl)) or switchSsd ):
                cmd='sudo rm -i %s'%(lnl)
                mf.runcmd(cmd,ropt)
            else:
                print 'EEE lnl: ',lnl,' is not symbolic link...sayounara'
                sys.exit()
            cmd="sudo ln -s %s %s"%(lnLinks[lnl],lnl)
            mf.runcmd(cmd,ropt,doCommandPrompt=1)
        
    
    for alinks in allLinks[computer]:
        alink=alinks[computer]
        rootDir=alink[0]
        lnLinks=alink[1]
        MF.sTimer(rootDir)
        MF.ChangeDir(rootDir)
        MF.dTimer(rootDir)
        print

        for lnl in lnLinks.keys():
            #print 'lll',rootDir,lnl,lnLinks[lnl]
            if(MF.ChkPath(lnl,verb=1) and os.path.islink(lnl) or switchSsd):
                cmd='rm -i %s'%(lnl)
                mf.runcmd(cmd,ropt)
            elif(not(switchSsd)):
                print 'EEE lnl: ',lnl,' is not symbolic link...sayounara'
                sys.exit()
            cmd="ln -s %s %s"%(lnLinks[lnl],lnl)
            mf.runcmd(cmd,ropt)
            #print 'ccc',cmd
        