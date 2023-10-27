function main(args)

i=1
dtg=subwrd(args,i) ; i=i+1 
model=subwrd(args,i); i=i+1

if(model = 'fimx') ; model='FIMX' ; endif
if(model = 'fimy') ; model='FIMY' ; endif
if(model = 'fim')  ; model='FIM'  ; endif

rc=gsfallow(on)
rc=const()

'open fim8.'model'.grb1.ctl'
'open fim8.'model'.grb2.ctl'
'open ../../../climo/cmean/cmean_1d.ctl'

tauf=120
taua=000

dx=2.5

dtgc='1959'substr(dtg,5,10)

gtime=dtg2gtime(dtg)
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
