#!/usr/bin/env python

# -- 20210331 -- brought over from mike3: w22-make3as2

from WxMAP2 import *

w22Files=[

'etc/.crontab.tenki7-mike3.20210329',           
#'git-w22-mike3as2-20210331.txt',                
'prc/fldanal/dtitle.gsf',                       
'prc/fldanal/w2-gfs-goes-loop.py',              
'prc/fldanal/w2-plot.py',                       
'prc/fldanal/w2-prw-loop.py',                   
'prc/flddat/get_gfs.pl',                        
'prc/flddat/w2-fld-wget-mirror-gfs-stbgoes.py', 
'prc/lib/python/M.py',                          
'prc/lib/python/M2.py',                         
'prc/lib/python/adVM.py',                       
'prc/lib/python/tcCL.py',                       
'prc/tcdat/w2-tc-wget-mirror-tigge-2-local.py',
#'prc/wxmap2/w2-ps-monitor-anl.py',              

]

sgit='origin/w22-mike3as2'
ropt='norun'
ropt=''

for w2 in w22Files:
    cmd='git checkout %s -- %s'%(sgit,w2)
    mf.runcmd(cmd,ropt)
