#!/usr/bin/env python

from M import *
MF=MFutils()

cmd='uptime'
output=MF.runcmdLog(cmd,quiet=1)
tt=output[0].split(',')

if(len(tt) == 4):
    ll=tt[-1].split()
    load1min=float(ll[-3])
    load5min=float(ll[-2])
    load15min=float(ll[-1])
    
else:
    
    load1min=tt[-3].split()
    load1min=float(load1min[-1])
    load5min=float(tt[-2])
    load15min=float(tt[-1])

print
print
print
print 'LLL: ',mf.dtg('dtg_hms'),' load 1min: %4.2f  5min: %4.2f  15min: %4.2f'%(load1min,load5min,load15min)
print
print
print
