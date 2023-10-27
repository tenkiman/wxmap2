function main(args)

rc=gsfallow('on')
rc=const()
i=1
ensemble=subwrd(args,i) ; i=i+1
doopen=subwrd(args,i) ; i=i+1

'set mpdset mres'

if(ensemble = 'eps')
  bdir='/storage3/nwp2/ecmwf/'ensemble
  ne=51
endif

if(ensemble = 'gefs')
  bdir='/storage3/nwp2/ncep/'ensemble
  ne=21

endif

bdtg=2008081400

if(doopen)

  n=0
  while(n<ne)
    fmt='%02.0f'
    rc=math_format(fmt,n)
    enum=e%rc
    path=bdir%'/'bdtg'/'enum'/'ensemble'.'bdtg'.'enum'.ctl'
    rc=ofile(path)
    
    print 'qqqq 'n' 'enum' 'path' 'fn.n
    n=n+1
  endwhile

endif

blat=-10
elat=60
blon=-140
elon=0

zglev=5860
zgcol=3
zgthk=3
zgstl=1
zgtau=96

zgdtg=dtginc(bdtg,zgtau)
zgtime=dtg2gtime(zgdtg)

print 'qqqqqqqqqqqqq 'zgdtg' 'zgtime' 'zgtau


'c'

'set lev 500'
'set lat 'blat' 'elat
'set lon 'blon' 'elon
'set time 'zgtime
'set ylint 10'
'set xlint 20'

if(ensemble = 'eps')
  t1='ECMWF EPS zg='zglev' m spaghetti bdtg: 'bdtg' tau: 'zgtau
endif

if(ensemble = 'gefs')
  t1='NCEP GEFS zg='zglev' m spaghetti bdtg: 'bdtg' tau: 'zgtau
endif


t2=ne' members'
n=0
while(n<ne)
  n=n+1
  'set dfile 'n
  'set clevs 'zglev
  zgcol=math_mod(n,16)
  'set ccols 'zgcol
  'set cthick 'zgthk
  'set cstyle 'zgstl 
  'set clab off'
  'd zg'

endwhile

'set map 1 0 8'
'draw map'

rc=toptitle(t1,t2,1.0,1,1)











return






