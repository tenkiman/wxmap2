function main(args)

*
*  Set color levels and indices for shading

'set rgb 20    0  29  29'
'set rgb 21    0  49  49'
'set rgb 22    0  69  69'
'set rgb 23    0  89  89'
'set rgb 24    0 109 109'
'set rgb 25    0 129 129'
'set rgb 26    0 149 149'
'set rgb 27    0 169 169'
'set rgb 28    0 189 189'
'set rgb 29    0 209 209'
'set rgb 30    0 229 229'
'set rgb 31    0 249 249'
'set rgb 32    0 209 255'
'set rgb 33    0 169 255'
'set rgb 34    0 129 255'
'set rgb 35    0  89 255'
'set rgb 36    0  49 255'
'set rgb 37   49   0 255'
'set rgb 38   89   0 255'
'set rgb 39  109   0 255'
'set rgb 40  149   0 255'
'set rgb 41  189   0 255'
'set rgb 42  209   0 255'
'set rgb 43  249   0 255'
'set rgb 44  255   0 209'
'set rgb 45  255   0 169'
'set rgb 46  255   0 129'
'set rgb 47  255   0  89'
'set rgb 48  255   0  49'
'set rgb 50   99   0  99'
'set rgb 51  159   0 159'
'set rgb 52  225   0 225'
'set rgb 53  205   0 255'
'set rgb 54  169   0 255'
'set rgb 55   99   0 255'
'set rgb 56    0   0 255'
'set rgb 57    0  79 255'
'set rgb 58    0 192 255'
'set rgb 59    0 255 255'
'set rgb 60    0 255 195'
'set rgb 61    0 255 179'
'set rgb 62    0 255  79'
'set rgb 63    0 255   0'
'set rgb 64  165 255   0'
'set rgb 65  205 255   0'
'set rgb 66  255 255   0'
'set rgb 67  255 205   0'
'set rgb 68  205 104   0'
'set rgb 69  255 102   0'
*
'set rgb 70  255   0   0'
'set rgb 71  225   0   0'
'set rgb 72  195   0   0'
'set rgb 73  165   0   0'
'set rgb 74  135   0   0'
'set rgb 75  105   0   0'
'set rgb 76   75   0   0'
*
'set rgb 81    0   0 255'
'set rgb 80    0 205   0'
'set rgb 67  255 205   0'
'set rgb 68  205 104   0'
'set rgb 69  255 102   0'


dy=0.6
dx=dy
xoff=1.2
j=1
icol=19
jmax=7
while(j<=jmax)
yb=0.7+(j-1)*1

i=1
while(i<=10)
  icol=icol+1
  y1=yb
  y2=y1+dy
  x1=(i-1)*(dx*1.5)+xoff
  x2=x1+dx
  xm=(x1+x2)*0.5
  ym=y1-0.2
  'set line 'icol
  'draw recf 'x1' 'y1' 'x2' 'y2
  'set strsiz 0.125'
  'set string 1 c 5'
  'draw string 'xm' 'ym' 'icol
  i=i+1 
endwhile
j=j+1
endwhile
'set strsiz 0.30'
'set string 1 c 8'
'draw string 5.5 8.2 NRL Colour Scheme'

return




