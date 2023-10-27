function main(args)

case=subwrd(args,1)

exp='awkk'
expa='108'
dtg='1987090700'

'open fld.tcbog.ctl'
'open tcbog.ctl'
'open fld.tcbog.full.ctl'
'open /scratch/ma/erf/tcanal/108.an.10.87090700.ctl'


'set mpdset hires'
'set map 15 0 6'

if(case = wpac)
'set lat 0 30'
'set lon 115 175'
exptle=exp' N16 (T21) 6-h FG 'dtg' -- WESTPAC'
exptlef=exp' N120 (T159) 6-h FG 'dtg' -- WESTPAC'
exptlea=expa' ANAL with TCBOG 'dtg' -- WESTPAC'
endif

if(case=lant)
'set lat 5 35'
'set lon -65 -10'
exptle=exp' N16 (T21) 6-h FG 'dtg' -- LANT'
exptlef=exp' N120 (T159) 6-h FG 'dtg' -- LANT'
exptlea=expa' ANAL with TCBOG 'dtg' -- LANT'
endif

scint=1
m2kt=1.84

dobog=1
if(dobog) 
'set gxout stream'
'set strmden 5' ; 'set cint 'scint
'set rbrange 0 12'
'd ua.3;va.3;mag(ua.3,va.3)'
'cbarn'

'set gxout stnmark'
'set ccolor 1'
'set cmark 3'
'd const(uf.2,0)'

'set gxout vector'
'set arrscl 0.75 10'
'set arrowhead -0.25'
'set ccolor 1'
'd uf.2;vf.2'
'draw title 'exptlef' \ N16 FG at bogus TC points'
pull cmd

'c'

'set gxout stream'
'set strmden 3' ; 'set cint 'scint
'set rbrange 0 12'
'd ua;va;mag(ua,va)'
'cbarn'

'set gxout stnmark'
'set ccolor 1'
'set cmark 3'
'd const(uf.2,0)'

'set gxout vector'
'set arrscl 0.75 10'
'set arrowhead -0.25'
'set ccolor 1'
'd uf.2;vf.2'
'draw title 'exptle' \ N16 FG at bogus TC points'
pull cmd

'c'
'set gxout stream'
'set strmden 3' ; 'set cint 'scint
'set rbrange 0 12'
'd ua;va;mag(ua,va)'
'cbarn'

'set gxout vector'
'set arrscl 0.75 10'
'set arrowhead -0.25'
'set ccolor 2'
'd um.2;vm.2'
'draw title 'exptle' \ TC motion (red)'
pull cmd

'c'
'set gxout stream'
'set strmden 3' ; 'set cint 'scint
'set rbrange 0 12'
'd ua;va;mag(ua,va)'
'cbarn'

'set gxout vector'
'set arrscl 0.75 10'
'set arrowhead -0.25'
'set ccolor 3'
'd ufb.2;vfb.2'
'draw title 'exptle' \ FG & Bias Correction'
pull cmd

'c'
'set gxout stream'
'set strmden 3' ; 'set cint 'scint
'set rbrange 0 12'
'd ua;va;mag(ua,va)'
'cbarn'

'set gxout vector'
'set arrscl 0.75 10'
'set arrowhead -0.25'
'set ccolor 2'
'd uf.2;vf.2'
'set ccolor 1'
'd ufc.2;vfc.2'
'draw title 'exptle' \ FG (red) & Env (white) [bias-corrected FG]'
pull cmd


'c'
'set gxout stream'
'set strmden 3' ; 'set cint 'scint
'd ua;va;mag(ua,va)'
cbarn

'set gxout barb'
'set ccolor 2'
'd utr.2;vtr.2'
'set ccolor 1'
'd u.2;v.2'
'draw title 'exptle' \ TC Rankine Vortex (red) & Synthetic Obs (white) [TC + Env]'
pull cmd
endif


bfile='exp.fg.'case'.'dtg
giffile=bfile'.gif'
gmfile=bfile'.gm'
psfile=bfile'.ps'

'c'
'set gxout stream'
'set strmden 5' ; 'set cint 'scint
'set rbrange 0 12'
'd ua.3;va.3;mag(ua.3,va.3)'
cbarn

'set gxout barb'
'set ccolor 2'
'set cthick 6'
'd utr.2;vtr.2'
'set ccolor 1'
'set cthick 7'
'd u.2;v.2'
'draw title 'exptlef' \ TC Rankine Vortex (red) & Synthetic Obs (white) [TC + Env]'
'wi 'giffile
'enable print 'gmfile
'print'
'disable print'
'!gxps -c -i 'gmfile' -o 'psfile
pull cmd

bfile='exp.an.'case'.'dtg
giffile=bfile'.gif'
gmfile=bfile'.gm'
psfile=bfile'.ps'

'c'
'set gxout stream'
'set strmden 5' ; 'set cint 'scint
'set rbrange 0 12'
'set lev 1000'
'd uas.4;vas.4;mag(uas.4,vas.4)'
cbarn

'set gxout barb'
'set ccolor 1'
'set cthick 6'
'd u.2;v.2'
'draw title 'exptlea' \ TC Rankine Vortex (red) & Synthetic Obs (white) [TC + Env]'
'wi 'giffile
'enable print 'gmfile
'print'
'disable print'
'!gxps -c -i 'gmfile' -o 'psfile
pull cmd

return





