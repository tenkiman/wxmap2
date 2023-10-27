function main(args)

rc=gsfallow('on')
rc=const()
rc=jaecol2a()

xsiz=1024
xsiz=900
ysiz=(xsiz*3.0)/4.0
'set xsize 'xsiz' 'ysiz

# change plev to 700 for tafb tropical wave analysis
# -- change to 925 for boundary layer
#
_plev=700
_plev=925

dtanal=6

i=1
_area=subwrd(args,i) ; i=i+1
dtg=subwrd(args,i) ; i=i+1
tau=subwrd(args,i) ; i=i+1
otau=subwrd(args,i) ; i=i+1

_model=subwrd(args,i) ; i=i+1
nwpdir=subwrd(args,i) ; i=i+1
tmpdir=subwrd(args,i) ; i=i+1


# -- set up bt
#
rc=settcbt()

# -- override _bttau from settcbt
#
_bttau=tau

if(_model = 'fim8' | _model = 'fv3g' | _model = 'fv3e') 
  dtanal=12
endif


dostrm=0

dtau=1
dotauloop=1
if(tau < 0) ; dotauloop=0 ; endif

if(dotauloop)
  btau=tau
  etau=otau
else
  btau=tau
  etau=tau
endif

bdtg=dtginc(dtg,tau)
bdtg0=substr(bdtg,1,8)%'00'

hh=substr(bdtg,9,2)
hplus=math_mod(hh,dtanal)
h6=math_int(hh/dtanal)
h06=h6*dtanal
h16=(h6+1)*dtanal

tau=btau
while (tau <= etau)

#
# find dtgs bracketing time
#
if(dotauloop = 0)

#
# going backwad so decrement the bdtg and set tau to 0 to indicate an analysis
#
  tau=0


  dtg0=dtginc(bdtg0,h06)
  dtg1=dtginc(bdtg0,h16)

  path0=nwpdir'/'dtg0'/'_model'.w2flds.'dtg0'.ctl'
  path1=nwpdir'/'dtg1'/'_model'.w2flds.'dtg1'.ctl'
  fh0=ofile(path0)
  fh1=ofile(path1)
if(fh0 = 0 | fh1 = 0)
print 'EEEEEEEEE no data for 'dtg0' 'dtg1
'quit'
endif

  vdtg=bdtg

  tau0=tau
  tau1=tau

#  print '------------mmmmmmmmmmmfile 'fh0' 'fh1' 'path0' 'path1

else

  path0=nwpdir'/'dtg'/'_model'.w2flds.'dtg'.ctl'
  path1=nwpdir'/'dtg'/'_model'.w2flds.'dtg'.ctl'
  fh0=ofile(path0)
  fh1=ofile(path1)
if(fh0 = 0 | fh1 = 0)
print 'EEEEEEEEE no data for 'dtg0' 'dtg1
'quit'
endif
#  print '------------oooooooooooofile 'fh0' 'fh1

  dtg0=dtg
  dtg1=dtg
  bdtg=dtg
  vdtg=dtginc(bdtg,tau)
  hplus=0
  tau0=tau
  tau1=tau

if(tau > 48)
  dtanal=12
endif

if(tau > 0)
  hplus=math_mod(tau,dtanal)
  t6=math_int(tau/dtanal)
  tau0=t6*dtanal
  tau1=(t6+1)*dtanal
endif


endif

'c'
#print 'pppppppp0 'path0
#print 'pppppppp1 'path1

ifact1=hplus/dtanal
ifact0=(1.0-ifact1)

#print 'tttttttttt 'tau0' 'tau1
#print 'iiiiiiiiii 'vdtg' 'ifact0' 'ifact1

'set lev '_plev
'set grads off'

ylinc=10
xlinc=10

if(_area = 'enso')
  xlinc=20
endif

'set xlint 'xlinc
'set ylint 'ylinc

rc=prwarea()

if(_blon < 0) ; _blon=360+_blon ; endif
if(_elon < 0) ; _elon=360+_elon ; endif

'set lon '_blon' '_elon
'set lat '_blat' '_elat

'set dfile 'fh0
'set t 1'


'pw0=prw.'fh0'(time+'tau0'hr)'
if(dostrm | dobarb)
  'u80=ua.'fh0'(time+'tau0'hr)'
  'v80=va.'fh0'(time+'tau0'hr)'
endif

'set dfile 'fh1
'set t 1'
'pw1=prw.'fh1'(time+'tau1'hr)'

if(dostrm | dobarb)
  'u81=ua.'fh1'(time+'tau1'hr)'
  'v81=va.'fh1'(time+'tau1'hr)'
endif

'pw=pw0*'ifact0' + pw1*'ifact1

if(dostrm | dobarb)
  'u8=u80*'ifact0' + u81*'ifact1
  'v8=v80*'ifact0' + v81*'ifact1
  'u8=u8*'_ms2kt
  'v8=v8*'_ms2kt
endif

'set gxout shaded'
'set rbrange 15 65'
'set clevs  15  20  25  30  35  40  45  50  55  60  65'
'set ccols 59 58  49  48  45  43  35  23  24  25  28  29'
'set cint 5'
'd pw'
'cbarn 0.8'

##rc=xy2llmap()

if(dostrm)
'set gxout stream'
'set strmden 5'
'set ccolor 0'
'set cthick 4'
'd u8;v8'
endif

if(dobarb)
bskip=5
if(_area = 'enso' | _model = 'gfs2'); bskip=10 ; endif
if(_area = 'enso'); bskip=16 ; endif
prwcut=30
dsiz0=0.04
if(_area = 'enso'); dsiz0=0.03 ; endif

'set gxout barb'
'set cthick 5'
'set ccolor 15'
'set digsiz 'dsiz0

'd maskout(u8,'prwcut'-pw);skip(v8,'bskip')'
'set ccolor 0'
'd maskout(u8,pw-'prwcut');skip(v8,'bskip')'
endif

ocol=91
'set rgb 90 100  50  25'
'set rgb 92 245 222 179'
'set rgb 91  10  20  85'
'set rgb 90 112 128 144'
'set rgb 90 119 136 153'

lcol=90
if(tau  > 0 & tau < 12) ; lcol=71 ; endif
if(tau >= 12 & tau < 24) ; lcol=72 ; endif
if(tau >= 24 & tau < 36) ; lcol=73 ; endif
if(tau >= 36 & tau < 48) ; lcol=74 ; endif
if(tau >= 48 & tau < 60) ; lcol=75 ; endif
if(tau >= 60 & tau < 72) ; lcol=76 ; endif
if(tau >= 72 & tau < 84) ; lcol=77 ; endif

#print 'lllllllllllllll 'lcol
'basemap.2 L 'lcol' 1'
'set mpdset mres'
'set map 0 0 4'
'draw map'

'set gxout contour'
'set grid on 3 0 4'
'set cmax -1000'
'd lat'
rc=plotdims()

fmt='%+03.0f'


if(tau <= 0)

'set clip '_xlplot' '_xrplot' '_ybplot' '_ytplot
rc=prwtcbt()
_btcoltc=3
_btcol=1
_btszscl=1.0

if(_area = 'enso') ; _btszscl=0.75 ; endif

rc=drawtcbt()
'set clip 0 '_pagex' 0 '_pagey
endif

if(tau >= 0 & dotauloop = 1) 

if(_area = 'enso') ; _ftszscl=0.75 ; endif
rc=prwtcft()
'set clip '_xlplot' '_xrplot' '_ybplot' '_ytplot
#
# get ft posits and draw
#
_tau=tau
_ftbcol=1
_ftfcol=4
rc=ftposits(tau,tau,dtau)
rc=drawtcft()
'set clip 0 '_pagex' 0 '_pagey
endif

if(dotauloop)
  vtau=tau*1.0
else
  vtau=otau*1.0
endif
otau=math_format(fmt,vtau)

if(_model = 'gfs2') ; tmodel='GFS 0.25`3.`0' ; endif
if(_model = 'fim8') ; tmodel='FIM8 0.5`3.`0' ; endif
if(_model = 'fv3g') ; tmodel='FV3 GF 0.5`3.`0' ; endif

t1=tmodel' PRW [mm]'

if(dobarb)
t1=tmodel' PRW [mm] + '_plev' winds [kt]'
endif

if(dostrm)
t1=tmodel' PRW [mm] + '_plev' flow'
endif


t2='BDTG: 'dtg' `3t`0= 'otau' h `4VDTG: 'vdtg
t3='runs 'dtg0'-'dtg1
t1col=1
t2col=1
t3col=1
scale=1.0

rc=toptitle(t1,t3,scale,t1col,t2col)
rc=stitle(t2,scale)

fmt='%03.0f'

# use the base dtg and set neg taus to mttt and fc as fttt
#
if(vtau < 0)
  ctau=math_format(fmt,vtau*-1.0)
  gname=tmpdir'/prw.'_model'.'dtg'.'_area'.m'ctau'.png'
  print 'MMMMM pnging: 'gname
else
  ctau=math_format(fmt,vtau*1.0)
  gname=tmpdir'/prw.'_model'.'bdtg'.'_area'.f'ctau'.png'
  print 'FFFFF pnging: 'gname
endif

'printim 'gname' x'xsiz' y'ysiz' png'

'q pos'
if(dotauloop = 0); 'quit' ; endif

tau=tau+dtau
endwhile

if(dotauloop = 1) ; 'quit' ; endif
return




function xy2llmap()

doshrink=0

if(doshrink)

_vpxb=0.1
_vpyb=0.1
_vpxe=10.9
_vpye=8.4

else

_vpxb=0.0
_vpyb=0.0
_vpxe=11.0
_vpye=8.5

endif

dxvp=_vpxe - _vpxb
dyvp=_vpye - _vpyb

'q gxinfo'
print result

rc=sublin(result,2)
dxs=subwrd(rc,4)
dys=subwrd(rc,6)

print 'sssssssss 'dxs' 'dys

rc=sublin(result,3)
xbs=subwrd(rc,4)
xes=subwrd(rc,6)

rc=sublin(result,4)
ybs=subwrd(rc,4)
yes=subwrd(rc,6)

'q xinfo'

rc=sublin(result,4)
dpx=subwrd(rc,4)
rc=sublin(result,5)
dpy=subwrd(rc,4)

print 'ppppppppp 'dpx' 'dpy
#
# ratio of pixels to real screen (rs)
#
dxrs=(dxs/dxvp)*11.0
dyrs=(dys/dyvp)*8.5

print 'rrrrrrrrrrr 'dxrs' 'dyrs
print 'sss2py 'dpy' 'dyrs

dyrs=dyrs
s2px=dpx/dxrs
s2py=dpy/dyrs

print 'spspspspsps 's2px' 's2py

pxoff=_vpxb*(dpx/dxs)
pyoff=_vpyb*(dpy/dys)


ndxs=2
ndys=2

dxsp=(xes-xbs)/ndxs
dysp=(yes-ybs)/ndys


bxoff=3
bxoff=0

byoff=3
byoff=0

print 'ssssssssssxxx 'nxs' 'xbs' 'xes' 'dxsp
print 'ssssssssssyyy 'nys' 'ybs' 'yes' 'dysp

xs=xbs
while(xs<=xes)
  ys=ybs
  while(ys<=yes)

    'q xy2w 'xs' 'ys

    lon=subwrd(result,3)
    lat=subwrd(result,6)
    xp=xs*s2px
    yp=ys*s2py

xp=xp+pxoff+bxoff
# 
# reverse
#
yp=yp+pyoff
yp=dpy-yp+byoff

    xp=math_nint(xp)
    yp=math_nint(yp)

    print 'qqqq xs: 'xs' 'ys' xp: 'xp' 'yp' ll: 'lon' 'lat

    ys=ys+dysp

  endwhile

  xs=xs+dxsp

endwhile

return
