#!/usr/bin/env python

from M import *
MF=MFutils()

from WxMAP2 import *
w2=W2()


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
            'ropt':         ['N','','norun',' norun is norun'],
            'dotc':         ['T',0,1,'do all clean'],
            'doall':        ['A',0,1,''],
            'keepPSlog':      ['P',1,0,'keep off ps files'],
            }

        self.defaults={
            }

        self.purpose='''
clean log files
(c) 2009-2012 Michael Fiorino,NOAA ESRL'''

        self.examples='''
%s -A'''

CL=w2CmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

ndayKeepPsMon=3

if(doall):
    MF.ChangeDir(w2.LogBdirW2,verb=verb)
    logfiles=glob.glob("log*") + glob.glob("out_*")
    for logfile in logfiles:
        if(mf.find(logfile,'LOGCLEAN') or (mf.find(logfile,'.PS') and keepPSlog)):
            print 'skipping....',logfile
        else:
            if(ropt == ''):
                print 'killing: logfile',logfile
                os.unlink(logfile)
            else:
                print 'WILL killing: logfile',logfile
                
    psmonFiles=glob.glob('w2-ps-mon*')
    for psmon in psmonFiles:
        psdtg=psmon.split('.')[4]
        psdiff=mf.dtgdiff(psdtg,curdtg)
        if(psdiff/24.0 <= ndayKeepPsMon):
            print 'keeping w2-ps-mon: ',psmon
        else:
            if(ropt == ''):
                print 'killing w2-ps-mon: ',psmon
                os.unlink(psmon)
            else:
                print 'WILL kill w2-ps-mon: ',psmon
    #cmd="rm log-w2.*"
    #mf.runcmd(cmd,ropt)

elif(dotc):
    MF.ChangeDir(w2.LogBdirW2)
    cmd="rm log-w2.tc.*"
    mf.runcmd(cmd,ropt)


