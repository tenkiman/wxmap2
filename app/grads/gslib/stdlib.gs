#----------------------------------------------------------------------
#  Author:	Mike Fiorino
#  History:	9 Feb, 2001 started
#
#  Mike Fiorino's basic scripts functions organized by type:
#  
#
#----------------------------------------------------------------------

#gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg
#
#  global variables
#
#  _gravity	ECMWF/WMO
#
#gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg

function const
_monamel='jan feb mar apr may jun jul aug sep oct nov dec'
_monameu='JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC'
_monday='31 28 31 30 31 30 31 31 30 31 30 31'

_pi=3.141592654

_m2ft=3.2808
_ms2kt=1.944
_gravity=9.80665

_author='PCMDI (M. Fiorino)'
return


#tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
#
#	titles
#
#	stitle(t1,scale)			1 plot title 
#	stitle2(t1,t2,scale)			2 plot title
#	toptitle(t1,t2,scale,t1col,t2col)	page top title
#	toptle3(t1,t2,scale,t1col,t2col)	3 line page top title
#	scrptle(scale)				anotate a plot
#	bottitle(t1,t2,scale,t1col,t2col)	page bottom title
#
#
#tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt

**************************************************
*
*  stitle2
*
**************************************************

function stitle2(t1,t2,scale)

  rc=plotdims()

n=1
while(n<=2)

  dxs=_xlplot
  dyt=_pagey-_ytplot

  if(n=1)
    tsiz=0.15
    xoff=0.75
    yoff=0.10
    title=t1
  endif

  if(n=2)
    xoff=0.75
    yoff=yoff*1.75+tsiz
    title=t2
  endif

  xs=_xlplot-xoff-tsiz/2
  xm=(_xlplot+_xrplot)/2
  ys=(_ybplot+_ytplot)/2

  if(scale != 'scale' & n=1)
    tsiz = tsiz * scale
    xs=_xlplot-xoff-tsiz/2
  endif

  angle=90
  tt=tsiz+yoff

  if(tt < dyt) 
    xs=xm
    ys=_ytplot+yoff+tsiz/2 
    angle=0
  endif
  
  'set line 0 '
  x1b=_xlplot
  x2b=_xrplot
  y1b=_ytplot+yoff-tsiz*0.6
  y2b=y1b+tsiz+tsiz*0.6

*  'draw recf 'x1b' 'y1b' 'x2b' 'y2b
  'set strsiz 'tsiz
  'set string 1 c 5 'angle
  'draw string 'xs' 'ys' 'title
  'set string 1 c 5 0'

  n=n+1
endwhile

return

**************************************************
*
*  stitle
*
**************************************************

function stitle(t1,scale)

  rc=plotdims()

  dxs=_xlplot
  dyt=_pagey-_ytplot

  tsiz=0.15
  xoff=0.75
  yoff=0.10

  xs=_xlplot-xoff-tsiz/2
  xm=(_xlplot+_xrplot)/2
  ys=(_ybplot+_ytplot)/2

  if(scale != 'scale')
    tsiz = tsiz * scale
    xs=_xlplot-xoff-tsiz/2
  endif

  angle=90
  tt=tsiz+yoff

  if(tt < dyt) 
    xs=xm
    ys=_ytplot+yoff+tsiz/2 
    angle=0
  endif
  
  'set line 0 '
  x1b=_xlplot
  x2b=_xrplot
  y1b=_ytplot+yoff-tsiz*0.6
  y2b=y1b+tsiz+tsiz*0.6

  'draw recf 'x1b' 'y1b' 'x2b' 'y2b
  'set strsiz 'tsiz
  'set string 1 c 5 'angle
  'draw string 'xs' 'ys' 't1
  'set string 1 c 5 0'

return

**************************************************
*
*  scrptle
*
**************************************************

function scrptle(scale)

  script=_gsdir'/'_gsname

  rc=plotdims()
#  '!dtg > dtg.cur'
#  rc=read(dtg.cur)
#  dtg=sublin(rc,2)
#  rc=close(dtg.cur)

  tsiz=0.09
  if(scale != 'scale')
    tsiz = tsiz * scale
  endif

  dx1=_pagex

  xoff=0.15
  yoff=0.07

  x1=xoff
  y1=yoff+tsiz/2

  x2=_pagex-xoff
  y2=y1

  x3=_pagex/2
  y3=y1

  'set strsiz 'tsiz
  'set string 1 l 4' 
  'draw string 'x1' 'y1' GrADS Script: 'script
  'set strsiz 'tsiz
#
#  use the internal time stamp
#
#  'set string 1 r 4' 
#  'draw string 'x2' 'y2' 'dtg
  'set string 1 c 4 0'
  'draw string 'x3' 'y3' '_author

return


**************************************************
*
*  toptitle3
*
**************************************************

function toptle3(t1,t2,t3,scale,t1col,t2col,t3col)

  rc=plotdims()

  xr=_pagex
  xl=0
  y1=_pagey-0.15
  xs=(xr-xl)*0.5
  tsiz=0.15
  if(scale != 'scale') ; tsiz = tsiz * scale ; endif
  if(t1col='') ; t1col=1 ; endif
  if(t2col='') ; t2col=1 ; endif
  if(t3col='') ; t3col=1 ; endif
  t2siz=tsiz*0.925
  t3siz=t2siz*0.925
  y2=y1-tsiz*1.5
  y3=y2-tsiz*1.5

  'set strsiz 'tsiz
  'set string 't1col' c 6'
  'draw string 'xs' 'y1' 't1

  if(t2 != '')
    'set string 't2col' c 8'
    'set strsiz 't2siz
    'draw string 'xs' 'y2' `0't2'`0'
  endif

  if(t3 != '')
    'set string 't3col' c 8'
    'set strsiz 't2siz
    'draw string 'xs' 'y3' `2't3'`0'
  endif

return
  
**************************************************
*
*-------------------------- bottitle ------------------
*
**************************************************

function bottitle(t1,t2,scale,t1col,t2col)

  'q gxinfo'
  card=sublin(result,2)

  pagex=subwrd(card,4)
  pagey=subwrd(card,6)

  xr=pagex
  xl=0
  y1=0.22
  y2=0.08

  xs=xl+(xr-xl)*0.5
*  xs=0.2


  tsiz=0.09
  if(scale != 'scale') ; tsiz = tsiz * scale ; endif

  'set strsiz 'tsiz
  'set string 't1col' c 4'
  'draw string 'xs' 'y1' 't1

  if(t2 != '')
    'set string 't2col' c 4'
    'draw string 'xs' 'y2' 't2
  endif

return
**************************************************
*
*  toptitle
*
**************************************************

function toptitle(t1,t2,scale,t1col,t2col)

  rc=plotdims()

  xr=_pagex
  xl=0
  y1=_pagey-0.15
  xs=(xr-xl)*0.5
  tsiz=0.15
  if(scale != 'scale') ; tsiz = tsiz * scale ; endif
  if(t1col='') ; t1col=1 ; endif
  if(t2col='') ; t2col=1 ; endif
  t2siz=tsiz*0.925
  y2=_pagey-0.15-tsiz*1.5

  'set strsiz 'tsiz
  'set string 't1col' c 6'
  'draw string 'xs' 'y1' 't1

  if(t2 != '')
    'set string 't2col' c 8'
    'set strsiz 't2siz
    'draw string 'xs' 'y2' `0't2'`0'
  endif

return

#dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
#
#   plotdims()		- page dimension info, global variables
#   metadata(j,varo)	- create file meta data arrays
#
#dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd



**************************************************
*
*  plotdims  - global variable page/plot dims
#  metadata(j,varo) --- file meta data into arrays
#  plotarea(np,pp,laydir,pytoff,pyboff) -- calc dims of N plots on a page
#  linelgd(nm,dxoff,xlsft,xlsz,yln,ylg,dyl) -- line legends
#
#**************************************************

function plotdims()
*
*	get the dimensions of the plot
*
*	do a dummy plot go the dimension
*
  'q gxinfo'
  card=sublin(result,2)
  _pagex=subwrd(card,4)
  _pagey=subwrd(card,6)
  if(_pagex>_pagey) ; _orient='land' ; endif
  if(_pagey>_pagex) ; _orient='port' ; endif

  card=sublin(result,3)
  _xlplot=subwrd(card,4)
  _xrplot=subwrd(card,6)

  card=sublin(result,4)
  _ybplot=subwrd(card,4)
  _ytplot=subwrd(card,6)

return

**************************************************
*
*  metadata
*
**************************************************

function metadata(j,varo)

'set dfile 'j
'q file'

card=sublin(result,5)
_nx.j=subwrd(card,3)
_ny.j=subwrd(card,6)
_nz.j=subwrd(card,9)
_nt.j=subwrd(card,12)
card=sublin(result,6)
_nv.j=subwrd(card,5)

if(varo='y') 
  i=1
  while(i<=_nv.j)
    ii=6+i
    card=sublin(result,ii)
    _vr.i.j=subwrd(card,1)
    _nl.i.j=subwrd(card,2)
    _un.i.j=subwrd(card,3)
    bd=wrdpos(card,4)
say 'bd = 'bd' 'card
    _ds.i.j=substr(card,bd,120)
    i=i+1
  endwhile
endif

return


function plotarea(np,pp,laydir,pytoff,pyboff)
*
*	switch the sense of the layout direction if portrait
*
if(_orient='port')
  if(laydir=1)
    laydir=0 
  else
    laydir=1
  endif
endif

dpagex=_pagex
dpagey=_pagey-(pytoff+pyboff)

nbl1="1 2 3 2 2 2 2 2 2 2 3 3"
nbl0="1 1 1 2 3 3 4 4 5 5 4 4"

npx=subwrd(nbl1,np)
npy=subwrd(nbl0,np)

if(laydir=0)
  npx=subwrd(nbl0,np)
  npy=subwrd(nbl1,np)
endif

dpx=dpagex/npx
dpy=dpagey/npy
dxb=(1.0-pp)*dpx*0.5
dyb=(1.0-pp)*dpy*0.5
### print 'qqq kk = 'np' 'npx' 'npy' 'dpx' 'dpy' 'dxb' 'dyb

l=1
j=npy
while(j>=1)

  y0=pyboff+(j-1)*dpy
  y1=pyboff+j*dpy

  i=1
  while(i<=npx & l<=np)
    x0=(i-1)*dpx
    x1=i*dpx

    _xpl.l=x0+dxb
    _xpr.l=x1-dxb
    _ypt.l=y1-dyb
    _ypb.l=y0+dyb

    i=i+1
    l=l+1
  endwhile
  j=j-1
endwhile

return

function linelgd(nm,dxoff,xlsft,xlsz,yln,ylg,dyl)
xlen=_pagex-2*dxoff
ylg=yln+dyl
dx=xlen/nm
xloff=(dx-xlsz*dx)*0.5-xlsft
j=1
while(j<=nm)
  xb=dxoff+(j-1)*dx+xloff
  xe=xb+xlsz*dx
  xm=(xb+xe)*0.5

  'set line '_lc.j' '_ls.j' '_lt.j
  'draw line 'xb' 'yln' 'xe' 'yln

  'set string 1 bc 6'
  'set strsiz 0.125'
  'draw string  'xm' 'ylg' '_s.j
  j=j+1
endwhile

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
#  misc:
#
#  tyear(dtg) - mo to da interp const
#  wk2da(dtg) - wk to da interpolation const
#
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

function wk2da(dtg)
ctime=dtghcur(dtg)
'set time 'ctime
'q dims'
card=sublin(result,5)
t0=subwrd(card,9)
tm1=t0-1
tp1=t0+1

dtg0=t2dtg(t0)
dtgm1=t2dtg(tm1)
dtgp1=t2dtg(tp1)

###print 'DDDDD tdtg 'dtg' :: 'dtgm1' 'dtg0' 'dtgp1

if(dtg > dtgm1 & dtg < dtg0)

  d2=dtgdiff(dtgm1,dtg)
  d1=dtgdiff(dtg,dtg0)
  dt=dtgdiff(dtgm1,dtg0)
  t1=tm1
  t2=t0
  dtg1=dtgm1
  dtg2=dtg0

endif

if(dtg = dtg0) 

  d1=0
  d2=1
  t1=tm1
  t2=t0
  dt=1
  dtg1=dtgm1
  dtg2=dtg0

endif


if(dtg > dtg0 & dtg < dtgp1)


#  print 'case 1'
  d2=dtgdiff(dtg0,dtg)
  d1=dtgdiff(dtg,dtgp1)
  dt=dtgdiff(dtg0,dtgp1)
  t1=t0
  t2=tp1
  dtg1=dtg0
  dtg2=dtgp1

endif

f1=d1/dt
f2=d2/dt

#print 'd1 = 'd1' d2 = 'd2' dt = 'dt
#print 'f1 = 'f1' f2 = 'f2

rc=f1' 'f2' 't1' 't2' 'dtg1' 'dtg2
return(rc)

function tyear(dtg)
###print 'qqqqqqq 'dtg
mo=substr(dtg,5,2)*1.0
hr=substr(dtg,9,2)/24.0
da=substr(dtg,7,2)*1.0+hr

imo=substr(dtg,5,2)
if(substr(imo,1,1) = '0') ; imo=substr(imo,2,1) ; endif
mda=_ndymon.imo*0.5

if(da<mda) 
  nda1=subwrd(_monday,imo)
  mda1=nda1*0.5
  imo=imo-1
  if(imo = 0) ; imo=12 ; endif
  nda2=subwrd(_monday,imo)
  mda2=nda2*0.5
  ndai=nda1-mda1+mda2
  da=ndai - (mda-da)
  mo=mo-1
  w1=1-(da/ndai)
  w2=1-w1
  imo1=imo
  imo2=imo+1
  if(imo2 > 12) ; imo2 = 1 ; endif
  return(imo1' 'w1' 'imo2' 'w2)
endif

if(da>mda)
  nda1=subwrd(_monday,imo)
  mda1=nda1*0.5
  imo1=imo
  imo=imo+1
  if(imo > 12) ;  imo=1 ; endif 
  if(imo = 0) ; imo = 12 ; endif
  nda2=subwrd(_monday,imo)
  mda2=nda2*0.5
  ndai=nda1-mda1+mda2
  da=da-mda
  w1=1-(da/ndai)
  w2=1-w1
  imo2=imo
  if(imo2 > 12) ; imo2 = 1 ; endif
  if(imo2 = 0) ; imo2 = 12 ; endif
  return(imo1' 'w1' 'imo2' 'w2)
endif

if(da=mda)
  imo1=imo
  imo2=imo
  w1=1.0
  w2=0.0  
  return(imo1' 'w1' 'imo2' 'w2)
endif

return('error')


#ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
#
#  strings
#
#  strlen(arg)
#
#ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss

*
*-------------------------- strlen ------------------
*
function strlen(arg)

i=1
while(substr(arg,i,1) != '' & i<250)
  i=i+1
endwhile
return(i-1)

#dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
#
#  time and DTG (YYYYMMHH):
#
#  curdtgh(ctime)	grads time -> dtg
#  dtghcur(dtgh)	dtg -> grads time
#  incdtgh(dtgh,inc)    increment dtg
#  mydate		readable format with weekday
#  t2dtg(t)		convert t index -> dtg
#  dtgdiff(dtg1,dtg2)	difference in hours between dtgs
#  ndayyear(yr)		# da in a year (gregorian)
#  ndaymo(yr,mo)	# da in a mo for year yr
#  moda2jul(yr,mo,da)	# yr/mo -> julian da
#
#

#dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd

*
*-------------------------- mydate ------------------
*
function mydate()
*
*  Function to reformat the GrADS date/time into something
*  more readable
*
  'query time'
  sres = subwrd(result,3)
  dayweek = subwrd(result,6)
  i = 1
  while (substr(sres,i,1)!='Z')
    i = i + 1
  endwhile
  hour = substr(sres,1,i)
  isav = i
  i = i + 1
  while (substr(sres,i,1)>='0' & substr(sres,i,1)<='9')
    i = i + 1
  endwhile
  day = substr(sres,isav+1,i-isav-1)
  month = substr(sres,i,3)
  year = substr(sres,i+5,2)
  return (dayweek' 'hour' 'day' 'month)

*
*-------------------------- curdtgh ------------------
*
function curdtgh(ctime)
*
*  convert current time to dtg 
*
  iyr=substr(ctime,11,2)
  nmo=substr(ctime,6,3)
  ida=substr(ctime,4,2)
  ihr=substr(ctime,1,2)
  i=1
  while (nmo!=subwrd(_monameu,i));i=i+1;endwhile
  imo=i
  if(imo < 10); imo='0'imo; endif
  if(ihr = 0); ihr='00';endif
  if(ihr < 10 & ihr != '00'); ihr='0'ihr; endif

  idtg=iyr%imo%ida%ihr

return (idtg)

*
*-------------------------- dtghcur ------------------
*

function dtghcur(dtgh)
*
*  convert FNMOC DTG (full) to GrADS time
*
  iyr=substr(dtgh,1,4)*1
  imo=substr(dtgh,5,2)*1
  ida=substr(dtgh,7,2)*1
  ihr=substr(dtgh,9,2)*1
  nmo=subwrd(_monamel,imo)
  imo=i
return (ihr%'Z'ida%nmo%iyr)

function incdtgh(dtgh,inc)
*
*  increment a dtg by inc hours
*  RESTRICTIONS!!  
*  (1)  inc > 0
*  (2)  inc < 24
*
  monday.1=31
  monday.2=28
  monday.3=31
  monday.4=30
  monday.5=31
  monday.6=30
  monday.7=31
  monday.8=31
  monday.9=30
  monday.10=31
  monday.11=30
  monday.12=31

  ict=substr(dtgh,1,2)*1
  iyr=substr(dtgh,3,2)*1
  imo=substr(dtgh,5,2)*1
  ida=substr(dtgh,7,2)*1
  ihr=substr(dtgh,9,2)*1
*   say 'qqq 'dtgh' 'inc
  if(mod(iyr,4)=0) 
    monday.2=29
  endif

  ihr=ihr+inc
*  say 'ihr = 'ihr' ida = 'ida

  while(ihr>=24)
    ihr=ihr-24
    ida=ida+1
  endwhile

  while(ihr<0)
    ihr=ihr+24
    ida=ida-1
  endwhile

*  say 'new ihr = 'ihr' new ida = 'ida' imo = 'imo

  if(ida > monday.imo)
    ida=ida-monday.imo
*    say 'inside check ida = 'ida' monday = 'monday.imo
    imo=imo+1
  endif

  while(ida < 0)
    imo=imo-1
    ida=monday.imo+ida
  endwhile

  if(ida = 0)
    imo=imo-1
    if(imo<=0)
      imo=imo+12
      iyr=iyr-1
      if(mod(iyr,4)=0) ; monday.2=29 ; endif
    endif
    ida=monday.imo
  endif

  if(imo<=0)
    imo=imo+12
    iyr=iyr-1
    if(mod(iyr,4)=0) ; monday.2=29 ; endif
  endif

  if(imo>=13)
    imo=imo-12
    iyr=iyr+1
  endif

if(iyr >= 100)
ict=ict+1
iyr=iyr-100
endif

if(ict<10);ict='0'ict;endif
if(iyr<10);iyr='0'iyr;endif
if(imo<10);imo='0'imo;endif
if(ida<10);ida='0'ida;endif
if(ihr<10);ihr='0'ihr;endif

return (ict%iyr%imo%ida%ihr)


function t2dtg(t)
'set t 't
'q time'
time=subwrd(result,3)
dtg=curdtgh(time)
return(dtg)

function dtgdiff(dtg1,dtg2)

iyr1=substr(dtg1,1,4)
imo1=substr(dtg1,5,2)
idy1=substr(dtg1,7,2)
ihr1=substr(dtg1,9,2)

iyr2=substr(dtg2,1,4)
imo2=substr(dtg2,5,2)
idy2=substr(dtg2,7,2)
ihr2=substr(dtg2,9,2)


jdy1=moda2jul(iyr1,imo1,idy1)
jdy2=moda2jul(iyr2,imo2,idy2)


if(iyr2 > iyr1)
  jdiff=(ndayyear(iyr1)-jdy1)+jdy2
endif

if(iyr2 < iyr1) 
  jdiff=(ndayyear(iyr2)-jdy2)+jdy1
endif

if(iyr2 = iyr1)
  jdiff=jdy2-jdy1
endif

ddiff=jdiff*24 + (ihr2-ihr1)
return(ddiff)

function ndayyear(yr)
nday=365
if(mod(yr,4) = 0) ; nday=366 ; endif
return(nday)


function ndaymo(yr,mo)
nday=subwrd(_monday,mo)
if(mod(yr,4) = 0 & mo = 2) ; nday=29 ; endif
return(nday)

function moda2jul(yr,mo,da)

mom1=mo-1
nn=0
if(mom1 = 0)
   jul=da
else
  i=1
  while(i<=mom1)
    nn=nn+ndaymo(yr,i)
    i=i+1
  endwhile
  jul=nn+da
endif
return(jul)


#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
#  script math interface
#
#  abs
#  atan2
#  sqrt
#  cos
#  sin
#  nint*
#  mod*
#  int*
#  * use grads, need to convert
#
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm


function abs(v)
rc=math_abs(v)
return(rc)

function atan2(u,v)
rc=math_atan2(u,v)
return(rc)

function sqrt(v)
rc=math_sqrt(v)
return(rc)

function cos(v)
rc=math_cos(v)
return(rc)

function sin(v)
rc=math_sin(v)
return(rc)

function nint(i0)
  i0=i0+0.5
  i=0
  while(i<12)
    i=i+1
    if(substr(i0,i,1)='.')
      i0=substr(i0,1,i-1)
      break
    endif
  endwhile
return(i0)

function mod(i0,inc)
  if(inc!=0)
    imod=int(i0/inc)
  else
    imod=int(i0/1)
  endif
  imod=i0-imod*inc
return(imod)

*
*-------------------------- int ------------------
*
function int(i0)
  i=0
  while(i<12)
    i=i+1
    if(substr(i0,i,1)='.')
      i0=substr(i0,1,i-1)
      break
    endif
  endwhile
return(i0)

#gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg
#
#  graphic primitives
#
#  darrow - draw arrow
#  ddot	  - draw dot
#  windbarb - wind barb
#  wdir - for windbarb
#  wspd - wind speed for windbarb
#  wu   - u comp of w
#  wv	- v comp of wind
#  exp  - e to the  for windbarb
#  round - rounding for windbarb
#  getuobs - parse stn output for u
#  getvobs - parse stn output for v
#  gettobs - parse stn output for t
#  dcircle - draw circle
#  eclogo  - draw ECMWF logo
#  jaecol  - color table from jae schemm, cpc
#  efscol  - colar table from steve swadley, nrl for EFS very nice
#
#gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg


function darrow(x,y,len,dir,acol,asty,athk,lab,labopt)

ss=0.10
'set strsiz 'ss
print 'qqq111 'labopt

arrang=30
arrscl=0.20
arrlen=len*arrscl
dd=dir*_d2r
xl=sin(dd)*len
yl=cos(dd)*len

xls=sin(dd)*len*1.05
yls=cos(dd)*len*1.05

da1=(dir+arrang)*_d2r
da2=(dir-arrang)*_d2r
xa1=sin(da1)*arrlen
ya1=cos(da1)*arrlen

xa2=sin(da2)*arrlen
ya2=cos(da2)*arrlen

xa1=x+xl-xa1
ya1=y+yl-ya1

xa2=x+xl-xa2
ya2=y+yl-ya2


x1=x+xl
y1=y+yl

print 'AAAA set line 'acol' 'asty' 'athk


'set line 'acol' 'asty' 'athk

'draw line 'x1' 'y1' 'xa1' 'ya1
'draw line 'x1' 'y1' 'xa2' 'ya2
'draw line 'x' 'y' 'x1' 'y1

print 'LLLLLLLLLLLLLLLLLLLLLLLLLL 'lab
if(lab = '' | lab ='lab') ; return ;endif

ddd=90-dir
jj='l'

if(ddd < -90)
jj='r'
ddd=ddd+180
endif



###  'set string 1 'jj' 3 'ddd

if(labopt = 't')
  'set string 1 bc 5 0'
  xls=xl
  yls=yl+0.10
endif

if(labopt = 'tc')
  'set string 1 bc 5 0'
  xls=xl
  yls=yl+0.10
endif

if(labopt = 'b')
  'set string 1 tc 5 0'
  xls=xl
  yls=yl-0.10
endif

if(labopt = 'bc')
  'set string 1 tc 5 0'
  xls=xl+len*0.5
  yls=yl-0.10
endif

if(labopt = 'r')
  'set string 1 l 5 0'
  xls=xl+0.10
  yls=yl
endif

if(labopt = 'rc')
  'set string 1 l 0'
  xls=xl+0.10
  yls=yl-len*0.5
print 'qqqq 'x' 'y' 'xls' 'yls' 'xl' 'yl
endif

if(labopt = 'l')
  'set string 1 r 5 0'
  xls=xl-0.10
  yls=yl
endif

xs=x+xls
ys=y+yls
'draw string 'xs' 'ys' 'lab

return

function ddot(x,y)

'set line 1 1 5'
siz=0.05
'draw mark 3 'x' 'y' 'siz

return


function windbarb(bx0,by0,wdir,wspd,wu,wv)
*
* ----------------- Wind Barb Profile Options ----------------------------
*
* All variables here are in units of inches, unless otherwise specified
*
*  barbint = Interval for plotting barbs (in units of levels)
*  poleloc = X-Location of profile.  Choose -1 for the default.
*  polelen = Length of wind-barb pole
*  Len05   = Length of each 5-knot barb 
*  Len10   = Length of each 10-knot barb
*  Len50   = Length of each 50-knot flag
*  Wid50   = Width of base of 50-knot flag 
*  Spac50  = Spacing between 50-knot flag and next barb/flag 
*  Spac10  = Spacing between 10-knot flag and next flag
*  Spac05  = Spacing between 5-knot flag and next flag
*  Flagbase= Draw flagbase (filled circle) for each windbarb [1=yes, 0 =no] 
*  Fill50  = Solid-fill 50-knot flag [1=yes, 0=no]
*  barbline= Draw a vertical line connecting all the wind barbs [1=yes, 0=no]
*
'set line 1 0 5'
_blenpole = 0.35
_blen05   = 0.07
_blen10   = 0.15
_blen50   = 0.15
_bwid50   = 0.06
_bspac50  = 0.07
_bspac10  = 0.05
_bspac05  = 0.05
_bfill50  = 1
_bflagbase= 1
_barbline= 1

if(wspd = 0) ; wspd=0.01 ; endif
if(wspd > 225) 
 say 'wspeed > 225'
return(-999)
endif

cc=_blenpole/wspd
xendpole=bx0-wu*cc
yendpole=by0-wv*cc
if (xendpole>0 & wspd >= 0.5)

  if (_bflagbase = 1) 
     "draw mark 3 "bx0 " " by0 " 0.05"
  endif
  "draw line " bx0 " " by0 "  " xendpole " " yendpole
  flagloop=wspd/10
  windcount=wspd
  flagcount=0
  xflagstart=xendpole
  yflagstart=yendpole
  dx=cos((180-wdir)*_d2r)
  dy=sin((180-wdir)*_d2r)

  while (windcount > 47.5)
    flagcount=flagcount+1
    dxflag=-_blen50*dx
    dyflag=-_blen50*dy
    xflagend=xflagstart+dxflag
    yflagend=yflagstart+dyflag
    windcount=windcount-50
    x1=xflagstart+0.5*_bwid50*wu/wspd
    by0=yflagstart+0.5*_bwid50*wv/wspd
    x2=xflagstart-0.5*_bwid50*wu/wspd
    y2=yflagstart-0.5*_bwid50*wv/wspd
    if(_bfill50 = 1) 
      "draw polyf "x1" "by0" "x2" "y2" "xflagend" "yflagend" "x1" "by0
    else
      "draw line "x1 " "by0 " " xflagend " " yflagend " "  
      "draw line "x2 " "y2 " " xflagend " " yflagend
      "draw line "x1 " "by0 " " x2 " " y2
    endif
    xflagstart=xflagstart+_bspac50*wu/wspd
    yflagstart=yflagstart+_bspac50*wv/wspd
  endwhile

  while (windcount > 7.5 ) 
    flagcount=flagcount+1
    dxflag=-_blen10*dx
    dyflag=-_blen10*dy
    xflagend=xflagstart+dxflag
    yflagend=yflagstart+dyflag
    windcount=windcount-10
    "draw line " xflagstart " " yflagstart " " xflagend " " yflagend
    xflagstart=xflagstart+_bspac10*wu/wspd
    yflagstart=yflagstart+_bspac10*wv/wspd
  endwhile
 
 if(windcount > 2.5) 
   flagcount=flagcount+1
   if(flagcount = 1) 
     xflagstart=xflagstart+_bspac05*wu/wspd
     yflagstart=yflagstart+_bspac05*wv/wspd
   endif
   dxflag=-_blen05*dx
   dyflag=-_blen05*dy
   xflagend=xflagstart+dxflag
   yflagend=yflagstart+dyflag
   windcount=windcount-5
   "draw line " xflagstart " " yflagstart " " xflagend " " yflagend
  endif
else
  if(wspd < 0.5 & wspd >= 0) 
    "draw mark 2 " bx0 " " by0 " 0.08"
  endif
endif

return



function wdir(u,v)
'set gxout stat'
'd 270-atan2('v','u')*'_r2d
rec=sublin(result,8)
dir=subwrd(rec,4)
if(dir < 0) 
dir=360+dir
endif
if(dir>360)
dir=dir-360
endif
return(dir)


function wspd(u,v)
'd mag('v','u')*'_ms2kt
rec=sublin(result,8)
spd=subwrd(rec,4)
return(spd)

function wu(wspd,wdir)
If (wspd > 0) 
   wu=wspd*cos((270-wdir)*_d2r)
Else
   wu = -9999.0
Endif
return(wu)

function wv(wspd,wdir)

If (wspd > 0) 
   wv=wspd*sin((270-wdir)*_d2r)
Else
   wv = -9999.0
Endif
return(wv)


function exp(i)

*------------------------------------------
* return exponential of i
*------------------------------------------

"set gxout stat"
"d exp("i")"
rec=sublin(result,8)
val=subwrd(rec,4)
return(val)

***********************************************************************
function round(i)

rr=abs(1.0*i)
rr=int(rr+0.5)
if (i < 0)
   rr=-1*rr      
endif
return(rr)


function getuobs()
ic=15
i=1
card=sublin(_uobs,ic)
_nu=subwrd(card,6)
ic=ic+2

while(i<=_nu) 
  card=sublin(_uobs,ic)
  _u.i=subwrd(card,6)
  ic=ic+1
  i=i+1
endwhile

return

function getvobs()
ic=15
i=1
card=sublin(_vobs,ic)
_nv=subwrd(card,6)
ic=ic+2

while(i<=_nv) 
  card=sublin(_vobs,ic)
  _lev.i=subwrd(card,5)
  _v.i=subwrd(card,6)
  say 'i = 'i' lev = '_lev.i' '_u.i' '_v.i
  ic=ic+1
  i=i+1
endwhile

return


function gettobs()
ic=15
i=1
card=sublin(_tobs,ic)
_nt=subwrd(card,6)
ic=ic+2

while(i<=_nt) 
  card=sublin(_tobs,ic)
  _levt.i=subwrd(card,5)
  _t.i=subwrd(card,6)
  say 'i = 'i' levt = '_levt.i' '_t.i
  ic=ic+1
  i=i+1
endwhile

return


function dcircle(x,y,col,siz,sty,thk,ss,lab)

'set line 'col' 'sty' 'thk
'set ccolor 'col
'set cstyle 'sty
'set cthick 'thk
'draw mark 2 'x' 'y' 'siz

ys=y+siz*0.5+siz*0.025
'set string 1 bc 3 0'
'set strsiz 'ss

if(lab != '')
'draw string 'x' 'ys' 'lab
endif

return



#gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg
#
#  graphics - colors bars
#  
#  cbarn(args) - function version of cbarn.gs color bar
#  cbarc(args) - paul dirmeyer quarter circle bar
#
#
#gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg

function cbarc(args)
*
*	circle colar bar
*
*	originally written by Paul Dirmeryer, COLA 
*	for the wx graphics on the COLA Web Page
*
*	generalized by Mike Fiorino, LLNL 26 Jul 1996
*
*	xc and yc are the center of the circle
*	bc is the background color
*
*	if not defined user upper left hand corner
*
*	sample call:
*
*	run cbarc 11 8.5 2
*	
*	or
*
*	run cbarc 
*
*	to use the defaults
*

xc=subwrd(args,1)
yc=subwrd(args,2)

if(xc='' | yc = '')
  'q gxinfo'
  card=sublin(result,2)
  pagex=subwrd(card,4)
  pagey=subwrd(card,6)
  xc=pagex
  yc=pagey
endif 
*
*	use black for the background as a default	
*
bc=subwrd(args,3)
if(bc = '' | bc='bc') ; bc=0; endif 

*
*	get the shades of the last graphic
*

aa = 2.00
rt = 0.59 * aa
ro = 0.575 * aa
ri = 0.30 * aa
xa = xc + 0.05
ya = yc + 0.05
ll = 1
data = sublin(_shades,1)
ll = subwrd(data,5)
ml=ll
mm = 1
while (mm <= ll)
  mmp1 = mm + 1
  data = sublin(_shades,mmp1)
  col.mm = subwrd(data,1)
  if (col.mm = 0)
    col.mm = bc
  endif
  lim.mm = subwrd(data,3)
  if (lim.mm = '>')
    lim.mm = ' '
    ml=ml-1
    break
  else 
    mm = mm + 1
  endif
endwhile

dd = 3.1415926*0.5/ll
id = 3.1415926*1.50

'set line 'bc' 1 12'
x1 = xc - aa
xe = xc + 0.01
y1 = yc - aa
'draw polyf 'x1' 'yc' 'xe' 'yc' 'xe' 'y1
*'set line 1 1 6'
*'draw line 'x1' 'yc' 'xc' 'y1

'd 'ro'*cos('id')'
xfo = subwrd(result,4) + xa
'd 'ro'*sin('id')'
yfo = subwrd(result,4) + ya
'd 'ri'*cos('id')'
xfi = subwrd(result,4) + xa
'd 'ri'*sin('id')'
yfi = subwrd(result,4) + ya
mm = 1 

while(mm<=ll)    
  id = id - dd
  'd 'ro'*cos('id')'
  xlo = subwrd(result,4) + xa
  'd 'ro'*sin('id')'
  ylo = subwrd(result,4) + ya
  'd 'ri'*cos('id')'
  xli = subwrd(result,4) + xa
  'd 'ri'*sin('id')'
  yli = subwrd(result,4) + ya
  'd 'rt'*cos('id')'
  xft = subwrd(result,4) + xa
  'd 'rt'*sin('id')'
  yft = subwrd(result,4) + ya
 
  did = id * 180 / 3.14159 - 180

  'set line 'col.mm' 1 3'
  'draw polyf 'xfi' 'yfi' 'xfo' 'yfo' 'xlo' 'ylo' 'xli' 'yli
  'set line 'bc
  'draw line 'xfi' 'yfi' 'xfo' 'yfo
  'set string 1 r 4 'did
  'set strsiz 0.08 0.11'

  if(mm<=ml)
    'draw string 'xft' 'yft' 'lim.mm
  endif

  xfo = xlo
  yfo = ylo
  xfi = xli
  yfi = yli
  mm = mm + 1
endwhile
*
*	default string
*
'set string 1 l 4 0'
*
return

function cbarn (args,lab,labstr)
*
*  Script to plot a colorbar
*
*  The script will assume a colorbar is wanted even if there is 
*  not room -- it will plot on the side or the bottom if there is
*  room in either place, otherwise it will plot along the bottom and
*  overlay labels there if any.  This can be dealt with via 
*  the 'set parea' command.  In version 2 the default parea will
*  be changed, but we want to guarantee upward compatibility in
*  sub-releases.
*
*
*	modifications by mike fiorino 940614
*
*	- the extreme colors are plotted as triangles
*	- the colors are boxed in white
*	- input arguments in during a run execution:
* 
*
*	rc=cbarn(args,lab,labstr)
*
*	where args="sf vert xmid ymid force"
*
*	sf   - scale the whole bar 1.0 = original 0.5 half the size, etc.
*	vert - 0 FORCES a horizontal bar = 1 a vertical bar
*	xmid - the x position on the virtual page the center the bar
*	ymid - the x position on the virtual page the center the bar
*	force - y - then use color info in _shdinfo.? array
*
*	if vert,xmid,ymid are not specified, they are selected
*	as in the original algorithm
*
*	to specify a color bar, in the call
*	
*	cbarg='0.90 0 5.5 0.78 y'  * where y is to force
*
*	and set the global variable _shdinfo 
*
*	_shdinfo.1='Number of levels = 13'
*	_shdinfo.2='9 < -20'
*	_shdinfo.3='14 -20 -15'
*	_shdinfo.4='4 -15 -10'
*	_shdinfo.5='11 -10 -5'
*	_shdinfo.6='5 -5 0'
*	_shdinfo.7='13 0 5'
*	_shdinfo.8='3 5 15'
*	_shdinfo.9='10 15 20'
*	_shdinfo.10='7 20 25'
*	_shdinfo.11='12 25 30'
*	_shdinfo.12='8 30 35'
*	_shdinfo.13='2 35 40'
*	_shdinfo.14='6 40 >'
*
*	where in _shdinfo.2 
*
*	9 = color
*	<	:	low value (< less than ; > greater than)
*	-20	:	high value
*
*


sf=subwrd(args,1)
vert=subwrd(args,2)
xmid=subwrd(args,3)
ymid=subwrd(args,4)
force=subwrd(args,5)
if(sf='');sf=1.0;endif


*
*  Check shading information
*
  
  if(force!='y') 
    'query shades'
    shdinfo = result
    if (subwrd(shdinfo,1)='None') 
     say 'Cannot plot color bar: No shading information'
     return
    endif
  else
    if (subwrd(_shdinfo.1,1)='None') 
     say 'Cannot plot color bar: No shading information'
     return
    endif
  endif
* 
*  Get plot size info
*
  'query gxinfo'
  rec2 = sublin(result,2)
  rec3 = sublin(result,3)
  rec4 = sublin(result,4)
  xsiz = subwrd(rec2,4)
  ysiz = subwrd(rec2,6)
  ylo = subwrd(rec4,4)
  xhi = subwrd(rec3,6)
  xd = xsiz - xhi

  ylolim=0.6*sf
  xdlim1=1.0*sf
  xdlim2=1.5*sf  
  barsf=0.8*sf
  yoffset=0.2*sf
  stroff=0.05*sf
  strxsiz=0.11*sf*0.95
  strysiz=0.12*sf*0.95
*
*  Decide if horizontal or vertical color bar
*  and set up constants.
*
  if (ylo<ylolim & xd<xdlim1) 
    say "Not enough room in plot for a colorbar"
    return
  endif

  if(force=y) 
    cnum = subwrd(_shdinfo.1,5)
  else
    cnum = subwrd(shdinfo,5)
  endif

*
*	logic for setting the bar orientation with user overides
*
  if (ylo<ylolim | xd>xdlim1)
    vchk = 1
    if(vert = 0) ; vchk = 0 ; endif
  else
    vchk = 0
    if(vert = 1) ; vchk = 1 ; endif
  endif
*
*	vertical bar
*

  if (vchk = 1 )

    if(xmid = '') ; xmid = xhi+xd/2 ; endif
    xwid = 0.2*sf
    ywid = 0.5*sf
    
    xl = xmid-xwid/2
    xr = xl + xwid
    if (ywid*cnum > ysiz*barsf) 
      ywid = ysiz*barsf/cnum
    endif
    if(ymid = '') ; ymid = ysiz/2 ; endif
    yb = ymid - ywid*cnum/2
    'set string 1 l 5'
    vert = 1

  else

*
*	horizontal bar
*

    ywid = 0.4
    xwid = 0.8

    if(ymid = '') ; ymid = ylo/2-ywid/2 ; endif
    yt = ymid + yoffset
    yb = ymid
    if(xmid = '') ; xmid = xsiz/2 ; endif
    if (xwid*cnum > xsiz*barsf)
      xwid = xsiz*barsf/cnum
    endif
    xl = xmid - xwid*cnum/2
    'set string 1 tc 5'
    vert = 0
  endif

*say 'cccccc 'xl' 'xr' 'yt' 'yb' 'xwid' 'ywid' 'cnum
*say 'cccccc 'strxsiz' 'strysiz' 'stroff

if(vert=1)
  bb=0.075*sf
  xlbb=xl - bb
  xrbb=xr + stroff + 3*strysiz + bb
  ybbb=yb - bb
  ytbb=yb + ywid*cnum + bb

*say 'cccccc 'xlbb' 'xrbb' 'ytbb' 'ybbb

  'set line 0'
  'draw recf 'xlbb' 'ybbb' 'xrbb' 'ytbb

endif



*
*  Plot colorbar
*


  'set strsiz 'strxsiz' 'strysiz
  num = 0
  while (num<cnum) 

    if(force = y)
      ii=num+2 
      rec=_shdinfo.ii
      col = subwrd(rec,1)
      hi = subwrd(rec,3)
    else
      rec = sublin(shdinfo,num+2)
      col = subwrd(rec,1)
      hi = subwrd(rec,3)
    endif
    if (vert) 
      yt = yb + ywid
    else 
      xr = xl + xwid
    endif

    if(num!=0 & num!= cnum-1)
    'set line 'col
    'draw recf 'xl' 'yb' 'xr' 'yt
    'set line 1 1 4'
    'draw rec 'xl' 'yb' 'xr' 'yt
    if (num<cnum-1)
      if (vert) 
        xp=xr+stroff
        'draw string 'xp' 'yt' 'hi
      else
        yp=yb-stroff
        'draw string 'xr' 'yp' 'hi
      endif
    endif
    endif

    if(num = 0 )

      if(vert = 1)

        xm=(xl+xr)*0.5
        'set line 'col
        'draw polyf 'xl' 'yt' 'xm' 'yb' 'xr' 'yt' 'xl' 'yt

        'set line 1 1 4'
        'draw line 'xl' 'yt' 'xm' 'yb
        'draw line 'xm' 'yb' 'xr' 'yt
        'draw line 'xr' 'yt' 'xl' 'yt


      else

        xm=(xl+xr)*0.5
        ym=(yb+yt)*0.5

        'set line 'col
       'draw polyf 'xl' 'ym' 'xr' 'yb' 'xr' 'yt' 'xl' 'ym
        'set line 1 1 4'
        'draw line 'xl' 'ym' 'xr' 'yb
        'draw line 'xr' 'yb' 'xr' 'yt
        'draw line 'xr' 'yt' 'xl' 'ym

      endif

    endif

    if (num<cnum-1)
      if (vert)
         xp=xr+stroff 
        'draw string 'xp' 'yt' 'hi
      else
         yp=yb-stroff
        'draw string 'xr' 'yp' 'hi
      endif
    endif

    if(num = cnum-1 )

      if( vert = 1)

        'set line 'col
        'draw polyf 'xl' 'yb' 'xm' 'yt' 'xr' 'yb' 'xl' 'yb

        'set line 1 1 4'
        'draw line 'xl' 'yb' 'xm' 'yt
        'draw line 'xm' 'yt' 'xr' 'yb
        'draw line 'xr' 'yb' 'xl' 'yb


        if(lab=y) 
          ylb=yt+0.25
          strxsizl=strxsiz*1.75
          strysizl=strysiz*1.75
          'set string 1 c 6'
          'set strsiz 'strxsizl' 'strysizl
          'draw string 'xm' 'ylb' 'labstr
          'set string 1 tc 5'
        endif
      else

        'set line 'col
        'draw polyf 'xr' 'ym' 'xl' 'yb' 'xl' 'yt' 'xr' 'ym

        'set line 1 1 4'
        'draw line 'xr' 'ym' 'xl' 'yb
        'draw line 'xl' 'yb' 'xl' 'yt
        'draw line 'xl' 'yt' 'xr' 'ym

        if(lab=y) 
          ylb=yt+0.15
          strxsizl=strxsiz*2.0
          strysizl=strysiz*2.0
          'set string 1 c 6'
          'set strsiz 'strxsizl' 'strysizl
          'draw string 'xmid' 'ylb' 'labstr
          'set string 1 tc 5'
        endif

      endif

    endif

    if (num<cnum-1)
      if (vert) 
        xp=xr+stroff
        'draw string 'xp' 'yt' 'hi
      else
        yp=yb-stroff
       'draw string 'xr' 'yp' 'hi
      endif
    endif

    num = num + 1
    if (vert); yb = yt;
    else; xl = xr; endif;
  endwhile
return

function eclogo(xb1,yb1,csiz)

x1=xb1-csiz*0.6
y1=yb1-csiz*0.6
x2=x1+csiz*1.5
y2=y1+csiz*1.0

'set line 0 0 0'
'draw recf 'x1' 'y1' 'x2' 'y2

cthk=0.55
cthk=csiz*cthk

xb2=xb1+csiz*0.5
yb2=yb1
'set line 1 0 0'
'draw mark 3 'xb1' 'yb1' 'csiz
'set line 0 0 0'
'draw mark 3 'xb1' 'yb1' 'cthk
'set line 1 0 0'
'draw mark 3 'xb2' 'yb2' 'csiz
'set line 0 0 0'
'draw mark 3 'xb2' 'yb2' 'cthk
'set line 0 0 0'
'draw mark 3 'xb1' 'yb2' 'cthk

blen=cthk
bhgt=0.5*blen

x1=xb2-blen*0.5+csiz*0.5
y1=yb2-bhgt*0.5
x2=xb2+blen*0.5+csiz*0.5
y2=yb2+bhgt*0.5
'set line 0 0 0'
'draw recf 'x1' 'y1' 'x2' 'y2

x1=xb1-blen*0.5-csiz*0.5
y1=yb1-bhgt*0.4
x2=xb1+blen*0.5-csiz*0.5
y2=yb1+bhgt*0.4

'set line 0 0 0'
'draw recf 'x1' 'y1' 'x2' 'y2

x1=xb1-csiz*0.5
y1=yb1-bhgt*0.25
x2=x1+cthk*0.8
y2=yb1+bhgt*0.25

'set line 1 0 0'
'draw recf 'x1' 'y1' 'x2' 'y2
return(0)


function jaecol()

*light yellow to dark red
'set rgb 21 255 250 170'
'set rgb 22 255 232 120'
'set rgb 23 255 192  60'
'set rgb 24 255 160   0'
'set rgb 25 255  96   0'
'set rgb 26 255  50   0'
'set rgb 27 225  20   0'
'set rgb 28 192   0   0'
'set rgb 29 165   0   0'
*
*light green to dark green
'set rgb 31 230 255 225'
'set rgb 32 200 255 190'
'set rgb 33 180 250 170'
'set rgb 34 150 245 140'
'set rgb 35 120 245 115'
'set rgb 36  80 240  80'
'set rgb 37  55 210  60'
'set rgb 38  30 180  30'
'set rgb 39  15 160  15'
*set rgb 39   5 150   5
*
*light blue to dark blue
'set rgb 41 200 255 255'
'set rgb 42 175 240 255'
'set rgb 43 130 210 255'
'set rgb 44  95 190 250'
'set rgb 45  75 180 240'
'set rgb 46  60 170 230'
'set rgb 47  40 150 210'
'set rgb 48  30 140 200'
'set rgb 49  20 130 190'
*
*light purple to dark purple
'set rgb 51 220 220 255'
'set rgb 52 192 180 255'
'set rgb 53 160 140 255'
'set rgb 54 128 112 235'
'set rgb 55 112  96 220'   
'set rgb 56  72  60 200'   
'set rgb 57  60  40 180'
'set rgb 58  45  30 165'
'set rgb 59  40   0 160'
*
*light pink to dark rose  
'set rgb 61 255 230 230'
'set rgb 62 255 200 200'
'set rgb 63 248 160 160'
'set rgb 64 230 140 140'
'set rgb 65 230 112 112'
'set rgb 66 230  80  80'   
'set rgb 67 200  60  60'   
'set rgb 68 180  40  40'
'set rgb 69 164  32  32'

'set rgb 71 250 250 250'
'set rgb 72 200 200 200'
'set rgb 73 160 160 160'
'set rgb 74 140 140 140'
'set rgb 75 112 112 112'
'set rgb 76  80  80  80'   
'set rgb 77  60  60  60'   
'set rgb 78  40  40  40'
'set rgb 79  32  32  32'

return



function efscol(cmap)

if(cmap=efs_1)
'set rgb 20    0  29  29'
'set rgb 21    0  49  49'
'set rgb 22    0  69  69'
'set rgb 23    0  89  89'
'set rgb 24    0 109 109'
'set rgb 25    0 129 129'
'set rgb 26    0 149 149'
'set rgb 27    0 169 169'
'set rgb 28    0 189 189'
'set rgb 29    0 209 209'
'set rgb 30    0 229 229'
'set rgb 31    0 249 249'
'set rgb 32    0 209 255'
'set rgb 33    0 169 255'
'set rgb 34    0 129 255'
'set rgb 35    0  89 255'
'set rgb 36    0  49 255'
'set rgb 37   49   0 255'
'set rgb 38   89   0 255'
'set rgb 39  109   0 255'
'set rgb 40  149   0 255'
'set rgb 41  189   0 255'
'set rgb 42  209   0 255'
'set rgb 43  249   0 255'
'set rgb 44  255   0 209'
'set rgb 45  255   0 169'
'set rgb 46  255   0 129'
'set rgb 47  255   0  89'
'set rgb 48  255   0  49'
return('20 48')

endif

if(cmap='efs_2')
'set rgb 20  99   0  99'
'set rgb 21 159   0 159'
'set rgb 22 255   0 255'
'set rgb 23 205   0 255'
'set rgb 24 169   0 255'
'set rgb 25  99   0 255'
'set rgb 26   0   0 255'
'set rgb 27   0  79 255'
'set rgb 28   0 192 255'
'set rgb 29   0 255 255'
'set rgb 30   0 255 205'
'set rgb 31   0 255 179'
'set rgb 32   0 255  79'
'set rgb 33   0 255   0'
'set rgb 34 165 255   0'
'set rgb 35 205 255   0'
'set rgb 36 255 255   0'
'set rgb 37 255 205   0'
'set rgb 38 255 154   0'
'set rgb 39 255 102   0'
'set rgb 40 255   0   0'
'set rgb 41 205   0   0'
'set rgb 42 165   0   0'
return('20 42')
endif

if(cmap='efs_3')

'set rgb 20   0   0   0'
'set rgb 21   0  55  55'
'set rgb 22   0  65  65'
'set rgb 23   0  75  75'
'set rgb 24   0  85  85'
'set rgb 25   0  95  95'
'set rgb 26   0 105 105'
'set rgb 27   0 115 115'
'set rgb 28   0 125 125'
'set rgb 29   0 135 135'
'set rgb 30   0 145 145'
'set rgb 31   0 155 155'
'set rgb 32   0 165 165'
'set rgb 33   0 175 175'
'set rgb 34   0 185 185'
'set rgb 35   0 195 195'
'set rgb 36   0 205 205'
'set rgb 37   0 215 215'
'set rgb 38   0 225 225'
'set rgb 39   0 235 235'
'set rgb 40   0 245 245'
'set rgb 41 255 255 255'
'set rgb 42 255 255 255'
return('20 42')

endif

if(cmap=efs_4)
'set rgb 50   0 100   0'
'set rgb 51   0 120   0'
'set rgb 52   0 140   0'
'set rgb 53   0 160   0'
'set rgb 54   0 180   0'
'set rgb 55   0 200   0'
'set rgb 56   0 220   0'
'set rgb 57   0 230   0'
'set rgb 58   0 240   0'
'set rgb 59   0 255   0'
'set rgb 60  85 255   0'
'set rgb 61 125 255   0'
'set rgb 62 165 255   0'
'set rgb 63 205 255   0'
'set rgb 64 255 225   0'
'set rgb 65 255 205   0'
'set rgb 66 225 185   0'
'set rgb 67 205 165   0'
'set rgb 68 185 120   0'
'set rgb 69 165 120   0'
'set rgb 70 145 100   0'
'set rgb 71  85  45   0'
'set rgb 72   0   0  55'
return('50 72')
endif

if(cmap='efs_5')

'set rgb 20   0   0   0'
'set rgb 21  05  05  05'
'set rgb 22  15  15  15'
'set rgb 23  20  20  20'
'set rgb 24  25  25  25'
'set rgb 25  35  35  35'
'set rgb 26  45  45  45'
'set rgb 27 050 050 050'
'set rgb 28 050 050 050'
'set rgb 29 060 060 060'
'set rgb 30 070 070 070'
'set rgb 31 075 075 075'
'set rgb 32 085 085 085'
'set rgb 33 090 090 090'
'set rgb 34 100 100 100'
'set rgb 35 120 120 120'
'set rgb 36 140 140 140'
'set rgb 37 165 165 165'
'set rgb 38 185 185 185'
'set rgb 39 205 205 205'
'set rgb 40 205 205 205'
'set rgb 41 225 225 224'
'set rgb 42 255 255 255'

return('20 42')
endif
return

return


#ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
#
#  file
#
#ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
*
*-------------------------- ofile ------------------
*
function ofile (fname)
'query files'
i = 0
while (1)  
  if (subwrd(result,1)='No')       
    ret = 0
    break;
  endif
  rec = sublin(result,i*3+2)
  if (rec='') 
    ret = 0;
    break; 
  endif
  if (subwrd(rec,2)=fname)
    rec = sublin(result,i*3+1)
    ret = subwrd(rec,2)
    break;
  endif
  i = i + 1
endwhile
if (ret=0) 
  'open 'fname
  if (rc>0) 
    say "Error opening "fname
    return (0)
  endif
  rec = sublin(result,2)
  ret = subwrd(rec,8)
endif
return (ret)
