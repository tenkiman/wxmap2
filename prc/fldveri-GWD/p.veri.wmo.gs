function main(args)

i=1
model=subwrd(args,i) ; i=i+1
vdtg=subwrd(args,i) ; i=i+1
tau=subwrd(args,i) ; i=i+1
vapath=subwrd(args,i) ; i=i+1
vfpath=subwrd(args,i) ; i=i+1
clpath=subwrd(args,i) ; i=i+1
odpath=subwrd(args,i) ; i=i+1

#
#  for debugging set prod=0
#

prod=1

w2path='wmo25.ctl'

otau=math_format('%03.0f',tau)

print 'qqq 'vdtg' 'model' 'vapath' 'vfpath' 'clpath' 'odpath' 'tau' 'otau


rc=gsfallow('on')
rc=const()

fa=ofile(vapath)
ff=ofile(vfpath)
fc=ofile(clpath)
fw=ofile(w2path)

'set dfile 'fc
rc=metadata1(n,n,1)

var='zg'
plev=500

vtime=dtg2gtime(vdtg)

#var='psl'
#plev='sfc'


na=3
areas='tropics nhem shem'

nv=10

if(model = 'cam' | model = 'cam_r2')
  varms='z500 psl u850 v850 maguva u200 v200 maguva uva uva'
  plevms='500 sfc  850  850    850  200  200    200 850 200'
endif
#
# do 200 wind in era40 fc
#
if(model = 'era40')
  nv=6
  varms='  zg psl  ua  va maguva uva'
  plevms='500 sfc 850 850    850 850'
  varcs=varms
  plevcs=plevms
else
  varms='  zg psl  ua  va maguva  ua  va maguva uva uva'
  plevms='500 sfc 850 850    850 200 200    200 850 200'
  varcs=varms
  plevcs=plevms
endif


i=1
j=1

while(i<=na)
  area=subwrd(areas,i)
  j=1
  while(j<=nv)
    varm=subwrd(varms,j)
    plevm=subwrd(plevms,j)
    varc=subwrd(varcs,j)
    plevc=subwrd(plevcs,j)

print 'asdfasdfasdfadsfasdfasdf 'varm

if(varm = 'uva' | varm = 'maguva')

#
# vector
#

if(model = 'cam' | model = 'cam_r2')
  if(plevm = 850)
    varum='u850'
    varvm='v850'
  endif
else
  varum='ua'
  varvm='va'
endif

varuc='ua'
varvc='va'

rc=makeuva(fa,varum,varvm,plevm,vtime,model)
rc=makeuvf(ff,varum,varvm,plevm,vtime,model)
rc=makeuvc(fc,varuc,varvc,plevc,vdtg)
rc=makel(fw)
'set dfile 'fw
if(plevm = 'sfc')
  'set z 0'
else
  'set lev 'plevm
endif
if(varm = 'uva')
'dfc=mag(fu-cu,fv-cv)' ; 'dac=mag(au-cu,av-cv)' ; 'dfa=mag(fu-au,fv-av)'
endif

if(varm = 'maguva')
'dfc=fw-cw' ; 'dac=aw-cw' ; 'dfa=fw-aw'
endif

acn=anomcorr(dfc,dac,area)
acau=anomcorr('au','fu',area)
acav=anomcorr('av','fv',area)
acaw=anomcorr('aw','fw',area)

if(varm = 'uva')
aca=0.5*acau + 0.5*acav
endif

if(varm = 'maguva')
aca=acaw
endif

rc=meanrms(dfa,area)
mean=subwrd(rc,1)
rms=subwrd(rc,2)


else

#
# scalar
#
rc=makea(fa,varm,plevm,vtime,model)
rc=makef(ff,varm,plevm,vtime,model)
rc=makec(fc,varc,plevc,vdtg)
rc=makel(fw)
'set dfile 'fw
if(plevm = 'sfc')
  'set z 0'
else
  'set lev 'plevm
endif
'dfc=f-c' ; 'dac=a-c' ; 'dfa=f-a'

acn=anomcorr(dfc,dac,area)
aca=anomcorr('a','f',area)
rc=meanrms(dfa,area)
mean=subwrd(rc,1)
rms=subwrd(rc,2)

endif



ocard=vdtg' 'model' 'tau' 'area' 'varc' 'plevm' 'acn' 'aca' 'mean' 'rms
print 'OOOOOOOOOO 'ocard
rc=write(odpath,ocard)

    j=j+1
  endwhile
  i=i+1
endwhile
  
if(prod=1) ; 'quit' ; endif

return


#ffffffffffffffffffff
# meanrms
#ffffffffffffffffffff

function meanrms(a,area)

rc=wmoarea(area)
lat1=subwrd(rc,1) ; lat2=subwrd(rc,2) ; lon1=subwrd(rc,3) ; lon2=subwrd(rc,4)
print 'llll 'lat1' 'lat2' 'lon1' 'lon2' 'rc

if(lon1 = 0 & lon2 = 360)
  'set x 1 144'
else
  'set lon 'lon1' 'lon2
endif

'set lat 'lat1' 'lat2

'set gxout stat'

'd 'a'*'a'*l'
card=sublin(result,10)
sumsqr=subwrd(card,2)

'd 'a'*l'
card=sublin(result,10)
sum=subwrd(card,2)

'd l'
card=sublin(result,10)
suml=subwrd(card,2)

'd sqrt('sumsqr'/'suml')'
card=sublin(result,8)
rms=subwrd(card,4)

'd 'sum'/'suml
card=sublin(result,8)
mean=subwrd(card,4)

return(mean' 'rms)


#ffffffffffffffffffff
# anomcorr
#ffffffffffffffffffff

function anomcorr(a,f,area)

verb=0
'set gxout stat'
rc=wmoarea(area)
lat1=subwrd(rc,1) ; lat2=subwrd(rc,2) ; lon1=subwrd(rc,3) ; lon2=subwrd(rc,4)

if(verb=1) ; print 'acacac 'area' 'lat1' 'lat2' 'lon1' 'lon2 ; endif

expr='d scorr('a','f',lon='lon1',lon='lon2',lat='lat1',lat='lat2')'
if(verb=1) ; print expr ; endif
expr
if(verb=1) ; print result ; endif
card=sublin(result,8)
rc=subwrd(card,4)

ac=math_format('%7.5f',rc)

return(ac)


#ffffffffffffffffffff
# makea - define verifying analysis
#ffffffffffffffffffff

function makea(fa,var,plev,vtime,model)
'set dfile 'fa
if(plev = 'sfc')
  'set z 0'
else
  'set lev 'plev
endif
'set time 'vtime
'set lat -90 90'
'set lon 0 360'
'a=regrid2('var',2.5)'
if(var='psl')
'a=a*0.01'
endif

print 'aaaaaaaaaaaa 'var' 'model
if(var = 'zg' & model = 'era40')
  'a=a/'_gravity
endif
return


#ffffffffffffffffffffvvvvvvvvvvvvvvvvvvvvvvvv
# makeuva - define verifying vector wind
#ffffffffffffffffffffuuuuuuuuuuuuuuuuuuuuuuuu

function makeuva(fa,varu,varv,plev,vtime,model)
'set dfile 'fa
if(plev = 'sfc')
  'set z 0'
else
  'set lev 'plev
endif
'set time 'vtime
'set lat -90 90'
'set lon 0 360'
'au=regrid2('varu',2.5)'
'av=regrid2('varv',2.5)'
'aw=mag(au,av)'

return

#ffffffffffffffffffffvvvvvvvvvvvvvvvvvvvvvvv
# makeuvf - define forecast vector wind
#ffffffffffffffffffffuuuuuuuuuuuuuuuuuuuuuuu

function makeuvf(ff,varu,varv,plev,vtime,model)
'set dfile 'ff
if(plev = 'sfc')
  'set z 0'
else
  'set lev 'plev
endif
'set time 'vtime
'set lat -90 90'
'set lon 0 360'
'fu=regrid2('varu',2.5)'
'fv=regrid2('varv',2.5)'
'fw=mag(fu,fv)'

return

#ffffffffffffffffffff
# makef - define forecast
#ffffffffffffffffffff

function makef(ff,var,plev,vtime,model)
'set dfile 'ff
if(plev = 'sfc')
  'set z 0'
else
  'set lev 'plev
endif
'set time 'vtime
'set lat -90 90'
'set lon 0 360'
'f=regrid2('var',2.5)'
if(var='psl')
'f=f*0.01'
endif
if(var = 'zg' & model = 'era40')
  'f=f/'_gravity
endif

return

#ffffffffffffffffffff
# makec - define climo
#ffffffffffffffffffff

function makec(fc,var,plev,vdtg)
'set dfile 'fc
'set lat -90 90'
'set lon 0 360'
if(plev = 'sfc') ; 'set z 0' ; endif
rc=bgdefmo(var,plev,vdtg,fc)
'c=regrid2(ffff,2.5)'
return

#ffffffffffffffffffffvvvvvvvvvvvvvvvvvvvvvvvvv
# makeuvc - define climo vector wind
#ffffffffffffffffffffuuuuuuuuuuuuuuuuuuuuuuuu

function makeuvc(fc,varu,varv,plev,vdtg)
'set dfile 'fc
'set lat -90 90'
'set lon 0 360'
'set lev 'plev
if(plev = 'sfc') ; 'set z 0' ; endif
rc=bgdefmo(varu,plev,vdtg,fc)
'cu=regrid2(ffff,2.5)'
rc=bgdefmo(varv,plev,vdtg,fc)
'cv=regrid2(ffff,2.5)'
'cw=mag(cu,cv)'

return

#ffffffffffffffffffff
# makel - define cos(lat) weight
#ffffffffffffffffffff

function makel(fw)
'set dfile 'fw
'set lat -90 90'
'set lon 0 360'
'l=cos(lat(t=1)*'_pi'/180.0)'
return


#ffffffffffffffffffff
# wmoarea - define lat/lon of standard wmo areas
#ffffffffffffffffffff

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
