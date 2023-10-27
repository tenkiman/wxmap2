function main(args)

'reinit'
'open tcbog.ctl'

'set gxout barb'
#'set gxout vector'

'set lev 1000'
'set lev 925'
'set lev 500'
_u='utr'
_v='vtr'
_u='u'
_v='v'
'd '_u'*1.94;'_v'*1.94'

rc=plotdims()

while(1)

  rc=rband()
  if(rc=99) ; break ; endif

endwhile

return

function plot(clat,clon)

'c'
cint=1.0
dlat=10

dlon=dlat*1.5
lat1=clat-dlat
lat2=clat+dlat
lon1=clon-dlon
lon2=clon+dlon

'set lat 'lat1' 'lat2
'set lon 'lon1' 'lon2

'd '_u'*1.94;'_v'*1.94'
'cbarn'


return


function rband

'set rband 10 box '_xlplot' '_ybplot' '_xrplot' '_ytplot

'q pos'
print 'trkgui ---- result 'result

x1=subwrd(result,3)
y1=subwrd(result,4)

btype=subwrd(result,5)
wtype=subwrd(result,6)
bnum=subwrd(result,7)

if(bnum=3)
  'set lat -90 90'
  'set lon 0 360'
  'c'
  return(1)
endif

say 'qqq wtype = 'wtype' 'btype' 'bnum

#----------------------------------------------------------------------
#
#	process rubber band
#
#----------------------------------------------------------------------

if(wtype=2)

  x2=subwrd(result,8)
  y2=subwrd(result,9)   

  if(x2 < x1) ; xx=x1 ; x1=x2 ; x2=xx ; endif
  if(y2 < y1) ; yy=y1 ; y1=y2 ; y2=yy ; endif

  say 'qqq 'x1' 'x2' 'y1' 'y2

  'set line 0 1 20'
  'draw rec 'x1' 'y1' 'x2' 'y2
  'set line 1 1 5'
  'draw rec 'x1' 'y1' 'x2' 'y2


  'q xy2w 'x1' 'y1
  ln1=subwrd(result,3)
  lt1=subwrd(result,6)

  ln1=nint(ln1)
  lt1=nint(lt1)

  'q xy2w 'x2' 'y2
  ln2=subwrd(result,3)
  lt2=subwrd(result,6)
  ln2=nint(ln2)
  lt2=nint(lt2)
  
  'set lat 'lt1' 'lt2
  'set lon 'ln1' 'ln2

  'c'


'd '_u'*1.94;'_v'*1.94'
'cbarn'
  return(99)

endif


*
*-------------------- utility script functions
*

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
*-------------------------- strlen ------------------
*
function strlen(arg)

i=1
while(substr(arg,i,1) != '' & i<250)
  i=i+1
endwhile
return(i-1)

*
*-------------------------- mod ------------------
*
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

*
*-------------------------- stitle ------------------
*
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
  'set string 1 c 6 'angle
  'draw string 'xs' 'ys' 't1
  'set string 1 c 6 0'



return


*
*-------------------------- scrptle ------------------
*
function scrptle(scale,type)

  rc=plotdims()

  tsiz=0.06
  if(scale != 'scale')
    tsiz = tsiz * scale
  endif

  xoff=0.15
  yoff=0.06
  
  if(type != 'type') 

    xb=0

    if(type=top)
      yb=_pagey
      yoff=-yoff
    endif
 
    if(type=bottom)
      yb=0
    endif
   
     xe=_pagex
     ye=_pagey
  
     x1=xb+xoff
     y1=yb+yoff+tsiz/2

     x2=xe-xoff
     y2=y1

  else

    x1=_xlplot+xoff
    y1=_ybplot+yoff+tsiz/2

    x2=_xrplot-xoff
    y2=y1
  endif

  'set strsiz 'tsiz
  'set string 1 l 4' 
  'draw string 'x1' 'y1' '_script


return

*
*-------------------------- bottitle ------------------
*
function bottitle(t1,t2,scale,t1col,t2col)

  '!dtg > dtg.cur'
  rc=read(dtg.cur)
  dtg=sublin(rc,2)
  rc=close(dtg.cur)

  'q gxinfo'
  card=sublin(result,2)

  pagex=subwrd(card,4)
  pagey=subwrd(card,6)

  xr=pagex
  xl=0
  y1=0.22
  y2=0.08

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

  'draw string 'x2' 'y2' 'dtg
  'set string 1 c 6 0'

return

*
*-------------------------- plotdims ------------------
*

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
*
*-------------------------- toptitle ------------------
*

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
  t2siz=tsiz*0.85
  y2=_pagey-0.15-tsiz*1.5

  'set strsiz 'tsiz
  'set string 't1col' c 6'
  'draw string 'xs' 'y1' 't1

  if(t2 != '')
    'set string 't2col' c 5'
    'set strsiz 't2siz
    'draw string 'xs' 'y2' 't2
  endif

return
*----------------------------------------------------------
*
*	metadata
*
*----------------------------------------------------------
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

*----------------------------------------------------------
*
*	metadata
*
*----------------------------------------------------------

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
*	run cbarn sf vert xmid ymid
*
*	sf   - scale the whole bar 1.0 = original 0.5 half the size, etc.
*	vert - 0 FORCES a horizontal bar = 1 a vertical bar
*	xmid - the x position on the virtual page the center the bar
*	ymid - the x position on the virtual page the center the bar
*
*	if vert,xmid,ymid are not specified, they are selected
*	as in the original algorithm
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
  strxsiz=0.11*sf*0.7
  strysiz=0.12*sf*0.7
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

*----------------------------------------------------------
*
*	jaecol
*
*	color table by Jae Schemm of CPC, NCEP
*
*----------------------------------------------------------

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
*
* black to light grey
'set rgb 71 250 250 250'
'set rgb 72 225 225 225'
'set rgb 73 200 200 200'
'set rgb 74 180 180 180'
'set rgb 75 160 160 160'
'set rgb 76 150 150 150'
'set rgb 77 140 140 140'
'set rgb 78 124 124 124'
'set rgb 79 112 112 112'
'set rgb 80  92  92  92'
'set rgb 81  80  80  80'   
'set rgb 82  70  70  70'   
'set rgb 83  60  60  60'   
'set rgb 84  50  50  50'   
'set rgb 85  40  40  40'
'set rgb 86  36  36  36'
'set rgb 87  32  32  32'

return




*
*-------------------------- dtghcur ------------------
*
function dtghcur(dtgh)
*
*  convert FNMOC DTG to GrADS time
*
  iyr=substr(dtgh,1,4)*1
  imo=substr(dtgh,5,2)*1
  ida=substr(dtgh,7,2)*1
  ihr=substr(dtgh,9,2)*1
  nmo=subwrd(_monamel,imo)
  imo=i
return (ihr%'Z'ida%nmo%iyr)
*
*-------------------------- incdtgh ------------------
*
function incdtgh(dtgh,inc)
*
*  increment a dtg by inc hours
*  RESTRICTIONS!!  
*  (1)  inc > 0
*  (2)  inc < 24
*
  iyr=substr(dtgh,1,4)*1
  imo=substr(dtgh,5,2)*1
  ida=substr(dtgh,7,2)*1
  ihr=substr(dtgh,9,2)*1

  if(mod(iyr,4)=0)
    _monday='31 29 31 30 31 30 31 31 30 31 30 31'
  endif

  ihr=ihr+inc

  while(ihr>=24)
    ihr=ihr-24
    ida=ida+1
  endwhile

  while(ihr<0)
    ihr=ihr+24
    ida=ida-1
  endwhile

  if(ida > subwrd(_monday,imo))
    ida=ida-subwrd(_monday,imo)
*    say 'inside check ida = 'ida' _monday = 'subwrd(_monday,imo)
    imo=imo+1
  endif

  while(ida < 0)
    imo=imo-1
    ida=subwrd(_monday,imo)-ida
  endwhile
  
  if(ida=0)
    imo=imo-1
    ida=subwrd(_monday,imo)
  endif

  if(imo>=13)
    imo=imo-12
    iyr=iyr+1
  endif

if(imo<10);imo='0'imo;endif
if(ida<10);ida='0'ida;endif
if(ihr<10);ihr='0'ihr;endif

return (iyr%imo%ida%ihr)

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
endif

return


*-----------------------------------------------------------
*
*	function setup
*
*-----------------------------------------------------------
function setup(rcfg)
*
*	dtg global variables
*
_monamel='jan feb mar apr may jun jul aug sep oct nov dec'
_monameu='JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC'
_monday='31 28 31 30 31 30 31 31 30 31 30 31'

return

function openfile()
*
*	open the files
*
nf=_cc.1
n=1
while(n<=nf)
  nn=n+1 
  _f.n=ofile(_cc.nn)
  if(_f.n=0) ; say 'unable to open '_cc.nn ; 'quit' ; endif
  n=n+1
endwhile

return(nn)


function plotarea(np,ppx,ppy,laydir,pytoff,pyboff,asymx,asymy)
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
dxb=(1.0-ppx)*dpx
dyb=(1.0-ppy)*dpy
say 'qqq kk = 'np' 'npx' 'npy' 'dpx' 'dpy' 'dxb' 'dyb

l=1
j=npy
while(j>=1)

  y0=pyboff+(j-1)*dpy
  y1=pyboff+j*dpy

  i=1
  while(i<=npx & l<=np)

    if(i=1)
      x0=0
      x1=dpagex*asymx
     _xpl.l=x0+dxb*1.25
     _xpr.l=x1-dxb*0.5

    endif

    if(i=2) 
      x0=x1
      x1=x0+dpagex*(1-asymx)
      _xpl.l=x0+dxb*0.75
      _xpr.l=x1-dxb*0.5
    endif

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



function getinfo()
'!xwininfo -int -name GrADS > wininfo'
i=0; gotid=0
while (1)
  res=read(wininfo)
  dum=sublin(res,1)
  cod=subwrd(dum,1)
  if(cod!=0)
    if(cod=1); say "Error opening file"; endif
    if(cod=8); say "File open for write"; endif
    if(cod=9); say "I/O error"; endif
    break
  endif
  i=i+1
  dum=sublin(res,2)
*
*	different output format?
*
  if(subwrd(dum,3)="Window" & subwrd(dum,4) = "id:") 
    _winid=subwrd(dum,5)
    gotid=1
    break
  endif

  if(subwrd(dum,2)="Window" & subwrd(dum,3) = "id:") 
    _winid=subwrd(dum,4)
    gotid=1
    break
  endif

endwhile
rc=close(wininfo)
'!rm wininfo'
return(gotid)

*
*-------------------------- abs ------------------
*
function abs(i0)
  siz=strlen(i0)
  if(substr(i0,1,1)='-') 
    iabs=substr(i0,2,siz)
  else
    iabs=i0
  endif
return(iabs)

*
*-------------------------- nint ------------------
*
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


*
*-------------------------- mod ------------------
*
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

*
*-------------------------- plotdims ------------------
*

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

  card=sublin(result,3)
  _xlplot=subwrd(card,4)
  _xrplot=subwrd(card,6)

  card=sublin(result,4)
  _ybplot=subwrd(card,4)
  _ytplot=subwrd(card,6)

return

*
*-------------------------- nint ------------------
*
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
*  convert FNMOC DTG to GrADS time
*
  iyr=substr(dtgh,1,2)*1
  imo=substr(dtgh,3,2)*1
  ida=substr(dtgh,5,2)*1
  ihr=substr(dtgh,7,2)*1
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

  iyr=substr(dtgh,1,2)*1
  imo=substr(dtgh,3,2)*1
  ida=substr(dtgh,5,2)*1
  ihr=substr(dtgh,7,2)*1
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


if(iyr<10);iyr='0'iyr;endif
if(imo<10);imo='0'imo;endif
if(ida<10);ida='0'ida;endif
if(ihr<10);ihr='0'ihr;endif

return (iyr%imo%ida%ihr)

function tcstat(nvtype,nbasin,nstorm,dtg)

fo=ofile(_vpath)
if(fo = 0) ; 'quit' ;endif

if(nvtype = 2) ; nstorm=nstorm+30 ; endif
'set dfile 'fo
'set x 6'
'set y 'nstorm
'set z 'nbasin

ntmax=0

t=1
te=4
while(t<=te) 
  'set t 't
  'd const(i(x=1),0,-u)'
  nti=subwrd(result,4)
  if(nti > ntmax) ; ntmax=nti ; endif
  t=t+1
endwhile

print 'QQQQQQQQ ntmax = 'ntmax

return(ntmax' 'fo)

function trkpstat(nbasin,nvtype)

#
#  dim env already set up
#
#'set dfile 'fo
#'set x 6'
#'set y 'nstorm
#'set z 'nbasin

ntmax=0
mwmax=0
femax=0
lsiz=0.125
lsiz=0.1

t=1
te=4
while(t<=te) 
  'set t 't
  'd const(i(x=1),0,-u)'
  nti=subwrd(result,4)
  if(nti > ntmax) ; ntmax=nti ; endif
  print 'nti 't' 'nti.t
  'd const(i(x=5),0,-u)'
  mwi=subwrd(result,4)
  if(mwi > mwmax) ; mwmax=mwi ; endif
  'd const(n(x=5),0,-u)'
  mwn=subwrd(result,4)
  if(mwn > mwmax) ; mwmax=mwn ; endif

  'd const(i(x=6),0,-u)'
  fei=subwrd(result,4)
  if(fei > femax) ; femax=fei ; endif
  'd const(n(x=6),0,-u)'
  fen=subwrd(result,4)
  if(fen > femax) ; femax=fen ; endif

  t=t+1
endwhile

'set warn off'
print 'femax = 'femax
print 'mwmax = 'mwmax
print 'ntmax = 'ntmax

feinc=100
femax=(int(femax/feinc)+1)*feinc
mwinc=10
mwmax=(int(mwmax/mwinc)+1)*mwinc
ntinc=2
ntmax=(int(ntmax/ntinc)+1)*ntinc

print 'femax = 'femax
print 'mwmax = 'mwmax
print 'ntmax = 'ntmax

'set t 1 last'

'pmi=((i(x=1)-i(x=2))/(i(x=1)))*100'
'pmn=((n(x=1)-n(x=2))/(n(x=1)))*100'

'set mproj off'
'set mpdraw off'
'set gxout bar'
'set bargap 50'
'set ccolor 3'
'set t 0.5 'te'.5'
'set vrange 0 'femax
'set yaxis 0 'femax' 'feinc
'set ylopts 1 4 'lsiz
'set xlopts 1 5 'lsiz
if(te=4)
'set xaxis -12 84 24'
'set xlabs  0h | 24h | 48h | 72h '
endif

if(te=6)
'set xaxis -12 132 24'
'set xlabs  0h | 24h | 48h | 72h | 96h | 120h '
endif

'd i'
'set bargap 75'
'set ccolor 4'
'd n'
'set ccolor 0'
'set cthick 10' 
'set baropts outline'
'd n'

rc=plotdims()

if(nbasin = 1)
  bname='LANT'
endif

if(nbasin = 2)
  bname='EASTPAC'
endif

if(nbasin = 3)
  bname='WESTPAC'
endif

if(nvtype = 1)
  vname='HETERO'
endif

if(nvtype = 2)
  vname='HOMO'
endif

t1=vname
rc=stitle(t1,0.5)

xyl=_xlplot-0.3
yyl=_ytplot+0.2
print 'qqqq 'xyl' 'yyl' '_xlplot' '_ytplot
'set string 1 l 5'
'set strsiz 'lsiz
'draw string 'xyl' 'yyl' FE (nm)'

xyl=_xlplot-0.45
print 'qqqq 'xyl' 'yyl' '_xlplot' '_ytplot
'set string 1 c 5'
'set strsiz 'lsiz
'draw string 'xyl' 'yyl' N '

xyl=_xrplot+0.2
print 'qqqq 'xyl' 'yyl' '_xlplot' '_ytplot
'set string 1 r 5'
'set strsiz 'lsiz
'draw string 'xyl' 'yyl' V`bmax`n (kts)'


'set gxout line'
'set ylpos 0 r'
'set ylopts 1 4 'lsiz
'set xlopts 1 4 'lsiz
'set vrange 0 'mwmax
'set yaxis 0 'mwmax' 'mwinc
'set grid off'

'set ccolor 0'
'set cthick 15'
'set ylopts 1 4 'lsiz
'set xlopts 1 4 'lsiz
'd i(x=5)'
'set ccolor 3'
'set cthick 4'
'd i(x=5)'

'set ccolor 0'
'set cthick 15'
'set ylopts 1 4 'lsiz
'set xlopts 1 4 'lsiz
'd n(x=5)'
'set ccolor 4'
'set cthick 4'
'd n(x=5)'

'set ylpos -0.40 l'
'set vrange 0 'ntmax
'set ylopts 1 4 'lsiz
'set yaxis 0 'ntmax' 'ntinc
'set grid off'

'set baropts fill'
'set bargap 90'
'set gxout errbar'

'set ccolor 0'
'set cthick 15'
'd i(x=1);i(x=2)'
'set ccolor 3'
'set cthick 6'
'd i(x=1);i(x=2)'

'set ccolor 0'
'set cthick 15'
'd n(x=1);n(x=2)'
'set ccolor 2'
'set cthick 6'
'd n(x=1);n(x=2)'

'set ccolor 0'
'set cthick 15'
'd n(x=1);n(x=1)'
'set ccolor 1'
'set cthick 6'
'd n(x=1);n(x=1)'


return

*
*-------------------- utility script functions
*

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
*-------------------------- strlen ------------------
*
function strlen(arg)

i=1
while(substr(arg,i,1) != '' & i<250)
  i=i+1
endwhile
return(i-1)

*
*-------------------------- mod ------------------
*
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

*
*-------------------------- stitle ------------------
*
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
  'set string 1 c 6 'angle
  'draw string 'xs' 'ys' 't1
  'set string 1 c 6 0'



return

*
*-------------------------- scrptle ------------------
*
function scrptle(scale)
 
  rc=plotdims()
  '!dtg > dtg.cur'
  rc=read(dtg.cur)
  dtg=sublin(rc,2)
  rc=close(dtg.cur)

  tsiz=0.06
  if(scale != 'scale')
    tsiz = tsiz * scale
  endif

  dx1=_pagex

  xoff=0.15
  yoff=0.06

  x1=xoff
  y1=yoff+tsiz/2

  x2=_pagex-xoff
  y2=y1

  x3=_pagex/2
  y3=y1

  'set strsiz 'tsiz
  'set string 1 l 4' 
  'draw string 'x1' 'y1' GrADS Script: '_script
  'set strsiz 'tsiz
  'set string 1 r 4' 
  'draw string 'x2' 'y2' 'dtg
  'set string 1 c 4 0'
  'draw string 'x3' 'y3' PCMDI (M. Fiorino)'

return

*
*-------------------------- plotdims ------------------
*

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
*
*-------------------------- toptitle ------------------
*

function toptitle(t1,t2,scale,t1col,t2col)

  rc=plotdims()

  xr=_pagex
  xl=0
  y1=_pagey-0.15
  y2=_pagey-0.35
  xs=(xr-xl)*0.5
  tsiz=0.15
  if(scale != 'scale') ; tsiz = tsiz * scale ; endif
  if(t1col=t1col) ; t1col=1 ; endif
  if(t2col=t2col) ; t2col=1 ; endif

  'set strsiz 'tsiz
  'set string 't1col' c 6'
  'draw string 'xs' 'y1' 't1

  if(t2 != '')
    'set string 't2col' c 5'
    'set strsiz 0.10'
    'draw string 'xs' 'y2' 't2
  endif

return
*----------------------------------------------------------
*
*	metadata
*
*----------------------------------------------------------
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

*----------------------------------------------------------
*
*	metadata
*
*----------------------------------------------------------

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
*	run cbarn sf vert xmid ymid
*
*	sf   - scale the whole bar 1.0 = original 0.5 half the size, etc.
*	vert - 0 FORCES a horizontal bar = 1 a vertical bar
*	xmid - the x position on the virtual page the center the bar
*	ymid - the x position on the virtual page the center the bar
*
*	if vert,xmid,ymid are not specified, they are selected
*	as in the original algorithm
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
  strxsiz=0.11*sf
  strysiz=0.12*sf
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
    'set line 1 1 10'
    'draw rec 'xl' 'yb' 'xr' 'yt
    'set line 'col
    'draw recf 'xl' 'yb' 'xr' 'yt
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
        'set line 1 1 10'
        'draw line 'xl' 'yt' 'xm' 'yb
        'draw line 'xm' 'yb' 'xr' 'yt
        'draw line 'xr' 'yt' 'xl' 'yt

        'set line 'col
        'draw polyf 'xl' 'yt' 'xm' 'yb' 'xr' 'yt' 'xl' 'yt

      else

        xm=(xl+xr)*0.5
        ym=(yb+yt)*0.5
        'set line 1 1 10'
        'draw line 'xl' 'ym' 'xr' 'yb
        'draw line 'xr' 'yb' 'xr' 'yt
        'draw line 'xr' 'yt' 'xl' 'ym

        'set line 'col
       'draw polyf 'xl' 'ym' 'xr' 'yb' 'xr' 'yt' 'xl' 'ym

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
        'set line 1 1 10'
        'draw line 'xl' 'yb' 'xm' 'yt
        'draw line 'xm' 'yt' 'xr' 'yb
        'draw line 'xr' 'yb' 'xl' 'yb

        'set line 'col
        'draw polyf 'xl' 'yb' 'xm' 'yt' 'xr' 'yb' 'xl' 'yb
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

        'set line 1 1 10'
        'draw line 'xr' 'ym' 'xl' 'yb
        'draw line 'xl' 'yb' 'xl' 'yt
        'draw line 'xl' 'yt' 'xr' 'ym

        'set line 'col
        'draw polyf 'xr' 'ym' 'xl' 'yb' 'xl' 'yt' 'xr' 'ym
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

*----------------------------------------------------------
*
*	jaecol
*
*	color table by Jae Schemm of CPC, NCEP
*
*----------------------------------------------------------

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
*
* black to light grey
'set rgb 71 250 250 250'
'set rgb 72 225 225 225'
'set rgb 73 200 200 200'
'set rgb 74 180 180 180'
'set rgb 75 160 160 160'
'set rgb 76 150 150 150'
'set rgb 77 140 140 140'
'set rgb 78 124 124 124'
'set rgb 79 112 112 112'
'set rgb 80  92  92  92'
'set rgb 81  80  80  80'   
'set rgb 82  70  70  70'   
'set rgb 83  60  60  60'   
'set rgb 84  50  50  50'   
'set rgb 85  40  40  40'
'set rgb 86  36  36  36'
'set rgb 87  32  32  32'

return
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
*  convert FNMOC DTG to GrADS time
*
  iyr=substr(dtgh,1,2)*1
  imo=substr(dtgh,3,2)*1
  ida=substr(dtgh,5,2)*1
  ihr=substr(dtgh,7,2)*1
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

  iyr=substr(dtgh,1,2)*1
  imo=substr(dtgh,3,2)*1
  ida=substr(dtgh,5,2)*1
  ihr=substr(dtgh,7,2)*1
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


if(iyr<10);iyr='0'iyr;endif
if(imo<10);imo='0'imo;endif
if(ida<10);ida='0'ida;endif
if(ihr<10);ihr='0'ihr;endif

return (iyr%imo%ida%ihr)



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
endif

return


*-----------------------------------------------------------
*
*	function setup
*
*-----------------------------------------------------------
function setup(rcfg)
*
*	dtg global variables
*
_monamel='jan feb mar apr may jun jul aug sep oct nov dec'
_monameu='JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC'
_monday='31 28 31 30 31 30 31 31 30 31 30 31'

if(rcfg='y')
*
*	ensemble name cfg
*
ecfg='g.generic.cfg'
iok=0
i=0
imax=1000
while(1)
  rc=read(ecfg)
  card=sublin(rc,2)
  iok=sublin(rc,1)
  if(iok != 0 & i = 0) 
    say 'Unable to read configuration file!!!'
    say 'BYE'
    'quit'
  endif
  if(iok=2) ; _ne=i ; break ; endif
  i=i+1
  _en.i=subwrd(card,1)
  if(i=imax) ; break ; endif
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
say 'qqq kk = 'np' 'npx' 'npy' 'dpx' 'dpy' 'dxb' 'dyb

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



function getinfo()
'!xwininfo -int -name GrADS > wininfo'
i=0; gotid=0
while (1)
  res=read(wininfo)
  dum=sublin(res,1)
  cod=subwrd(dum,1)
  if(cod!=0)
    if(cod=1); say "Error opening file"; endif
    if(cod=8); say "File open for write"; endif
    if(cod=9); say "I/O error"; endif
    break
  endif
  i=i+1
  dum=sublin(res,2)
*
*	different output format?
*
  if(subwrd(dum,3)="Window" & subwrd(dum,4) = "id:") 
    _winid=subwrd(dum,5)
    gotid=1
    break
  endif

  if(subwrd(dum,2)="Window" & subwrd(dum,3) = "id:") 
    _winid=subwrd(dum,4)
    gotid=1
    break
  endif

endwhile
rc=close(wininfo)
'!rm wininfo'
return(gotid)


