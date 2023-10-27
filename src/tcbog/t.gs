
while(1)
'reinit'
'open tcbog.ctl'
'set gxout barb'
'set lev 1000'
u='utr*1.94'
v='vtr*1.94'
ut='u*1.94'
vt='v*1.94'
um='(utr+um)*1.94'
vm='(vtr+vm)*1.94'
'd 'u';'v
'q pos'
say result
x=subwrd(result,3)
y=subwrd(result,4)
'q xy2w 'x' 'y
print result
clon=subwrd(result,3)
clat=subwrd(result,6)
dlat=10
dlon=dlat*1.5
lat1=clat-dlat
lat2=clat+dlat
lon1=clon-dlon
lon2=clon+dlon
'set lat 'lat1' 'lat2
'set lon 'lon1' 'lon2
'c'
'set ccolor 1'
'd 'u';'v
'q pos'

'set ccolor 2'
'd 'ut';'vt
'q pos'

'set ccolor 3'
'd 'um';'vm
'q pos'

endwhile
