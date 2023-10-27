#!/usr/bin/env python

from WxMAP2 import *
w2=W2()
MF=MFutils()

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#

class MssCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['yearOpt',    'no default'],
            }

        self.defaults={
            }

        self.options={
            'verb':          ['V',0,1,'verb=1 is verbose'],
            'ropt':          ['N','','norun',' norun is norun'],
            'doTxtInv':      ['I',0,1,'make txt inv?'],
            'usb2':          ['2',0,1,'usb2'],
            'unzip':         ['u',0,1,'unzip in prep for rsync'],
            'sourceOpt':     ['S:',None,'a',"""source: 'tmtrkN' | 'mftrkN' | 'trk-tmtrkN'"""],
            'rsync2to3':     ['R',0,1,'rsync usb2 to mike3'],
            'moOpt':         ['M:',None,'a','month Opt'],
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

# -- handle single dtg
#
if(mf.find(yearOpt,'cur')): 
    dtgs=mf.dtg_dtgopt_prc(yearOpt)
    # -- use first one
    yearOpt=dtgs[0]
    
doDtgOnly=0
if(len(yearOpt) == 10):
    years=[yearOpt[0:4]]
    moOpt=yearOpt[4:6]
    doDtgOnly=1
    
else:
    tt=yearOpt.split('.')
    if(mf.find(yearOpt,'cur')):
        years=[curyear]
        months=[int(curdtg[4:6])]
        
    elif(len(tt) == 1):
        years=[yearOpt]
    else:
        years=mf.yyyyrange(tt[0],tt[-1], inc=1)
    
# -- MMM month
#
if(moOpt != None and moOpt == 'all'):
    months=range(1,13)
else:
    tt=moOpt.split('.')
    if(len(tt) == 2):
        bmo=int(tt[0])
        emo=int(tt[1])
        months=range(bmo,emo+1)
    elif(len(tt) == 1):
        if(mf.find(moOpt,'cur')):
            CL.ls()
        else:
            months=[int(moOpt)]
            

sources=['tmtrkN','mftrkN','trk-tmtrkN']
#sources=['tmtrkN','mftrkN']
if(sourceOpt != None):
    sources=[sourceOpt]
    
# -- check of tmtrkN running and sourceOpt is 'trk-tmtrkN'
#
if(sourceOpt == 'trk-tmtrkN'):
    job='w2-tc-tmtrkN.py'
    rc=MF.chkRunning(job,strictChkIfRunning=0,
                     killjob=0, verb=verb, nminWait=0)
    print 'RRRRRRRRRRRRRRRRRRRRRRRRRRRCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC',rc
    if(rc > 1):
        print 'WWW-bailing because two or more tmtrkN are running and doing sourceOpt: ',sourceOpt
        sys.exit()
    
    
MF.sTimer('all-zip-adeck')
for year in years:

    for source in sources:
        
        sbdir=w2.TcDatDir
        if(usb2): sbdir='/usb2/dat/tc-mike2'
        if(source == 'trk-tmtrkN'):
            sdir="%s/tmtrkN"%(sbdir)
            tbdir="%s/%s"%(sdir,year)
            MF.ChkDir(tbdir,'mk')
            tdir="./%s"%(year)
        else:
            sdir="%s/adeck/%s/%s"%(sbdir,source,year)
            tdir='.'
            
        # -- SSSSS -- change to source
        #
        rc=MF.ChangeDir(sdir)
    
        if(rc == 0): 
            print 'WWW -- cannot change to sdir: ',sdir,'sayounara...'
            sys.exit()

        for mo in months:

            # -- rsync between usb2 and mike3
            #
            if(rsync2to3):
                
                yyyymm="%s%02d"%(year,mo)

                sbdir2='/usb2/dat/tc-mike2'
                sbdir3=w2.TcDatDir
                
                if(source == 'trk-tmtrkN'):
                    sdir2="%s/tmtrkN/%s"%(sbdir2,year)
                    sdir3="%s/tmtrkN/%s"%(sbdir3,year)
                else:
                    sdir2="%s/adeck/%s/%s"%(sbdir2,source,year)
                    sdir3="%s/adeck/%s/%s"%(sbdir3,source,year)
                
                # -- first unzip
                #
                dozip2=0
                dozip3=0
                
                MF.ChangeDir(sdir2)
                zipfile2='%s-%s%02d.zip'%(source,year,mo)
                siz2=MF.GetPathSiz(zipfile2)
                if(siz2 > 0): dozip2=1
                
                if(dozip2):
                    print '2222222222',zipfile2,'SS: ',siz2
                    zipcmd="unzip -o %s"%(zipfile2)
                    mf.runcmd(zipcmd,ropt)
                
                MF.ChangeDir(sdir3)
                zipfile3='%s-%s%02d.zip'%(source,year,mo)
                siz3=MF.GetPathSiz(zipfile3)
                if(siz3 > 0): dozip3=1
                
                if(dozip3):
                    print '3333333333',zipfile3,'SS: ',siz3
                    zipcmd="unzip -o %s"%(zipfile3)
                    mf.runcmd(zipcmd,ropt)
                 
                # -- do the rsync
                #
                rsyncOpt='-alv'
                cmd2to3='''rsync %s --exclude "*.zip" --include "*%s*" --size-only %s/ %s/'''%(rsyncOpt,yyyymm,sdir2,sdir3)
                cmd3to2='''rsync %s --exclude "*.zip" --include "*%s*" --size-only %s/ %s/'''%(rsyncOpt,yyyymm,sdir3,sdir2)
                
                if(dozip2):
                    mf.runcmd(cmd2to3,ropt)
                if(dozip3):
                    mf.runcmd(cmd3to2,ropt)
                
                # -- now zip up
                #
                MF.ChangeDir(sdir2)
                zipcmd2="zip %s -u -m -r %s%02d????"%(zipfile2,year,mo)
                mf.runcmd(zipcmd2,ropt)
                
                MF.ChangeDir(sdir3)
                zipcmd3="zip %s -u -m -r %s%02d????"%(zipfile3,year,mo)
                mf.runcmd(zipcmd3,ropt)

                continue
            # -- clean up
            #
            if(not(unzip)):

                if(source == 'tmtrkN'):
                    rmcmd="rm %s%02d????/tctrk.*.*.???.txt"%(year,mo)
                    mf.runcmd(rmcmd,ropt)
                    
                elif(source == 'trk-tmtrkN'):
                    rmC='rm'
                    #rmC='ls -la'
                    if(doDtgOnly):
                        rmcmd="%s %s/*/*.pyp"%(rmC,yearOpt)
                        mf.runcmd(rmcmd,ropt)
                        
                        rmcmd="%s %s/*/*grb*"%(rmC,yearOpt)
                        mf.runcmd(rmcmd,ropt)
                        
                        rmcmd="%s %s/*/*.dat"%(rmC,yearOpt)
                        mf.runcmd(rmcmd,ropt)
                        
                        rmcmd="%s %s/*/fort.*"%(rmC,yearOpt)
                        mf.runcmd(rmcmd,ropt)
            
                        
                    else:
                        rmcmd="%s %s%02d????/*/*.pyp"%(rmC,year,mo)
                        mf.runcmd(rmcmd,ropt)
                        
                        rmcmd="%s %s%02d????/*/*grb*"%(rmC,year,mo)
                        mf.runcmd(rmcmd,ropt)
                        
                        rmcmd="%s %s%02d????/*/*.dat"%(rmC,year,mo)
                        mf.runcmd(rmcmd,ropt)
                        
                        rmcmd="%s %s%02d????/*/fort.*"%(rmC,year,mo)
                        mf.runcmd(rmcmd,ropt)
            
            
            zipfile='%s/%s-%s%02d.zip'%(tdir,source,year,mo)
            
            if(unzip):
                zipcmd="unzip -o %s"%(zipfile)
                mf.runcmd(zipcmd,ropt)
                
            else:

                if(doDtgOnly):
                    zipcmd="zip %s -u -m -r %s"%(zipfile,yearOpt)
                else:
                    zipcmd="zip %s -u -m -r %s%02d????"%(zipfile,year,mo)
                mf.runcmd(zipcmd,ropt)

            if(doTxtInv):
                invfile='%s/%s-%s%02d-inv.txt'%(tdir,source,year,mo)
                unzipcmd="unzip -l %s > %s"%(zipfile,invfile)
                mf.runcmd(unzipcmd,ropt)

MF.dTimer('all-zip-adeck')
