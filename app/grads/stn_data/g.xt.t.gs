function main(args)

'open stn.ctl'

'set x 1'
'set y 1'
'set lev 1000 100'

'collect 1 free'

oe='u(stid=dummy)'

nt=4
t=1
while(t<=nt)
  'set t 't
  'collect 1 'oe
  t=t+1
endwhile

#
#  set the xaxis to four time points
#
'set x 1 'nt


#
# set string with x labels
#

xlabs=''
t=1
while(t<=nt)
  if(t = nt)
    xlabs=xlabs' t't
  else
    xlabs=xlabs' t't' |'
  endif
  t=t+1
endwhile

'set xlabs 'xlabs

'set gxout grfill'
'd coll2gr(1,-u)'
'cbarn'

return

