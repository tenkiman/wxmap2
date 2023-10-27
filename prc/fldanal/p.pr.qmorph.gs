function main(args)

rc=gsfallow(on)
rc=const()
rc=jaecol2()

i=1
_curdtgh=subwrd(args,i)  ; i=i+1
_source=subwrd(args,i)   ; i=i+1
_area=subwrd(args,i)     ; i=i+1

xs=1024
ys=768

ntback=24
_nave=2
#_nave=6

#
# accum 30 min rain and convert to mm/day
#
nhr=_nave*0.5
ndy=24.0/nhr

_scale=1.0/_nave
_units='mm/h'

_scale=24.0/(2*_nave)
_units='mm/d'

runave=0

dore=0

dozoom=1
setzoom=0
dobasemap=0

pltbase=0
dlzoom=25
dlzoom=30
dlinc=10
aspect=1024/768
aspect=aspect*1.25


print 'sssssssssssssssssssssssss '_source'sssssssssssss'
if(_source = '')
  _source='qmorph'
endif

bddir='/dat1/dat/pr/'_source'/30min_025deg/grib'
bpdir='/dat1/dat/pr/'_source'/30min_025deg/plt'

ctlpath=bddir'/'_source'.ctl'


if(_area != '')

  if(_area = 'global')
    dozoom=0
  else
    rc=prwarea()
    dozoom=-1
  endif
endif

print 'qqqqqqqqqqqqqqq '_area
'set xsize 'xs' 'ys

print 'ccccccccccccccccccccccccc 'ctlpath
rc=ofile(ctlpath)

ntback=ntback*2

'set mpdset mres'
'set t last'
'q time'

if(_curdtgh != '')
  curtime=dtg2gtime(_curdtgh)
  print 'cccccccccccc'curtime
  'set time 'curtime
  'q time'
  print 'cccccccccctime 'result
endif

'q dim'
card=sublin(result,5)
print card
nt=subwrd(card,9)
print card
print 'nnnnnnnnnnn 'nt

bt=nt-ntback-1
if(math_mod(bt,2) = 0) ; bt=bt+1 ; endif

dt=2
et=nt-1

print 'eeeeeeeeeeeeeeeeeee 'bt' 'et' 'dt

if(dozoom = -1)

if(_blon < 0) ; _blon=360+_blon ; endif
if(_elon < 0) ; _elon=360+_elon ; endif

'set lon '_blon' '_elon
'set lat '_blat' '_elat

endif

if(dozoom = 0)
  'set lon 20 380'
endif

'q dim'
print result

t=bt
while(t <= et)

  'c'
  'set t 't

if(runave = 1)
  'pra=ave(pr,t-'_nave',t+'_nave')*'_scale 
else
####  'pra=ave(pr,t-'_nave',t+'0')*'_scale
print  'pra=sum(pr,t-'_nave',t+'0')*'_scale
  'pra=sum(pr,t-'_nave',t+'0')*'_scale
  'd aave(pra,g)*24'
print result

endif

if(dore=1)
  'pra=re(pra,0.5)'
endif

if(dobasemap = 1)

#
# do dummy plot for setup
#
  'set cmin -999'
  'd pra'
  rc=prwbasemap(0,1)
endif


rcpr=plotpr()
'q pos'


if(dozoom = 1 & setzoom = 0 & rcpr = 1)

  x1=subwrd(result,3)
  y1=subwrd(result,4)
  'q xy2w 'x1' 'y1
  lon1=subwrd(result,3)
  lat1=subwrd(result,6)

  lat1=math_nint(lat1)
  lon1=math_nint(lon1)
  
  lat1=math_nint(lat1/dlinc)
  lat1=lat1*dlinc
  
  lon1=math_nint(lon1/dlinc)
  lon1=lon1*dlinc
  print 'lat1 lon1 'lat1' 'lon1
  
  
  blat=lat1-dlzoom
  elat=lat1+dlzoom
  
  blon=lon1-dlzoom*aspect
  elon=lon1+dlzoom*aspect
  
  'set lat 'blat' 'elat
  'set lon 'blon' 'elon
  
  t=bt
  'set t 't
  rc=plotpr()
  'q pos'

  pltbase='pr.'_source'.zoom.'runave'.'_nave'.'lat1'.'lon1
  
  doplt=0
  setzoom=1
  
endif

if(dozoom = 0)
  pltbase='pr.global.'runave'.'_nave
endif

if(dozoom = -1)
  pltbase='pr.'_area'.'runave'.'_nave
endif

pltpath=bpdir'/'pltbase'.'_gdtg'.png'
print 'pppppppppppppptttttttttttt 't' 'tb' 'pltpath

if(t >= bt)
  pint 'pppppppppppppp 'pltpath
  'printim 'pltpath' x'xs' y'ys
endif

  t=t+dt
endwhile



'quit'
return





function plotpr()

  'c'

  rc=getgdtg()
  rcpra=datachk(pra)

if(rcpra < 0)
   print 'gggggggggggggggggggg 'rcpra
   rc=0
   return(rc)
endif

if(_units = 'mm/h')
  'set clevs   0.25  0.5  1.0  1.5  2.0. 3.0   5.0  4.0   6.0  8.0  10.0 12.0 14.0 16.0 18.0 20.0 25.0'
  'set ccols 0     49   47   45   43    39   35   31   21    23   26    27   29   55 57 59 67 63 61'

else
  'set clevs   1  2  4  8  16  32 64 128 256'
  'set rgb 98 185 255 00 50'
  'set ccols 0 39 37 36 98 22 24 26 28 45 41'
endif

  'set gxout shaded'
  'set csmooth on'
  'set cterp on'
#
# 20000614 - change rec by dan reinhart
#
  'set csmooth on'
  'set cterp on'
  'set grads off'
  'set timelab on'
  'd pra'
  'cbarc'
  'draw title '_source' '_gdtg' nave: '_nave

return(1)


function getgdtg()
  'q time'  
  gtime=subwrd(result,3)
  _gdtg=gtime2dtg(gtime)
return
