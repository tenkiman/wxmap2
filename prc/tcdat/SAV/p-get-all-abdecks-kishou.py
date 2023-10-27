#!/usr/bin/env python

from WxMAP2 import *

cmds=[
"""rsync --timeout=20    -alv --exclude-from=/w21/etc/ex-w21.txt fiorino@kishou.fsl.noaa.gov:/w21/dat/tc/bdeck/jtwc/ /w21/dat/tc/bdeck/jtwc/""",
"""rsync --timeout=20    -alv --exclude-from=/w21/etc/ex-w21.txt fiorino@kishou.fsl.noaa.gov:/w21/dat/tc/bdeck/nhc/ /w21/dat/tc/bdeck/nhc/""",

"""rsync --timeout=20    -alv --exclude-from=/w21/etc/ex-w21.txt fiorino@kishou.fsl.noaa.gov:/w21/dat/tc/adeck/tmtrkN/ /w21/dat/tc/adeck/tmtrkN/""",
"""rsync --timeout=20    -alv --exclude-from=/w21/etc/ex-w21.txt fiorino@kishou.fsl.noaa.gov:/w21/dat/tc/adeck/ncep/ /w21/dat/tc/adeck/ncep/""", 
"""rsync --timeout=20    -alv --exclude-from=/w21/etc/ex-w21.txt fiorino@kishou.fsl.noaa.gov:/w21/dat/tc/adeck/jtwc/ /w21/dat/tc/adeck/jtwc/""",
"""rsync --timeout=20    -alv --exclude-from=/w21/etc/ex-w21.txt fiorino@kishou.fsl.noaa.gov:/w21/dat/tc/adeck/nhc/ /w21/dat/tc/adeck/nhc/""",
"""rsync --timeout=20    -alv --exclude-from=/w21/etc/ex-w21.txt fiorino@kishou.fsl.noaa.gov:/w21/dat/tc/adeck/atcf-form/ /w21/dat/tc/adeck/atcf-form/""",
"""rsync --timeout=20    -alv --exclude-from=/w21/etc/ex-w21.txt fiorino@kishou.fsl.noaa.gov:/w21/dat/tc/adeck/ecmwf/ /w21/dat/tc/adeck/ecmwf/""",
"""rsync --timeout=20    -alv --exclude-from=/w21/etc/ex-w21.txt fiorino@kishou.fsl.noaa.gov:/w21/dat/tc/adeck/ukmo/ /w21/dat/tc/adeck/ukmo/""",
    ]

cmdsT=[
"""rsync --timeout=20    -alv --exclude-from=/w21/etc/ex-w21.txt fiorino@kishou.fsl.noaa.gov:/w21/dat/tc/adeck/tmtrkN/%s/ /w21/dat/tc/adeck/tmtrkN/%s/""",
#"""rsync --timeout=20    -alv --exclude-from=/w21/etc/ex-w21.txt fiorino@kishou.fsl.noaa.gov:/w21/dat/tc/tmtrkN/ /w21/dat/tc//tmtrkN/""",
    ]

cmds=[
"""rsync --timeout=20    -alv --exclude-from=/w21/etc/ex-w21.txt fiorino@kishou.fsl.noaa.gov:/w21/dat/tc/names/ /w21/dat/tc/names/""",
"""rsync --timeout=20  --include="md*" --exclude="*"  -alv --exclude-from=/w21/etc/ex-w21.txt fiorino@kishou.fsl.noaa.gov:/w21/dat/tc/DSs/ /w21/dat/tc/DSs/""",
    ]

# -- can now get from wxmap2.com
#
cmds=[]

years=[2007,2011]
years=range(2012,2020)
years=[2014,2019]
years=[2014,2015]
years=[2015]

ropt='norun'
ropt=''

for cmd in cmds:
    mf.runcmd(cmd,ropt)

for year in years:
    cyear=str(year)
    for cmd in cmdsT:
        cmd=cmd%(cyear,cyear)
        mf.runcmd(cmd,ropt)
    
