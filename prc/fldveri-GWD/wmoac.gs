function wmoac(args)

rc=gsfallow(on)
rc=const()

i=1
vdtg=subwrd(args,i) ; i=i+1 
tauf=subwrd(args,i) ; i=i+1 

taua=000

dx=2.5

dtgc='1959'substr(vdtg,5,10)

gtime=dtg2gtime(vdtg)
gtimec=dtg2gtime(dtgc)
print 'gtime 'gtime' 'gtimec

'set time 'gtime
'set lon 0 380'
'set lat -90 90'
'set lev 500'

'zc=re2(zg.3(time='gtimec'),'dx')'
rc=datachk(zc)
if(rc != 0); print 'FFF failed to find climo for gtimec 'gtime ; 'quit' ; endif

'zf=re2(zg.1(ens=f'tauf'),'dx')'
rc=datachk(zf)
print 'qqqqqqqqqqqq 11111111111111 'rc
if(rc != 0) 
'zf=re2(zg.2(ens=f'tauf'),'dx')'
rc=datachk(zf)
print 'qqqqqqqqqqqq 2222222222222 'rc
endif

'za=re2(zg.1(ens=f'taua'),'dx')'
rc=datachk(za)
if(rc != 0) 
'za=re2(zg.2(ens=f'taua'),'dx')'
rc=datachk(za)
endif

'zaa=za-zc'
'zfa=zf-zc'
'ze=zf-za'

'd scorr(zfa,zaa,lon=0,lon=360,lat=20,lat=80)'
card=sublin(result,1)
ac=subwrd(card,4)
print 'AC 'ac' 'card

return

'set mpvals -290 70 15 90'
'set mproj nps'
'set mpdset mres'

'set cint 60'
'set black -60 60'
'set gxout shaded'
'set gxout grfill'
'set rbrange -300 300'
'set csmooth on'
'd maskout(maskout(zgaa,lt1-20),80-lt1))'
'cbarn'

'q pos'
'c'
'set gxout contour'
'set cint 60'
'set cthick 5'
'd zgfa-zgaa'

return



function wmoarea(name)

if(name = 'nhem')
  lat1=20
  lat2=90
  lon1=0
  lon2=360
endif

if(name = 'shem')
  lat1=-90
  lat2=-20
  lon1=0
  lon2=360
endif

if(name = 'tropics')
  lat1=-20
  lat2=20
  lon1=0
  lon2=360
endif

if(name = 'namerica')
  lat1=25
  lat2=60
  lon1=180+50
  lon2=180+145
endif

if(name = 'europe')
  lat1=25
  lat2=70
  lon1=-10
  lon2=28
endif

if(name = 'asia')
  lat1=25
  lat2=65
  lon1=60
  lon2=145
endif

if(name = 'ausnz')
  lat1=-55
  lat2=-10
  lon1=90
  lon2=180
endif


rc=lat1' 'lat2' 'lon1' 'lon2

return(rc)
