function main(args)

rc = gsfallow(on)
rc = const()

rc=plotdims()
rc=plotarea(2,0.1,0,0.05,0.05)

print 'xxx '_xpl.1' '_xpr.1' '_ybt.1' '_ypt.1

'open /w21/prc/fldveri/fields.ctl'

_vmodel=gfs2
_vanl=gfs2
_vvar=zg
_vlev=500
_varea=nhem
_vbdtg=2014050918
_vtau=120

rc=getArea(_varea)

print 'QQQQ '_latb' '_late' '_lonb' '_lone
fcdtg=dtginc(_vbdtg,_vtau)
fcgtime=dtg2gtime(fcdtg)

print 'ffffff'fcgtime' 'fcdtg

'quit'

_vpg.1
'set lat '_latb' '_late
'set lon '_lonb' '_lone
'set lev '_vlev
'set time 'fcgtime
'set t 1'
'set mproj scaled'

'forecast=vf'
'analysis=va'
'diff=vf-va'
'anldiff=vfa-vaa'

'set gxout shaded'
'set rbrange -100 100'
'd vfa'
'run cbarn'
 
'set gxout contour'
'd forecast'

'draw title Forecast Verification'

'set map 0 1 8'
'draw map'
'set map 15 1 3'
'draw map'

_vpg.2


'set gxout shaded'
'set rbrange -100 100'
'd vaa'
'run cbarn'

'set gxout contour'
'd analysis' 

'draw title Analysis Verification'

_vpg.3

'set gxout shaded'
'set rbrange -100 100'
'd diff'
'run cbarn'

'set gxout contour'
'd forecast'

'draw title Difference Verification Analysis'

_vpg.4

'set gxout shaded'
'set rbrange -100 100'
'd anldiff'
'run cbarn'

'set gxout contour'
'd forecast'

'draw title Anomaly Difference Verification Analysis `3t`0='_vtau

ofile=_vmodel'-'_vanl'-'_vvar'-'_vlev'-'_varea'-'_vbdtg'-'_vtau'.png'

'gxyat -x 1048 -y 768 -r 'ofile

return

function getArea(area)

if(area = 'nhem')
_latb=20
_late=90
_lonb=0
_lone=360
endif

rc=latb' 'late' 'lonb' 'lone

return(rc)
