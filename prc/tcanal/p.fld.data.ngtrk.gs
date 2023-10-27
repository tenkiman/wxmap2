function main(args)

rc=gsfallow('on')
rc=const()

n=1
dtg=subwrd(args,n) ; n=n+1
model=subwrd(args,n) ; n=n+1
dpath=subwrd(args,n) ; n=n+1
opath=subwrd(args,n) ; n=n+1

regrid=1
if(model='gfs' |  model='ngp'  |  model='ngp2' | model = 'fg4' | model = 'ukm' | model = 'ecm'  | model = 'cmc') 
  regrid=0
endif

dtau=12
etau=120

tau=0
it=1

rc=ofile(dpath)
if(rc=0)
  print 'unable to open 'dpath
  'quit'
endif

'set x 1 360'
'set y 1 181'

'set fwrite 'opath
'set gxout fwrite'

while(tau<=etau)

  cdtg=dtginc(dtg,tau)
  ctime=dtg2gtime(cdtg)
  print 'TTTTTTTTTTTTTT tau = 'tau' 'cdtg' 'ctime
  'set time 'ctime

  'set lon 0 359'
  'set lat -90 90'

  'us=uas'
  'vs=vas'

  if(regrid=1)

    'set lat -90 90'
    'set lon 0 360'
    'us=uas'
    'vs=vas'
#    'us=regrid2(us,1.0,1.0,bs)'
#    'vs=regrid2(vs,1.0,1.0,bs)'
    'us=re(us,360,linear,0.0,1.0,181,linear,-90,1.0,ba)'
    'vs=re(vs,360,linear,0.0,1.0,181,linear,-90,1.0,ba)'

  endif
 
#
# set undef to 0.0 for ngtrk.x app -- for ukm2 without pole points
#
  'us=const(us,0.0,-u)'
  'vs=const(vs,0.0,-u)'
  

#
#  do 850 vort vice sfc
#
  'set lon -1 361'
  'set lev 850'
  'vort=hcurl(ua,va)*1e5'

  if(regrid=1)
    'vort=re(vort,360,linear,0.0,1.0,181,linear,-90,1.0,ba)'
  endif

'vort=const(vort,0.0,-u)'
  
'set gxout fwrite'
'set lon 0 359'
'd us'
'd vs'
'd vort'

  tau=tau+dtau
endwhile


'disable fwrite'
'quit'

return
