function rbtab(args)
  i=1
  red=255
  blue=255
  g=0
  glim=255

  inc.1=0
  inc.2=128
  inc.3=16
  inc.4=16
  inc.5=16
  inc.6=16
  inc.7=16
  inc.8=16
 
  while(i<=8)
    g=g+inc.i
    if(g>glim);g=glim;endif
    cn1=20+i
    cn2=37-i
    r=255
    b=255
    'set rgb 'cn1' 'r' 'g' 'g
    'set rgb 'cn2' 'g' 'g' 'b

*    say 'set rgb 'cn1' 'r' 'g' 'g
*    say 'set rgb 'cn2' 'g' 'g' 'b
   i=i+1
  endwhile
return

