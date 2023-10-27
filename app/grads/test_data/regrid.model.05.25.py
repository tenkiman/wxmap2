#!/usr/bin/env python

import mf

ropt='norun'
ropt=''

gb2cmd='/nwprod/util/exec/copygb2'
cnvcmd='/nwprod/util/exec/cnvgrib'

taus=range(0,73,24)

for tau in taus:
    print 'tau: ',tau
    i2file="model.f%03d.grb2"%(tau)
    o2file="model.25.f%03d.grb2"%(tau)
    o1file="model.25.f%03d.grb1"%(tau)
    grid="\"0 6 0 0 0 0 0 0 144 73 0 0 90000000 0 48 -90000000 357500000 2500000 2500000 0\""
    recmd="%s -x -g %s %s %s"%(gb2cmd,grid,i2file,o2file)
    mf.runcmd(recmd,ropt)

    g21cmd="%s -g21 %s %s"%(cnvcmd,o2file,o1file)
    mf.runcmd(g21cmd,ropt)




  
    
