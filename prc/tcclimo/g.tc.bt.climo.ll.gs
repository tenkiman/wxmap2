function main(args)

rc=gsfallow('on')
rc=const()

_script='g.tc.bt.climo.ll.gs'

_prod=0
_newclimo=1
_dowi=0
_docp=0
_dops=0

_author='CDR M. Fiorino, USNR, NRL Monterey NR S&T 114 TC Analysis Project'
_author='CDR M. Fiorino, USN, NR CNE-C6F DET 802 JTWC TC Analysis Project'
_author='Dr. M. Fiorino, TechDevAppUnit TPC/NHC, Miami FL'
_author='Dr. M. Fiorino, NOAA ESRL/GSD/AMB, Boulder, CO'
_author='Dr. Mike Fiorino (mike@wxmap2.com) WxMAP2 Ave Maria, FL'

_ysizepng=768
_xsizepng=_ysizepng*(4/3)


n=1
_basin=subwrd(args,n)      ; n=n+1
_dtg1=subwrd(args,n)       ; n=n+1
_dtg2=subwrd(args,n)       ; n=n+1
_pdir=subwrd(args,n)       ; n=n+1
_pname=subwrd(args,n)      ; n=n+1
_tcexpr=subwrd(args,n)     ; n=n+1
_curdtg=subwrd(args,n)     ; n=n+1
_btdfile=subwrd(args,n)    ; n=n+1
_flagrl=subwrd(args,n)     ; n=n+1
_byearClimo=subwrd(args,n) ; n=n+1
_eyearClimo=subwrd(args,n) ; n=n+1


rc=bsetup()

print 'DDDDDDDDDDD: '_btdfile
print 'TTTTTTTTTTT: '_tcexpr

f=ofile(_btdfile)

rc=metadata(1,'n')

rc=plotdims()

if(_newclimo = 0) ; rc=motww() ; endif


*	options
*

pp=0.825
pytoff=0.65
pyboff=0.65

*
*	laydir = 1 then lay out plots in direction of orientation 
*       laydir = 0 then lay plots counter to orientation
*
laydir=1
np=3
rc=plotarea(np,pp,laydir,pytoff,pyboff)

# -- make climo
#
rc=stcclimo();
if(rc=999); return ;endif


i=1
while(i<=np)
  say 'set parea '_xpl.i' '_xpr.i' '_ypb.i' '_ypt.i
  'set parea '_xpl.i' '_xpr.i' '_ypb.i' '_ypt.i
  rc=ptcclimo(i)
  i=i+1
endwhile

_t1=_t1
if(_t3 != '_t3')
  rc=toptle3(_t1,_t2,_t3,_ttlscl,_t1col,_t2col)
else
 rc=toptitle(_t1,_t2,_ttlscl,_t1col,_t2col)
endif

tack1=_author
tack2=_epsfile
rc=bottitle(tack1,tack2,0.8,1,1)

#rc=scrptle(0.75)

if(_dops = 1)
  'enable print '_gmpath
  'print'
  'disable print'
endif

if(_dowi = 1) 
  'wi '_gifpath
endif

if(_ploty > _plotx)
  'printim '_pngpath' x'_ysizepng' y'_xsizepng' white'
#  'gxyat -o '_pngpath' -x '_ysizepng' -y '_xsizepng
else
  'printim '_pngpath' x'_xsizepng' y'_ysizepng' white'
#  'gxyat -o '_pngpath' -x '_xsizepng' -y'_ysizepng
endif

if(_dops = 1) 
#'!gxps -c -i '_gmpath' -o '_pspath
'!gxeps -c -i '_gmpath' -o '_epspath
#'!ps2epsi '_epspath' '_epsipath
'!rm '_gmpath
endif

if(_docp)
 rc=cpplots()
endif

if(_prod);
  'quit'
else
  'q pos'
  'quit'
endif

return


function cpplots(tdir)

csfile='/tmp/zy0x1s2.tc'
'!echo $WXMAP_TC_CURRENT_SEASON > 'csfile
'!echo $WXMAP_TC_SITREP_DIR >> 'csfile
rc=read(csfile)
_curseason=subwrd(rc,2)

rc=read(csfile)
_sitrepdir=subwrd(rc,2)
'!rm 'csfile

tdir=_sitrepdir'/'_curseason'/plt'

if(tdir != '')
'!cp '_gifpath' 'tdir
'!cp '_pngpath' 'tdir
#'!cp '_pspath' 'tdir
'!cp '_gmpath' 'tdir
endif

logfile='/tmp/plot.log_g.tc.bt.climo.ll.gs_.txt'

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


#-----------------------------------------------------------------------------
#
# motww -- month 2 week
#
#-----------------------------------------------------------------------------

function motww

yymmb=substr(_dtg1,1,6)
yymme=substr(_dtg2,1,6)
yymm=yymmb



n=0
while(yymm<=yymme)
  yy=substr(yymm,1,4)*1
  mm=substr(yymm,5,2)*1

  dtg=yymm'0100'
  dtgm=yymm'0100'

  if(yymm = yymmb)
    dtg=_dtg1
  endif

  if(yymm = yymme)
    dtg=_dtg2
  endif

  ctime=dtghcur(dtgm)
  'set time 'ctime
  'q dims'
  card=sublin(result,5)
  t1=subwrd(card,9)
  rc=ymdw(dtg)
  ww=subwrd(rc,4)
  if(yymm=yymme)
    ww=1-ww
  endif

  n=n+1

  _tbt.n=t1
  _tcl.n=mm*1
  _wbt.n=ww

  mm=mm+1
  if(mm = 13)
    yy=yy+1
    mm=1
  endif
  if(mm<10)
    mm='0'mm
  endif
  yymm=yy%mm


endwhile


_nmo=n


verb=0
if(verb)
  n=1
  while(n<=_nmo) 
   print 'n = 'n' tbt = '_tbt.n' wbt = '_wbt.n' tcl = '_tcl.n
   n=n+1
 endwhile
endif

return


function stcclimo()

_ym1=substr(_dtg1,1,6)
_ym2=substr(_dtg1,1,6)
ymd1=substr(_dtg1,1,8)
ymd2=substr(_dtg2,1,8)

_ptle.1='observed'
_ptle.2=_byearClimo'-'_eyearClimo' climo'
_ptle.3='anom'
_stlscl=0.8

_ttlscl=0.85
_t1col=1
_t2col=4

if(_tcexpr = 'ts')
  _t1a='TC Activity for: 'ymd1'-'ymd2
  _t2='Activity = sum of TCdays ; TC=1.0 for TCs >= 35 kts'
endif

if(_tcexpr = 'tcstr')
  _t1a='TC Activity sTCd (scaled TCdays) for: 'ymd1'-'ymd2
  _t2='sTCd = sum of TC(scaled Vmax) every 6h * 1[d]/4[6h] units: days'
  _t3='TC=0.25(TD), 0.50(TS), 1.0(TY), 2.0(STY) climo: '_byearClimo'-'_eyearClimo
endif

if(_tcexpr = 'tcace')
  _t1a='TC Activity sACEd index|days (sACEd) for: 'ymd1'-'ymd2
  _t2='sACEd=ACE scaled by 1/(4(6h/1d)*65kt*65kt units: days'
  _t3='ACE = sum of Vmax*Vmax every 6h if Vmax>=35kt climo: '_byearClimo'-'_eyearClimo
endif

if(_tcexpr = 'huace')
  _t1a='Hurricnae HUsACEd index|days (HUsACEd) for: 'ymd1'-'ymd2
  _t2='HUsACEd=HUACE scaled by 1/(4(6h/1d)*65kt*65kt units: days'
  _t3='HUACE = sum of Vmax*Vmax every 6h if Vmax>=65kt climo: '_byearClimo'-'_eyearClimo
  
endif


if(_basin='epaclant')
  'set lat 0 60'
  'set lon 180 360'
  _pxlint=20
  _pylint=10
  _t1='EASTPAC + LANT '_t1a
  _ptscale=0.75
  _pcint=0.25
  _tcm=6

endif

if(_basin='epac')
  'set lat 0 60'
  'set lon 180 270'
  _pxlint=20
  _pylint=10
  _t1='EASTPAC '_t1a
  _ptscale=0.75
  _pcint=0.25
  _tcm=6

endif

if(_basin='lant')
  'set lat 0 60'
#  'set lon 180 360'
  'set lon 260 360'
  _pxlint=20
  _pylint=10
  _t1='LANT '_t1a
  _ptscale=0.75
  _pcint=0.25
  _tcm=6

endif

if(_basin='wpac')
  'set lat 0 60'
  'set lon 100 200'
  _pxlint=20
  _pylint=10
  _t1='WESTPAC '_t1a
  _ptscale=0.75
  _pcint=0.25
  _tcm=6

endif

#
# map display NOT calc
#
if(_basin='nio')

  'set lat 0 40'
  'set lon 40 110'
  _pxlint=20
  _pylint=10
  _t1='NIO '_t1a
  _ptscale=0.75
  _pcint=0.25
  _tcm=6

endif

if(_basin='shem')
  'set lat -50 0'
  'set lon 30 240'
  _pxlint=20
  _pylint=10
  'set mproj latlon'
  _t1='SHEM '_t1a
  _ptscale=0.85
  _pcint=0.25
  _tcm=6

endif

if(_basin='sio')
  _blat=-50
  _elat=0
  _blon=30
  _elon=135
  'set lat '_blat' '_elat
  'set lon '_blon' '_elon
  _pxlint=20
  _pylint=10
  'set mproj latlon'
  _t1='SIO '_t1a
  _ptscale=0.85
  _pcint=0.25
  _tcm=6
endif

if(_basin='swpac')
  _blat=-50
  _elat=0
  _blon=135
  _elon=240
  'set lat '_blat' '_elat
  'set lon '_blon' '_elon
  _pxlint=20
  _pylint=10
  'set mproj latlon'
  _t1='SWPAC '_t1a
  _ptscale=0.85
  _pcint=0.25
  _tcm=6
endif

if(_basin='nhem')

_blat=0
_elat=60
_blon=40
_elon=350

  'set lat '_blat' '_elat
  'set lon '_blon' '_elon
  _pxlint=20
  _pylint=10
  'set mproj latlon'
  _t1='NHEM '_t1a
  _ptscale=0.85
  _pcint=0.25
  _tcm=6

endif

if(_basin='global')

_blat=-60
_elat=60
_blon=30
_elon=350

  'set lat '_blat' '_elat
  'set lon '_blon' '_elon
  _pxlint=40
  _pylint=20
  'set mproj latlon'
  _t1='Global '_t1a
  _ptscale=0.85
  _pcint=0.25
  _tcm=6

endif


_pcint=0.10
_tcmax=2.50

#rc=setbackground(1)
rc=setgrads()
if(_newclimo = 1)
  rc=doclimoNew()
else
  rc=doclimo()
endif



if(_tcexpr = 'tcstr')
  _pt2.1='sTCd`bobs`n='_ntc
  _pt2.2='sTCd`bclimo`n='_ntcc
  _pt2.3='sTCd`banom`n='_ntca' `2%`bClimo`n ='_ptca'%'
endif

if(_tcexpr = 'tcace')
  _pt2.1='sACEd`bobs`n='_ntc
  _pt2.2='sACEd`bclimo`n='_ntcc
  _pt2.3='sACEd`banom`n='_ntca' `2%`bClimo`n ='_ptca'%'
endif

if(_tcexpr = 'huace')
  _pt2.1='HUsACEd`bobs`n='_ntc
  _pt2.2='HUsACEd`bclimo`n='_ntcc
  _pt2.3='HUsACed`banom`n='_ntca' `2%`bClimo`n ='_ptca'%'
endif

rc=efscol(efs_2)

_gmpath=_pdir'/'_pname'.gm'
_pspath=_pdir'/'_pname'.ps'
_epspath=_pdir'/'_pname'.eps'
_epsipath=_pdir'/'_pname'.epsi'
_gifpath=_pdir'/'_pname'.gif'
_pngpath=_pdir'/'_pname'.png'

_epsfile='~/'_pname'.eps'

print 'png   : '_pngpath
print 'eps   : '_epspath

return

 -- fffffffffffffffffffff ccccccccccccclllllllllllllllliiiiiiiiiiiiiiimmmmmmmmmmmmmmmmmmooooooooooooooooo
#
function doclimoNew()

'tc=c'_tcexpr
't='_tcexpr
'ta=a'_tcexpr


ntc=tccount(_basin,'t')
ntcc=tccount(_basin,'tc')
ntca=tccount(_basin,'ta')

print 'ntc,c,a: 'ntc' 'ntcc' 'ntca

if(ntcc = 0) 
  ptca=0.0
else
  ptca=((ntca)/ntcc)*100.0
  _ptca=math_nint(ptca)
endif

_ntc=math_format("%5.1f",ntc)
_ntcc=math_format("%5.1f",ntcc)
_ntca=math_format("%5.1f",ntca)

print 'NEW ntc,c,a '_ntc' '_ntcc' '_ntca' '_ptca

if(_ptca>0) ; _ptca='+'_ptca ; endif

return


# -- fffffffffffffffffffff ccccccccccccclllllllllllllllliiiiiiiiiiiiiiimmmmmmmmmmmmmmmmmmooooooooooooooooo
#
function doclimo()

'set time jan'_byearClimo' dec'_byearClimo
'q dims'
card=sublin(result,5)
t1=subwrd(card,11)
t2=subwrd(card,13)
####print 'beg climo year t1,t2 = 't1' 't2
'set t 't1' 't2


'set time jan'_byearClimo' dec'_eyearClimo
'q dims'
card=sublin(result,5)
t1c=subwrd(card,11)
t2c=subwrd(card,13)
####print 'ccccccccc t1c,t2c = 't1c' 't2c
'set t 't1' 't2

nyear=t2c-t1c+1
nyear=nyear/12

'set time jan'_byearClimo' dec'_eyearClimo

'tcs=sum(const('_tcexpr',0,-u),t+0,t='t2c',12)/'nyear
'modify tcs seasonal'

'tc=const(tcs,0,-a)'

'set t 't1
n=1
while(n<=_nmo)
  'tc=tc+const(tcs(t='_tcl.n'),0,-u)*'_wbt.n
  n=n+1
endwhile

'set t 1'
't=const('_tcexpr'(t=1),0,-a)'

#
# special case -- 2006 activity in lant != 31L from 2005
#
if((_basin='lant' | _basin='nhem') & ymd1 = 20060101)
  _wbt.1=0
endif


n=1
while(n<=_nmo)
wbttc=_wbt.n
if(_flagrl=1 & n = _nmo); wbttc=1.0 ; endif
###print  't=t+const('_tcexpr'(t='_tbt.n'),0,-u)*'wbttc
  't=t+const('_tcexpr'(t='_tbt.n'),0,-u)*'wbttc
  n=n+1
endwhile

'ta=const(t,0,-u)-const(tc,0,-u)'

acescl=1.0/(4*65.0*65.0)
if(_tcexpr = 'tcace' | _tcexpr = 'huace')
'tc=tc*'acescl
't=t*'acescl
'ta=ta*'acescl
endif
_ntc=tccount(_basin,'t')
_ntcc=tccount(_basin,'tc')
_ntca=tccount(_basin,'ta')

print 'ntc,c,a: '_ntc' '_ntcc' '_ntca

if(ntcc = 0) 
  ptca=0.0
else
  ptca=((_ntca)/_ntcc)*100.0
  _ptca=math_nint(ptca)
endif

_ntc=math_format("%5.1f",_ntc)
_ntcc=math_format("%5.1f",_ntcc)
_ntca=math_format("%5.1f",_ntca)

print 'NEW ntc,c,a '_ntc' '_ntcc' '_ntca' '_ptca

if(_ptca>0) ; _ptca='+'_ptca ; endif

return


# -- fffffffffffffffffffffffffffffffffffffff  ttttttttttttttttttttttttttcccccccccccccccccccccc
#
function tccount(basin,var)

var='const('var',0,-u)'

if(basin='epac' | basin = 'lant')

  narea=4
  lon1.1=180    ; lon2.1=258  ; lat1.1=0 ; lat2.1=90
  lon1.2=lon2.1 ; lon2.2=270  ; lat1.2=0 ; lat2.2=17
  lon1.3=lon2.2 ; lon2.3=275  ; lat1.3=0 ; lat2.3=14
  lon1.4=lon2.3 ; lon2.4=285  ; lat1.4=0 ; lat2.4=9


  if(basin='lant')
    n=2
    ntsx=asum'('var',lon='lon1.n',lon='lon2.n',lat='lat2.n',lat=90)'
    n=3  
    while(n<=narea)
      ntsx=ntsx' + asum('var',lon='lon1.n',lon='lon2.n',lat='lat2.n',lat=90)'
      n=n+1
    endwhile
    ntsx=ntsx' + asum('var',lon='lon2.4',lon=360,lat=0,lat=90)'
    tbasin='LANT'
  endif

  if(basin='epac')
    n=1
    ntsx=asum'('var',lon='lon1.n',lon='lon2.n',lat='lat1.n',lat='lat2.n')'
    n=2  
    while(n<=narea)
      ntsx=ntsx' + asum('var',lon='lon1.n',lon='lon2.n',lat='lat1.n',lat='lat2.n')'
      n=n+1
    endwhile
    tbasin='EASTPAC'
  endif
  ntcmax=200
endif

if(basin='wpac')
  lon1=100
  lon2=180
  lat1=0
  lat2=60
  ntsx=asum'('var',lon='lon1',lon='lon2',lat='lat1',lat='lat2')'
endif

if(basin='nio')
  lon1=30
  lon2=100
  lat1=0
  lat2=60
  ntsx=asum'('var',lon='lon1',lon='lon2',lat='lat1',lat='lat2')'
endif

if(basin='epaclant')
  lon1=180
  lon2=360
  lat1=0
  lat2=60
  ntsx=asum'('var',lon='lon1',lon='lon2',lat='lat1',lat='lat2')'
endif

if(basin='shem')
  lon1=30
  lon2=240
  lat1=-50
  lat2=0
  ntsx=asum'('var',lon='lon1',lon='lon2',lat='lat1',lat='lat2')'
endif

if(basin='nhem' | basin = 'global' | basin = 'sio' | basin = 'swpac')
  lon1=_blon
  lon2=_elon
  lat1=_blat
  lat2=_elat
  ntsx=asum'('var',lon='lon1',lon='lon2',lat='lat1',lat='lat2')'
endif

'd 'ntsx
ntc=subwrd(result,4)
ntc=ntc*1.0

return(ntc)


function ptcclimo(i)


'set gxout shaded'
'set csmooth on'

'set rbcols 20 21 22 23 24 25  26  27 28 29  31 0  32 33 34 35 36 37 38 39 40 41 42'
'set rbcols 20 21 22 23 24 25  26  27 28 29  31 32 33 34 35 36 37 38 39 40 41 42'
'set rbcols 21 22 23 24 25  26  27 28 29'


if(i=1)


'c'
'set grads off'
'set timelab on'
'set xlint '_pxlint
'set ylint '_pylint
# -- turn values > 2.5 (_tcmax) to _tcmax+0.1
#
't1=abs(t)'
'tm=const(maskout(t,'_tcmax'-t1),'_tcmax'+0.1,-u)'

't1=abs(tc)'
'tcm=const(maskout(tc,'_tcmax'-t1),'_tcmax'+0.1,-u)'

't1=abs(ta)'
'tam=const(maskout(ta,'_tcmax'-t1),'_tcmax'+0.1,-u)'


  rc=efscol(efs_2)
#rc=jaecol()
print 'rc = 'rc
  'set cint '_pcint
  'set black -0.1 0.1'
  'set rbrange 0 '_tcmax
'set rbcols 20 21 22 23 24 25  26  27 28 29  31 32 33 34 35 36 37 38 39 40 41 42'
###'set rbcols 20 21 22 23 24 25  26  27 28 29  31 32 33 34 35 36 37 38 39 40 41 42'
#  'd t'
  'd tm'
  rc=plotdims()
  xb=_xrplot+0.4
  yb=(_ypb.1+_ypt.2)*0.5
  cbarg='0.60 1 'xb' 'yb
  rc=cbarn(cbarg)
endif

if(i=2)
  'set cint '_pcint
  'set black -0.1 0.1'
  'set rbrange 0 '_tcmax
  'set rbcols 20 21 22 23 24 25  26  27 28 29  31 32 33 34 35 36 37 38 39 40 41 42'
#  'd tc'
  'd tcm'   
   
endif


if(i=3)
##rc=efscol(efs_2)
  'set cint '_pcint
  'set black -0.2 0.2'
  'set rbrange -'_tcmax' '_tcmax
'set rbcols 69 68 67 66 65 64 63 62 21 41 42 43 44 45 46 47 48 49'
'set rbcols 20 21 22 23 24 25  26  27 28 29  31 32 33 34 35 36 37 38 39 40 41 42'
#  'd ta'
  'd tam'

  xb=_xpr.i+0.5
  yb=(_ypb.i+_ypt.i)*0.5

  xb=(_xpr.i+_xpl.i)*0.5
  yb=_ypb.i - 0.5

  cbarg='0.75 0 'xb' 'yb
  rc=cbarn(cbarg)
endif

rc=stitle2h(_pt2.i,_ptle.i,_ptscale)

return


function bsetup 

_dogif=0
_gsdir='./'
_gsname='g.tc.bt.climo.ll..gs'
_cfg=_gsname'.cfg'


return

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


return


#tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
#
#	titles
#
#	stitle2(t1,t2,scale)
#	stitle(t1,scale)
#
#tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt

**************************************************
*
*  stitle2h
*
**************************************************

function stitle2h(t1,t2,scale)

  rc=plotdims()

n=1
while(n<=2)

  dxs=_xlplot
  dyt=_pagey-_ytplot

  xoff=0
  if(n=1)
    tsiz=0.15
    yoff=0.10
    title=t1
    xs=_xlplot+xoff
    cl=2
    or='l'
    tk=7
 endif

  if(n=2)
    tsiz=0.15
    yoff=0.10
    title=t2
    xs=_xrplot-xoff
    cl=1
    or='r'
    tk=5
  endif

  ys=_ytplot+yoff+tsiz/2 

  if(scale != 'scale' | scale != '')
   tsiz=tsiz*scale
  endif
  'set strsiz 'tsiz
  'set string 'cl' 'or' 'tk
  'draw string 'xs' 'ys' 'title

  n=n+1
endwhile

return

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
print '333333'
  'set string 1 c 4 0'
  'draw string 'x3' 'y3' '_author

return

**************************************************
*
*  plotdims
*
**************************************************

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

  print '44444'
  'set string 1 bc 6'
  'set strsiz 0.125'
  'draw string  'xm' 'ylg' '_s.j
  j=j+1
endwhile






#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
#
#  misc:
#
#  tyear(dtg) - calculate weight for monthly interp
#  wk2da(dtg) - calculate weight for weekly interp
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


function ymdw(dtg)
yy=substr(dtg,1,4)
mm=substr(dtg,5,2)
dd=substr(dtg,7,2)
nn=ndaymo(yy,mm)
ww=((nn-dd)/(nn-1))

return(yy' 'mm' 'dd' 'ww)




function tyear(dtg)
###print 'qqqqqqq 'dtg
mo=substr(dtg,5,2)*1.0
hr=substr(dtg,9,2)/24.0
da=substr(dtg,7,2)*1.0+hr

imo=substr(dtg,5,2)
if(substr(imo,1,1) = '0') ; imo=substr(imo,2,1) ; endif
mda=subwrd(_monday,imo)*0.5

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
#  DTG (YYYYMMHH):
#
#  curdtgh(ctime)	grads time -> dtg
#  dtghcur(dtgh)	dtg -> grads time
#  incdtgh(dtgh,inc)    increment dtg
#  mydate		readable format with weekday
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
#  math
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
print '555555'
  'set string 1 bc 5 0'
  xls=xl
  yls=yl+0.10
endif

if(labopt = 'tc')
print '666666'
  'set string 1 bc 5 0'
  xls=xl
  yls=yl+0.10
endif

if(labopt = 'b')
print '7777777'
  'set string 1 tc 5 0'
  xls=xl
  yls=yl-0.10
endif

if(labopt = 'bc')
print '88888888'
  'set string 1 tc 5 0'
  xls=xl+len*0.5
  yls=yl-0.10
endif

if(labopt = 'r')
print '999999999'
  'set string 1 l 5 0'
  xls=xl+0.10
  yls=yl
endif

if(labopt = 'rc')
print '1010101010101'
  'set string 1 l 0'
  xls=xl+0.10
  yls=yl-len*0.5
endif

if(labopt = 'l')
print '11 11 11 11'
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
print '12 12 12 12'
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
#  cbarn
#
#
#gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg


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
    print '13 13 13 13'
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
    print '14 14 14 14'
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
          print '15 15 15 15 15'
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
'set rgb 20   0 100   0'
'set rgb 21   0 120   0'
'set rgb 22   0 140   0'
'set rgb 23   0 160   0'
'set rgb 24   0 180   0'
'set rgb 25   0 200   0'
'set rgb 26   0 220   0'
'set rgb 27   0 230   0'
'set rgb 28   0 240   0'
'set rgb 29   0 255   0'
'set rgb 30  85 255   0'
'set rgb 31 125 255   0'
'set rgb 32 165 255   0'
'set rgb 33 205 255   0'
'set rgb 34 255 225   0'
'set rgb 35 255 205   0'
'set rgb 36 225 185   0'
'set rgb 37 205 165   0'
'set rgb 38 185 120   0'
'set rgb 39 165 120   0'
'set rgb 40 145 100   0'
'set rgb 41  85  45   0'
'set rgb 42   0   0  55'
return('20 42')
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

*
*-------------------------- bottitle ------------------
*
function bottitle(t1,t2,scale,t1col,t2col)

  'q gxinfo'
  card=sublin(result,2)

  pagex=subwrd(card,4)
  pagey=subwrd(card,6)

  xr=pagex
  xl=0
  y1=0.22*scale
  y2=0.08*scale

  xoff=0.20
  yoff=0.06
  x2=xr-xoff

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
