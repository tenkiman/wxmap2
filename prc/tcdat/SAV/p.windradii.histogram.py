#!/usr/bin/env python

"""%s

purpose:

  make plot of wind radii histogram

usage:

  %s basinopt -C

  -C   cumulative prob

examples:

%s w.1-8

"""

import os
import sys
import copy

import cPickle as pickle

import string
import glob
import getopt

import TCw2 as TC
import TCveri as TCV
import mf
import w2
from const import knots2ms,nm2km

tcpyppath="/ptmp/tc.pyp"
ropt=''
docum=0
verb=0
doplotonly=0


curdtg=mf.dtg()
curyear=curdtg[0:4]
curtime=mf.dtg('curtime')
curdir=os.getcwd()

pyfile=sys.argv[0]

narg=len(sys.argv)-1

i=1
if(narg >= 1):

    stmopt=sys.argv[1]

    try:
        (opts, args) = getopt.getopt(sys.argv[2:], "PCNV")

    except getopt.GetoptError:
        mf.usage(__doc__,pyfile,curdtg,curtime)
        print "EEE invalid getopt opt"
        sys.exit(2)

    for o, a in opts:
        if o in ("-N",""): ropt='norun'
        if o in ("-P",""): doplotonly=1
        if o in ("-C",""): docum=1
        if o in ("-V",""): verb=1

else:
    mf.usage(__doc__,pyfile,curdtg,curtime)
    sys.exit(2)



if(not(doplotonly)):
    cmd="w2-tc-posit.py %s -R"%(stmopt)
    mf.runcmd(cmd,ropt)

if(ropt == 'norun'): sys.exit()

PS=open(tcpyppath)
tcpyp=pickle.load(PS)
(stmids,r34,r50,rmax)=tcpyp
PS.close()

def stmtitle(stmids):
    basins=[]
    years=[]
    for stmid in stmids:
        tt=stmid.split('.')
        b1id=tt[0][2]
        basins.append(b1id)
        year=tt[1]
        years.append(year)

    basins=mf.uniq(basins)
    years=mf.uniq(years)

    btitle=''

    lb=len(basins)
    for i in range(0,lb):
        b=basins[i]
        bb=TC.Basin1toBasinNameShort[b]
        btitle=btitle+bb.lower()
        if(i < lb-1 and i > 0):
            btitle=btitle+' '

    ytitle="%s-%s"%(years[0],years[-1])

    stitle="Basins: %s  Years: %s"%(btitle.upper(),ytitle)
        
    return(stitle,btitle,ytitle)
    

(stitle,btitle,ytitle)=stmtitle(stmids)


import numpy

def smooth(x,window_len=10,window='hanning'):
    """smooth the data using a window with requested size.
    
    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.
    
    input:
        x: the input signal 
        window_len: the dimension of the smoothing window
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal
        
    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)
    
    see also: 
    
    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter
 
    TODO: the window parameter could be the window itself if an array instead of a string   
    """

    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."


    if window_len<3:
        return x


    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"


    s=numpy.r_[2*x[0]-x[window_len:1:-1],x,2*x[-1]-x[-1:-window_len:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=numpy.ones(window_len,'d')
    else:
        w=eval('numpy.'+window+'(window_len)')

    y=numpy.convolve(w/w.sum(),s,mode='same')
    return y[window_len-1:-window_len+1]




import matplotlib.pyplot as plt

xmax=400
xint=50

nbins=(xmax/xint)
nbins=35

x3=r34
x2=r50
x1=rmax

hrange=[0,xmax]

fc1='green'
fc2='red'
fc3='blue'

if(docum):
    ptype='step'
    ec1=fc1
    ec2=fc2
    ec3=fc3
else:
    ptype='bar'
    ec1=ec2=ec3='black'

(n3, bins, patches) = plt.hist(x3,nbins,histtype=ptype,range=hrange,normed=1,cumulative=docum,facecolor=fc1,edgecolor=ec1, alpha=0.85,align='mid')
(n2, bins, patches) = plt.hist(x2,nbins,histtype=ptype,range=hrange,normed=1,cumulative=docum,facecolor=fc2,edgecolor=ec2, alpha=0.75,rwidth=0.50,align='mid')
(n1, bins, patches) = plt.hist(x1,nbins,histtype=ptype,range=hrange,normed=1,cumulative=docum,facecolor=fc3,edgecolor=ec3, alpha=1.0,rwidth=0.15,align='mid')

print n3,len(n3)
print bins,len(bins)
xs=[]
for i in range(0,len(bins)-1):
    xs.append( (bins[i]+bins[i+1])*0.5 )

n1s=smooth(n1,window_len=5,window='hamming')
n2s=smooth(n2,window_len=5,window='hamming')
n3s=smooth(n3,window_len=5,window='hamming')

def zerolt0(ys):
    oys=[]
    for y in ys:
        if(y < 0.0):
            oys.append(0.0)
        else:
            oys.append(y)
    return(oys)

rmaxM=numpy.interp([0.5],n1,xs)
r34M=numpy.interp([0.5],n2,xs)
r50M=numpy.interp([0.5],n3,xs)
print 'mmmmmmmmmm ',rmaxM,r34M,r50M

print '333 ',n3s[-1],n2s[-1],n1s[-1]

plt.plot(xs,zerolt0(n1s),'b',lw=2,ls='-')
plt.plot(xs,zerolt0(n2s),'r',lw=2,ls='-')
plt.plot(xs,zerolt0(n3s),'g',lw=2,ls='-')


n34=len(r34)
n50=len(r50)
nrmax=len(rmax)

plt.xlabel('R [nm]')

if(docum):
    plt.ylabel('Cumulative Prob')
else:
    plt.ylabel('Prob')
    
plt.title("Rmax (blue, N:%d) R50 (red, N:%d) R34 (green, N:%d)\n%s"%(nrmax,n50,n34,stitle))


plt.xlim(0,xmax)
xaxis=range(0,xmax+1,xint)
plt.xticks(xaxis)

if(docum):
    yaxis=[0.0,0.25,0.50,0.75,1.0,1.25]
    plt.yticks(yaxis)

plt.grid(True)

if(docum):
    plt.text(205,1.18,r'Rmax$_{50}$ = %3.0f nm'%(rmaxM),size=12)
    plt.text(205,1.14,r'R50$_{50}$    = %3.0f nm'%(r34M),size=12)
    plt.text(205,1.10,r'R34$_{50}$    = %3.0f nm'%(r50M),size=12)
    
if(docum):
    pngpath="/ptmp/wind.radii.%s.%s.cumulative.prob.png"%(btitle,ytitle)
    epspath="/ptmp/wind.radii.%s.%s.cumulative.prob.eps"%(btitle,ytitle)
else:
    pngpath="/ptmp/wind.radii.%s.%s.prob.png"%(btitle,ytitle)
    epspath="/ptmp/wind.radii.%s.%s.prob.eps"%(btitle,ytitle)
    
plt.savefig(pngpath)
plt.savefig(epspath)
plt.show()


sys.exit()
