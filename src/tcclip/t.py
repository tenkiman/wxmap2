#!/usr/bin/env python

import tc

tcs=tc.findtc(1990090700)

n=0
for tc in tcs:
    n=n+1
    print "T: ",n,tc

