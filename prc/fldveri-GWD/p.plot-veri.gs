function main(args)

rc = gsfallow(on)
rc = const()

_vtype='midlat'
_vmodel=gfs2
_vanl=gfs2
_vvar=zg
_vlev=500
_varea=nhem
_vbdtg=2014050918
_vtau=120
_vscore=0.884



if(_vtype = 'midlat') ; playout=1 ; endif
if(_vtype = 'tropics') ; playout=0 ; endif

# page layout 1-landscape ; 0-portrait

# -- percent area plot
# -- 
pp=0.95
pytoff=0.25
pyboff=0.50
_stlscl=0.85
_ttlscl=1.0

rc=plotdims()
# -- located in /w21/app/grads/gslib/
rc=plotarea(2,pp,playout,pytoff,pyboff)
if(rc=0); 'quit' ; endif

# -- toptitles
tt2=_vmodel' run verified against '_vanl' analyses run dtg: '_vbdtg
tt1='WMO DMV AnoCorr: '_vscore' for: '_vvar' lev: '_vlev' area: '_varea

fvtau=math_format('%03.0f',_vtau)

bdir='/w21/dat/nwp2/ensFC/FIELDS/'_vbdtg
vfile=_vmodel'_'_vanl'.'_vvar'.'_vlev'.'_varea'.'_vbdtg'.f'fvtau'.ctl'
vpath=bdir'/'vfile

fv=ofile(vpath)

rc=getArea(_varea)

fcdtg=dtginc(_vbdtg,_vtau)
fcgtime=dtg2gtime(fcdtg)

'set lat '_latb' '_late
'set lon '_lonb' '_lone

'set clopts -1 4 0.075'
'set clskip 2'

'set mproj nps'
'set mpdset mres'
'set mpvals -290 70 '_latb' '_late

'set ylint 20'
'set xlint 30'

'set lev '_vlev

'set t 1'

fctitle='FC `3t`0= '_vtau' valid: 'fcdtg
rc=setParea(1)
rc=plotZg(vfa,vf,fctitle)

antitle='Veri AN `3t`0=0 valid: 'fcdtg
rc=setParea(2)
rc=plotZg(vaa,va,antitle)

rc=toptitle(tt1,tt2,_ttlscl,1,1,5,5)

_xmidp=_pagex*0.5
_ymidp=_ymid-(pyboff*0.5)

'cbarn 0.75  0 '_xmidp' '_ymidp 

ofile=_vmodel'-'_vanl'-'_vvar'-'_vlev'-'_varea'-'_vbdtg'-'_vtau'.png'

'gxyat -x 1048 -y 768 -r 'ofile

'quit'
return


function plotZg(var1,var2,stitle)

'set grads off'
'set timelab on'
'set gxout shaded'
'set cint 30'
'set black -30 30'
'set rbrange -180 180'
'd 'var1

'set gxout contour'

'set cint 60'
'set ccolor 0'
'set cthick 10'
'd 'var2

'set cint 60'
'set ccolor 1'
'set cthick 4'
'd 'var2

'set map 0 1 8'
'draw map'
'set map 3 1 3'
'draw map'

rc=stitle(stitle,_stlscl)

return



function getArea(area)

rc=0
if(area = 'nhem')
_latb=20
_late=90
_lonb=0
_lone=360
rc=1
endif

if(rc = 0)
print 'invalid area: 'area' in setParea()'
endif

return(rc)


function setParea(np)

'set parea '_xpl.np' '_xpr.np' '_ypb.np' '_ypt.np

_xmid=(_xpl.np+_xpr.np)*0.5
_ymid=_ypb.np+0.25

return