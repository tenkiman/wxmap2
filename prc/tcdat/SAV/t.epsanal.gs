function main(args)

_model='ecmt'
_stmid='02W.2009'

_ddir='/w21/dat/tc/tceps/ecmwf/2009/2009050312'
_cfile='tceps.grid.02W.2009.2009050312.ecmt.ctl'

_pdir='/w21/dat/tc/tceps/ecmwf/2009/2009050312'


latc=14.8
lonc=126.0



_bkgpath=_pdir'/bkg.'_stmid'.png'

_dtau=12
if(_model = 'ecmt') ; _nens=51 ; endif
if(_model = 'ukmo') ; _nens=17 ; endif


rc=gsfallow('on')
rc=const()
rc=jaecol2()

_xsiz=1024
_ysiz=_xsiz*(3.0/4.0)

_dobasemap=1
_lnint=10
_ltint=5


'open '_ddir'/'_cfile
'set t 1'
_bdtg=curdtg()



if(_dobasemap = 1) ; rc=pltbmap() ; endif

rc=gettrk()

ntaumax=11

ntau=1
while(ntau <= ntaumax)
  rc=pltsp(ntau,latc,lonc,'hit')
  ntau=ntau+1
endwhile

ntau=1
while(ntau <= ntaumax)
  rc=pltsp(ntau,latc,lonc,'sp')
  ntau=ntau+1
endwhile

return



function pltbmap()


  'set xsize '_xsiz' '_ysiz
  'set xlint '_lnint
  'set ylint '_ltint
  'set mpdset mres'
  'set map 1 0 8'
  'set map 15 0 6'

  'set grads off'
  'set timelab on'

  'define d=const(n,0,-a)'
  'set cmax -1'
  'set gxout fgrid'
  'set fgvals 1 1'
  'd d'

  'set rgb 41 245 255 255'
  'basemap L 72 1 M'
  'basemap O 41 1 M'
  'd d'
  'printim '_bkgpath' x'_xsiz' y'_ysiz' white'
#   'gxyat -o '_bkgpath' -x '_xsiz' -y'_ysiz

return



function d03tau(tau)

if(tau > 100)            ; otau=tau     ; endif
if(tau > 10 & tau < 100) ; otau='0'tau  ; endif
if(tau >=0 & tau < 10 )  ; otau='00'tau ; endif

return(otau)



function pltsp(ntau,latc,lonc,ptype)

'c'

'set xsize '_xsiz' '_ysiz
'set xlint '_lnint
'set ylint '_ltint
'set mpdset mres'
'set map 1 0 8'
'set map 15 0 6'

'set grads off'
'set timelab on'

'set grads off'
'set xlint '_lnint
'set ylint '_ltint
'set t 'ntau

tau=(ntau-1)*_dtau
cdtg=curdtg()

otau=d03tau(tau)


if(ptype = 'sp')

  'set gxout shaded'
  'set csmooth on'
  'set clevs   5  10  20  30  40  50  60  70  80  90  '
  'set ccols 0   6  2   8   7   10   3  5   11   4  9 '
  'd sp'
  'cbarn'

  t1='ECMWF EPS for TC: '_stmid' bdtg: '_bdtg' Counts at `3t`0= 'otau
  t2='valid dtg: 'cdtg' %`bfound`n:'nf' %`bmissed`n:'nm 

  pngpath=_pdir'/eps.sp.'ntau'.png'

endif


if(ptype = 'hit')

  'p=(n/asum(n,g))*100.0'
  'p=n'
  'd const(asum(n,g),0,-u)'
  card=sublin(result,1)
  nf=subwrd(card,4)
  nf=(nf/_nens)*100.0
  nm=100.0-nf

  nf=math_format('%3.0f',nf)
  nm=math_format('%3.0f',nm)

  'pp=const(p,-1,-u)'
  
  'set gxout grfill'
  'set clevs   0   1    2    3     4   5    6    7    8   10   50'
  'set ccols 0  39   37   35    33   31  23   25   26   27  28   29'
  'set ccols 0  39   23   35    27   33  43   75   46   77  48   1'

  'd pp'
  'cbarn'

  t1='ECMWF EPS for TC: '_stmid' bdtg: '_bdtg' Counts at `3t`0= 'otau
  t2='valid dtg: 'cdtg' %`bfound`n:'nf' %`bmissed`n:'nm 

  pngpath=_pdir'/eps.hit.'ntau'.png'

endif

#
#  plot ensemble tracks
#
rc=plttrk(ntau)


#
#  plot best track at tau=0
#
'drawtcbt 'latc' 'lonc' 45 0.5'

#
# toptitle
#
rc=toptitle(t1,t2,1,1,1)

if(_dobasemap = 1)
print    'printim 'pngpath' -b '_bkgpath' -t 0 x'_xsiz' y'_ysiz' white'
  'printim 'pngpath' -b '_bkgpath' -t 0 x'_xsiz' y'_ysiz' white'
else
  'printim 'pngpath' x'_xsiz' y'_ysiz
endif

return



function gettrk()

tfile='/tmp/t.txt'

rc=0

ntrk=1

while(rc = 0)

  result=read(tfile)
  rc=sublin(result,1)
  card=sublin(result,2)
  imax=100
  i=1
  j=1
  jd=1
  while(i<imax)
    if(ntrk = 1)
      _lat.i.ntrk=subwrd(card,jd)
      _detlat.i=subwrd(card,jd) ; jd=jd+1
      _lon.i.ntrk=subwrd(card,jd)
      _detlon.i=subwrd(card,jd) ; jd=jd+1
    endif
    _lat.i.ntrk=subwrd(card,j) ; j=j+1
    _lon.i.ntrk=subwrd(card,j) ; j=j+1

    if(_lat.i.ntrk = '')
      npos=i-1
      if(ntrk = 1)
         _detnpos=npos
      endif
      i=imax+1
    endif
    i=i+1
  endwhile

  _npos.ntrk=npos

  ntrk=ntrk+1

endwhile

_ntrk=ntrk-1

return




function plttrk(ntau)

ntrk=1

n=1
while(n<=_ntrk)

  if(n = 1)
    rct=ptrk(_detnpos,1,_detnpos)
  endif

  rct=ptrk(_npos.n,n,ntau)

  n=n+1

endwhile

rct=ptrk(_detnpos,1,_detnpos)

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
  else
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

else

  'set line 5 3 4'
  'draw line 'x1' 'y1' 'x2' 'y2

endif

  n=n+1

endwhile

rct=0

return(rct)
