#!/usr/bin/env python

from WxMAP2 import *
w2=W2()


class W2WebCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv

        self.argv=argv

        self.argopts={
            1:['dtgopt',    'no default'],
            }

        self.defaults={
            }

        self.options={
            'update':          ['u',0,1,'update wx.html index.htm'],
            'ropt':            ['N','','norun',' norun is norun'],
            'verb':            ['V',0,1,'verb=1 is verbose'],
            'doregen':         ['R',0,1,'regen to wxmap2a/'],
            'doRsync2Wx2':     ['x',0,1,'do rsync 2 wxmap2.com'],
            'doRsync2Wx2Only': ['X',0,1,'do rsync 2 wxmap2.com Only'],
            
            }

        self.purpose='''
purpose -- generate home page
%s dtg [-u]
'''
        self.examples='''
%s cur -u
'''

argv=sys.argv
CL=W2WebCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

tdtgs=mf.dtg_dtgopt_prc(dtgopt)

# -- check how old this run -- if 'tooold' force regen
#
howold=mf.dtgdiff(tdtgs[-1],curdtg)/24.0
tooold=(howold > w2.W2MaxOldRegen)
if(tooold and doregen == 0):  doregen=1

#ggggggggggggggggggggggggggg
#
# mf 20050817
#
#  update current grf dir with latest plots
#  before updating web page
#
#ggggggggggggggggggggggggggg

#if(doGrfupdate):

    #pdir=w2.wxpdWxmap
    #pcmd='wxmap.grf.current.update.py cur'
    #cmd="%s/%s"%(pdir,pcmd)
    #mf.runcmd(cmd,ropt)

template=w2.htmMainTemplate

setEcmModel=None
setNavModel=None

if(doregen):
    wdir=w2.wxhWeb=w2.wxhWeba
    setEcmModel='ecmt'
    setNavModel='ngpc'
    # -- hard wire here
    template="%s/template/wxmap.main.template.ecmt.txt"%(w2.wxhWeb)

wdir=w2.wxhWeb

for tdtg in tdtgs:

    htm=w2.HtmlWxmapMain(tdtg,curdtg,curphr,template,verb=verb,
                         setEcmModel=setEcmModel,setNavModel=setNavModel)

    wdtgpath="%s/wx.%s.htm"%(wdir,tdtg)
    print "IIII write dtg main htm: %s"%(wdtgpath)
    MF.WriteString2Path(htm,wdtgpath)

    if(update):
        wcurpath="%s/wx.htm"%(wdir)
        widxpath="%s/index.html"%(wdir)
        print "IIII write current main htm: %s  %s"%(wcurpath,widxpath)
        MF.WriteString2Path(htm,wcurpath)
        MF.WriteString2Path(htm,widxpath)
        
        print wdtgpath,wcurpath,widxpath

    

# -- rsync to wxmap2
#
if(doRsync2Wx2):
    rc=rsync2Wxmap2('wxmap2',ropt)


sys.exit()
