#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#
# command line setup
#
def RsyncPr2JetTheia4Kaze(source='qmorph',ropt=''):

    bdir="pr/model/pr_%smorph/grib/"%(source[0])
    
    tdirPRJ="%s/dat/%s"%(w2.W2WjetW2base,bdir)
    tdirPRT="%s/dat/%s"%(w2.W2TheiaW2base,bdir)
    tdirPRH="%s/dat/%s"%(w2.W2HeraW2base,bdir)

    tdirJ='%s@%s:%s'%(w2.WjetScpServerLogin,w2.WjetScpServer,tdirPRJ)
    tdirT='%s@%s:%s'%(w2.TheiaScpServerLogin,w2.TheiaScpServer,tdirPRT)
    tdirH='%s@%s:%s'%(w2.HeraScpServerLogin,w2.HeraScpServer,tdirPRH)
    
    sdirPR="%s/%s"%(w2.DatBdirW2data,bdir)
    cmd='''rsync --timeout=30 --protocol=29 -alv %s  "%s"'''%(sdirPR,tdirJ)
    mf.runcmd(cmd,ropt)

    cmd='''rsync --timeout=30 --protocol=29 -alv %s  "%s"'''%(sdirPR,tdirT)
    mf.runcmd(cmd,ropt)
    
    cmd='''rsync --timeout=30 --protocol=29 -alv %s  "%s"'''%(sdirPR,tdirH)
    mf.runcmd(cmd,ropt)
    
    return


class WgetCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            #1:['dtgopt',    'no default'],
            }

        self.defaults={
            }
        self.options={
            'override':         ['O',0,1,'override'],
            'verb':             ['V',0,1,'verb=1 is verbose'],
            'ropt':             ['N','','norun',' norun is norun'],
            'doit':             ['X',0,1,'execute'],
            }

        self.purpose='''
convert cpc qmorph from compressed binary to grib'''

        self.examples="""
%s 
%s -N"""




#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#


argv=sys.argv
CL=WgetCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

rc=RsyncPr2JetTheia4Kaze(source='qmorph',ropt=ropt)
rc=RsyncPr2JetTheia4Kaze(source='cmorph',ropt=ropt)


