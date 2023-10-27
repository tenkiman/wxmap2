function main(args)

rc=gsfallow("on")

_xsiz=1024
_ysiz=768
disolvfrc=25

fh=ofile('dum.ctl')

rc=pcod()

fbase='pcod.'_stm'.'_dtg'.'_model

pngcone=fbase'.CONE.png'
pngbase=fbase'.BASE.png'
pngall=fbase'.ALL.png'
gmfile=fbase'.gm'
psfile=fbase'.ps'

'set mpdset hires'

lcol=90
ocol=91
pcol=94

'set rgb 90 100 50 25'
'set rgb 91 10 20 85'

'set rgb 93 100 100 100 10'

'set rgb 94 150 150 150 10'
'set rgb 94 50 50 50 5'
'set rgb 94 255 155 0'


#
# make cone graphic and make black/white transparent
#
rc=dpcodraw(0)
rc=dpcod(pcol)
rc=dpcodpng(pngcone)
rc=dpcodtrn(pngcone)
'q pos'

#
# now make everything but cone
#
rc=dpcodraw(1)
rc=dpcodsea(ocol)
rc=dpcodlnd(lcol)
rc=dpcodmap()

rc=dpcodbnd()
rc=dpcodfc()
rc=dpcodbt()
rc=dpcodgrd()
rc=dpcodtle()
rc=dpcodpng(pngbase)

#
# and dissolve cone into base
#
rc=dpcoddslv(pngcone,pngbase,pngall,disolvfrc)
'q pos'

#
# make print graphic
#
rc=dpcodraw(1)
rc=dpcodsea(ocol)
rc=dpcod(pcol)
rc=dpcodlnd(lcol)
rc=dpcodmap()

rc=dpcodbnd()
rc=dpcodfc()
rc=dpcodbt()
rc=dpcodgrd()
rc=dpcodtle()

rm=dpcodlpr(gmfile,psfile)

return



#------------------------ ffffffffffffffffffffffffffffffffffffffffffffffffffffffffff

function dpcodmap()
'set map 0 0 10'
'draw map'

'set map 1 0 3'
'draw map'
return


function dpcodraw(domap)

'c'
'set lat '_latmin' '_latmax
'set lon '_lonmin' '_lonmax

'set grads off'
'set ylint 5'
'set xlint 5'

if(domap = 0)
'set grid off'
'set xlab off'
'set ylab off'
'set map 0 0 0'
endif

'set cmax -1000'
'd lat'

return


function dpcoddslv(pngcone,pngbase,pngall,disolvfrc)
'!composite -dissolve 'disolvfrc' 'pngcone' 'pngbase' 'pngall
return


function dpcodpng(pngfile)
'printim 'pngfile' x'_xsiz' y'_ysiz
return

function dpcodtrn(pngfile)
# -- can't use opengrads 'grads' srcript on the mac -- sets libfontconfig
#
'!convert -transparent black 'pngfile' 'pngfile
'!convert -transparent white 'pngfile' 'pngfile
return



function dpcodsea(ocol)
#
# draw sea
#
'basemap.2 O 'ocol' 1 '
return

function dpcodlnd(lcol)
#
# draw the land
#
'basemap.2 L 'lcol' 1 '
return


function dpcodgrd()

#
# draw the map
#
'set map 0 1 6'
'draw map'

'set map 1 1 2'
'draw map'


'set ylint 1'
'set xlint 1'
'set grid on 3 0 4'
'set xlopts 1 0 0'
'set ylopts 1 0 0'
'set cmax -1000'
'd lat'

'set ylint 1'
'set xlint 1'
'set grid on 3 93 4'
'set xlopts 1 0 0'
'set ylopts 1 0 0'
'set cmax -1000'
'd lat'

'set ylint 5'
'set xlint 5'
'set grid on 1 0 10'
'set xlab on'
'set ylab on'
'set cmax -1000'
'd lat'

'set grid on 1 1 3'
'set cmax -1000'
'd lat'

return


function dpcodlpr(gmfile,psfile)
  'enable print 'gmfile
  'print'
  'disable print'
print 'psfile 'psfile
  '!gxps -c -i 'gmfile' -o 'psfile
return


function dpcodtle()
  'draw title PCOD for '_model' '_stm' '_dtg
return



function dpcod(pcol)
#
# shade draw the pcod using polyf
#

polygon='polyf '
i=1
while (i <= _pcodn)
  lon=subwrd(_pcod.i,2)
  lat=subwrd(_pcod.i,1)
 'q w2xy 'lon' 'lat
  xp=subwrd(result,3)
  yp=subwrd(result,6)
  polygon=polygon' 'xp' 'yp
  i=i+1
endwhile

'set line 'pcol' 0 0'
print polygon
'draw 'polygon

return


function dpcodbnd()
#
# draw line around polygon
#


i=1
while (i <= _pcodn+1)

  im0=i
  im1=i-1
  if(i = _pcodn+1)
     im0=1
     im1=_pcodn
  endif

  lon=subwrd(_pcod.im0,2)
  lat=subwrd(_pcod.im0,1)

  'q w2xy 'lon' 'lat
  xp=subwrd(result,3)
  yp=subwrd(result,6)

  if( i > 1)

    lon0=subwrd(_pcod.im1,2)
    lat0=subwrd(_pcod.im1,1)
    'q w2xy 'lon0' 'lat0
    xp0=subwrd(result,3)
    yp0=subwrd(result,6)

   'set line 1 0 15'
   'draw line 'xp0' 'yp0' 'xp' 'yp

   'set line 0 0 5'
   'draw line 'xp0' 'yp0' 'xp' 'yp

  endif

#  mtype=3
#  msiz=0.05
# 'draw mark 'mtype' 'xp' 'yp' 'msiz
# 'q pos'

  i=i+1
endwhile

return


function dpcodfc()
i=1
while (i <= _fcn)

  'set line 3 0 8'

  lon=subwrd(_fc.i,2)
  lat=subwrd(_fc.i,1)
  'q w2xy 'lon' 'lat

  xp=subwrd(result,3)
  yp=subwrd(result,6)

  if( i > 1)
    im1=i-1
    lon0=subwrd(_fc.im1,2)
    lat0=subwrd(_fc.im1,1)
    'q w2xy 'lon0' 'lat0
    xp0=subwrd(result,3)
    yp0=subwrd(result,6)

   'draw line 'xp0' 'yp0' 'xp' 'yp

  endif


  mtype=3
  msiz=0.1
  'draw mark 'mtype' 'xp' 'yp' 'msiz

  i=i+1

endwhile

return


function dpcodbt()

i=1
while (i <= _btn)

  lon=subwrd(_bt.i,2)
  lat=subwrd(_bt.i,1)

  'q w2xy 'lon' 'lat
  xp=subwrd(result,3)
  yp=subwrd(result,6)

  'set line 2 0 8'

  if( i > 1)
    im1=i-1
    lon0=subwrd(_bt.im1,2)
    lat0=subwrd(_bt.im1,1)
    'q w2xy 'lon0' 'lat0
    print lon' 'lat' 'result
    xp0=subwrd(result,3)
    yp0=subwrd(result,6)
   'draw line 'xp0' 'yp0' 'xp' 'yp
  endif

  mtype=41
  msiz=0.25
  'draw wxsym 'mtype' 'xp' 'yp' 'msiz

  i=i+1

endwhile

return

