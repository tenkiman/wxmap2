t=1
tmax=11
while(t<=tmax)
 'set map 1 0 8'
 'set t 't
 'set gxout stnmark'
 'set cmark 5'
 'set rbrange 0 35'
 'set cint 2.5'
 'd mag(u,v)*1.94'
 'cbarn'
 'draw title t = 't
 'set gxout stream'
 'set strmden 5'
 'set ccolor 0'
 'set cthick 10'
 'd uas.2(t='t');vas.2(t='t')'
 'set rbrange 0 35'
 'set ccolor rainbow'
 'set cthick 5'
 'set cint 2.5'
 'd uas.2(t='t');vas.2(t='t');mag(uas.2(t='t'),vas.2(t='t'))*1.94'
 'set gxout contour'
 'set ccolor 0'
 'set cthick 10'
 'set clevs 15'
 'd mag(uas.2(t='t'),vas.2(t='t'))*1.94'
 'set ccolor 1'
 'set clevs 15'
 'set cthick 6'
 'd mag(uas.2(t='t'),vas.2(t='t'))*1.94'
 'q pos'
 'c'
 t=t+1
endwhile
