*
*  Script to look at surface data
*
*  Open files
*
  _safile = ofile('/data/wx/grads/sa.ctl')
  _wxfile = ofile('/data/wx/grads/wx.ctl')
  _obfile = ofile('/data/wx/grads/sareps.ctl')

  if (_safile=0|_wxfile=0|_obfile=0) 
    say 'Error opening files'
    return
  endif
  'set dfile '_safile

*
*  Set Defaults 
*

  _mtype = 2
  _efact = 1
  'set t last'
  'set digsiz 0.08'
  'set dignum 0'
  'set stid off'
  'set grid off'

*  Set up rgb definitions

  rc = dorgb()
 
* 
*  Display loop.
*

  while (_mtype!=0)
    rc = domap()
    rc = quser()
  endwhile

  'set map auto'
  return
   
function domap()

  'clear'

  rc = area()

  if (_efact=3) 
    rc = domdl()
    return
  endif
  if (_mtype=1); rc=dotemp(); endif; 
  if (_mtype=2); rc=dowx(); endif; 
  if (_mtype=3); rc=dowind(); endif; 
  if (_mtype=4); rc=dodwpt(); endif; 
  if (_mtype=5); rc=dotend(); endif; 

*  Function to set up drawing area

function area()

  'set parea 0.2 10.8 1.5 8.0'
  if (_efact=1) 
    'set lon -150 -50'
    'set lat 10 70'
    'set mproj nps'
    'set mpvals -120 -75 25 53'
    'set mpdset nam'
    return
  endif
  if (_efact=2) 
    ltd = 5
    lnd = 8.5
  endif
  if (_efact=3)
    ltd = 1.5
    lnd = 2.6
  endif
  lonlo = _lon-lnd
  lonhi = _lon+lnd
  latlo = _lat-ltd
  lathi = _lat+ltd
  'set mpvals 'lonlo' 'lonhi' 'latlo' 'lathi
  lonlo = lonlo-5
  lonhi = lonhi + 5
  latlo = latlo - 5
  lathi = lathi + 5
  'set lat 'latlo' 'lathi
  'set lon 'lonlo' 'lonhi
  'set mproj nps'
  'set mpdset nam'
  return

*  Function to draw buttons and get user response

function quser()
  if (_efact<3) 
    'draw button 1 3.5 0.25 1 0.4 TS'
    'draw button 2 4.5 0.25 1 0.4 WX/SLP'
    'draw button 3 5.5 0.25 1 0.4 Wind'
    'draw button 4 6.5 0.25 1 0.4 DP'
    'draw button 5 7.5 0.25 1 0.4 Tend'
  endif
  'draw button 0 0.55 0.25 1 0.4 Quit'
  if (_efact>1) 
    'draw button 10 10.45 0.25 1 0.4 UnZoom'
  endif
    
  if (_efact=1); say 'Point and click to zoom'; endif;
  if (_efact=2)
    say 'Click with left button to zoom, right button to pan'
  endif
  if (_efact=3)
    say 'Click with left button for time series, right button to pan'
  endif
  'q pos'
  btn = subwrd(result,7)
  if (btn=-999) 
    x = subwrd(result,3)
    y = subwrd(result,4)
    mbtn = subwrd(result,5)
    'q gxinfo'
    rec = sublin(result,3)
    xlo = subwrd(rec,4)
    xhi = subwrd(rec,6)
    rec = sublin(result,4)
    ylo = subwrd(rec,4)
    yhi = subwrd(rec,6)
    if ( x>xlo & x<xhi & y>ylo & y<yhi) 
      if (_efact=3 & mbtn=1) 
        rc = timser(x,y)
      else
        'q xy2w 'x' 'y
        _lon = subwrd(result,3)
        _lat = subwrd(result,6)
        if (mbtn=1 | _efact=1) 
          _efact = _efact + 1
        endif
      endif
    endif
  else 
    if (btn=10) 
      _efact = _efact - 1
    else 
      _mtype = btn
    endif
  endif
  
  return

*  Following function draw various map types

function dowind ()

  if (_efact!=1) 
    'set dfile '_safile
    'set gxout stream'
    'set grads off'
    'set map 15 1 1'
    'set ccolor 11'
    'd us;vs'
    'set dfile '_obfile
    'set grads off'
    'set gxout barb'
    'set ccolor 71'
    'set cthick 1'
    'd us;vs'
    'draw title Surface Winds'
    'set gxout contour'
  else 
    'set gxout vector'
    'set ccolor 1'
    'set map 8 1 1 '
    'set dfile '_safile
    'set grads off'
    'd us;vs'
    'draw title Surface Winds (Knots)'
    'set gxout contour'
  endif
  rc = putdate()
  return

function dodwpt ()

  'set map 15 1 1 '
  'set dfile '_safile
  'set grads off'
  if (_efact=1) 
    'set clevs 55'
    'set ccols 0 17'
    'set gxout shaded'
    'd smth9(smth9(ds*9/5+32))'
    'set gxout contour'
    'set ccolor rainbow'
    'set cint 5'
    'd smth9(smth9(ds*9/5+32))'
  else
    'set cint 2'
    'd ds*9/5+32'
  endif
  'draw title Surface Dewpoints (F)'
  if (_efact!=1) 
    'set dfile '_obfile
    'set grads off'
    'd ds*9/5+32'
  endif
  rc = putdate()
  return

function dotemp ()

  if (_efact=1) 
    rc = natmap()
    return
  endif
  'set map 15 1 1 '
  'set dfile '_safile
  'set grads off'
  'set cint 2'
  'd ts*9/5+32'
  'draw title Surface Temperatures (F)'
  'set dfile '_obfile
  'set grads off'
  'd ts*9/5+32'
  rc = putdate()
  return

function dotend ()

  'set map 15 1 1 '
  'set dfile '_safile
  'set grads off'
  if (_efact=1) 
    'set cint 0.5'
    'd smth9(smth9(smth9(slp-slp(t-3))))'
  else
    'set cint 0.2'
    'd slp-slp(t-3)'
  endif
  'draw title 3hr Pressure Change (mb)'
  if (_efact!=1) 
    'set dfile '_obfile
    'set grads off'
    'd slp-slp(t-3)'
  endif
  rc = putdate()
  return

function dowx ()

  'set gxout fgrid'
  'set map 1 1 1 '
  'set fgvals  2 51 3 52 4 53 5 54 6 55 7 56 8 57 9 58 10 59 11 60 12 61 13 62'
  'set grads off'
  'set dfile '_wxfile
  'd wx'
  'set ccolor 70  '
  if (_efact=1) 
    'set cint 2 '
  else
    'set cint 1'
  endif
  'set gxout contour'
  'set cmax 99.5'
  'set grads off'
  'set clab forced'
  'set dfile '_safile
  'd smth9(slp - 900)'
  'set ccolor 70'
  if (_efact=1) 
    'set cint 2 '
  else
    'set cint 1'
  endif
  'set cmin -0.5'
  'set grads off'
  'd smth9(slp - 1000)'
  'draw title Current Isobars / Observed WX'
  'set strsiz 0.12 0.14'
  'set string 1 l '
  'set line 1 1 '
  'draw rec 0.7 1.2 1.0 1.4'
  'draw string 1.05 1.3 Clear, '
  'draw string 1.05 1.1 Scattered, '
  'draw string 1.05 0.9 or Missing'
  'set line 51 1'
  'draw recf 2.7 1.2 3.0 1.4'
  'draw string 3.05 1.3 Broken'
  'set line 52 1'
  'draw recf 2.7 0.95 3.0 1.15'
  'draw string 3.05 1.05 Overcast  '
  'set line 53 1'
  'draw recf 2.7 0.7 3.0 0.9'
  'draw string 3.05 0.8 Obscured ' 
  'set line 54 1'
  'draw recf 4.5 1.2 4.8 1.4'
  'draw string 4.85 1.3 Lght Rain '
  'set line 55 1'
  'draw recf 6.3 1.2 6.6 1.4'
  'draw string 6.65 1.3 Lght Snow '
  'set line 56 1'
  'draw recf 8.0 1.2 8.3 1.4'
  'draw string 8.35 1.3 Lght Freezing'
  'set line 57 1'
  'draw recf 4.5 0.95 4.8 1.15'
  'draw string 4.85 1.05 Mod Rain '
  'set line 58 1'
  'draw recf 6.3 0.95 6.6 1.15'
  'draw string 6.65 1.05 Mod Snow '
  'set line 59 1'
  'draw recf 8.0 0.95 8.3 1.15'
  'draw string 8.35 1.05 Mod Freezing'
  'set line 60 1'
  'draw recf 4.5 0.7 4.8 0.9'
  'draw string 4.85 0.8 Hvy Rain '
  'set line 61 1'
  'draw recf 6.3 0.7 6.6 0.9'
  'draw string 6.65 0.8 Hvy Snow '
  'set line 62 1'
  'draw recf 8.0 0.7 8.3 0.9'
  'draw string 8.35 0.8 Hvy Freezing'
  if (_efact!=1) 
    'set dfile '_obfile
    'set grads off'
    'set gxout wxsym'
    'set ccolor 0'
    'set cthick 12'
    'set digsiz 0.14'
    'd wx'    
    'set ccolor rainbow'
    'set cthick 3'
    'd wx'
    'set digsiz 0.08'
    'set gxout value'
  endif
  rc = putdate()
  return

function natmap ()

  'set dfile '_safile
  'set gxout shaded'
  set = 'set clevs -30 -25 -20 -15 -10 -5 0 5 10 15 20 25 30 35 '
  set = set%'40 45 50 55 60 65 70 75 80 85 90 95 100 105 110 115 120'
  set
  set = 'set ccols 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 '
  set = set%'35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50'
  set
  'set map 1 1 6'
  'set grads off'
  'd ts*9/5+32'
  'set ccolor 0'
  'set gxout contour'
  'set cstyle 3'
  'set clevs 32'
  'set grads off'
  'd ts*9/5+32'
  'set cint 5'
  'set ccolor 0'
  'set clab off'
  'set grads off'
  'set cstyle 1'
  'd ts*9/5+32'
  'set cint 10'
  'set ccolor 0'
  'set grads off'
  'set cstyle 1'
  'set clab on'
  'd ts*9/5+32'

  line = 19
  while (line<51) 
    'set line 'line' 1'
    x = (line-19)*'0.3'+'0.7'
    'draw recf 'x' 1.2 '%(x+'0.3')%' 1.4'
    line = line+1
  endwhile
  'set strsiz 0.12 0.14'
  'set string 1 bc 3'
  val = '-30'
  x = '1.0'
  while (val<125) 
    'draw string 'x' 0.95 'val
    val = val + 10
    x = x+'0.6'
  endwhile
  'draw title Current Surface Temperatures (F)'
  rc = putdate
  return

function domdl()
  
  'set parea 0.2 10.8 0.7 8.0'
  'set map 15 1 1'
  'set dfile '_obfile
  'set gxout model'
  'set digsiz 0.07'
  'set mdlopts dig3'
  'set grads off'
  'd us;vs;ts*9/5+32;ds*9/5+32;slp*10;(slp-slp(t-1))*10;cld;wx;vis'
  'draw title Current Observations'
  rc = putdate
  'set gxout value'
  return

function dorgb()
  'set rgb 17 0 120 0'
  'set rgb 19 176 160 192'
  'set rgb 20 160 144 176'
  'set rgb 21 144 128 160'
  'set rgb 22 128 112 144'
  'set rgb 23 144 96 160'
  'set rgb 24 160 64 176'
  'set rgb 25 176 32 192'
  'set rgb 26 160 32 208' 
  'set rgb 27 144 32 224'
  'set rgb 28 128 0 255'
  'set rgb 29 64 64 255'
  'set rgb 30 64 128 240'
  'set rgb 31 64 160 240'
  'set rgb 32 32 196 240'
  'set rgb 33 0 208 208'
  'set rgb 34 0 224 176'
  'set rgb 35 0 240 144'
  'set rgb 36 0 240 0'  
  'set rgb 37 160 240 0'
  'set rgb 38 212 240 60' 
  'set rgb 39 250 250 80'
  'set rgb 40 240 228 85' 
  'set rgb 41 228 196 85' 
  'set rgb 42 240 160 70'
  'set rgb 43 240 128 50'
  'set rgb 44 250 105 30'
  'set rgb 45 255 0 0'
  'set rgb 46 224 0 60'
  'set rgb 47 208 0 80'
  'set rgb 48 192 0 96'
  'set rgb 49 176 0 112'
  'set rgb 50 160 0 128'
  'set rgb 51 100 100 100 '
  'set rgb 52 120 120 120 '
  'set rgb 53 200 190 60 '
  'set rgb 54 50 150 70 '
  'set rgb 55 50 50 170'
  'set rgb 56 170 50 50 '
  'set rgb 57 70 210 70 '
  'set rgb 58 100 100 220'
  'set rgb 59 220 90 90 '
  'set rgb 60 90 245 90 '
  'set rgb 61 110 110 255'
  'set rgb 62 255 110 110 '
  'set rgb 70 255 220 140'
  'set rgb 71 255 255 130'
return

*  Function to reformat the GrADS date/time into something
*  more readable
 
function mydate
  'query time'
  sres = subwrd(result,3)
  i = 1
  while (substr(sres,i,1)!='Z')
    i = i + 1
  endwhile
  hour = substr(sres,1,i)
  isav = i
  i = i + 1
  while (substr(sres,i,1)>='0' & substr(sres,i,1)<='9')
    i = i + 1
  endwhile
  day = substr(sres,isav+1,i-isav-1)
  month = substr(sres,i,3)
  year = substr(sres,i+3,4)
  return (hour' 'month' 'day', 'year)

function putdate ()

  'q gxinfo'
  rec = sublin(result,3)
  x = subwrd(rec,4)
  rec = sublin(result,4)
  y = subwrd(rec,4)
  x = x + 0.02
  y = y + 0.02
  'set string 1 l 3'
  'set strsiz 0.15 0.16'
  'set line 0'
  'draw recf 'x' 'y' '%(x+2.5)%' '%(y+0.25)
  'draw string '%(x+0.05)%' '%(y+0.15)%' 'mydate()
  return

function timser (x,y)
  
  'set gxout findstn'
  'd ts;'x';'y
  stid = subwrd(result,1)
  lon = subwrd(result,2)
  lat = subwrd(result,3)
  'set parea 1.0 10.0 2.0 7.5'
  'set dfile '_obfile
  'set x 1'
  'set y 1'
  'set t 1 last'
  'clear'
  'set grid on'
  'd ts(stid='stid')*9/5+32'
  'draw title 'stid' 'lon' 'lat
  'q pos'
  'set t last'
  'set grid off'
  return

*
* Following function returns the file number given a descriptor
* file name.  The file is opened if necessary. 
*

function ofile (fname)
  'query files'
  i = 0
  while (1)  
    if (subwrd(result,1)='No')       
      ret = 0
      break;
    endif
    rec = sublin(result,i*3+2)
    if (rec='') 
      ret = 0;
      break; 
    endif
    if (subwrd(rec,2)=fname)
      rec = sublin(result,i*3+1)
      ret = subwrd(rec,2)
      break;
    endif
    i = i + 1
  endwhile
  if (ret=0) 
    'open 'fname
    if (rc>0) 
      say "Error opening "fname
      return (0)
    endif
    rec = sublin(result,2)
    ret = subwrd(rec,8)
  endif
  return (ret)
