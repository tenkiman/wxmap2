function philo(args)

var=subwrd(args,1)
hlfmt=subwrd(args,2)
hlpcntl=subwrd(args,3)

'q gxinfo'
card=sublin(result,2)
pgx=subwrd(card,4)
pgy=subwrd(card,6)

card=sublin(result,3)
xlp=subwrd(card,4)
xrp=subwrd(card,6)

card=sublin(result,4)
ybp=subwrd(card,4)
ytp=subwrd(card,6)

*
*	defaults to philo
*
if(hlfmt='' | hlfmt='hlfmt') ; hlfmt='"i5"' ; endif
if(hlpcntl='' | hlpcntl = 'hlpcntl') ; hlpcntl='0.25' ; endif

*
*	plotting params
*
*	the mark
hlmk=1
hlmksiz=0.05
hlmkthk=0.05
hlmkcol=1

hlchoffx=0.0
hlchoffy=0.10

hlchsizl=0.10
hlchcoll=1
hlchthkl=6
hlchfntl=5

hlchsizh=0.10
hlchcolh=1
hlchthkh=6
hlchfnth=5

hlvlsiz=0.06
hlvlcol=1
hlvlthk=6

pcnth=1
pcntl=1

'!rm udf.grhilo.out'

'd grhilo('var','hlfmt','hlpcntl')'

rc=read(udf.grhilo.out)
card=sublin(rc,2)
iok=sublin(rc,1)
if(iok!=0) ; return; endif
nh=subwrd(card,1)
nl=subwrd(card,2)
rmgh=subwrd(card,3)
rmlh=subwrd(card,4)
rmgl=subwrd(card,5)
rmll=subwrd(card,6)

*
*	read and plot H's
*

i=1
while(i<=nh)
  rc=read(udf.grhilo.out)
  card=sublin(rc,2)
  iok=sublin(rc,1)
  chrhl.i=subwrd(card,1)
  lonhl.i=subwrd(card,2)
  lathl.i=subwrd(card,3)
  valhl.i=subwrd(card,4)
  grdhl.i=subwrd(card,5)
  lplhl.i=subwrd(card,6)
  i=i+1
endwhile

nhp=nint(nh*pcnth)
i=1
while(i<=nhp)

  if(lplhl.i >= rmlh)
  'q w2xy 'lonhl.i' 'lathl.i
  xhl=subwrd(result,3)
  yhl=subwrd(result,6)
  if( (xhl > xlp) & (xhl < xrp) & (yhl > ybp) & (yhl < ytp) ) 

  'set line 'hlmkcol
  'draw mark 'hlmk' 'xhl' 'yhl' 'hlmksiz

  xhlc=xhl+hlchoffx
  yhlc=yhl+hlchoffy

  'set string 'hlchcolh' c 'hlchthkh
  'set strsiz 'hlchsizh
  'draw string 'xhlc' 'yhlc' `'hlchfnth%chrhl.i

  xhlv=xhl-hlchoffx
  yhlv=yhl-hlchoffy

  'set string 'hlvlcol' c 'hlvlthk
  'set strsiz 'hlvlsiz
  'draw string  'xhlv' 'yhlv' 'valhl.i
 
  endif
  endif

  i=i+1

endwhile

*
*	read and plot L's
*

i=1
while(i<=nl)
  rc=read(udf.grhilo.out)
  card=sublin(rc,2)
  iok=sublin(rc,1)
  chrhl.i=subwrd(card,1)
  lonhl.i=subwrd(card,2)
  lathl.i=subwrd(card,3)
  valhl.i=subwrd(card,4)
  grdhl.i=subwrd(card,5)
  lplhl.i=subwrd(card,6)
  i=i+1
endwhile


nlp=nint(nl*pcntl)
i=1
while(i<=nlp)

  if(lplhl.i >= rmll) 

  'q w2xy 'lonhl.i' 'lathl.i

  xhl=subwrd(result,3)
  yhl=subwrd(result,6)

  if( (xhl > xlp) & (xhl < xrp) & (yhl > ybp) & (yhl < ytp) ) 

  'set line 'hlmkcol
  'draw mark 'hlmk' 'xhl' 'yhl' 'hlmksiz

  xhlc=xhl+hlchoffx
  yhlc=yhl+hlchoffy

  'set string 'hlchcoll' c 'hlchthkl
  'set strsiz 'hlchsizl
  'draw string 'xhlc' 'yhlc' `'hlchfntl%chrhl.i

  xhlv=xhl-hlchoffx
  yhlv=yhl-hlchoffy

  'set string 'hlvlcol' c 'hlvlthk
  'set strsiz 'hlvlsiz
  'draw string  'xhlv' 'yhlv' 'valhl.i

  endif
  endif

  i=i+1

endwhile


return
*
*-------------------------- nint ------------------
*
function nint(i0)
  i0=i0+0.5
  i=0
  while(i<12)
    i=i+1
    if(substr(i0,i,1)='.')
      i0=substr(i0,1,i-1)
      break
    endif
  endwhile
return(i0)

