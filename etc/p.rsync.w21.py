#!/usr/bin/env python

"""%s

purpose:

rsync  kishou://w21 <-> wjet 

usages:

-N -- nrun
-X -- run
-D -- 2wjet | 2kishou | 2linux | 2tacc | 4linux | 4tacc 
-u -- update mode

"""

import os
import sys
import time
import getopt

import mf

#ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss

curdtg=mf.dtg()
curtime=mf.dtg('curtime')
curphr=mf.dtg('phr')
curdir=os.getcwd()

pyfile=sys.argv[0]

roptopt='norun'
doupdate=0

narg=len(sys.argv)-1

i=1
if(narg >= 2):

    try:
        (opts, args) = getopt.getopt(sys.argv[1:], "NXD:u")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime)
        print "EEE invalid getopt opt"
        sys.exit(2)

    for o, a in opts:
        if o in ("-N",""): roptopt='norun'
        if o in ("-X",""): roptopt=''
        if o in ("-D",""): direction=a
        if o in ("-u",""): doupdate=1

else:
    mf.usage(__doc__,pyfile,curdtg,curtime)
    sys.exit(2)


taccdirs=['prc/fim','prc/lib','etc','prc/flddat','prc/hfip']

if(direction == '2kishou'):

    sw21='/lfs1/projects/fim/fiorino/w21'
    ssvr='fiorino@jetscp.rdhpcs.noaa.gov:'
    tw21='/w21'
    tsvr=''
    dirs=['prc/wxmap2','prc/fim','prc/fimbao','prc/lib','etc','prc/flddat']
    
elif(direction == '2tacc'):

    sw21='/w21'
    ssvr=''
    tw21='/work/01233/mfiorino/w21'
    tsvr='mfiorino@ranger.tacc.utexas.edu:'
    dirs=taccdirs
    
elif(direction == '4tacc'):

    tw21='/w21'
    tsvr=''
    sw21='/work/01233/mfiorino/w21'
    ssvr='mfiorino@ranger.tacc.utexas.edu:'
    dirs=taccdirs
    
elif(direction == '2wjet'):

    sw21='/w21'
    ssvr=''
    tw21='/lfs1/projects/fim/fiorino/w21'
    tsvr='fiorino@jetscp.rdhpcs.noaa.gov:'
    dirs=['prc','etc']

elif(direction == '2linux'):

    sw21='/mnt/hgfs/dat1/w21'
    ssvr=''
    tw21='/w21'
    tsvr=''
    dirs=['prc','etc']

elif(direction == '4linux'):

    sw21='/w21'
    ssvr=''
    tw21='/mnt/hgfs/dat1/w21'
    tsvr=''
    dirs=['prc','etc']

else:

    print 'EEEEEEEE invalid direction -- no defualts'
    print 'either 2wjet -- rsync kishou -> wjet'
    print '       2kishou -- rsync wjet --> kishou'
    print '       2linux -- rsync kishou.linux--> kishou.mac'
    sys.exit()
    
    


for dir in dirs:

    print 'rsync dir: ',dir
    exfile='ex-w21.txt'
    uopt=''
    if(doupdate): uopt='-u'
    
    if(roptopt == 'norun'):
        xopt='-n'
	ropt=''
    elif(roptopt == ''):
        xopt=''
        ropt=''
        
    #
    # now rsync from storage5 to kishou
    #
    cmd="rsync --exclude-from=%s -alv %s %s \"%s%s/%s/.\"  \"%s%s/%s/.\""%(exfile,xopt,uopt,ssvr,sw21,dir,tsvr,tw21,dir)
    mf.runcmd(cmd,ropt)










