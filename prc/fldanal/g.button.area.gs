function main (args)
'reinit'
_bdtg=subwrd(args,1)
_area=subwrd(args,2)
_type=subwrd(args,3)
_title1=subwrd(args,4)
_title2=subwrd(args,5)
_model=subwrd(args,6)

say 'qqq 'args

*if(_area = asia)
*  _title='E. Asia'
*endif
*if(_area = conus)
*  _title='CONUS'
*endif

_otype=gif
rc=jaecol()
*
*	read the configuration file
*
'open dum.ctl'
*
*	set up the area
*
rc=setplot(_area)

'set xlint '_xlint
'set ylint '_ylint
'set rgb 91 50 50 50'
'set background 91'

tt=_title1
_title1=''
i=1
while(i<=15)
  ch=substr(tt,i,1)
  if(ch='') ; break ; endif
  if(ch='_') ; ch=' ' ; endif
  _title1=_title1%ch
  i=i+1
endwhile

tt=_title2
_title2=''
i=1
while(i<=15)
  ch=substr(tt,i,1)
  if(ch='') ; break ; endif
  if(ch='_') ; ch=' ' ; endif
  _title2=_title2%ch
  i=i+1
endwhile

_xs=100
_ys=75

_xs=115
_ys=90

if(_type=area)
  'set xsize '_xs' '_ys
  'set map 1 0 8'
scale=0.9
siz=1.5
siz=siz*scale
  'set strsiz 'siz
  'set cmin 100000000'
  'set grads off'
  'd lat'

lcol=90
ocol=91
'set rgb 90 100 50 25'
'set rgb 91 10 20 85'

'basemap.2 L 'lcol' 1'
'basemap.2 O 'ocol' 1'

'set map 0 0 10'
'draw map'

'set map 1 0 3'
'set cmin 100000'
'd lat'
'draw map'
  'set string 0 c 20'
if(_title2 != 'NULL')
  'draw string 5.5 3.85 '_title1
  'set string 2 c 10'
  'draw string 5.4 3.95 '_title1
endif
if(_title2 = 'NULL') ; _title2=_title1 ; endif
  'set string 0 c 20'
  'draw string 5.5 1.55 '_title2
  'set string 2 c 10'
  'draw string 5.4 1.65 '_title2
else
  'set xsize 64 32'
  'set map 1 0 1'
  'set cmin 100000000'
  'set grads off'
  'set parea 0 11.0 0 8.5'
  'd psl'
  'set strsiz 2.0 4.0'
  'set string 0 c 10'
  'draw string 5.5 6.5 '_model 
  if(_model='AVN') ; 'set string 2 c 10' ; endif
  if(_model='MRF') ; 'set string 3 c 10' ; endif
  if(_model='NGP') ; 'set string 4 c 10' ; endif
  
  'draw string 5.3 6.3 '_model 
scale=0.8
xsiz=1.5
ysiz=3.0
xsiz=xsix*scale
ysiz=ysiz*scale
  'set strsiz 'xsiz' 'ysiz
  'set string 0 c 10'
  'draw string 5.5 1.5 '_title
  'set string 5 c 10'
  'draw string 5.3 1.7 '_title
endif


if(_otype=gif)
  gifname=_area'.'_type'.button.gif'
  pngname=_area'.'_type'.button.png'
  'printim 'pngname'  x'_xs' y'_ys
'!convert 'pngname' 'gifname
#  'quit'
endif

'quit'

return
*
*-------------------------- mydate ------------------
*
function mydate
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
*-----------------------------  pman ---------------
*		
function pman(k,j,opt)

'set parea 0.4 10.8 0.65 8.25'

if(opt=full)
  'c'
  'set vpage 0 11 0 8.5'
  'set vpage 0.1 10.9 0.1 8.4'
else
  if(j=1)
    'set vpage 0 5.5 4.25 8.5'
  endif

  if(j=2)
    'set vpage 5.5 11 4.25 8.5'
  endif

  if(j=3)
    'set vpage 0 5.5 0 4.25'
  endif

  if(j=4)
    'set vpage 5.5 11 0 4.25'
  endif
endif

if(_tau.j < 0) ; 'set dfile '_fna ; else ; 'set dfile '_fnf ; endif

'set time '_time.j

pstat=1

if(k=1) ; rc=gpz500(j) ; endif
if(k=2) ; rc=gppsl(j) ; endif
if(k=3) ; rc=gpprecip(j,_prvar) ; endif
if(k=4) ; rc=gp850(j) ; endif

if(rc = 0) ; pstat=0 ; endif
if(rc = 99) ; pstat=99 ; endif
return(pstat) 

*
*-------------------------- gpz500 ------------------
*
function gpz500(k)
t1='500mb  Heights / Rel Vort / 12h Ht Change'
rc=dtitle(t1,k)
pstat=1
_shades=0
'set lev 500'
'set grads off'
rc=datachk(zg) 
if(rc != 0)
  return(pstat)
endif

rc=datachk(ua)
if(rc=0)
pstat=0
'set gxout shaded'
rc=jaecol()

pcol.2='49 48 47 46 45 44 43 42 41 21 22 23 24 25 26 27 28 29'
pcol.2='49 48 47 46 45 44 43 42 41 31 32 33 34 35 36 37 38 39'
pcol.1='69 68 67 66 65 63 61 61 53 55 56 57 58 59'
pcol.1='59 58 57 55 55 53 52 51 61 62 63 64 65 66 67 68 69'
pcol.1='59 58 57 55 55 53 52 62 63 64 65 66 67 68 69'
*pcol.1='49 48 47 45 44 43 42 62 63 64 65 66 67 68 69'
pcol.1='54 53 52 61 42 43 44 45 47 48 49 69 68 67 66 65 64 63 21 22 23 24 25 26'

'set rbrange -14 20'
'set rbcols 'pcol.1
'set black -2 2'
'set cint 2'
'd hcurl(ua,va)*1e5'
'q shades'
_shades=result

vrtcnt=1
if(vrtcnt)
'set gxout contour'
'set cint 4'
'set ccolor 0'
'set clab off'
'set black -2 2'
'set grads off'
'd hcurl(ua,va)*1e5'
endif

endif


plotdzdt=1
if(plotdzdt) 

if(_dtau=12)
  'set cint 30'
else
  'set cint 15'
endif

if(_dtgp.k != 999) 
say 'qqqqq zd 'k' '_fn.k' '_fnp.k' '_timep.k
  'define zd=zg.'_fn.k'-zg.'_fnp.k'(time='_timep.k')'
  rc=dtitle(t1,k)
  rc=datachk(zd) 
  if(rc=0)
  'set gxout contour'
  'set ccolor 0'
  'set cthick 10'
  'set grads off'
  'set clab off'
  'd zd'
  'set ccolor rainbow'
  'set ccolor 3'
  'set cthick 5'
  'set clab off'
  'd zd'
  'set cthick 10'
  'set clevs 0'
  'set ccolor 3'
  'set clab off'
  'd zd'
  else
*    return(rc)
  endif
endif

endif
*
*	z 500 
*
'set grads off'
'set gxout contour'
'set rbcols auto'
'set ccolor 0'
'set cthick 12'
'set cint 60'
'd zg(lev=500)'

'set ccolor 1'
'set cthick 5'
'set cint 60'
'set clab on'
'd zg(lev=500)'

rc=dtitle(t1,k)
if(_shades!=0) ; rc=cbarc() ; endif
return(pstat)


*
*-------------------------- gppsl ------------------
*
function gppsl(k)
pslci=4
'draw map'
t1='Sea Level Pressure / 1000-500mb Heights'
rc=datachk(psl)

if(rc != 0) ; return(rc) ; endif

'set gxout contour'
'set grads off'

'set ccolor 0'
'set cthick 10'
'set cint 'pslci
'set clab off'
'd psl/100'

'set ccolor rainbow'
'set rbrange 980 1024'
'set cthick 4'
'set cint 'pslci
'set clab off'
'd psl/100'

'set ccolor rainbow'
'set rbrange 980 1024'
'set clab on'
'set cint 4'
'd psl/100'

rc=datachk(zg) 
if(rc=0)
'set gxout contour'
'set ccolor 1'
'set cstyle 5'
'set clab on'
'set grads off'
'set cint 6'
'd (zg(lev=500)-zg(lev=1000))/10'
'set clevs 540'
'set ccolor 1'
'set cthick 10'
'set cstyle 1'
'set grads off'
'd (zg(lev=500)-zg(lev=1000))/10'
endif
rc=dtitle(t1,k)
return(0)
*
*-------------------------- gpprecip ------------------
*
function gpprecip(k,prvar)
if(_model=avn | _model=mrf)
  t1='SLP [hPa] / 540 Line / Prev 6-h Prcp Rate [mm/day]'
else
  t1='SLP [hPa] / 540 Line / Prev 12-h Prcp Rate [mm/day]'
endif

_shades=0
if(_tau.k <= 0) ; return ; endif
rc=datachk(prvar)
if (rc != 0) ; return(rc) ; endif 
'set clevs   1  2  4  8  16  32 64'
'set gxout shaded'
'set ccols 0 32 33 35 36 37 39'
'set ccols 0 39 37 36 35 22 24 26'
'set csmooth on'
'set grads off'

if(t!=1)
  'd 'prvar
else
  'd 'prvar'(t=2)'
endif
'q shades'
_shades=result
'set gxout contour'
'set ccolor 0'
'set cthick 10'
'set cint 2'
'set clab off'
'd psl/100'

'set ccolor rainbow'
'set rbrange 980 1024'
'set cthick 4'
'set cint 2'
'set clab off'
'd psl/100'

'set ccolor rainbow'
'set rbrange 980 1024'
'set clab on'
'set cint 4'
'd psl/100'

plot500=0
if(plot500)
'set gxout contour'
'set ccolor 0'
'set cthick 12'
'set cint 60'
'd zg(lev=500)'

'set ccolor 1'
'set cthick 5'
'set cint 60'
'set clab on'
'd zg(lev=500)'
endif

rc=datachk(zg) 
if(rc=0)
'set gxout contour'


*
*	plot 540 thickness line
*
'set clevs 540'
'set ccolor 1'
'set cthick 20'
'set cstyle 1'
'set grads off'
'd (zg(lev=500)-zg(lev=1000))/10'

'set clevs 540'
'set ccolor 4'
'set cthick 10'
'set cstyle 1'
'set grads off'
'd (zg(lev=500)-zg(lev=1000))/10'
endif
rc=dtitle(t1,k)
if(_shades!=0) ; rc=cbarc() ; endif
return(0)

*
*-------------------------- gp850 ------------------
*
function gp850(k)
t1='850mb Temperatures / RH / Winds'
'set lev 850'
pstat=1
_shades=0
if(_res=10 & _model=ngp)
*  ddp0=25
*  'define hur=(('ddp0'-ddp)/'ddp0')*100'
  rc=datachk(ddp)
  if(rc=0) 
    'hur=(esmrf(ta-ddp)/esmrf(ta))*100'
  endif
endif

rc=datachk(hur)
if (rc = 0) 
'set grads off'
'set gxout shaded'
'set clevs  50 70 90'
'set ccols 0 73 76 79'
'set ccols 0 76 74 72'
'd hur'
'q shades'
_shades=result
else
  'draw map'
endif

rc=datachk(ta) ; if(rc!=0) ; return(rc) ; endif
pstat=0
tcint=3
'set gxout contour'
'set ccolor 0'
'set cint 'tcint
'set cthick 12'
'set grads off'
'set clab off'
'd ta-273.16'
'set rbrange -20 20'
'set ccolor rainbow'
'set cint 'tcint
'set cthick 5'
'set grads off'
'set clab on'
'd ta-273.16'
'set ccolor 1'
'set clevs 0'
'set cthick 12'
'set grads off'
'set clab off'
'd ta-273.16'
'set ccolor 0'
'set clevs 0'
'set cthick 1'
'set grads off'
'set clab off'
'd ta-273.16'

rc=datachk(ua) ; if(rc!=0) ; return(rc) ; endif
'set gxout barb'
'set digsiz 0.05'
*
*	winds greater than 8 kts
*
'set ccolor 0'
'set cthick 10'
'd skip(ua*1.944,'_vskip');maskout(va*1.944,(mag(ua,va)*1.944-8.0))'

'set cthick 4'
'set ccolor 1'
'd skip(ua*1.944,'_vskip');maskout(va*1.944,(mag(ua,va)*1.944-8.0))'

*
*	plot winds greater than 25 kts in yellow
*
'set ccolor 0'
'set cthick 10'
'd skip(ua*1.944,'_vskip');maskout(va*1.944,(mag(ua,va)*1.944-24.0))'

'set cthick 4'
'set ccolor 12'
'd skip(ua*1.944,'_vskip');maskout(va*1.944,(mag(ua,va)*1.944-24.0))'
*
*	plot winds greater than 35 kts in orange
*
'set ccolor 0'
'set cthick 10'
'd skip(ua*1.944,'_vskip');maskout(va*1.944,(mag(ua,va)*1.944-34.0))'

'set cthick 4'
'set ccolor 8'
'd skip(ua*1.944,'_vskip');maskout(va*1.944,(mag(ua,va)*1.944-34.0))'
*
*	plot winds greater than 50 kts in red
*
'set ccolor 0'
'set cthick 10'
'd skip(ua*1.944,'_vskip');maskout(va*1.944,(mag(ua,va)*1.944-49.0))'

'set cthick 4'
'set ccolor 2'
'd skip(ua*1.944,'_vskip');maskout(va*1.944,(mag(ua,va)*1.944-49.0))'

*'draw map'
rc=dtitle(t1,k)

if(_shades!=0) ; rc=cbarc() ; endif

return(pstat)

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
*-------------------------- curdtgh ------------------
*
function curdtgh()
*
*  convert current time to dtg 
*
  moname='JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC'
  'q time'
  t1=subwrd(result,3)
  iyr=substr(t1,11,2)
  nmo=substr(t1,6,3)
  ida=substr(t1,4,2)
  ihr=substr(t1,1,2)
  i=1
  while (nmo!=subwrd(moname,i));i=i+1;endwhile
  imo=i
  if(imo < 10); imo='0'imo; endif
  if(ihr = 0); ihr='00';endif
  if(ihr < 10 & ihr != '00'); ihr='0'ihr; endif

  idtg=iyr%imo%ida%ihr

return (idtg)

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
    endif
    ida=monday.imo
  endif

  if(imo<=0)
    imo=imo+12
    iyr=iyr-1
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

*
*-------------------------- dtghcur ------------------
*
function dtghcur(dtgh)
*
*  convert FNMOC DTG to GrADS time
*
 moname='JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC'
  iyr=substr(dtgh,1,2)*1
  imo=substr(dtgh,3,2)*1
  ida=substr(dtgh,5,2)*1
  ihr=substr(dtgh,7,2)*1
  nmo=subwrd(moname,imo)
  imo=i
return (ihr%'Z'ida%nmo%'19'%iyr)

function dtghval(cdtg)
  iyr=substr(cdtg,1,2)*1
  imo=substr(cdtg,3,2)*1
  ida=substr(cdtg,5,2)*1
  ihr=substr(cdtg,7,2)*1
  idtg=iyr*1000000+imo*10000+ida*100+ihr
return(idtg)
*
*----------------- setplot ----------------
*
function setplot(area)
*
*	read an input file for the plot parameters
*
fname='../cfg/area.'_area'.cfg'
print 'qqqq 'fname

iok=0
i=0
ncards=13
while(iok = 0 & i <= ncards)

  rc=read(fname)
  card=sublin(rc,2)
  iok=sublin(rc,1)
  i=i+1

  if(iok != 0 & i = 1) 
    say 'unable to open plot set up data for area= '_area
    say 'BYE'
    'quit'
  endif
 
  if(iok != 0 & i <= ncards)
    say 'premature EOF in area set up file= 'fname
    say 'BYE'
    'quit'
  endif

  if(i=1)  ; _proj    = subwrd(card,1) ; endif
  if(i=2)  ; _geores  = subwrd(card,1) ; endif
  if(i=3)  ; _pareabd = card           ; endif
  if(i=4)  ; _lon1    = subwrd(card,1) ; endif
  if(i=5)  ; _lon2    = subwrd(card,1) ; endif
  if(i=6)  ; _lat1    = subwrd(card,1) ; endif
  if(i=7)  ; _lat2    = subwrd(card,1) ; endif
  if(i=8)  ; _mplon1  = subwrd(card,1) ; endif
  if(i=9)  ; _mplon2  = subwrd(card,1) ; endif
  if(i=10) ; _mplat1  = subwrd(card,1) ; endif
  if(i=11) ; _mplat2  = subwrd(card,1) ; endif
  if(i=12) ; _xlint   = subwrd(card,1) ; endif
  if(i=13) ; _ylint   = subwrd(card,1) ; endif

endwhile

rc=close(fname)

*
*	defaults do the sets
*
  if(_proj    = default ) ; _proj     = latlon  ; endif 
  if(_geores  = default ) ; _geores   = lowres ; endif 
  if(substr(_pareabd,1,3) = def ) 
    _pareabd  = '1 10 1 8'
   endif 
  if(_lon1    = default ) ; _lon1     = 0      ; endif 
  if(_lon2    = default ) ; _lon2     = 360    ; endif 
  if(_lat1    = default ) ; _lat1     = -90    ; endif 
  if(_lat2    = default ) ; _lat2     = 90     ; endif 
  if(_mplon1  = default ) ; _mplon1   = ''     ; endif 
  if(_mplon2  = default ) ; _mplon2   = ''     ; endif 
  if(_mplat1  = default ) ; _mplat1   = ''     ; endif 
  if(_mplat2  = default ) ; _mplat2   = ''     ; endif 
  if(_xlint   = default ) ; _xlint    = ''     ; endif 
  if(_ylint   = default ) ; _ylint    = ''     ; endif 

  'set mproj '_proj
  'set mpdset '_geores
  if(_pareabd != '') ; 'set parea '_pareabd ; endif
  'set lon '_lon1' '_lon2
  'set lat '_lat1' '_lat2
  
  if( (_proj = 'nps' | _proj = 'sps' | _proj = 'lambert') & mplon1 != '') 
    'set mpvals '_mplon1' '_mplon2' '_mplat1' '_mplat2
  else
    if(_proj = 'nps')
      _mplon1=-90
      _mplon2=270
      _mplat1=0
      _mplat2=90
    endif
    if(_proj = 'sps')
      _mplon1=-90
      _mplon2=270
      _mplat1=-90
      _mplat2=0
    endif
  endif  
*
*	skip on winds
* 
  dlat=_lat2-_lat1
  dlon=_lon2-_lon1
  
  sc1=150
  sc2=240
  sc3=360
  _vskip=1

  if( (dlat >= sc1 & dlat < sc2) | (dlon >= sc1 & dlon < sc2) )
    _vskip=2
  endif
  if( (dlat >= sc2 & dlat <= sc3) | (dlon >= sc2 & dlon <= sc3) )
    _vskip=3
  endif

*
*	1deg data
*
  if(_res=10)
     if(_vskip=3) ; _vskip=5; endif
     if(_vskip=2) ; _vskip=3; endif
  endif

return


function datachk(var)
'set gxout stat'
'd 'var
i=1
while(i<100)
  card=sublin(result,i)
  test=subwrd(card,1)%subwrd(card,2)
  if(test=Undefcount) 
    undef=subwrd(card,4)
    break
  endif
  i=i+1
endwhile

'set gxout grid'
return(undef)

function dtitle(t1,k)

'set line 0'
'draw recf 0.05 0.05 10.95 0.35'
'set strsiz 0.15 0.18'
'set string 3 l 10'
'draw string 0.2 0.46 Verify: 'mydate()
'set string 3 r 10'
'draw string 10.80 0.46 't1
'draw recf 0.05 8.15 10.95 8.50'
if(_res=10)
  tres='`21.0`3.`0 Fields`0'
else
  tres='2.5`3. `0 Fields'
endif

ttau=_tau.k*1.0

'set string 2 l 10'
if(_model=ngp)
'draw string 0.2 8.30 NOGAPS '_bdtg' run 'tres' `3t`0 = 'ttau' h'
endif

if(_model=avn)
'draw string 0.2 8.30 NCEP AVN  '_bdtg' run 'tres' `3t`0 = 'ttau' h'
endif

if(_model=mrf)
'draw string 0.2 8.30 NCEP MRF '_bdtg' run 'tres' `3t`0 = 'ttau' h'
endif
return


function setmtau

  _tau.1=_taubeg
  i=1
  while(i<=4)
    if(_tau.i > _taumax) 
      _dtg.i=999
      _dtgp.i=999
    else
      _dtg.i=incdtgh(_bdtg,_tau.i)
      _time.i=dtghcur(_dtg.i)
      if(_tau.i < 0) ; _fn.i=_fna ; else ; _fn.i=_fnf ; endif 
      taup=_tau.i-_dtau
      if(taup < _taumin ) 
        _dtgp.i=999
      else 
        if(taup < 0) ; _fnp.i=_fna ; else ; _fnp.i=_fnf ; endif 
        _dtgp.i=incdtgh(_bdtg,taup)
        _timep.i=dtghcur(_dtgp.i)
      endif
    endif
    tauold=_tau.i
    i=i+1
    _tau.i=tauold+_tauinc

  endwhile

return

function setstau

  _tau.1=_taubeg

  _dtg.1=incdtgh(_bdtg,_tau.1)
  _time.1=dtghcur(_dtg.1)
  if(_tau.1 < 0) ; _fn.1=_fna ; else ; _fn.1=_fnf ; endif 
  taup.1=_tau.1-_dtau
  if(taup.1 < 0) ; _fnp.1=_fna ; else ; _fnp.1=_fnf ; endif 
  _dtgp.1=incdtgh(_bdtg,taup.1)
  _timep.1=dtghcur(_dtgp.1)

  i=2
  while(i<=4)
    _tau.i=_tau.1
    _time.i=_time.1
    _timep.i=_timep.1
    _fn.i=_fn.1
    _fnp.i=_fnp.1
    i=i+1
  endwhile

return
*
*-------------------------- scrptle ------------------
*
function scrptle(scale,type)

  rc=plotdims()
  '!dtg > dtg.cur'
  rc=read(dtg.cur)
  dtg=sublin(rc,2)
  rc=close(dtg.cur)

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
  'set strsiz 'tsiz
  'set string 1 r 4' 
  'draw string 'x2' 'y2' 'dtg
  'set string 1 c 6 0'


return

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

function getinfo()
'q'
card=sublin(result,1)
gradsver=subwrd(card,3)
winname='"GrADS 'gradsver'"'
'!xwininfo -int -name 'winname' > wininfo'
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

