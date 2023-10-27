function main(args)

rc=gsfallow('on')
rc=const()

_area=subwrd(args,1)

* makebg.gs
*
* This script creates a background image that shows topographic texture
* It requires an OPeNDAP-enabled version of GrADS and also uses the external
* ImageMagick utility "composite" to merge the intermediate gif files
* see http://www.imagemagick.org for info on how to get this software

* Get the topographic data and define variables
#'sdfopen http://monsoondata.org:9090/dods/navytopo'

#if(_area = '') ; _area='tropwpac' ; endif

_prcdir='/w21/prc/fldanal'
_fm=3

_xsize=900
_ysize=_xsize*(3.0/4.0)

'set xsize '_xsize' '_ysize

'open /w21/dat/geog/navy/navytopo.ctl'
'open /w21/dat/geog/navy/navyh2o.ctl'
'open /w21/dat/geog/geo.1deg.ctl'

rc=setplot()
print  'qqqqqqqqqqqqqqq '_pareabd

rc=jaecol()
if(_pareabd != '') 
 'set parea '_pareabd
else
 'set parea 0.4 10.8 0.65 8.25'
endif
'set vpage 0.1 10.9 0.1 8.4'


'define shadow = hdivg(smth9(z),const(z,0))'

* Set colors
'set rgb 24   1   1   1'
'set rgb 25  16  16  16'
'set rgb 26  32  32  32'
'set rgb 30 222 222 222'
'set rgb 92 216 255 255'


* Set map characteristics
*'set mproj nps'
*'set mpvals -120 -76 25 50'  ;* Coordinates for the United States 


* Draw the shadow images
'c'
'set grads off'
'set gxout shaded'
'set xlint '_xlint
'set ylint '_ylint
'set clevs -0.015 -0.003 '
'set ccols 26 25 24 '
'set map 0 0 10'
'd shadow'
'set map 1 0 3'
'draw map'

'printim shadow1.gif gif x'_xsize' y'_ysize

'c'
'set grads off'
'set mpdraw off'
'set grid off'
'set xlab off'
'set ylab off'

#'set mpdraw on'
#'set grid on'
#'set xlint '_xlint
#'set ylint '_ylint

'set clevs 0.003 0.015'
'set ccols 24 25 26 '
'set map 1 0 3'
'd shadow'
'set map 1 0 3'
'draw map'

'printim  shadow2.gif gif x'_xsize' y'_ysize

'c'

'set grads off'
'set mpdraw on'
'set grid on'

'set xlint '_xlint
'set ylint '_ylint


lcol=90
ocol=91

'set gxout contour'
'set rgb 90 100 50 25'
'set rgb 91 10 20 85'
'set map 0 0 10'
'set cmin 100000'
'd orog.3(t=1)'

'basemap.2 L 'lcol' 1'
'basemap.2 O 'ocol' 1'

'set map 1 0 3'
'draw map'

'printim water.gif gif  x'_xsize' y'_ysize

donavyh2o=0
if(donavyh20=1)
* Draw the water mask
'c'
'set grads off'
'set clevs 50'
'set ccols 30 92'
'set ccols 90 91'
'd w.2'
'printim water.gif gif  x'_xsize' y'_ysize
endif

* Combine the images to create bg.gif
'!composite -compose plus water.gif shadow1.gif e1.gif'
'!composite -compose minus e1.gif shadow2.gif bg.gif'

* Create a copy in png format
'!convert bg.gif ../../plt/basemap/basemap.'_area'.topo.png'

* Clean up
'!rm -f shadow1.gif'
'!rm -f shadow2.gif'
'!rm -f water.gif'
'!rm -f e1.gif'
'!rm -f bt.gif'
'!rm -f bg.gif'

'quit'

return








function setplot()
*
*	read an input file for the plot parameters
*
fname=_prcdir'/../cfg/area.'_area'.cfg'

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
#
# create land-sea mask always for lterp
#  
  pland=50
  'ls=const(const(maskout(sftlf.'_fm'(t=1),sftlf.'_fm'(t=1)-'pland'),-1),0,-u)'

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

#
# do in modelvar.gsf vice here
#

#
# turn off lon fill since using "2" models
#
dollfill=0

 _ukfill=0

if(dollfill = 1)

  #
  # 20060814 -- fill accross error in ukm gempak interp
  #


  if(_model = 'ukm')
    if(_lon1< -20 & _lon2 > -20)
      _ukfill=1
    endif
    if(_lon1>=340 & _lon2 <350)
      _ukfill=1
    endif
    if(_lon1>=180 & _lon2 > 370 )
      _ukfill=1
    endif
  endif

  if(_model = 'cmc')
    if(_lon1< -0 & _lon2 > 0)
      _ukfill=1
    endif
    if(_lon1>=360 & _lon2 < 390)
      _ukfill=1
    endif
    if(_lon1>=180 & _lon2 > 360 )
      _ukfill=1
    endif
  endif

  _dlatfill=2.0
  if(_model = 'cmc' & _ukfill=1) ; _dlatfill=4.0 ; endif

endif


return

