#!/usr/bin/env python
from WxMAP2 import *

invfile='all-ecm5-dat16.txt'
invfile='all-ecm5-2023-dat83.txt'
cards=open(invfile).readlines()

doIt=0
doIt=1
sizMin=780
sizS={}
for card in cards:
    #print card[0:-1]
    tt=card.split()
    dtg=tt[0]
    #print(len(dtg))
    
    if(len(dtg) == 12):
        dtg=dtg[2:]
        siz=tt[-1].split(',')[0]
        #print 'ddd',dtg,siz
        sizS[dtg]=int(siz)
        
dtgs=sizS.keys()
dtgs.sort()

redos=[]
for dtg in dtgs:
    siz=sizS[dtg]
    if(siz < sizMin):
        redos.append(dtg)
        print 'sss',dtg,siz
 
if(not(doIt)):
    sys.exit()
     
#redos=[
#'2023071412',
#'2023072612',
#'2023080212',
#'2023081612',
#'2023082312',
#'2023082412',
#'2023082612',
#'2023090212',
#'2023090612',
#'2023090912',
#'2023091912',
#]

ropt='norun'
ropt=''

for redo in redos:
    cmd="do-ecm5.py %s -J -O"%(redo)
    mf.runcmd(cmd,ropt)
