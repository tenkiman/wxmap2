function main(args)
* Setup parameters
'open dum'
rc=butncons()
rc=colors()
***  MAIN LOOP  ***
while (1)
  rc=init()
  rc=clear()
  rc=menubar()
  while (1)
   'q pos'
    mbt=subwrd(result,5)
    wgt=subwrd(result,6)
    btn=subwrd(result,7)
    if(wgt=3)
      if(subwrd(result,8)=0)
        drw=subwrd(result,8)
      else
        drw=subwrd(result,7)%subwrd(result,8)
      endif
    endif
    if (drw=11); break; endif
    if (wgt>=0&mbt=1); rc=domenu(drw); drw=rc; endif
    if (_quit=1); break; endif
  endwhile
  if (_quit=1); break; endif
endwhile
'quit'
***  MAIN LOOP  ***

function butncons()
'q gxinfo'
  dum=sublin(result,2)
  _xpur=subwrd(dum,4)
  _ypur=subwrd(dum,6)
  _xpll=0.0
  _ypll=0.0
* Size of menu buttons
  _mbh=0.4
  _mbw=1.0 
* Size of submenu buttons
  _sbh=0.25
  _sbw=0.85
* Size of variable buttons
  _vbh=0.4
  _vbw=6.0
* Set border for frames and button
  _brd=0.02
  _brd=0.001
* Set menu names and submenus
  _menus=8
  _menu.1=' File |Reset |Save |Exit'
  _menu.2=' Images |VIS |IR |None'
  _menu.3=' Fronts |Cold |Warm |Occluded |Stationary |Trough'
  _menu.4=' Symbols |High |Low |Fog |Rain |Snow |Storm |Sunny'
  _menu.5=' Patterns |Cold Air Mass|Warm Air Mass|Safe Area|Hazardous Area|Jets'
  _menu.6=' Heights |Fronts |Symbols |Areas |Jets'
  _menu.7=' Options |Major Cities'
  _menu.8=' Help |How to |How to'
return

function clear()
'clear'
'set line 95'
'draw recf '_xpll' '_ypll' '_xpur' '_ypur
return

function colors()
*  Set colors
  cn = 128
  tl = 156
  br = 100
  bg = 25
  mb = 180
  dg = 76
*  Button colors: 90-center; 91-top,left; 92-bottom,right
  'set rgb 90 'cn' 'cn' 'cn
  'set rgb 91 'tl' 'tl' 'tl
  'set rgb 92 'br' 'br' 'br
  'set rgb 93 'mb' 'mb' 'mb
  'set rgb 94 'dg' 'dg' 'dg
  'set rgb 96 15 15 15'
*  Background color
  'set rgb 95 0 0 'bg
return

function domenu(drw)
 rc=menufix()
 if (drw=12|drw=13)
   if (drw=12); return; endif
   if (drw=13); _quit=1; return; endif
 endif
 if (drw>=21&drw<=23)
   if (drw=21); rc=redraw(1); endif
   if (drw=22); rc=redraw(2); endif
   if (drw=23); rc=redraw(0); endif
 endif
 if (drw>=31&drw<=59)
   str1='Click on map at desired positions'
   if (drw=31); str2=' of Cold front'; endif
   if (drw=32); str2=' of Warm front'; endif
   if (drw=33); str2=' of Occluded front'; endif
   if (drw=34); str2=' of Stationary front'; endif
   if (drw=35); str2=' of Trough'; endif
   str1='Click on map at desired position'
   if (drw=41); str2=' of High symbol'; endif
   if (drw=42); str2=' of Low symbol'; endif
   if (drw=43); str2=' of Fog symbol'; endif
   if (drw=44); str2=' of Rain symbol'; endif
   if (drw=45); str2=' of Snow symbol'; endif
   if (drw=46); str2=' of Storm symbol'; endif
   if (drw=47); str2=' of Sunny symbol'; endif
   str1='Click on map at desired perimeter'
   if (drw=51); str2=' of Cold air mass'; endif
   if (drw=52); str2=' of Warm air mass'; endif
   if (drw=53); str2=' of Safe area'; endif
   if (drw=54); str2=' of Hazardous area'; endif
   str1='Click on map at desired positions'
   if (drw=55); str2=' of Jet stream'; endif
   rc=tile(_xpll,_ypll,_xpur,_ypll+_mbh,90,91,92,1)
   rc=tile(_xpll+_brd,_ypll+_brd,_xpur-_brd,_ypll+_mbh-_brd,90,92,91,1)
   'set string 0 l'
   'set strsiz 0.15'
   'draw string '_xpll+0.5' '_mbh/2' 'str1%str2
 endif
 if (drw>=61&drw<=64)
   str1='Click buttons for desired height'
   if (drw=61); str2=' of Fronts'; endif
   if (drw=62); str2=' of Symbols'; endif
   if (drw=63); str2=' of Areas'; endif
   if (drw=64); str2=' of Jets'; endif
   rc=tile(_xpll,_ypll,_xpur,_ypll+_mbh,90,91,92,1)
   rc=tile(_xpll+_brd,_ypll+_brd,_xpur-_brd,_ypll+_mbh-_brd,90,92,91,1)
   'set string 0 l'
   'set strsiz 0.15'
   'draw string '_xpll+0.5' '_mbh/2' 'str1%str2
   rc=gethgt(drw-60); drw=0
 endif
 if (drw=0)
   rc=tile(_xpll,_ypll,_xpur,_ypll+_mbh,95,95,95,1)
   return   
 endif
return drw

function gethgt(n)
 xll=6.0
 xur=7.0
 xav=(xll+xur)/2
 yav=(_ypll+_mbh)/2
 yll=yav-_mbh/2+_brd
 yur=yav+_mbh/2-_brd
 bh=_mbh-_brd*4
'set string 0 c'
'set strsiz 0.15'
'set button 0 90 0 1 0 90 1 0 1'
 dn = ' <'; up = ' >'
 new=_hgt.n
'draw string 'xav+1.0' 'yav' meters'
 while (1) 
  'draw string 'xav' 'yav' '_hgt.
  'draw button 71 '_xpur-bh*3/2-_brd*3' 'yav+_brd' 'bh' 'bh' 'dn 
  'draw button 72 '_xpur-bh*1/2-_brd*3' 'yav+_brd' 'bh' 'bh' 'up 
  'q pos'
   btn=subwrd(result,7)
   nbr=subwrd(result,5)
   if ((btn!=71&btn!=72)|nbr<0)
     break
   else
     if(btn=71); new=new-1000; endif
     if(btn=72); new=new+1000; endif
   endif
   if (new < 0); new = 0; endif
   rc=tile(xll,yll+_brd*2,xur,yur-_brd*2,90,90,90,1)
  'draw string 'xav' 'yav' 'new
  _hgt.n=new
 endwhile 
return 

function init()
 _hgt.1=5000
 _hgt.2=2000
 _hgt.3=10000
 _hgt.4=30000
 _quit=0
return

function menubar()
 rc=tile(_xpll,_ypur-_mbh,_xpur,_ypur,90,93,94,1)
'set button 96 90 1 0 1 90 94 93 1'
 mby=_ypur-0.45*_mbh
 mbh=_mbh*1.0
 i=1; mbr=0
 while (i <= _menus)
   len=strlen(_menu.i,1)
   mbw=(len+2)*0.15
   mbr=mbr+mbw
   mbx=mbr-mbw/2+0.2
   if(i=_menus)
    mbr=_xpur-2*_brd
    mbx=mbr-mbw
   endif
   'draw dropmenu 'i' 'mbx' 'mby' 'mbw' 'mbh' '_menu.i
   i=i+1
 endwhile
 rc=menufix()
return

function menufix()
 mby=_ypur-0.45*_mbh
 mbh=_mbh*1.0
 i=1; mbr=1
 while (i <= _menus)
   len=strlen(_menu.i,1)
   mbw=(len+2)*0.15
   mbr=mbr+mbw
   mbx=mbr-mbw/2+0.2
   if(i=_menus)
    mbr=_xpur-2*_brd
    mbx=mbr-mbw
   endif
   'set line 90'
   xl=mbx-mbw/2
   xr=mbx+mbw/2
   'draw recf 'xl-2*_brd' 'mby-0.5*_mbh' 'xl+4*_brd' 'mby+0.5*_mbh-2*_brd
   'draw recf 'xr-2*_brd' 'mby-0.5*_mbh' 'xr+4*_brd' 'mby+0.5*_mbh-2*_brd
   i=i+1
 endwhile
 rc=tile(_xpll,_ypur-_mbh,_xpur,_ypur,90,93,94,0)
return

function redraw()
return

function strlen(list,l)
 str=subwrd(list,l)
 i=1
 while (chr != "")
   chr=substr(str,i,1)
   i=i+1
 endwhile
return i-2

function tile(x1,y1,x2,y2,cn,tl,br,fl)
 'set line 'cn
 if(fl=1)
   'draw recf 'x1' 'y1' 'x2' 'y2
 endif
  a=_brd; b=0.005; c=0
 'set line 'tl
  while (c<=a)
   'draw line 'x1+c' 'y1+c' 'x1+c' 'y2-c
   'draw line 'x1+c' 'y2-c' 'x2-c' 'y2-c
    c=c+b
  endwhile
  c=0
 'set line 'br
  while (c<=a)
   'draw line 'x1+c' 'y1+c' 'x2-c' 'y1+c
   'draw line 'x2-c' 'y1+c' 'x2-c' 'y2-c
    c=c+b
  endwhile
return

