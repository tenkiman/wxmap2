#!/bin/sh

cd ../tcdat

w2.tc.posit.py 2000010100.2001010100 -n /tmp/ngtrp.tcactivity.2000010100.2001010100.txt -T
rm /home/work/wxmap2/plt/tc/ops/climo/2007.nhem/tc.act.spec.2000010100.*
cd ../tcclimo
g.tc.activity.pl 2000010100 2001010100 /tmp/ngtrp.tcactivity.2000010100.2001010100.txt /home/work/wxmap2/plt/tc/ops/climo/2007.nhem
rm /home/work/wxmap2/plt/tc/ops/climo/2007.nhem/tc.act.llmap.nhem.20000101*
g.tc.bt.climo.ll.py -y 2000010100.2000071718 -b nhem -d /home/work/wxmap2/plt/tc/ops/climo/2007.nhem
rm /home/work/wxmap2/plt/tc/ops/climo/2007.nhem/tc.act.llmap.wpac.20000101*
g.tc.bt.climo.ll.py -y 2000010100.2000071718 -b wpac -d /home/work/wxmap2/plt/tc/ops/climo/2007.nhem
rm /home/work/wxmap2/plt/tc/ops/climo/2007.nhem/tc.act.llmap.epac.20000101*
g.tc.bt.climo.ll.py -y 2000010100.2000071718 -b epac -d /home/work/wxmap2/plt/tc/ops/climo/2007.nhem
rm /home/work/wxmap2/plt/tc/ops/climo/2007.nhem/tc.act.llmap.lant.20000101*
g.tc.bt.climo.ll.py -y 2000010100.2000071718 -b lant -d /home/work/wxmap2/plt/tc/ops/climo/2007.nhem
