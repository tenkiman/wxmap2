function main(args)

rc=gsfallow('on')
rc=const()

'open /pcmdi/reanal/ecmwf/era40/fc/tcanal/1989/256.fc.e4.10.1989090612.ctl'
#'open /tmp/avn.10.2003041400.ctl'
'set gxout fwrite'
#'set fwrite -sq -le uv.850.dat'
#
# get the input 850 winds to do the filtering
#
'set fwrite uv.850.dat'
'set lev 850'
'set x 1 360'
'set y 1 181'
'd ua'
'd va'
'disable fwrite'

#
#  now get the fields to vortecomise
#
'set fwrite psl.dat'
'd ua(lev=850)'
'd va(lev=850)'
'd ua(lev=200)'
'd va(lev=200)'

#'d psl*0.01'
#'d ua(lev=200)-ua(lev=850)*'_ms2kt
#'d va(lev=200)-va(lev=850)*'_ms2kt
#'d ua'
#'d va'
#'disable fwrite'

'quit'
return
end