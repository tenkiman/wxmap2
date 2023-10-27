#!/usr/bin/env python

from WxMAP2 import *

bdir='/usb2/dat/tc-mike3'
#bdir='/usb2/dat/tc-mike2'
MF.ChkDir(bdir,'mk')
MF.ChangeDir(bdir)

tcdirs=[
    
'adeck/cmc',
'adeck/ecmwf',
'adeck/esrl',
'adeck/jtwc',
'adeck/ncep',
'adeck/nhc',
'adeck/ukmo',
'adeck/mftrkN',
'adeck/tmtrkN',
'adeck/atcf-form',
'bdeck/nhc',
'bdeck/jtwc',
'cmc/tigge',
'carq',
'bt',
'cira/mtcswa',
'ecmwf',
'ncep/tigge',
'mdeck',
'stext',
'tceps/cmc',
'tceps/ecmwf',
'tceps/ncep',
'tcgen',
'tmtrkN',
'ukmo/tigge',

]


tcdirsAll=[
'adeck/2019/',
'adeck/2020/',
'adeck/atcf-form/2019/',
'adeck/atcf-form/2020/',
'adeck/cmc/',
'adeck/cmc/2020/',
'adeck/ecmwf/2019/',
'adeck/esrl/2018/',
'adeck/esrl/2019/',
'adeck/esrl/2020/',
'adeck/jtwc/2019/',
'adeck/jtwc/2020/',
'adeck/mftrkN/2019/',
'adeck/mftrkN/2020/',
'adeck/ncep/2019/,'
'adeck/ncep/2020/',
'adeck/nhc/2018/',
'adeck/nhc/2019/',
'adeck/nhc/2020/',
'adeck/tmtrkN/2019/',
'adeck/tmtrkN/2020/',
'adeck/ukmo/',
'adeck/ukmo/2020/',
'bdeck/jtwc/2019/',
'bdeck/jtwc/2020/',
'bdeck/nhc/2019/',
'bdeck/nhc/2020/',
'bt/2019/',
'bt/2020/',
'carq/2019/',
'carq/2020/',
'cira/mtcswa/',
'cira/mtcswa/2020/',
'climo/',
'cmc/tigge/2019/',
'cmc/tigge/2020/',
'com/',
'dis/',
'DSs/',
'ecmwf/wmo-essential/',
'edeck/',
'fdeck/',
'jtwc/',
'mdeck/2019/',
'mdeck/2020/',
'names/',
'ncep/tigge/',
'ncep/tigge/2020/',
'nhc/',
'stext/nhc/',
'stext/jtwc/',
'tcanal/',
'tcanal/2020/',
'tceps/cmc/',
'tceps/cmc/2020/',
'tceps/ecmwf/',
'tceps/ecmwf/2020/',
'tceps/ncep/',
'tceps/ncep/2020/',
'tcgen/2019/',
'tcgen/2020/',
'tcvitals/',
'tmtrkN/2019/',
'tmtrkN/2020/',
'ukmo/tigge/',
'ukmo/tigge/2020/',

]

ropt='norun'
ropt=''

for tcd in tcdirsAll:
    cmd="mkdir -p %s"%(tcd)
    mf.runcmd(cmd,ropt)

    
