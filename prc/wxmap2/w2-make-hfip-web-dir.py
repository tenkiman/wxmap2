#!/usr/bin/env python

from WxMAP2 import *
w2=W2()

w2.ls('EnvVar')

hd=w2.W2EnvVarHfipDat
hh=w2.W2EnvVarHfip
hw=w2.W2EnvVarWeb

print 'dddddddddd',hd
MF.ChangeDir(hd)
Ddirs=['jtdiagDAT','tcactDAT','tcdiagDAT','tcepsDAT','tcgenDAT']

for dd in Ddirs:
    print dd

MF.ChangeDir(hh)
mf.runcmd('ls -l','')


#lrwxrwxr-x. 3 fiorino fiorino 4096 Mar 14  2019 fiorino
#lrwxrwxrwx. 1 fiorino fiorino   23 Mar 14  2019 jtdiag -> /w21/web-config/jtdiag/
#lrwxrwxrwx. 1 fiorino fiorino   48 Sep 13  2020 jtdiagDAT -> $W2_HFIP/hfip/jtdiagDAT/
#lrwxrwxrwx. 1 fiorino fiorino   22 Mar 14  2019 tcact -> /w21/web-config/tcact/
#lrwxrwxrwx. 1 fiorino fiorino   47 Sep 13  2020 tcactDAT -> $W2_HFIP/hfip/tcactDAT/
#lrwxrwxrwx. 1 fiorino fiorino   23 Mar 14  2019 tcdiag -> /w21/web-config/tcdiag/
#lrwxrwxrwx. 1 fiorino fiorino   48 Sep 13  2020 tcdiagDAT -> $W2_HFIP/hfip/tcdiagDAT/
#lrwxrwxrwx. 1 fiorino fiorino   25 May 18 21:32 tcdiagDAT0 -> /dat13/dat/tc/tcdiagDAT0/
#drwxrwxr-x. 4 fiorino fiorino 4096 May 18 21:28 tcdiagDAT0-ssd1
#lrwxrwxrwx. 1 fiorino fiorino   22 Mar 14  2019 tceps -> /w21/web-config/tceps/
#lrwxrwxrwx. 1 fiorino fiorino   47 Sep 13  2020 tcepsDAT -> $W2_HFIP/hfip/tcepsDAT/
#lrwxrwxrwx. 1 fiorino fiorino   22 Mar 14  2019 tcgen -> /w21/web-config/tcgen/
#lrwxrwxrwx. 1 fiorino fiorino   47 Sep 13  2020 tcgenDAT -> $W2_HFIP/hfip/tcgenDAT/
#lrwxrwxrwx. 1 fiorino fiorino   26 Sep 25  2019 tctrkveri -> /w21/web-config/tctrkveri/
#drwxrwxr-x. 7 fiorino fiorino 4096 May 11 11:54 tctrkveriDAT

#lrwxrwxrwx.  1 fiorino fiorino    35 Jun 23 14:11 web -> $W2_HFIP/wxmap2/
#lrwxrwxrwx.  1 fiorino fiorino    26 Jun 23 14:12 web-config -> /ssd1/data/w22/web-config/
#lrwxrwxrwx.  1 fiorino fiorino    26 May  1 15:58 web-config-m4 -> /ssd1/data/w22/web-config/
#drwxrwxr-x.  9 fiorino fiorino   131 May  1 15:58 web-config-mike4
#lrwxrwxrwx.  1 fiorino fiorino    35 Dec 11  2020 web-m4 -> $W2_HFIP/wxmap2/


