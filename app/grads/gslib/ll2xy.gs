lon1=140
lat1=0
lon2=180
lat2=40
'q ll2xy 'lon1' 'lat1
x1=subwrd(result,1)
y1=subwrd(result,2)
'q ll2xy 'lon2' 'lat2
x2=subwrd(result,1)
y2=subwrd(result,2)
say 'qqq 'x1' 'y1' 'x2' 'y2
'draw rec 'x1' 'y1' 'x2' 'y2
