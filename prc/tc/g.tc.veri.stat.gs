function main(args)

_nbscl1=0.98
_nbscl2=0.99

_nbcol2=11
_nbcol1=3

rc=gsfallow('on')
rc=const()

rc=tcgvstat()

rc=setpstat()
rc=pstat()

if(_prod=1);
 '!sleep 1'
 'quit'
endif
return


function pstat()


'set t 1 last'
rc=setbackground(1)
rc=setgrads()

if(_etau = 120)
  'set t 0.5 6.5'
  'set xaxis -12 132 24'
  'set xlopts 1 5 0.15'
  'set xlabs  0 h | 24 h | 48 h | 72 h | 96 h | 120 h '
else
  'set t 0.5 3.5'
  'set xaxis -12 8424'
  'set xlopts 1 5 0.15'
  'set xlabs  0 h | 24 h | 48 h | 72 h '
endif


#pppppppppppppppppppppppppppppppppppppppppppppppppp
#
#
#
#oooooooooooooooooooooooooooooooodddddddddddddddddd

if(_plttype = 'pod') 

#
#  data
#
'pdm1=m1(x='_xpd')'
'pdm2=m2(x='_xpd')'

#
#  plot pod
#

'set gxout bar'
'set bargap 50'
'set ccolor 3'
'set vrange 0 120'
'set yaxis 0 120 10'
'd pdm1'

'set bargap 75'
'set ccolor 4'
'd pdm2'

'set ccolor 0'
'set cthick 10' 
'set baropts outline'
'd pdm2'

#
#  draw 100% line
# 
'q gr2xy 0.5 100' ; x1=subwrd(result,3) ; y1=subwrd(result,6)
'q gr2xy 6.5 100' ; x2=subwrd(result,3) ; y2=subwrd(result,6)
'set line 1 1 10'
'draw line 'x1' 'y1' 'x2' 'y2

dobullet=1

if(dobullet) 
#
#  plot bullet bars 
#

'set ylpos -0.50 l'
'set vrange 0 '_ntmax
'set yaxis 0 '_ntmax' '_ntinc
'set grid off'

rc=numbar(m2,_nbcol2,_nbscl2)
rc=numbar(m1,_nbcol1,_nbscl1)

rc=plotdims()
xyl=_xlplot-0.3
yyl=_ytplot+0.2

#
# label N
#
xyl=_xlplot-0.6
'set string 1 c 5'
'set strsiz 0.15'
'draw string 'xyl' 'yyl' N '
endif

#
# label pod
#

'set string 1 l 5'
'set strsiz 0.15'
'draw string 'xyl' 'yyl' POD [%]'



endif


if(_plttype = 'impclp') 

#
#  data
#
'icm1=m1(x='_xic')'
'icm2=m2(x='_xic')'

#
#  plot pod
#

imin=-30
imax=70
'set gxout bar'
'set bargap 50'
'set barbase 0'
'set ccolor 3'
'set vrange 'imin' 'imax
'set yaxis 'imin' 'imax
'd icm1'

'set bargap 75'
'set ccolor 4'
'd icm2'

'set ccolor 0'
'set cthick 10' 
'set baropts outline'
'd icm2'

#
#  draw 0% line
# 
'q gr2xy 0.5 0' ; x1=subwrd(result,3) ; y1=subwrd(result,6)
'q gr2xy 6.5 0' ; x2=subwrd(result,3) ; y2=subwrd(result,6)
'set line 1 1 10'
'draw line 'x1' 'y1' 'x2' 'y2

dobullet=1

if(dobullet) 
#
#  plot bullet bars 
#

'set ylpos -0.50 l'
'set vrange 0 '_ntmax
'set yaxis 0 '_ntmax' '_ntinc
'set grid off'

rc=numbar(m2,_nbcol2,_nbscl2)
rc=numbar(m1,_nbcol1,_nbscl1)

rc=plotdims()
xyl=_xlplot-0.3
yyl=_ytplot+0.2


#
# label N
#
xyl=_xlplot-0.6
'set string 1 c 5'
'set strsiz 0.15'
'draw string 'xyl' 'yyl' N '

endif
#
# label pod
#

'set string 1 l 5'
'set strsiz 0.15'
'draw string 'xyl' 'yyl' % ImpCLP'

endif

#iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
#
# intensity
#
#iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii


if(_plttype = 'vmax') 

#
#  data
#
'iem1=m1(x='_xfve')'
'iem2=m2(x='_xfve')'
'ieum1=m1(x='_xfveu')'
'ieum2=m2(x='_xfveu')'

#
#  plot mean abs error
#

imin=-50
imax=50
'set gxout bar'
'set bargap 50'
'set barbase 0'
'set ccolor 3'
'set vrange 'imin' 'imax
'set yaxis 'imin' 'imax
'd ieum1'

'set bargap 75'
'set ccolor 4'
'd ieum2'

'set ccolor 0'
'set cthick 10' 
'set baropts outline'
'd ieum2'

#
#  draw 0% line
# 
'q gr2xy 0.5 0' ; x1=subwrd(result,3) ; y1=subwrd(result,6)
'q gr2xy 6.5 0' ; x2=subwrd(result,3) ; y2=subwrd(result,6)
'set line 1 1 10'
'draw line 'x1' 'y1' 'x2' 'y2

'set gxout line'
'set vrange 'imin' 'imax
'set yaxis 'imin' 'imax

'set ccolor 0'
'set cthick 10' 
'd iem1'
'set cthick 5' 
'set ccolor 3'
'd iem1'

'set ccolor 0'
'set cthick 10' 
'd iem2'
'set cthick 5' 
'set ccolor 4'
'd iem2'




#
#  plot bullet bars 
#

'set ylpos -0.50 l'
'set vrange 0 '_ntmax
'set yaxis 0 '_ntmax' '_ntinc
'set grid off'

rc=numbar(m2,_nbcol2,_nbscl2)
rc=numbar(m1,_nbcol1,_nbscl1)

rc=plotdims()
xyl=_xlplot-0.3
yyl=_ytplot+0.2

#
# label pod
#

'set string 1 l 5'
'set strsiz 0.15'
'draw string 'xyl' 'yyl' Mean Abs VE'

#
# label N
#
xyl=_xlplot-0.6
'set string 1 c 5'
'set strsiz 0.15'
'draw string 'xyl' 'yyl' N '

endif


#fffffffffffffffffffffffffffffffffffffffffffffffffffffff
#
#
#
#eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee

if(_plttype='fe')

#
# data
#
'm1fe=m1(x='_xfe')'  ;  'm2fe=m2(x='_xfe')'
'm1mw=m1(x='_xfmw')' ;  'm2mw=m2(x='_xfmw')' ; 'btmw=m1(x='_xbmw')'

if(_units=metric)
  'm1fe=m1fe*'_nm2km ; 'm2fe=m2fe*'_nm2km
  'm1mw=m1mw*'_kt2ms ; 'm2mw=m2mw*'_kt2ms  ; 'btmw=btmw*'_kt2ms
endif

#
# plot fe
#

'set gxout bar'
'set bargap 50'
'set ccolor 3'
'set vrange 0 '_femax
'set yaxis 0 '_femax' '_feinc
'd m1fe'

'set bargap 75'
'set ccolor 4'
'd m2fe'

'set ccolor 0'
'set cthick 10' 
'set baropts outline'
'd m2fe'

#
#  plot max wind
#

'set gxout line'
'set ylpos 0 r'
'set vrange 0 '_mwmax
'set yaxis 0 '_mwmax' '_mwinc
'set grid off'

'set ccolor 0' ; 'set cthick 15' ; 'd m1mw'
'set ccolor 3' ; 'set cthick 4'  ; 'd m1mw'
'set ccolor 0' ; 'set cthick 15' ; 'd m2mw'
'set ccolor 4' ; 'set cthick 4'  ; 'd m2mw'
'set ccolor 0' ; 'set cthick 15' ; 'set cstyle 2' ; 'd btmw'
'set ccolor 1' ; 'set cthick 5'  ; 'set cstyle 2' ; 'd btmw'

#
#  plot bullet bars 
#

'set ylpos -0.50 l'
'set vrange 0 '_ntmax
'set yaxis 0 '_ntmax' '_ntinc
'set grid off'

rc=numbar(m2,_nbcol2,_nbscl2)
rc=numbar(m1,_nbcol1,_nbscl1)

#
# plot ct/at circles
#

rc=plotdims()

rc=ctaterr(24)
if(rc = -9999) ; return (-9999) ;endif

rc=ctaterr(72)
if(rc = -9999) ; return (-9999) ;endif

if(_etau=120)
rc=ctaterr(120)
endif

#
# label Vmax
#

xyl=_xrplot+0.2   
yyl=_ytplot+0.2

'set string 1 r 5'
'set strsiz 0.15'
if(_units=english) ; ltle='V`bmax`n [kt]' ; endif
if(_units=metric)  ; ltle='V`bmax`n [ms`a-1`n]' ; endif
'draw string 'xyl' 'yyl' 'ltle

#
# label FE 
#

xyl=_xlplot-0.3 

'set string 1 l 5' ; 'set strsiz 0.15'
if(_units=english) ; ltle='FE [nm]' ; endif
if(_units=metric)  ; ltle='FE [km]' ; endif
'draw string 'xyl' 'yyl' 'ltle

#
# label N
#

xyl=_xlplot-0.6
'set string 1 c 5' ;  'set strsiz 0.15'
'draw string 'xyl' 'yyl' N '

endif

#ttttttttttttttttttttttttttttttttttttttttttttttttttttt
#
# titles
#
#ttttttttttttttttttttttttttttttttttttttttttttttttttttt


rc=plotdims()
rc=modelab()
rc=toptitle(_tt1,_tt2,_ttlscl,_t1col,_t2col)

rc=stitle(_st1,0.7,1,8)
rc=stitle(_st2,0.7,2,8)
rc=stitle(_st3,0.7,3,8)
rc=bottitle(_tack1,_tack2,1,1,1)


#ppppppppppppppppppppppppppppppppppppppppppppppppppppppp
#
# printing
#
#ppppppppppppppppppppppppppppppppppppppppppppppppppppppp

'enable print '_gmpath
'print'
'disable print'
#'!gxps -c -i '_gmpath' -o '_pspath
'!gxeps -c -i '_gmpath' -o '_epspath
'printim '_pngpath' x'_xsizepng' y'_ysizepng' white'
'!rm '_gmpath

return


function setpstat()

_script='g.tc.stat.basin.gs'
_author='CDR M. Fiorino, USNR, NR ONR/NRL S&T 114 TC Analysis Project'
_author='CDR M. Fiorino, USN(RC), NR COMPACFLT DET 520 JTWC TC Analysis Project'

_ttlscl=0.85
_t1col=1
_t2col=1

_xsizepng=800
_ysizepng=600

_etau=120

_xnt=1
_xnf=2
_xpd=3
_xic=4
_xfe=5
_xct=6
_xat=7
_xfmw=9
_xbmw=10
_xfve=11
_xfveu=12

#
#  open the file
#

rc=ofile(_vpath)
if(rc = 0)  ; print 'unable to open: '_vpath ;  'quit' ; endif

#
# set the plot area
#

ppx=0.90
ppy=0.90
ppy=0.90
pytoff=0.65
pyboff=0.25
pyboff=-0.10
_stlscl=0.8

laydir=1
np=1
asymx=1.0
asymy=0.5

rc=plotdims()
i=np
rc=pltarea2(np,ppx,ppy,laydir,pytoff,pyboff,asymx,asymy)
'set parea '_xpl.i' '_xpr.i' '_ypb.i' '_ypt.i

#
# bounds 
#

_tack1=_author
_tack2=_epsfile


'set x 1'


setmax=0
if(_ntmax = '' | _ntmax = 0)
  _ntmax=0
  _mwmax=0
  _femax=0
  setmax=1
  t=1
  te=6
  while(t<=te) 
    'set t 't
    'd m1(x='_xnt')'
    nti=subwrd(result,4)
    if(nti < 1e20 & nti > _ntmax) ; _ntmax=nti ; endif
    print 'nti 't' 'nti' '_ntmax

    'd m1(x='_xfmw')'
    mwi=subwrd(result,4)
    print 'mwi 't' 'mwi' '_mwmax
    if(mwi <- 1e20 & mwi > _mwmax) ; _mwmax=mwi ; endif

    'd m2(x='_xfmw')'
    mwn=subwrd(result,4)
    if(mwn < 1e20 & mwn > _mwmax) ; _mwmax=mwn ; endif

    'd m1(x='_xfe')'
    fei=subwrd(result,4)
    if(fei < 1e20 & fei > _femax) ; _femax=fei ; endif

    'd m2(x='_xfe')'
    fen=subwrd(result,4)
    if(fen < 1e20 & fen > _femax) ; _femax=fen ; endif
    t=t+1
  endwhile


  _femax=(nint(_femax/_feinc)+1)*_feinc
  _mwmax=(nint(_mwmax/_mwinc)+1)*_mwinc
  _ntmax=(nint(_ntmax/_ntinc)+1)*_ntinc

  if(_ntmax >= 1000)
    _ntinc=200
  endif

  if(_ntmax > 500)
    _ntinc=50
  endif
endif

if(_units = english) 
  _feinc=50
  _mwinc=10
  _ntinc=10
endif

if(_units = metric) 
  _feinc=100
  _mwinc=5
  _ntinc=10
endif

if(_ntmax >= 400)
  _ntinc=25
endif

if(_ntmax >= 800)
  _ntinc=50
endif

if(_units=metric & setmax=1)
  _femax=_femax*_nm2km
endif

'set warn off'

return






function getcurdtg(type)

'!dtg > /tmp/dtg.txt'
rc=read('/tmp/dtg.txt')
ok=sublin(rc,1)
if(ok = 0)
  curdtg=sublin(rc,2)
  print 'ccc 'curdtg
  yyyymmdd=substr(curdtg,1,8)
endif

if(type = 'yyyymmdd')
  return(yyyymmdd)
else
  return(curdtg)
endif



function modelab()

xl=_xlplot+0.05
yl=_ytplot-0.15
'set string 3 l 6'
'set strsiz 0.14'
'draw string 'xl' 'yl' '_m1tup

#xl=xl+0.70
#'set string 1 l 7'
#'draw string 'xl' 'yl' v '
#xl=xl+0.15

yl=yl-0.15
xlv=xl+0.10
'set string 1 l 7'
'draw string 'xlv' 'yl' v '

yl=yl-0.20
'set string 4 l 6'
'draw string 'xl' 'yl' '_m2tup

return

function numbar(m,bcol,fact)

bgo=86*fact
bgb0=92*fact
bgb=94*fact
bge=90*fact

bgo=95*fact
bge=95*fact

bgb=99*fact
bgb0=100*fact

'set bargap 'bgo
'set baropts outline'
'set gxout errbar'

'set ccolor 0'
'set cthick 15'
'd 'm'(x='_xnt');'m'(x='_xnt')'
'set ccolor 1'
'set cthick 6'
'd 'm'(x='_xnt');'m'(x='_xnt')'

'set bargap 'bge
'set gxout errbar'

'set ccolor 0'
'set cthick 15'
'd 'm'(x='_xnt');'m'(x='_xnf')'

'set ccolor 'bcol
'set cthick 5'
'd 'm'(x='_xnt');'m'(x='_xnf')'

'set bargap 'bgo
'set baropts outline'
'set gxout errbar'
'set ccolor 0'
'set cthick 15'
'd 'm'(x='_xnt');'m'(x='_xnt')'

'set ccolor 1'
'set cthick 6'
'd 'm'(x='_xnt');'m'(x='_xnt')'


'set baropts filled'
'set bargap 'bgb0
'set gxout bar'

'set ccolor 0'
'd 'm'(x='_xnt');'m'(x='_xnf')'

'set bargap 'bgb
'set ccolor 'bcol
'set cthick 6'
'd 'm'(x='_xnt');'m'(x='_xnf')'

return



#------------------------------------------------------------------------------
#
#  cp plots for web  and create a log
#
#------------------------------------------------------------------------------

function cpplots(tdir)

if(_curseason = '' | _curseason='_curseason')

  csfile='/tmp/zy0x1s2.tc'

  '!echo $WXMAP_TC_CURRENT_SEASON > 'csfile
  '!echo $WXMAP_TC_SITREP_DIR >> 'csfile
  rc=read(csfile)
  _curseason=subwrd(rc,2)

  rc=read(csfile)
  _sitrepdir=subwrd(rc,2)
  '!rm 'csfile

endif

tdir=_sitrepdir'/'_curseason'/plt'

if(tdir != '')
  '!cp '_gifpath' 'tdir
  '!cp '_pngpath' 'tdir
  '!cp '_pspath' 'tdir
  '!cp '_gmpath' 'tdir
endif

logfile='/tmp/plot.log_g.tc.bt.climo.ll.gs_.txt'
q
rc=write(logfile,_gmpath)
rc=write(logfile,_gifpath)
rc=write(logfile,_pngpath,append)
rc=write(logfile,_pspath,append)
rc=write(logfile,_epspath,append)
rc=write(logfile,_epsipath,append)

return


function setbackground(opt)

if(opt = 1)
  'set display color white'
  'set rgb 99 254 254 254'
  'set background 99'
endif

return

function setgrads()

  'c'
  'set grads off'
  'set timelab on'
#  'set xlopts 1 '_lthk
#  'set ylopts 1 '_lthk 

return

return
*
*-------------------------- stitle ------------------
*
function stitle(t1,scale,n,tcol)

  rc=plotdims()
  dxs=_xlplot
  dyt=_pagey-_ytplot

  tsiz=0.15
  xoff=0.75
  yoff=0.10
  if(n=1) ; yoff=1.00*scale ; endif
  if(n=2) ; yoff=0.75*scale ; endif
  if(n=3) ; yoff=0.50*scale ; endif

  yoff=yoff+0.1

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
  'set string 'tcol' c 5 'angle
  'draw string 'xs' 'ys' 't1
  'set string 'tcol' c 5 0'

return

function ctaterr(tau,opt1)

# ------------------------------------------------------
#
#	get the errrors
#
# ------------------------------------------------------

xx=(tau/24)+1
'set t 'xx

if(opt1='test')

  'set x 1'
  'set y 1'
  'set z '_nbasin
  x0=5.5
  y0=4.5
  csiz=4.0

else

  csiz=1.0
  'q gr2xy 'xx' 1'
  yoff=0.25
  x0=subwrd(result,3)
  y0=_ytplot-(csiz)*0.5-yoff

 print 'x0, y0 = 'x0' 'y0' '_ytplot

endif


'd m1(x='_xfe')'
fe1=subwrd(result,4)

'd m1(x='_xct')'
cte1=subwrd(result,4)

'd m1(x='_xat')'
ate1=subwrd(result,4)

'd m2(x='_xfe')'
fe2=subwrd(result,4)

'd m2(x='_xct')'
cte2=subwrd(result,4)

'd m2(x='_xat')'
ate2=subwrd(result,4)

if(_units='metric' & cte1 !=1e20 & cte2 !=1e20)
  fe1=fe1*_nm2km
  fe2=fe2*_nm2km
  cte1=cte1*_nm2km
  cte2=cte2*_nm2km
  ate1=ate1*_nm2km
  ate2=ate2*_nm2km
endif

fe1=nint(fe1)
cte1=nint(cte1)
ate1=nint(ate1)

fe2=nint(fe2)
cte2=nint(cte2)
ate2=nint(ate2)

bcol1=3
bcol2=4
#print 'fffffffff fe1, cte1, ate1 = 'fe1' 'cte1' 'ate1' '_model1' '_m1
#print 'fffffffff fe2, cte2, ate2 = 'fe2' 'cte2' 'ate2' '_model2' '_m2

if(fe1 = 1e20)
  return(-9999)
endif

if(cte2 = 1e20)  ; cte2= '***' ; endif
if(ate2 = 1e20)  ; ate2= '***' ; endif

colct=8
colat=2

if(cte1 < 1000)
rc=errcirc(x0,y0,csiz,fe1,cte1,ate1,bcol1,opt,colct,colat)
rc=errlab(x0,y0,csiz,cte1,ate1,cte2,ate2,colct,colat)
endif

x0=x0+0.025
y0=y0+0.025

opt='nocirc'
csiz=csiz*(fe2/fe1)

#print 'cccccccccccccccccccc 'cte1' 'cte2

if(cte2 < 1000 & cte2 != '***')
rc=errcirc(x0,y0,csiz,fe2,cte2,ate2,bcol2,'nocirc',colct,colat)
endif
return



function errlab(x0,y0,csiz,cte1,ate1,cte2,ate2,colct,colat)

ss=csiz*0.07
dx=csiz*0.5
dy=dx*0.5
yoff=0.05
xoff=yoff
soff=0.025*(csiz/1.5)

x1=x0-dx-xoff*0.5
x2=x1+dx
y1=y0-dx - dy - yoff
y2=y1+dy

'set line 3'
'draw rec 'x1' 'y1' 'x2' 'y2
'draw line 'x1' 'y1' 'x2' 'y2

'set string 'colct' l'
'set strsiz 'ss
xs=x1+soff
ys=y2-soff*4

'draw string 'xs' 'ys' 'cte1

'set string 'colat' r'
xs=x2-soff
ys=y1+soff*4

'draw string 'xs' 'ys' 'ate1

x1=x2+xoff
x2=x1+dx
'set line 4'
'draw rec 'x1' 'y1' 'x2' 'y2
'draw line 'x1' 'y1' 'x2' 'y2

'set string 'colct' l'
xs=x1+soff
ys=y2-soff*4

'draw string 'xs' 'ys' 'cte2

'set string 'colat' r'
xs=x2-soff
ys=y1+soff*4

'draw string 'xs' 'ys' 'ate2



return



function errcirc(x0,y0,csiz,fe,cte,ate,bcol,opt,colct,colat)

angcte=atan2(cte,0)
angcte=angcte*_r2d
angcte=angcte+270

angate=atan2(0,ate)
angate=angate*_r2d
angate=angate+270

angctate=atan2(cte,ate)
angctate=angctate*_r2d
angctate=angctate+270

### print 'angcte = 'angcte' 'cte
### print 'angate = 'angate' 'ate
### print 'angctate = 'angctate

ctate=sqrt(cte*cte+ate*ate)
ctate=nint(ctate)
alen=ctate/fe
cte=cte
### print 'alen = 'alen' 'fe' 'cte' 'csiz
alencte=csiz*(abs(cte)/fe)*0.5
alenate=csiz*(abs(ate)/fe)*0.5
alenctate=csiz*(abs(ctate)/fe)*0.5
clab=fe
alab='('cte' 'ate')'
dir=ang
ss=csiz*0.125

acol=bcol
asty=1
athk=10

jcte='tc'
if(cte < 0) ; jcte='bc' ; endif

jate='bc'
if(ate < 0) ; jate='r' ; endif

felab=fe' nm'
if(_units = 'metric') ; felab=fe' km' ; endif

if(opt !='nocirc')

rc=dcircle(x0,y0,2,csiz,1,5,ss,felab)
rc=dcircle(x0,y0,1,csiz*0.75,1,2,ss,'')
rc=dcircle(x0,y0,2,csiz*0.50,1,4,ss,'')
rc=dcircle(x0,y0,1,csiz*0.25,1,2,ss,'')
endif

rc=darrow(x0,y0,csiz*0.5,270,acol,asty,athk,'',l)
rc=darrow(x0,y0,alencte,angcte,colct,1,6,'',jcte)
rc=darrow(x0,y0,alenate,angate,colat,1,6,'',jate)
rc=darrow(x0,y0,alenctate,angctate,acol,1,6,'',jate)

if(opt != 'nocirc') 
rc=ddot(x0,y0)
endif


return



function darrow(x,y,len,dir,acol,asty,athk,lab,labopt)

ss=0.10
'set strsiz 'ss

###print 'qqq111 'labopt

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

'set line 'acol' 'asty' 'athk

'draw line 'x1' 'y1' 'xa1' 'ya1
'draw line 'x1' 'y1' 'xa2' 'ya2
'draw line 'x' 'y' 'x1' 'y1

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
### print 'qqqq 'x' 'y' 'xls' 'yls' 'xl' 'yl
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

function abs(v)
if(v!=0)
rc=math_abs(v)
else
rc=0
endif
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
