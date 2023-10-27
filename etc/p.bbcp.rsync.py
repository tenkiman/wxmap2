#!/usr/bin/env python

from M import *

MF=MFutils()


def bbcpSyncTrackFiles(sdir,tdir,fmask,dtg,ropt='norun',verb=0):

    bbcpcmd='bbcp -f -v -w 1M -s 64'
    jetscp='fiorino@137.75.21.111'
    
    tfiles=[]
    sfiles=[]

    cmd="ssh fiorino@137.75.21.111 ls -l %s/"%(tdir)
    cards=os.popen(cmd).readlines()
    for card in cards:
        card=card.strip()
        tt=card.split()
        if(len(tt) <= 2): continue
        tpath=tt[-1]
        tsize=long(tt[4])
        (dir,file)=os.path.split(tpath)
        if(verb): print 'TTTTTTTTTTTTTTTTTTTTTT ',card,tpath,tsize
        tfiles.append((file,tsize))

    cmd="ls -l %s/%s.%s"%(sdir,fmask,dtg[2:4])
    cards=os.popen(cmd).readlines()

    for card in cards:
        card=card.strip()
        tt=card.split()
        spath=tt[-1]
        (dir,file)=os.path.split(spath)
        ssize=MF.GetPathSiz(spath)
        if(verb): print 'SSSSSSSSSSSSSSSSSSSSSSS ',card,spath,ssize

	sfiles.append((file,ssize))


    getfiles=[]
    
    tfiles.sort()
    sfiles.sort()

    for (sfile,ssize) in sfiles:
        gotit=0
        for (tfile,tsize) in tfiles:
            if(sfile == tfile and ssize == tsize):
                gotit=1

        if(gotit == 0):
            getfiles.append(sfile)


    if(verb): print 'gggggggggggggg ',getfiles
    
    if(len(getfiles) > 0):
        cmd=bbcpcmd
        for getfile in getfiles:
            cmd="%s %s/%s "%(cmd,sdir,getfile)
        
    
        cmd="%s %s:/%s/."%(cmd,jetscp,tdir)
        mf.runcmd(cmd,ropt)
        


def bbcpSyncFiles(sdir,tdir,dtg,ropt='norun'):


    bbcpcmd='bbcp -f -v -w 1M -s 64'
    jetscp='fiorino@137.75.21.111'
    
    tfiles=[]
    sfiles=[]

    cmd="ssh fiorino@137.75.21.111 ls %s/"%(tdir)
    cards=os.popen(cmd).readlines()
    for card in cards:
	card=card.strip()
	if(mf.find(card,dtg[4:])):
            print 'remote: ',card[0:-1]
            tfiles.append(card)

    cmd="ls %s/*%s*"%(sdir,dtg[4:])
    cards=os.popen(cmd).readlines()

    for card in cards:
        print 'local:  ',card[0:-1]
        card=card.strip()
        (dir,file)=os.path.split(card)
	if(mf.find(card,dtg[4:])):
            print 'local:  ',card[0:-1]
            sfiles.append(file)


    getfiles=[]
    
    tfiles.sort()
    sfiles.sort()

    for sfile in sfiles:
        gotit=0
        for tfile in tfiles:
            if(sfile == tfile):
                gotit=1

        if(gotit == 0):
            getfiles.append(sfile)



    if(len(getfiles) > 0):
        cmd=bbcpcmd
        for getfile in getfiles:
            cmd="%s %s/%s "%(cmd,sdir,getfile)
        
    
        cmd="%s %s:/%s/."%(cmd,jetscp,tdir)
        mf.runcmd(cmd,ropt)
        
        
    

	






#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
#

class MFCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            1:['dtgopt',    'no default'],
            }

        self.options={
            'verb':['V',0,1,'verb=1 is verbose'],
            'ropt':['N','','norun',' norun is norun'],
            'override':['O',0,1,'override'],
            'doinventory':['I',1,0,"""do NOT do inventory for gfsenkf.php """],
            'doKlean':['K',1,0,'1 - os.unlink fort.?? and i/o files'],
            'dorsync':['R',1,0,"""do NOT rsync plots from wjet to /data/projects/hftp/gfsenkfDAt """],
            }

        self.purpose="""
purpose -- create .ctl for gfsenkf
"""
        self.examples='''
%s cur-12
'''


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
# main
#


argv=sys.argv
CL=MFCmdLine(argv=argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

dtgs=mf.dtg_dtgopt_prc(dtgopt,opsfhr=3.0)
print 'dddddddddddd ',dtgs

# --------------------- ecnogaps
#

sdir='/ptmp/wx52jw/ecnogaps'
tdir='/lfs1/projects/fim/fiorino/w21/dat/ecnogaps'

for dtg in dtgs:
    rc=bbcpSyncFiles(sdir,tdir,dtg,ropt)

# ---------------------  track.atcfunix.10
#
sdir='/com/hur/prod/global'
tdir='/lfs1/projects/fim/fiorino/w21/dat/ncep/com/hur/prod/global'
fmask="tracks.atcfunix"

for dtg in dtgs:
    rc=bbcpSyncTrackFiles(sdir,tdir,fmask,dtg,ropt,verb=verb)


# -------------------- genstrack
#

sdir='/ptmp/wx52jw/genstracks'
tdir='/lfs1/projects/fim/fiorino/w21/dat/genstracks'
pdir='/u/wx80mf/w21/prc'

cmd='''rsync -e ssh -alv --delete --exclude-from="%s/ex-genstracks.txt" /%s/ fiorino@137.75.21.111:/%s/'''%(pdir,sdir,tdir)
mf.runcmd(cmd,ropt)



