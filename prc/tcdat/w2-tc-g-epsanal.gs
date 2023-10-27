function main(args)

rc=gsfallow('on')
rc=const()
rc=jaecol2()

i=1
_stmid=subwrd(args,i); i=i+1
_stmname=subwrd(args,i); i=i+1
_bdtg=subwrd(args,i); i=i+1
_model=subwrd(args,i); i=i+1
_ddir=subwrd(args,i); i=i+1
_pdir=subwrd(args,i); i=i+1
_critdist=subwrd(args,i); i=i+1
_nmembers=subwrd(args,i); i=i+1
_ntaumax=subwrd(args,i); i=i+1
_dtau=subwrd(args,i); i=i+1
_veribt=subwrd(args,i); i=i+1
_xsize=subwrd(args,i); i=i+1
_curpid=subwrd(args,i); i=i+1

_verb=0
#_verb=1
_btsymscl=0.75
_btGsymscl=1.25
_sthk=6
_lthk=6

_cfileh='tceps.grid.'_stmid'.'_bdtg'.'_model'.hit.ctl'
_cfiles='tceps.grid.'_stmid'.'_bdtg'.'_model'.skp.ctl'
_tefile='tctrk.ensemble.'_stmid'.'_bdtg'.'_model'.txt'
_tdfile='tctrk.det.'_stmid'.'_bdtg'.'_model'.txt'
_bfile='bt.'_stmid'.'_bdtg'.'_model'.txt'
_bGfile='bt.gt0.'_stmid'.'_bdtg'.'_model'.txt'

_tepath=_ddir'/'_tefile
_tdpath=_ddir'/'_tdfile
_btpath=_ddir'/'_bfile
_btGpath=_ddir'/'_bGfile

_llpath=_pdir'/db.esrl.eps.pagell.'_stmid'.'_bdtg'.txt'
if(_verb) ; print 'LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL '_llpath ; endif

_bkgpath=_pdir'/bkg.'_stmid'.png'


if(_model = 'ecmt')
 _tt1='ECMWF EPS(tigge)'
endif

if(_model = 'ecmb')
 _tt1='ECMWF EPS(bufr)'
endif


if(_model = 'ncep-ecmwf')
 _tt1='ECMWF EPS(NCEP tracker)'
endif

if(_model = 'ukmo')
  _tt1='UKMO MOGREPS'
endif

if(_model = 'ncep')
  _tt1='NCEP GEFS(T254L42)'
endif

if(_model = 'cmc')
  _tt1='CMC eps'
endif

if(_model = 'esrl')
  _tt1='ESRL FIM8 eps'
endif

if(_model = 'gfsenkf')
  _tt1='GFS(T254) EnKF eps'
  _tt1='GFS(T382L64); EnKF(T382L64)'
endif

if(_model = 'fimens')
  _tt1='FIM(40kmL64; 01-10) GEFS(11-20)'
endif

_ysize=_xsize*(3.0/4.0)

_outopt='printim'
#_outopt='gxyat'

_gxyatopt=' -w 0.75'
_gxyatopt=''
_pngNcols=256

_printBmap=1
_dobasemap=1
#_dobasemap=0
_lnint=10
_ltint=5

fh=ofile(_ddir'/'_cfileh)
fs=ofile(_ddir'/'_cfiles)

if(fh = 0 | fs = 0)
print 'EEEEEEEEEEEEEEEEEEEEEE unable to ooen '_ddir'/'_cfileh' and/or '_cfiles
'quit'
endif

#bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
# 
# bt processing
#
rc=rdbt()
if(rc != 0); latc=subwrd(rc,1) ; lonc=subwrd(rc,2) ; btmw=subwrd(rc,3) ; endif


#ffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
#
#
rc=gettrk(_tdpath,'det')
rc=gettrk(_tepath,'ensemble')
if(_dobasemap = 1) ; rc=pltbmap() ; endif


ntau=1
while(ntau <= _ntaumax)
  rc=pltsp(ntau,latc,lonc,btmw,'hit')
  ntau=ntau+1
endwhile

ntau=1
while(ntau <= _ntaumax)
  rc=pltsp(ntau,latc,lonc,btmw,'sp')
  ntau=ntau+1
endwhile

'quit'

return


#ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
#
#  
function rdbt()

rc=read(_btpath)
card=sublin(rc,2)
iok=sublin(rc,1)
if(iok != 0 ) ; print 'unable to read _btpath '_btpath ; 'quit' ; endif

nbt=subwrd(card,3)

rcbt=0
i=1
while(i<=nbt) 
  rc=read(_btpath)
  card=sublin(rc,2)
  iok=sublin(rc,1)
  if(iok != 0 ) ; print 'eof reading '_btpath ; 'quit' ; endif
  if(_verb) ; print 'BT card = 'card ; endif

  _btdtg.i.1=subwrd(card,1)
  _btlt.i.1=subwrd(card,2)
  _btln.i.1=subwrd(card,3)
  _btmw.i.1=subwrd(card,4)
  _bttau.i.1=000
  _btvflg.i.1=subwrd(card,5)
  

  if(_verb) ; print 'BTTTTTT: '_dtg.i.1' '_lt.i.1' '_ln.i.1' '_mw.i.1 ; endif
  i=i+1 
endwhile

_btnt.1=nbt*1


#
# get bt for tau >= 0
#
rc=read(_btGpath)
card=sublin(rc,2)
iok=sublin(rc,1)
if(iok != 0 ) ; print 'unable to read _btGpath '_btGpath ; 'quit' ; endif

nbtgt0=subwrd(card,3)

rcbtgt0=0
i=1
while(i<=nbtgt0) 
  rc=read(_btGpath)
  card=sublin(rc,2)
  iok=sublin(rc,1)
  if(iok != 0 ) ; print 'eof reading '_btGpath ; 'quit' ; endif
  if(_verb) ; print 'BTGT0 card = 'card ; endif

  _btGdtg.i.1=subwrd(card,1)
  _btGlt.i.1=subwrd(card,2)
  _btGln.i.1=subwrd(card,3)
  _btGmw.i.1=subwrd(card,4)
  _btGtau.i.1=000
  _btGvflg.i.1=subwrd(card,5)
  

  if(_verb) ; print 'BTGT0TTTTT: '_dtg.i.1' '_lt.i.1' '_ln.i.1' '_mw.i.1 ; endif
  i=i+1 
endwhile

_btGnt.1=nbtgt0*1


rcbt=_btlt.nbt.1' '_btln.nbt.1' '_btmw.nbt.1

return(rcbt)




#ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
#
#  setup trk plot parms
#

function trkset()

*
*	draw the initial positions as a working best track
*
col12='29 27 25 23 49 47 45 43 39 37 35 33 69 67 65 63'
col12='2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 2 3 4 5 6 7 8 9 10 11 12 13 14'
col12='2 1 4 2 1 4 2 1 4 2 1 4 2 1 4 2 1 4 2 1 4 2 1 4 2 1 4 2 1 4 2 1 4 2 1 4 2 1 4 '
col12='2 1 3 4 2 1 3 4 2 1 3 4 2 1 3 4 2 1 3 4 2 1 3 4 2 1 3 4 2 1 3 4 2 1 3 4 2 1 3 4 2 1 3 4 2 1 3 4 2 1 4 '
col12='2 1 3 4 8'
col12='2 1 3 4'
col12=col12' 'col12' 'col12' 'col12' 'col12' 'col12' 'col12' 'col12' 'col12' 'col12' 'col12' 'col12' 'col12

i=1
n12=0

while(i<=_btnt.1)

  hh=substr(_btdtg.i.1,9,2)
  
  btc=1
  btlc=12
  btc=btlc
  btls=1
  btvf=_btvflg.i.1
  
  if(_hh = '00and12') 
    htest=(hh='12' | hh='00')
  endif
  
  if(_hh = '06and18')
    htest=(hh='06' | hh='18')
  endif

#
# only put verifying bts in legend
#

  if(htest)

    n12=n12+1
    btc=subwrd(col12,n12)
    bdtg=_btdtg.i.1
    _tcl.bdtg=btc

    btvmax=_btmw.i.1
    btsizmx=0.225
    btsizmn=0.150

#btsizmn=0.30
#btsizmx=0.40

    btsiz=btsizmx*(btvmax/135)
    if(btsiz<btsizmn) ; btsiz=btsizmn ; endif

    btsym=41
    if(btvmax < 65) ; btsym=40 ; endif
    if(btvmax < 25) ; btsym=1 ; endif
    
    if(btvf = 0)
      btsym=1
#      btc=15
      btsiz=btsizmn
#     btvmax=XX
    endif

    _btlgd.siz.n12=btsiz*_btsymscl
    _btlgd.sym.n12=btsym
    _btlgd.col.n12=btc
    _btlgd.dtg.n12=substr(bdtg,5,6)
    _btlgd.mw.n12=btvmax
    _btlgd.n=n12
#
# save the veri flag
#
    _btlgdvf.n12=btvf

  endif

  i=i+1

endwhile

#bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbt > tau0
#
#
i=1
n12=0

while(i<=_btGnt.1)

  hh=substr(_btGdtg.i.1,9,2)
  
  btc=1
  btlc=12
  btc=btlc
  btls=1
  btvf=_btGvflg.i.1
  
  if(_hh = '00and12') 
    htest=(hh='12' | hh='00')
  endif
  
  if(_hh = '06and18')
    htest=(hh='06' | hh='18')
  endif

#
# only put verifying bts in legend
#

  if(htest)

    n12=n12+1
    btc=subwrd(col12,n12)
    bdtg=_btGdtg.i.1
    _tcl.bdtg=btc

    btvmax=_btGmw.i.1
    btsizmx=0.275
    btsizmn=0.175

#btsizmn=0.30
#btsizmx=0.40

    btsiz=btsizmx*(btvmax/135)
    if(btsiz<btsizmn) ; btsiz=btsizmn ; endif

    btsym=41
    if(btvmax < 65) ; btsym=40 ; endif
    if(btvmax < 25) ; btsym=1 ; endif
    
    if(btvf = 0)
      btsym=1
#      btc=15
      btsiz=btsizmn
#     btvmax=XX
    endif

    _btGlgd.siz.n12=btsiz*_btGsymscl
    _btGlgd.sym.n12=btsym
    _btGlgd.col.n12=1
    _btGlgd.dtg.n12=substr(bdtg,5,6)
    _btGlgd.mw.n12=btvmax
    _btGlgd.n=n12
#
# save the veri flag
#
    _btGlgdvf.n12=btvf

  endif

  i=i+1

endwhile

if(_btnt.1 = 0) ; _btlgd.n=0 ; endif

return

#ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
#
#

function bt2xy()
#
#	convert track to plot coord
#
i=1
while(i<=_btnt.1)
  'q w2xy '_btln.i.1' '_btlt.i.1
  _xbt.i.1=subwrd(result,3)
  _ybt.i.1=subwrd(result,6)
  _dbt.i.1=1
  i=i+1
endwhile


i=1
while(i<=_btGnt.1)
  'q w2xy '_btGln.i.1' '_btGlt.i.1
  _xbtG.i.1=subwrd(result,3)
  _ybtG.i.1=subwrd(result,6)
  _dbtG.i.1=1
  i=i+1
endwhile

return


#ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
#
# plot BT > tau0
#

function plotbtG(ntau)

'set parea 1.15 9.75 0.5 8.0'
rc=plotdims()

'set clip '_xlplot' '_xrplot' '_ybplot' '_ytplot

i=1
n12=0
np=_btGnt.1
np=ntau
if(np > _btGnt.1) ; np=_btGnt.1 ; endif
while(i<=np & _veribt = 1)

  hh=substr(_btGdtg.i.1,9,2)
  btc=1
  btlc=12
  btc=btlc
  btls=1
  btvf=_btGvflg.i.1

  if(_hh = '00and12') 
    htest=(hh='12' | hh='00')
  endif

  if(_hh = '06and18') 
    htest=(hh='06' | hh='18')
  endif

  if(htest)
    n12=n12+1
    btsiz=_btGlgd.siz.n12
    btsym=_btGlgd.sym.n12
    btc=_btGlgd.col.n12
    bdtg=_btGlgd.dtg.n12
    btc=1
#
# check to see if there is a bt to put on legend
#
#    if(btsym <= 128)
       'draw wxsym 'btsym' '_xbtG.i.1' '_ybtG.i.1' 'btsiz' 'btc' 6'
#    endif
  else

    btsiz=0.040
    'set line 'btc
    if(hh='00') ; btsym=3 ; endif
    if(hh='06') ; btsym=2 ; endif
    if(hh='18') ; btsym=4 ; endif

    btsym=3
    'draw mark 'btsym' '_xbtG.i.1' '_ybtG.i.1' 'btsiz

  endif

_btlthk=8
  im1=i-1 
  if(i > 1)
    'set line 'btlc' 'btls' 6'
    'set line 1 1 '_btlthk
    'draw line '_xbtG.im1.1' '_ybtG.im1.1' '_xbtG.i.1' '_ybtG.i.1
  endif
  i=i+1
endwhile

'set clip 0 '_pagex' 0 '_pagey
return



function plotbt()

'set parea 1.15 9.75 0.5 8.0'
rc=plotdims()

'set clip '_xlplot' '_xrplot' '_ybplot' '_ytplot

i=1
n12=0
while(i<=_btnt.1)

  hh=substr(_btdtg.i.1,9,2)
  btc=1
  btlc=12
  btc=btlc
  btls=1
  btvf=_btvflg.i.1

  if(_hh = '00and12') 
    htest=(hh='12' | hh='00')
  endif

  if(_hh = '06and18') 
    htest=(hh='06' | hh='18')
  endif

  if(htest)
    n12=n12+1
    btsiz=_btlgd.siz.n12
    btsym=_btlgd.sym.n12
    btc=_btlgd.col.n12
    bdtg=_btlgd.dtg.n12
#
# check to see if there is a bt to put on legend
#
#    if(btsym <= 128)
      'draw wxsym 'btsym' '_xbt.i.1' '_ybt.i.1' 'btsiz' 'btc' 6'
#    endif
  else

    btsiz=0.040
    'set line 'btc
    if(hh='00') ; btsym=3 ; endif
    if(hh='06') ; btsym=2 ; endif
    if(hh='18') ; btsym=4 ; endif

    btsym=3
    'draw mark 'btsym' '_xbt.i.1' '_ybt.i.1' 'btsiz

  endif

  ip1=i+1 
  if(i != _btnt.1)
    'set line 'btlc' 'btls' 6'
    'draw line '_xbt.i.1' '_ybt.i.1' '_xbt.ip1.1' '_ybt.ip1.1
  endif
  i=i+1
endwhile

'set clip 0 '_pagex' 0 '_pagey
return



#ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
#
#  BT trklgd
#

function trklgd()

'set clip 0 '_pagex' 0 '_pagey
i=1
lscl=1.0
lscl=0.85
x=_xrplot+(0.10)*(1.5/lscl)
xs=x+(0.15)*lscl
y=_ytplot
y=7.9
dy=0.165*lscl
yss=dy*0.60*lscl

while(i<=_btlgd.n)

  if(_btlgdvf.i >= 0)
    'draw wxsym '_btlgd.sym.i' 'x' 'y' '_btlgd.siz.i' '_btlgd.col.i' 8'
    'set string 1 l '_sthk
    'set strsiz 'yss
    dddd=_btlgd.dtg.i
    d4=substr(dddd,5,6)
    d4=dddd
    lmw=_btlgd.mw.i
    if(lmw < 100) ; lmw=' 'lmw ; endif
    lgd='- 'd4' 'lmw
    'draw string 'xs' 'y' 'lgd
    y=y-dy
  endif
  i=i+1
endwhile

i=1
while(i<=_btGlgd.n & _veribt = 1)

  if(_btGlgdvf.i >= 0)
    'draw wxsym '_btGlgd.sym.i' 'x' 'y' '_btGlgd.siz.i' '_btGlgd.col.i' 8'
    'set string 1 l '_sthk
    'set strsiz 'yss
    dddd=_btGlgd.dtg.i
    d4=substr(dddd,5,6)
    d4=dddd
    lmw=_btGlgd.mw.i
    if(lmw < 100) ; lmw=' 'lmw ; endif
    lgd='- 'd4' 'lmw
    'draw string 'xs' 'y' 'lgd
    y=y-dy
  endif
  i=i+1
endwhile
return



function pltbmap()

  'set parea 1.15 9.75 0.5 8.0'
  rc=plotdims()

  'set xsize '_xsize' '_ysize
  'set xlint '_lnint
  'set ylint '_ltint
  'set mpdset mres'
  'set map 1 0 8'
  'set map 15 0 6'
  'set grid on 3 15 5'

  'set grads off'
  'set timelab off'

  'define d=const(n,0,-a)'
  'set cmax -1'
  'set gxout fgrid'
  'set fgvals 1 1'
  'd d'

  'set rgb 41 245 255 255'
  'basemap L 72 1 M'
  'basemap O 41 1 M'
  'd d'

  rc=bt2xy()
  rc=trkset()
  rc=plotbt()
  rc=trklgd()

if(_printBmap = 1)
  print 'BBBB: '_bkgpath' using: '_outopt
#  if(_outopt = 'printim') ; 'printim '_bkgpath' -t 0 x'_xsize' y'_ysize' white'          ; endif
  if(_outopt = 'printim') ; 'printim '_bkgpath' x'_xsize' y'_ysize' white'          ; endif
  if(_outopt = 'gxyat')   ; 'gxyat '_gxyatopt' -o '_bkgpath' -x '_xsize' -y'_ysize  ; endif
endif


#
#  lat/lon of corners for anis flash
#
rc=plotdims()

'q xy2w 0 0'
plonw=subwrd(result,3)
plats=subwrd(result,6)
'q xy2w '_pagex' '_pagey
plone=subwrd(result,3)
platn=subwrd(result,6)
if(plonw > 180.0); plonw=plonw-360.0; endif
if(plone > 180.0); plone=plone-360.0; endif

#-- correction for different aspect ratio for gxyat
#-- factor because gxyat is a little shorter than printim
#
if(_outopt = 'gxyat') 
  plats=plats+(platn-plats)*(1.0-0.97)
 endif

if(plonw > 0.0 & plone < 0.0) ; plone=360+plone ; endif
pagell='coordinates= 'platn' 'plonw' 'plats' 'plone' '_xsize

if(_verb) ; print 'ppllppll pagell: 'pagell ; endif
rc=write(_llpath,pagell)
rc=close(_llpath)


return



function d03tau(tau)

if(tau > 100)            ; otau=tau     ; endif
if(tau > 10 & tau < 100) ; otau='0'tau  ; endif
if(tau >=0 & tau < 10 )  ; otau='00'tau ; endif

return(otau)



function pltsp(ntau,latc,lonc,btmw,ptype)

tmppngpath='/tmp/tt.'_curpid'.png'
###print 'TTTTTTTTTTTTTTTTTTTTTTTTTTTTT tmppngpath in pltsp: 'tmppngpath

'set parea 1.15 9.75 0.5 8.0'
rc=plotdims()
if(_printBmap = 1)
  'c'
endif

cbscl=0.75
cbvert=1
cbxmid=_xlplot-0.75
if(cbxmid < 0.15); cbxmid=0.15 ; endif
cbymid=_pagey*0.5

'set xsize '_xsize' '_ysize
'set xlint '_lnint
'set ylint '_ltint
'set mpdset mres'
'set map 1 0 8'
'set map 15 0 6'
#  'set grid on 2 15'

'set grads off'
'set timelab off'

'set xlint '_lnint
'set ylint '_ltint
'set t 'ntau

tau=(ntau-1)*_dtau
cdtg=curdtg()

otau=d03tau(tau)

#
# get stats on # of members using first file
#
'set dfile 1'
'p=(n/asum(n,g))*100.0'
'p=n'
'd const(asum(n,g),0,-u)'
card=sublin(result,1)
nf=subwrd(card,4)


#
# bail of no members
#

if(nf = 0)
   return(0)
endif

nf=(nf/_nmembers)*100.0
nm=100.0-nf

nf=math_format('%3.0f',nf)
nm=math_format('%3.0f',nm)

'set clip '_xlplot' '_xrplot' '_ybplot' '_ytplot

if(ptype = 'sp')

  fileT='StikeP (d<='_critdist' km)'
  fileX='skp'
  'set dfile 2'
  'set gxout shaded'
  'set csmooth on'
  'set clevs   5  10  20  30  40  50  60  70  80  90  '
  'set ccols 0   6  2   8   7   10   3  5   11   4  9 '
  'd smth2d(sp,2,0.5,-0.5)'
  'cbarn 'cbscl' 'cbvert' 'cbxmid' 'cbymid
endif


if(ptype = 'hit')

  fileT='Hit count'
  fileX='hit'
  'set dfile 1'
  'pp=const(p,-1,-u)'
  
  'set gxout grfill'
  'set clevs   0   1    2    3     4   5    6    7    8   10   50'
  'set ccols 0  39   37   35    33   31  23   25   26   27  28   29'
  'set ccols 0  39   23   35    27   33  43   75   46   77  48   1'

if(_dobasemap = 1)
'set map 0 0 0'
'set grid off'
'set xlopts 0 0 0'
'set ylopts 0 0 0'
'set frame off'
endif

'd pp'
'cbarn 'cbscl' 'cbvert' 'cbxmid' 'cbymid

endif

t1=_tt1' TC: '_stmid'('_stmname') '_bdtg' 'fileT'  `3t`0= 'otau
t2='valid: 'cdtg'  FOUND:'nf'%  MISS:'nm'%    Nmembers: '_nmembers

if(_veribt = 1)
  pngpath=_pdir'/esrl.eps.veri.'_model'.'fileX'.'_stmid'.'otau'.png'
else
  pngpath=_pdir'/esrl.eps.'_model'.'fileX'.'_stmid'.'otau'.png'
endif

#
#  plot ensemble tracks
#
rc=plttrk(ntau)

'q pos'

rc=plotbtG(ntau)
#
#  plot best track at tau=0
#
'drawtcbt 'latc' 'lonc' 'btmw' 2.5'

'set clip 0 '_pagex' 0 '_pagey
#
# toptitle
#
rc=toptitle(t1,t2,0.85,1,1,6,6)
#
# bottom title
#
bt1='GREEN track: mean of esmenble tracks'
bt2='RED (if available): deterministic track'
rc=bottitle(bt1,bt2,0.85,3,2,'left')

'set map 1 1 5'
'draw map'

if(_dobasemap = 1)
  if(_printBmap = 1) 
    if(_outopt = 'printim') 
#      'printim 'pngpath' -b '_bkgpath' -t 0 x'_xsize' y'_ysize' white'
      'printim 'tmppngpath' x'_xsize' y'_ysize' white'
      '!convert.ksh -transparent white 'tmppngpath' 'tmppngpath
      '!composite.ksh 'tmppngpath' '_bkgpath' 'tmppngpath
      '!pngquant '_pngNcols' < 'tmppngpath' > 'pngpath
      '!rm 'tmppngpath

    endif

    if(_outopt = 'gxyat')
      'gxyat '_gxyatopt' -o 'tmppngpath' -x '_xsize' -y'_ysize
      '!convert.ksh -transparent white 'tmppngpath' 'tmppngpath
      '!composite.ksh 'tmppngpath' '_bkgpath' 'tmppngpath
      '!pngquant '_pngNcols' < 'tmppngpath' > 'pngpath
      '!rm 'tmppngpath
    endif
  else
    if(_outopt = 'printim') 
      'printim 'pngpath' -x '_xsize' -y'_ysize
    endif
    if(_outopt = 'gxyat') 
      'gxyat '_gxyatopt' -o 'pngpath' -x '_xsize' -y'_ysize
    endif
  endif

else
  if(_outopt = 'printim') 
    'printim 'pngpath' x'_xsize' y'_ysize
  endif
  if(_outopt = 'gxyat') 
    'gxyat '_gxyatopt' -o 'pngpath' -x '_xsize' -y'_ysize
  endif
endif

if(_verb = 1 | _verb = 0); print 'PPPP: 'pngpath ; endif

return



#----------------------------------------------------------------------------------------------------
#
#

function gettrk(tpath,topt)

rc=0

if(topt = 'det')
  nt=1
else
  nt=2
endif

print 'tpath: 'tpath

while(rc = 0)

  result=read(tpath)
  rc=sublin(result,1)
  card=sublin(result,2)
  imax=100
  i=1
  j=1
  jd=1
  je=1
  while(i<imax)

    if(nt = 1)
      _detlat.i=subwrd(card,jd) ; jd=jd+1
      _detlon.i=subwrd(card,jd) ; jd=jd+1
    endif

    if(nt = 2)
      _emnlat.i=subwrd(card,je) ; je=je+1
      _emnlon.i=subwrd(card,je) ; je=je+1
    endif

    _lat.i.nt=subwrd(card,j) ; j=j+1
    _lon.i.nt=subwrd(card,j) ; j=j+1

    if(_lat.i.nt = '')
      npos=i-1
      if(nt = 1)
         _detnpos=npos
      endif
      if(nt = 2)
         _emnnpos=npos
      endif
      i=imax+1
    endif
    i=i+1
  endwhile

  _npos.nt=npos

  nt=nt+1

endwhile

_ntrk=nt-2


return




function plttrk(ntau)

'set clip '_xlplot' '_xrplot' '_ybplot' '_ytplot

n=1
while(n<=_ntrk)

  if(n = 1)
    rct=ptrk(_detnpos,1,_detnpos)
  endif

  if(n = 2)
    rct=ptrk(_emnnpos,2,_emnnpos)
  endif

  if(n > 2) 
    rct=ptrk(_npos.n,n,ntau)
  endif

  n=n+1

endwhile

rct=ptrk(_detnpos,1,_detnpos)
rct=ptrk(_emnnpos,2,_emnnpos)

n=1
nmark=_ntrk
nmark=2

while(n<=nmark)
  if(n = 1)
    rcm=ptrkmk(_detnpos.n,1,ntau)
  endif
  if(n = 2)
    rcm=ptrkmk(_emnnpos.n,2,ntau)
  endif
  n=n+1
endwhile

return


function ptrk(npos,ntrk,ntau)


n=2

if(npos >= ntau)
  nmax=ntau
else
  nmax=npos
endif
while(n <= nmax)

  nm1=n-1

  if(ntrk = 1)
    lat1=_detlat.nm1
    lat2=_detlat.n
    lon1=_detlon.nm1
    lon2=_detlon.n
  endif

  if(ntrk = 2)
    lat1=_emnlat.nm1
    lat2=_emnlat.n
    lon1=_emnlon.nm1
    lon2=_emnlon.n
  endif

  if(ntrk > 2)
    lat1=_lat.nm1.ntrk
    lat2=_lat.n.ntrk
    lon1=_lon.nm1.ntrk
    lon2=_lon.n.ntrk
  endif

  'q w2xy 'lon1' 'lat1
  rc1=result
  'q w2xy 'lon2' 'lat2
  rc2=result

  x1=subwrd(rc1,3)
  y1=subwrd(rc1,6)

  x2=subwrd(rc2,3)
  y2=subwrd(rc2,6)

#'set line 0 1 6'
#'draw line 'x1' 'y1' 'x2' 'y2

if(ntrk = 1)
  'set line 0 1 15'
  'draw line 'x1' 'y1' 'x2' 'y2

  'set line 2 1 10'
  'draw line 'x1' 'y1' 'x2' 'y2
endif

if(ntrk = 2)

  'set line 0 1 15'
  'draw line 'x1' 'y1' 'x2' 'y2

  'set line 3 1 10'
  'draw line 'x1' 'y1' 'x2' 'y2

endif

# -- ensemble members
#
fcol=4
fthk=4
if(_model = 'fimens')
  nm=ntrk-2
  if(nm >= 1 & nm <= 5)   ; fcol=6 ; fthk=7 ; endif
  if(nm >= 6 & nm <= 10)  ; fcol=7 ; fthk=7 ; endif
  if(nm >= 11 & nm <= 20) ; fcol=4 ; fthk=4 ; endif
endif

if(ntrk > 2)

  'set line 0 1 6'
  'draw line 'x1' 'y1' 'x2' 'y2

  'set line 'fcol' 1 'fthk
  'draw line 'x1' 'y1' 'x2' 'y2

endif

  n=n+1

endwhile

rct=0

return(rct)


function ptrkmk(npos,ntrk,ntau)

ftm=3
ftsiz=0.075
ftsizs=ftsiz+0.010
ftsizi=ftsiz-ftsiz*0.75

n=1

if(npos >= ntau)
  nmax=ntau
else
  nmax=npos
endif

while(n <= nmax)

  if(ntrk = 1)
    lat2=_detlat.n
    lon2=_detlon.n
  endif

  if(ntrk = 2)
    lat2=_emnlat.n
    lon2=_emnlon.n
  endif

  if(ntrk > 2)
    lat2=_lat.n.ntrk
    lon2=_lon.n.ntrk
  endif

if(lon2 = '') ; return(1) ; endif


  'q w2xy 'lon2' 'lat2
  'q w2xy 'lon2' 'lat2
  rc2=result

  x2=subwrd(rc2,3)
  y2=subwrd(rc2,6)


if(ntrk = 1) ; ftc=2 ; ftci=0 ; endif
if(ntrk = 2) ; ftc=3 ; ftci=0 ; endif
if(ntrk = 3) ; ftc=5 ; ftci=0 ; endif

  'set line 0'
  'draw mark 'ftm' 'x2' 'y2' 'ftsizs

  'set line 'ftc
  'draw mark 'ftm' 'x2' 'y2' 'ftsiz

  'set line 'ftci
  'draw mark 'ftm' 'x2' 'y2' 'ftsizi


  n=n+1

endwhile

rct=0

return(rct)
