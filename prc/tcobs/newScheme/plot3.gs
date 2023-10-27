"open /w21/dat/tc/obs/satwinds/new/tcobs.cira.2010062512.04e.IRWD.ctl"
"open grid.ctl"
"open obs.2010062512.04E.220.ctl"
"open obs.2010062512.04E.223.ctl"
"open obs.2010062512.04E.224.ctl"
"open obs.2010062512.04E.233.ctl"
"open obs.2010062512.04E.245.ctl"
"open obs.2010062512.04E.280.ctl"
"open obs.2010062512.04E.282.ctl"

"set timelab off"
"set grads off"

"set lev 700"
"set lat -1.59 27.59"
"set lon -131.52 -103.52"

"set gxout barb"
"set cthick 12"
"set ccolor 0"
"d uo.3(lev+300,lev-300)*1.94;vo.3(lev+300,lev-300)*1.94"
"set cthick 4"
"set ccolor 15"
"d uo.3(lev+300,lev-300)*1.94;vo.3(lev+300,lev-300)*1.94"

"set cthick 12"
"set ccolor 0"
"d uo.4(lev+300,lev-300)*1.94;vo.4(lev+300,lev-300)*1.94"
"set cthick 4"
"set ccolor 15"
"d uo.4(lev+300,lev-300)*1.94;vo.4(lev+300,lev-300)*1.94"

"set cthick 12"
"set ccolor 0"
"d uo.5(lev+300,lev-300)*1.94;vo.5(lev+300,lev-300)*1.94"
"set cthick 4"
"set ccolor 15"
"d uo.5(lev+300,lev-300)*1.94;vo.5(lev+300,lev-300)*1.94"

"set cthick 12"
"set ccolor 0"
"d uo.6(lev+300,lev-300)*1.94;vo.6(lev+300,lev-300)*1.94"
"set cthick 4"
"set ccolor 15"
"d uo.6(lev+300,lev-300)*1.94;vo.6(lev+300,lev-300)*1.94"

"set cthick 12"
"set ccolor 0"
"d uo.7(lev+300,lev-300)*1.94;vo.7(lev+300,lev-300)*1.94"
"set cthick 4"
"set ccolor 15"
"d uo.7(lev+300,lev-300)*1.94;vo.7(lev+300,lev-300)*1.94"

"set cthick 12"
"set ccolor 0"
"d uo.8(lev+300,lev-300)*1.94;vo.8(lev+300,lev-300)*1.94"
"set cthick 4"
"set ccolor 15"
"d uo.8(lev+300,lev-300)*1.94;vo.8(lev+300,lev-300)*1.94"

"set cthick 12"
"set ccolor 0"
"d uo.9(lev+300,lev-300)*1.94;vo.9(lev+300,lev-300)*1.94"
"set cthick 4"
"set ccolor 15"
"d uo.9(lev+300,lev-300)*1.94;vo.9(lev+300,lev-300)*1.94"

"gxyat test5.png"
