#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

ropt='norun'
ropt=''
misspath="/ptmp/missing-ecmt.txt"
cards=open(misspath).readlines()

dodtgs=[]
for card in cards:
    tt=card.split()
    if(len(tt) > 1):
        dtg=tt[1]
    else:
        break
    
    if(mf.find(dtg,'Z') or mf.find(dtg,'L') or mf.find(dtg,'N')):
        dodtg=dtg.split('-')[1]
        dodtgs.append(dodtg)
    if(mf.find(tt[0],'exit')): break
    


for dodtg in dodtgs:
    cmd="w2.fld.tigge.ecmwf.py %s -O -t"%(dodtg)
    mf.runcmd(cmd,ropt)

#ecmt   N-2016021400  999    999.90     0 <--- NO DATA localdir: /w21/dat/nwp2/w2flds/dat/ecmt/2016021400
#ecmt   N-2016031012  999    999.90     0 <--- NO DATA localdir: /w21/dat/nwp2/w2flds/dat/ecmt/2016031012
#ecmt   N-2016032300  999    999.90     0 <--- NO DATA localdir: /w21/dat/nwp2/w2flds/dat/ecmt/2016032300
#ecmt   N-2016051600  999    999.90     0 <--- NO DATA localdir: /w21/dat/nwp2/w2flds/dat/ecmt/2016051600
#ecmt   N-2016052500  999    999.90     0 <--- NO DATA localdir: /w21/dat/nwp2/w2flds/dat/ecmt/2016052500
#ecmt   N-2016062800  999    999.90     0 <--- NO DATA localdir: /w21/dat/nwp2/w2flds/dat/ecmt/2016062800
#ecmt   N-2016062900  999    999.90     0 <--- NO DATA localdir: /w21/dat/nwp2/w2flds/dat/ecmt/2016062900

# dtg:  L-2016020600 2016020600
# dtg:  Z-2016021400 2016021400
# dtg:  Z-2016021500 2016021500
# dtg:  Z-2016021600 2016021600
# dtg:  Z-2016021700 2016021700
# dtg:  Z-2016021800 2016021800
# dtg:  N-2016022300 2016022300
# dtg:  N-2016031000 2016031000
# dtg:  N-2016031012 2016031012
# dtg:  N-2016031100 2016031100
# dtg:  N-2016031112 2016031112
# dtg:  N-2016031200 2016031200
# dtg:  N-2016031212 2016031212
# dtg:  N-2016031300 2016031300
# dtg:  N-2016031312 2016031312
# dtg:  N-2016032000 2016032000
# dtg:  N-2016032012 2016032012
# dtg:  N-2016032100 2016032100
# dtg:  N-2016032112 2016032112
# dtg:  N-2016032200 2016032200
# dtg:  N-2016032212 2016032212
# dtg:  N-2016032300 2016032300
# dtg:  Z-2016051400 2016051400
# dtg:  Z-2016051500 2016051500
# dtg:  Z-2016051600 2016051600
# dtg:  Z-2016051700 2016051700
# dtg:  Z-2016051800 2016051800
# dtg:  L-2016051812 2016051812
# dtg:  Z-2016051900 2016051900
# dtg:  Z-2016052000 2016052000
# dtg:  Z-2016052100 2016052100
# dtg:  Z-2016052200 2016052200
# dtg:  Z-2016052300 2016052300
# dtg:  L-2016052312 2016052312
# dtg:  Z-2016052400 2016052400
# dtg:  L-2016052412 2016052412
# dtg:  Z-2016052500 2016052500
# dtg:  Z-2016052600 2016052600
# dtg:  Z-2016052700 2016052700
# dtg:  Z-2016052800 2016052800
# dtg:  Z-2016052900 2016052900
# dtg:  Z-2016053000 2016053000
# dtg:  Z-2016053100 2016053100
# dtg:  Z-2016060100 2016060100
# dtg:  Z-2016060200 2016060200
# dtg:  Z-2016060300 2016060300
# dtg:  Z-2016060400 2016060400
# dtg:  Z-2016060500 2016060500
# dtg:  Z-2016060600 2016060600
# dtg:  Z-2016060700 2016060700
# dtg:  Z-2016060800 2016060800
# dtg:  Z-2016060900 2016060900
# dtg:  Z-2016061000 2016061000
# dtg:  Z-2016062600 2016062600
# dtg:  Z-2016062700 2016062700
# dtg:  Z-2016062800 2016062800
