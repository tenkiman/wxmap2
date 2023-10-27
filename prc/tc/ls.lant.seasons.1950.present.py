#!/usr/bin/env python

import mf


byear=1950
eyear=2008
path="lant.storms.atcf.%s.%s.txt"%(byear,eyear)

for year in range(byear,eyear,1):
    cmd="/wxmap2/trunk/prc/tc/w2.tc.season.py %s l >> %s"%(year,path)
    mf.runcmd(cmd)

