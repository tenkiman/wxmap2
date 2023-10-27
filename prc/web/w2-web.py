#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

#import wxmap

#llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
#
# local defs
#

def CleanModelAreaHtm(dtg,model,areaopt,ropt=''):

    htmrootdir=w2.wxhWeb
    rc=0

    if(areaopt == 'all'):
        areas=w2.W2_AREAS
    else:
        areas=[areaopt]

    if(model == 'all'):
        models=w2.wxModels2
    else:
        models=[model]

    for model in models:
        for area in areas:
            hmodel=w2.Model2Model2PlotModel(model)
            htmmask="%s/web_%s/%s/*%s.htm"%(htmrootdir,hmodel,dtg,area)
            cmd="rm %s"%(htmmask)
            mf.runcmd(cmd,ropt)
            rc=1

    return(rc)
    



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
            'model':           ['m:','all','a','stmopt'],
            'areaopt':         ['a:','all','a','stmopt'],
            'update':          ['u',0,1,'update wx.html index.htm'],
            'ropt':            ['N','','norun',' norun is norun'],
            'verb':            ['V',0,1,'verb=1 is verbose'],
            'doGrfupdate':     ['G',0,1,'doGrfupdate - '],
            'doregen':         ['R',0,1,'doregen - '],
            'dorsync':         ['r',0,1,'dorsync - '],
            'docleanhtm':      ['C',0,1,'clear off .htm'],
            'dopublic':        ['P',0,1,'dopublic - '],
            'domain':          ['M',1,0,'do NOT do main'],
            'doRsync2Wx2':     ['x',1,0,'do rsync 2 wxmap2.com default is yes'],
            'doRsync2Wx2Only': ['X',0,1,'do rsync 2 wxmap2.com Only'],
            }

        self.purpose='''
purpose -- generate wxmap2 web
%s dtg [-u]
'''
        self.examples='''
%s cur -u
'''
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#  
# main
#
#

argv=sys.argv
CL=W2WebCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

MF.ChangeDir(w2.PrcDirWebW2)

tdtgs=mf.dtg_dtgopt_prc(dtgopt)


for dtg in tdtgs:

    # -- check how old this run -- if 'tooold' force regen
    #
    howold=mf.dtgdiff(dtg,curdtg)/24.0
    tooold=(howold > w2.W2MaxOldRegen)
    if(tooold):  doregen=1

    if(doregen):
        w2.W2_BDIRWEB=w2.W2_BDIRWEBA
        dorsync=0


    MF.sTimer(tag='chkifrunning')
    rc=w2.ChkIfRunningNWP(dtg,pyfile,model)
    if(rc > w2.nMaxPidInCron and w2.dochkifrunning):
        if(ropt != 'norun'):
            print 'AAA allready running...sayounara'
            sys.exit()
    MF.dTimer(tag='chkifrunning')

    if(docleanhtm):
        rc=CleanModelAreaHtm(dtg,model,areaopt)

    if(not(doregen)):
        eventtype='web'
        eventtag='HTML-H-'
        w2.PutEvent(pyfile,eventtype,eventtag,model,dtg,areaopt)

    wxpre='wxmap'
    #if(doregen): wxpre='wxmapa'

    #
    # make htm, movie then main
    #

    if(dopublic):
        cmd="%s.htm.Pub.pl %s %s %s"%(wxpre,dtg,areaopt,model)
    else:
        cmd="%s.htm.pl %s %s %s"%(wxpre,dtg,areaopt,model)
    mf.runcmd(cmd,ropt)

    if(dopublic):
        if(areaopt == 'all'):
            cmd="%s.movie.js.Pub.pl %s all %s"%(wxpre,dtg,model)
        else:
            cmd="%s.movie.js.Pub.pl %s %s %s"%(wxpre,dtg,areaopt,model)
    else:
        if(areaopt == 'all'):
            cmd="%s.movie.js.pl %s all %s"%(wxpre,dtg,model)
        else:
            cmd="%s.movie.js.pl %s %s %s"%(wxpre,dtg,areaopt,model)

    mf.runcmd(cmd,ropt)

    if(not(doregen)):
        eventtag='HTML-M-'
        w2.PutEvent(pyfile,eventtype,eventtag,model,dtg,areaopt)


    updateopt=''
    if(update): updateopt='-u'

    pubopt=''
    archopt=''
    if(doregen): archopt="-R"
    if(dopublic):  pubopt="-P"
    if(not(domain)):
        print 'III doing just model/area html...'
        continue
        
    cmd="w2-web-main.py %s %s %s %s"%(dtg,updateopt,archopt,pubopt)
    mf.runcmd(cmd,ropt)
    
# -- archive
#
cmd="wxmap.web.archive.pl"
mf.runcmd(cmd,ropt)
    
# -- rsync to wxmap2
#
if(doRsync2Wx2):
    rc=rsync2Wxmap2('wxmap2',ropt)



