#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

#cmd='''find -L %s/ -xtype l -name "fort.??" -exec rm {} \;'''%(w2.TcDatDir)
cmd='''find -L %s/ -xtype l -name "fort.??" '''%(w2.TcDatDir)
cmd='''find -L %s// -xtype l  -exec rm -v {} \;'''%(w2.TcDatDir)
mf.runcmd(cmd)
