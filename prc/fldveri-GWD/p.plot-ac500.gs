function main(args)

rc = gsfallow(on)
rc = const()
rc = jaecol()

aspect=3/4
_xsize=1048
_xsize=1200
_ysize=_xsize*aspect

_undef=1e5

'set xsize '_xsize' '_ysize

plottype='trunk'
plottype='gwd'
#plottype='gfs'
plottype='gwd-trunk'
plottype='gwd-2014'

if(plottype = 'gfs')   ; bdtg=2014062200 ; endif
if(plottype = 'trunk') ; bdtg=2014050918 ; endif
if(plottype = 'gwd')   ; bdtg=2014050918 ; endif
acpath='ac.500-'bdtg'.ctl'

if(plottype = 'gwd-trunk')
  bdtg=2014050918
#  bdtg=2014051000
  bdtg=2013122400
  acpath='all.'bdtg'.ctl'
endif

if(plottype = 'gwd-2014')
  bdtg=2014050918
#  bdtg=2014051000
#  bdtg=2013122400
  acpath='all.'bdtg'.ctl'
endif

btau=0
etau=240
etau=168
etau=etau+24
bgtime=dtg2gtime(bdtg)
edtg=dtginc(bdtg,etau)
egtime=dtg2gtime(edtg)

fa=ofile(acpath)

if(fa = 0); print 'EEE opening 'acpath ; endif

# -- number of plots/models and labels

_vvar='ac'

if(plottype = gfs)

_nmodel=4
_model.1='ECMWF'
_model.2='GFS'
_model.3='FIM8'
_model.4='NAVG'

_varx.1='ecm2'  ; _vcol.1=1 ; _vmark.1=0 ; _vthk.1=10
_varx.2='gfs2'  ; _vcol.2=2 ; _vmark.2=0 ; _vthk.2=6
_varx.3='fim8'  ; _vcol.3=3 ; _vmark.3=0 ; _vthk.3=6
_varx.4='navg'  ; _vcol.4=4 ; _vmark.4=0 ; _vthk.4=6
_vmin=-8.0
_vmax=8.0

tt1='GFS dropoff `3t`0 d+5 v ECMWF v FIM8 v NAVGEM - 201405062200'
tt2='500 NHEM AnomCorr'

ppath='ac-500-gfs-dropoff-2014062200.png'

endif


if(plottype = 'trunk')
_nmodel=3
_model.1='GFS'
_model.2='FIMtrunk'
_model.3='FIMphy12'

_varx.1='gfs2'   ; _vcol.1=1 ; _vmark.1=0 ; _vthk.1=10
_varx.2='fim8'   ; _vcol.2=2 ; _vmark.2=0 ; _vthk.2=6
_varx.3='f2012'  ; _vcol.3=3 ; _vmark.3=0 ; _vthk.3=6
_vmin=-8.0
_vmax=8.0
tt1='FIM8 v GFS phys 2012 v 4301 trunk - 2014050918'
tt2='500 NHEM AnomCorr'

ppath='ac-500-fimtrunk.png'

endif

if(plottype='gwd')
_nmodel=6
_model.1='GFS'
_model.2='FIM-gwd12-sf40'
_model.3='FIM-gwd12-sf10'
_model.4='FIM-gwd12-sf01'
_model.5='FIM-NO-gwd'
_model.6='FIMtrunk'

_varx.1='gfs2'   ; _vcol.1=1  ; _vmark.1=0 ; _vthk.1=10
_varx.2='fsf40'  ; _vcol.2=12 ; _vmark.2=0 ; _vthk.2=6
_varx.3='fsf10'  ; _vcol.3=8  ; _vmark.3=0 ; _vthk.3=6
_varx.4='fsf01'  ; _vcol.4=3  ; _vmark.4=0 ; _vthk.4=6
_varx.5='fngwd'  ; _vcol.5=11 ; _vmark.5=0 ; _vthk.5=6
_varx.6='fim8'   ; _vcol.6=2  ; _vmark.6=0 ; _vthk.6=6

_vmin=-8.0
_vmax=8.0

tt1='FIM8 v GFS - gravity wave experiments - 2014050918'
tt2='500 NHEM AnomCorr'

ppath='ac-500-nhem-gwd.png'

endif

# -------------------------------------------------------- latest

_vvar='wa'  ; _vlev=250 ; _vstat='ac'
_vvar='uva' ; _vlev=250 ; _vstat='ac'
_vvar='uva' ; _vlev=250 ; _vstat='corr'
_vvar='wa'  ; _vlev=250 ; _vstat='bias'
_vvar='wa'  ; _vlev=250 ; _vstat='rmst'
_vvar='uva' ; _vlev=250 ; _vstat='rmst'
_vvar='uva' ; _vlev=850 ; _vstat='rmst'
_vvar='wa'  ; _vlev=850 ; _vstat='bias'

_vvar='zg'  ; _vlev=500 ; _vstat='ac'
_vvar='wa'  ; _vlev=250 ; _vstat='bias'

_varea='nhem'
_vbarrev=0

if(_vstat = 'ac') ;   _xvar=1 ; endif
if(_vstat = 'corr') ; _xvar=2 ; endif
if(_vstat = 'rmst') ; _xvar=3 ; endif
if(_vstat = 'bias') ; _xvar=6 ; endif

if(_varea = 'nhem')    ; _yvar=1 ; endif
if(_varea = 'tropics') ; _yvar=2 ; endif
if(_varea = 'shem')    ; _yvar=3 ; endif

if(_vstat = 'ac' | _vstat = 'corr')
  _vmin=-8.0
  _vmax=8.0
  _mfact=100.0
  _vrange0=0
  _vrange1=110
  _vylint=10
  _vlim=60
endif

if(_vstat = 'corr' & _vvar = 'uva')
  _vlim=70
endif


if(_vstat = 'bias')

  _vmin=-2.0
  _vmax=2.0
  _mfact=1.0
  _vrange0=-6.0
  _vrange1=6.0
  _vylint=0.5
  _vlim=0
  _vbarrev=1
  if(_vvar = 'wa' & _vlev < 300)   ; _vrange0=-6.0 ; _vrange1=6.0 ; _vmin=-2.0 ; _vmax=2.0 ; _vylint=1.0 ; endif
  if(_vvar = 'wa' & _vlev >= 500)  ; _vrange0=-6.0 ; _vrange1=6.0 ; _vmin=-2.0 ; _vmax=2.0 ; _vylint=1.0 ; endif

endif

if(_vstat = 'rmst')

  _vmax=2.0
  _mfact=1.0
  _vbarrev=0
  if(_vvar = 'wa')                  ; _vrange0=-3.0 ; _vrange1=15.0 ; _vmin=-2.0 ; _vmax=2.0 ; _vylint=1.0 ; endif
  if(_vvar = 'uva' & _vlev < 300)   ; _vrange0=-5.0 ; _vrange1=25.0 ; _vmin=-4.0 ; _vmax=4.0 ; _vylint=2.5 ; endif
  if(_vvar = 'uva' & _vlev >= 500)  ; _vrange0=-3.0 ; _vrange1=15.0 ; _vmin=-2.0 ; _vmax=2.0 ; _vylint=1.0 ; endif
  _vlim=0
  _vbarrev=1

endif



if(plottype='gwd-trunk')

_nmodel=5
_model.1='GFS'
_model.2='FIM4301'
_model.3='FIM4237-gwd12-sf01'
_model.4='FIM4373-gwd12-sf01'
_model.5='FIM4307-2012phys'

_varx.1=_vvar'(ens=gfs2)'   ; _vcol.1=1  ; _vmark.1=0 ; _vthk.1=10
_varx.2=_vvar'(ens=fim8)'   ; _vcol.2=14 ; _vmark.2=0 ; _vthk.2=6
_varx.3=_vvar'(ens=fsf01)'  ; _vcol.3=8  ; _vmark.3=0 ; _vthk.3=6
_varx.4=_vvar'(ens=ftk01)'  ; _vcol.4=3  ; _vmark.4=0 ; _vthk.4=6
_varx.5=_vvar'(ens=f2012)'  ; _vcol.5=6 ; _vmark.5=0 ; _vthk.5=6

# -- 
_nmodel=4

_model.1='GFS'
_model.2='FIM4301'
_model.3='FIM4237-gwd12-sf01'
_model.4='FIM4237-gwd12-sf40'

_varx.1=_vvar'(ens=gfs2)'   ; _vcol.1=1  ; _vmark.1=0 ; _vthk.1=10
_varx.2=_vvar'(ens=fim8)'   ; _vcol.2=14 ; _vmark.2=0 ; _vthk.2=6
_varx.3=_vvar'(ens=fsf01)'  ; _vcol.3=8  ; _vmark.3=0 ; _vthk.3=6
_varx.4=_vvar'(ens=fsf40)'  ; _vcol.4=6  ; _vmark.4=0 ; _vthk.4=6


tt1='FIM8 v GFS - gravity wave experiments - 'bdtg
tt2=_vvar' '_vlev' '_varea' '_vstat'- 2 trunks + 2012 GWD'

ppath=_vvar'-'_vstat'-'_vlev'-'_varea'-'plottype'-'bdtg'.png'

_bgcolor=77

endif

if(plottype='gwd-2014')

# -- 
_nmodel=6

_model.1='GFS'
_model.2='FIM4301'
_model.3='FIM3773'
_model.4='FIM4237-gwd12-sf01'
_model.5='FIM3773-2014phys'
_model.6='FIM2014phys-NB'
_model.6='FIM4567'
_model.6='FIM4567'

_varx.1=_vvar'(ens=gfs2)'   ; _vcol.1=1  ; _vmark.1=0 ; _vthk.1=10
_varx.2=_vvar'(ens=fim8)'   ; _vcol.2=14 ; _vmark.2=0 ; _vthk.2=6
_varx.3=_vvar'(ens=ftk12)'  ; _vcol.3=3  ; _vmark.3=0 ; _vthk.2=6
_varx.4=_vvar'(ens=fsf01)'  ; _vcol.4=8  ; _vmark.4=0 ; _vthk.3=6
_varx.5=_vvar'(ens=f2014)'  ; _vcol.5=6  ; _vmark.5=0 ; _vthk.5=6
_varx.6=_vvar'(ens=f2014nb)'  ; _vcol.6=7  ; _vmark.6=0 ; _vthk.6=6


tt1='FIM8 v GFS - gravity wave experiments - 'bdtg
tt2=_vvar' '_vlev' '_varea' '_vstat'- 2 trunks + 2012 GWD'

_nmodel=6

_model.1='GFS'
_model.2='FIM4301'
_model.3='FIM-gfs1534-sf40'
_model.4='FIM-gfs574-sf40'
_model.5='FIM-gfs1534-sf01'
_model.6='FIM-gfs1534-sf01'

_varx.1=_vvar'(ens=gfs2)'   ; _vcol.1=1  ; _vmark.1=0 ; _vthk.1=10
_varx.2=_vvar'(ens=fim8)'   ; _vcol.2=14 ; _vmark.2=0 ; _vthk.2=6
_varx.3=_vvar'(ens=ftk12)'  ; _vcol.3=3  ; _vmark.3=0 ; _vthk.2=6
_varx.4=_vvar'(ens=fr4567)'  ; _vcol.4=8  ; _vmark.4=0 ; _vthk.3=6
_varx.5=_vvar'(ens=fr4567gwd20)'  ; _vcol.5=6  ; _vmark.5=0 ; _vthk.5=6
_varx.6=_vvar'(ens=fr4567gwd10)'  ; _vcol.6=7 ; _vmark.6=0 ; _vthk.6=6


tt1='FIM8 v GFS - gravity wave experiments - 'bdtg
tt2=_vvar' '_vlev' '_varea' '_vstat'- 2 trunks + 2012 GWD'

ppath=_vvar'-'_vstat'-'_vlev'-'_varea'-'plottype'-'bdtg'.png'

_bgcolor=77

# --  exp with 2014 gfs gwd with gfs574/1534 settings

_nmodel=6

_model.1='GFS'
_model.2='FIM4301'
_model.3='FIM5002-gfs1534-01'
_model.4='FIM5002-gfs1534-40'
_model.5='FIM5002-gfs574-01'
_model.6='FIM5002-gfs574-40'

_varx.1=_vvar'(ens=gfs2)'   ; _vcol.1=1  ; _vmark.1=0 ; _vthk.1=10
_varx.2=_vvar'(ens=fim8)'   ; _vcol.2=14 ; _vmark.2=0 ; _vthk.2=6
_varx.3=_vvar'(ens=fr5002g1501)'  ; _vcol.3=3  ; _vmark.3=0 ; _vthk.2=6
_varx.4=_vvar'(ens=fr5002g1540)'  ; _vcol.4=8  ; _vmark.4=0 ; _vthk.3=6
_varx.5=_vvar'(ens=fr5002g5701)'  ; _vcol.5=6  ; _vmark.5=0 ; _vthk.5=6
_varx.6=_vvar'(ens=fr5002g5740)'  ; _vcol.6=7 ; _vmark.6=0 ; _vthk.6=6

tt1='FIM8 v GFS - gravity wave experiments - 'bdtg
tt2=_vvar' '_vlev' '_varea' '_vstat'- 2014 GFS GWD for 1574/574'

ppath=_vvar'-'_vstat'-'_vlev'-'_varea'-'plottype'-gfs2014-'bdtg'.png'

_bgcolor=77



endif


# -- plot controls by var and level


_bmdl=1

# -- set the dimension env

'set background '_bgcolor
'c'
'set x '_xvar
'set y '_yvar
'set lev '_vlev
'set time 'bgtime' 'egtime
'set grads off'
'set timelab on'

# -- set ranges of plot and tick mark intervals

rcolmin=29
rcolmax=39

if(_vbarrev = 1)
rcolmax=29
rcolmin=39
endif

'set vrange '_vrange0' '_vrange1
'set ylint '_vylint
'set xlint 1'

# -- set plotarea in grads plot xy coords
# -- xbp = x start of plot ["]; dxp = length of plot ["] (width)
# -- ybp = y start of plot ; dyp = y length plot (height)
# -- dyb = y size of blocks
# -- xsoff = offset to the right in x to start block label

xbp=0.50
dxp=8.50
xep=xbp+dxp

ybp=0.75
dyp=7
yep=ybp+dyp

dyb=0.175
xsoff=0.05

# -- set the plot area

'set parea 'xbp' 'xep' 'ybp' 'yep
'set missconn on'

# -- plot the time series

i=1
while(i<=_nmodel)
  'set gxout line'
  'set cmark '_vmark.i
  'set ccolor '_vcol.i
  'set cthick '_vthk.i
  _vexpr.i=_varx.i'*'_mfact
  'd '_vexpr.i
  if(i > 1)
    'set gxout errbar'
    'set bargap 90'
    'set ccolor '_vcol.i
    'set cthick 10'
    'd '_vexpr.1';'_vexpr.i
  endif
  i=i+1
endwhile


# -- get the dim (_qdim array ) and plot env

rc=getdimenv()
rc=plotdims()

# -- plot the 0.6 line

'q w2xy 'bgtime' '_vlim
x60b=subwrd(result,3)
y60b=subwrd(result,6)

'q w2xy 'egtime' '_vlim
x60e=subwrd(result,3)
y60e=subwrd(result,6)

'set line 1 1 15'
print 'draw line 'x60b' 'y60b' 'x60e' 'y60e
'draw line 'x60b' 'y60b' 'x60e' 'y60e

# -- find the diff between the base time series #1 and the others

nblock=_qdim.te 
dxb=(_xrplot-_xlplot)/(nblock-1)

j=2
while(j<=_nmodel)
  l=1
  while(l <= _qdim.te)
    'set t 'l
    'd '_varx._bmdl
    vvalbase=subwrd(result,4)
    print 'vvalbase 'vvalbase
if(vvalbase < -999999.)
    'set t 'l+1
    'd '_varx._bmdl
    vvalbasep1=subwrd(result,4)
    'set t 'l-1
    'd '_varx._bmdl
    vvalbasem1=subwrd(result,4)
    vvalbase=(vvalbasep1+vvalbasem1)*0.5
    print 'vvalbase UNDEF 'vvalbase
   'set t 'l
endif

    'd '_varx.j'-'vvalbase
    vval=subwrd(result,4)*_mfact
    _diff.l.j=vval
    vval=math_format('%6.2g',vval)
print 'vval: '_model.j' '_varx._bmdl' 'vval
    l=l+1
  endwhile

  j=j+1
endwhile

# -- set intervals to plot the diffs as blocks

rc=setBand(_vmin,_vmax,1,rcolmax,rcolmin)

nbcols=_jaeninc

# -- loop by models in Y

j=1
while (j <= _nmodel)

  yb1=_ybplot+dyb*(j-1)
  yb2=yb1+dyb

  xbb=_xlplot

# -- make colorized blocks in X

   n=1
   while (n <= nblock)

     if(j = 1)
       rcol=15
     else
       vval=_diff.n.j
       rcol=getBand(vval,nbcols)
     endif
     
     if(n = 1)
       xb1=xbb
       xb2=xb1+dxb*0.5
     endif
  
    if(n > 1 & n < nblock)
      xb1=xb2
      xb2=xb1+dxb
    endif
  
    if(n = nblock)
       xb1=xb2
       xb2=xb1+dxb*0.5
    endif

# -- draw color recfill

    'set line 'rcol' 1 0' 
    'draw recf 'xb1' 'yb1' 'xb2' 'yb2

# -- draw border

    'set line 0 1 10' 
    'draw rec 'xb1' 'yb1' 'xb2' 'yb2

    'set line 1 1 4' 
    'draw rec 'xb1' 'yb1' 'xb2' 'yb2
    
  
# -- convert plot x,y to pixel x y for each box

    rc=xy2pp(xb1,yb1)
    pxb1.n.j=subwrd(rc,1)
    pyb1.n.j=subwrd(rc,2)

    rc=xy2pp(xb2,yb2)
    pxb2.n.j=subwrd(rc,1)
    pyb2.n.j=subwrd(rc,2)

#    print 'GGGXXX  xb1: 'xb1' 'xb2' 'yb1' 'yb2
#    print 'PPPXXX pxb1: 'pxb1' 'pxb2' 'pyb1' 'pyb2
  
    if(j = _nmodel)
      lsz=dyb*0.5
      if(n = 1 | n = nblock) ; lsz=lsz*0.75 ; endif
      tl=(n-1)
      xtl=(xb1+xb2)*0.5
      ytl=yb2+0.05
      'set string 1 bc 6'
      'set strsiz 'lsz
      'draw string 'xtl' 'ytl' d+'tl
    endif
    
    n=n+1

  endwhile

# -- draw the model label to the right of the blocks

  xs1=xb2+xsoff
  ys1=yb1+dyb*0.5
  'set string '_vcol.j' l 6'
  'set strsiz 'dyb*0.5
  'draw string 'xs1' 'ys1' '_model.j

  j=j+1
endwhile

# -- cbarns (.gsf script call to cbarn)

xcboff=0.50
ycboff=0.75
sf=0.75
vert=1
xmid = xep+xcboff
ymid = (yep+ybp)*0.5 + ycboff
sfstr=0.90
force='y'

rc=cbarns(sf,vert,xmid,ymid,sfstr,force,'','',_bgcolor)

# -- toptitle
ttscl=0.8

rc=toptitle(tt1,tt2,ttscl)
'gxyat -x '_xsize' -y '_ysize' -r 'ppath

print 'pppppppppppppppath: 'ppath

'!cp 'ppath' ~/Dropbox/.'

# -- output

'q pos'
'quit'

return

# -- get the color for a value in the intervals from setBand()

function getBand(vval,nbcols)

verb=0
zerocol=15
undefcol=0

n=1
while(n<=nbcols)

  if(vval = 0.0)
    return(zerocol)
  endif
  
  if(math_abs(vval) > _undef )
     return(undefcol)
  endif

  if(vval < _lbound.1)
     if(verb) ; print 'LLL 'vval' '_lbound.1' '_jcol.1 ; endif
    return(_jcol.1)
  endif
  
  if(vval > _ubound.nbcols)
    if(verb) ; print 'UUU 'vval' '_ubound.nbcols' '_jcol.nbocls ; endif 
    return(_jcol._jaeninc)
  endif
  
  if(vval >= _lbound.n & vval < _ubound.n)
      if(verb) ; print 'MMM 'vval' n: 'n' '_lbound.n' '_ubound.n ; endif
     return(_jcol.n)
  endif

  n=n+1
endwhile

return(999)


# -- set the colors and intervals based on the jaecol colorbars

function setBand(vmin,vmax,njae,jaemax,jaemin)

nfrmt='%6.2g'
epsilon=1e-4

if(njae=1)
  ninc=18
  ncols=9
  ncolinc=1
endif

if(njae=2)
  ninc=10
  ncols=5
  ncolinc=2
endif

vinc=(vmax-vmin)/(ninc-2)
_jaeninc=ninc

n=1
_shdinfo.n='Number of levels = 'ninc
print 'HHH 'n' '_shdinfo.n

nlhalf=ninc/2

while(n<=ninc)
  
  nn=n+1
  
# -- negative colorbar
  vnegbar=vmin

  if(n <= nlhalf)
    jcol=jaemin-(n-1)

    if(n = 1)
       ovmin=math_format(nfrmt,vnegbar)
      _shdinfo.nn=jcol' < 'ovmin
      _jcol.n=jcol
      _lbound.n=vnegbar
      _ubound.n=vnegbar
    else
       lbound=vnegbar+vinc*(n-2)
       ubound=lbound+vinc
       if(math_abs(lbound) < epsilon); lbound=0.0 ; endif
       if(math_abs(ubound) < epsilon); ubound=0.0 ; endif

      _lbound.n=lbound
      _ubound.n=ubound
      
       lbound=math_format(nfrmt,lbound)
       ubound=math_format(nfrmt,ubound)
      _shdinfo.nn=jcol' 'lbound' 'ubound
      _jcol.n=jcol
    endif
#print 'LLL 'nn' '_shdinfo.nn' n: 'n' '_jcol.n' '_lbound.n' '_ubound.n
  endif
  
  
# -- positive colorbar

  if(n > nlhalf)
    
    vposbar=vmax
    n2=n-nlhalf
    jcol=jaemax - (ninc-n)*ncolinc
    
    if(n = ninc)
      ovmax=math_format(nfrmt,vposbar)
      _shdinfo.nn=jaemax' > 'ovmax
      _jcol.n=jaemax
      _lbound.n=vposbarn
      _ubound.n=vposbarn
    else
       lbound=vmin+vinc*(n-2)
       ubound=lbound+vinc
       if(math_abs(lbound) < epsilon); lbound=0.0 ; endif
       if(math_abs(ubound) < epsilon); ubound=0.0 ; endif
      _lbound.n=lbound
      _ubound.n=ubound

       lbound=math_format(nfrmt,lbound)
       ubound=math_format(nfrmt,ubound)
      _shdinfo.nn=jcol' 'lbound' 'ubound
      _jcol.n=jcol
    endif
#print 'UUU nn: 'nn' '_shdinfo.nn' n: 'n' '_jcol.n' '_lbound.n' '_ubound.n
  endif

  n=n+1
endwhile

return


# -- convert xy to pixel xy
#
function xy2pp(x1,y1)

px1=(x1/_pagex)*_xsize
py1=(y1/_pagey)*_ysize

px1=math_nint(px1)
py1=math_nint(py1)

rc=px1' 'py1
return(rc)
