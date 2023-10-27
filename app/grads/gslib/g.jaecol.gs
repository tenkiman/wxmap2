function main(args)
rc=gsfallow(on)
#rc=jaecolw2()
#rc=jaecol()
rc=jaecol2bw()

dy=0.75
dy=0.65
dx=dy*1.25
xoff=1.0
yoff=0.25
j=1
icol=20
jmax=6
jmax=7

while(j<=jmax)
yb=yoff+(j-1)*1.15

i=1
while(i<=9)
  icol=20+10*(j-1)+i
  y1=yb
  y2=y1+dy
  x1=(i-1)*(dx*1.0)+xoff
  x2=x1+dx
  xm=(x1+x2)*0.5
  ym=y1-0.10
  'set line 'icol
  'draw recf 'x1' 'y1' 'x2' 'y2
  'set strsiz 0.1'
  'set string 1 c 5'
  'draw string 'xm' 'ym' 'icol
  i=i+1 
endwhile
j=j+1
endwhile
'set strsiz 0.20'
'set string 1 c 8'
#'draw string 5.5 8.2 jaecolw2.gsf colors'
'draw string 5.5 8.2 jaecol2.gsf colors'

pname='coltbl.jaecolw2'
pname='coltbl.jaecol2bw.pdf'

'gxyat 'pname
return


'enable print 'pname'.gm'
'print'
'disable print'
'!gxps -c -i 'pname'.gm -o 'pname'.ps'

return

