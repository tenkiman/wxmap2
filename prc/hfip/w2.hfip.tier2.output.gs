function main(args)

rc=gsfallow(on)
rc=const()

regrid=0
batch=1

cnm='esrl'
comment='grib1 output for hfip tier2 2009 summer demo'

dataopt='hfip'
area='global'
area='lant'

dtau=6
etau=168
timeu='fminute'
#timeu='fhour'

outconv='grads_grib'
#outconv='grib_only'


i=1
bdtg=subwrd(args,i) ; i=i+1 
model=subwrd(args,i) ; i=i+1 
dpath=subwrd(args,i) ; i=i+1
opath=subwrd(args,i) ; i=i+1
if(i>=5) ; dataopt=subwrd(args,i) ; i=i+1 ; endif
if(i>=6) ; area=subwrd(args,i) ; i=i+1 ; endif

yyyy=substr(bdtg,1,4)
mm=substr(bdtg,5,2)*1
dd=substr(bdtg,7,2)*1
hh=substr(bdtg,9,2)*1


lofile=opath


#------------------------------ hfip
#
if(dataopt = 'hfip')

nvs=8

# variable name -- in table
svar.1='psl' ; svts.1='instant'
svar.2='pr'  ; svts.2='accum'
svar.3='prw' ; svts.3='instant'
svar.4='uas' ; svts.4='instant'
svar.5='vas' ; svts.5='instant'
svar.6='tas' ; svts.6='instant'
# -- brain dead req from dtc -- call skin tmp 'wtmp' - water temp... in lats.hfip.
svar.7='ts'  ; svts.7='instant'
svar.8='tads'; svts.8='instant'

# variable time statistic -- instant | accum | average


nvu=5

uvar.1='ua'
uvts.1='instant'

uvar.2='va'
uvts.2='instant'

uvar.3='ta'
uvts.3='instant'

uvar.4='tad'
uvts.4='instant'

uvar.5='zg'
uvts.5='instant'

nl=5
ulev.1=850
ulev.2=700
ulev.3=500
ulev.4=300
ulev.5=200

endif

#--------------------------------------------- tm tracker (gettrk.wjet.x)
#
if(dataopt='tmtrk')

nvs=3

# variable name -- in table

svar.1='psl'
svar.2='uas'
svar.3='vas'

# variable time statistic -- instant | accum | average
svts.1='instant'

nvu=3

uvar.1='ua'
uvts.1='instant'

uvar.2='va'
uvts.2='instant'

uvar.3='zg'
uvts.3='instant'

nl=3
ulev.1=850
ulev.2=700
ulev.3=500


endif




*************************
*
*11111111111111 open the GrADS grid data file -- a dummy data set which provides grid information
*
*************************

fd=ofile (dpath)
if(fd<=0) ; say 'no data file' ; 'quit' ; endif

*
*	get the meta data
*

rc=metadata(fd,'n')

'set_lats parmtab lats.hfip.table.txt'

'set_lats convention 'outconv
'set_lats calendar standard'


deltat=dtau
if(timeu='fminute') ; deltat=dtau*60 ; endif
'set_lats deltat 'deltat

'set_lats model "'model'"'
'set_lats center 'cnm
'set_lats comment "'comment'"'

'set_lats timeoption dim_env'

if(timeu = 'fhour')   ;  'set_lats frequency forecast_hourly'  ; endif
if(timeu = 'fminute') ;  'set_lats frequency forecast_minutes' ; endif

'set_lats create 'lofile
id_file=subwrd(result,5)
if(id_file<=0) ; say 'unable to create LATS output file 'lofile' sayoonara, baaaaby! ' ; 'quit' ; endif

'set_lats basetime 'id_file' 'yyyy' 'mm' 'dd' 'hh' 0 0'
#'set_lats basetime 'id_file' 2010 1 25 0 0 0'



#gggggggggggggggggggg -- grid

'set_lats gridtype linear'

if(area = 'lant')
  'set lon -105 -15'
  'set lat 0 50'
else
  'set x 1 '_nx.1
  'set y 1 '_ny.1
endif


# create a define a var for setting the grid -- lats_grid returns output from the re2 extension...

if(regrid > 0)
  'vargrid=re2('svar.1','regrid')'
else
  'vargrid='svar.1
endif

'set t 1'
'set yflip on'
'lats_grid vargrid'
id_grid=subwrd(result,5)
if(!id_grid) ; say 'unable to define the LATS GRID; sayoonara, baby' ; 'quit' ; endif

#llllllllllllllllllll -- levels

if(nvu > 0)
  lexpr='set_lats vertdim plev '
  l=1
  while(l<=nl)
     lexpr=lexpr' 'ulev.l
     l=l+1
  endwhile

# run the expression...
  lexpr
  id_vdim=subwrd(result,5)
  if(!id_vdim) ; print 'unable to set LATS vertdim using 'lexpr' sayoonara baaaaaaaby'; 'quit'; endif
endif

#vvvvvvvvvvvvvvvvvvvv -- variables -- surface

n=1
while(n<=nvs)
  'set_lats var 'id_file' 'svar.n' 'svts.n' 'id_grid' 0'
  id_svar.n=subwrd(result,5)
  if(!id_svar.n) ; print 'unable to define the LATS 'svar.n' n: 'n'; sayoonara, baby' ; 'quit' ; endif
  n=n+1
endwhile


#vvvvvvvvvvvvvvvvvvvv -- variables -- ua

n=1
while(n<=nvu)
print  'set_lats var 'id_file' 'uvar.n' 'uvts.n' 'id_grid' 'id_vdim
  'set_lats var 'id_file' 'uvar.n' 'uvts.n' 'id_grid' 'id_vdim
  id_uvar.n=subwrd(result,5)
  if(!id_uvar.n) ; print 'unable to define the LATS VAR 1; sayoonara, baby' ; 'quit' ; endif
  n=n+1
endwhile


#oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
#	output section
#	loop through time, sfc and ua variables 

btau=0

tau=btau
while(tau<=etau)

cdtg=dtginc(bdtg,tau)
gtime=dtg2gtime(cdtg)
print 'TTT tau: 'tau 'bdtg: 'bdtg' cdtg: 'cdtg' gtime: 'gtime

'set time 'gtime

ftim=tau

if(timeu='fhour')
  ftime=tau
  'set_lats fhour 'ftime
endif
if(timeu='fminute') 
  ftime=tau*60 
  'set_lats fminute 'ftime
endif

n=1

while(n <= nvs)

'set_lats write 'id_file' 'id_svar.n
id_write=subwrd(result,5)
if(!id_write) ; say 'unable to set up write for VAR 1; sayoonara, baby' ; 'quit' ; endif

if(regrid > 0)
  ovar='re2('svar.n','regrid')'
else
  ovar=svar.n
endif

if(svar.n = 'tads') ; ovar='dewpt(tas,hurs)' ; endif
'lats_data 'ovar

n=n+1
endwhile

n=1
while(n <= nvu)

  l=1
  while(l<=nl)
    'set_lats write 'id_file' 'id_uvar.n' 'ulev.l
    id_write=subwrd(result,5)
    if(!id_write) ; say 'unable to set up write for VAR 1; sayoonara, baby' ; 'quit' ; endif

var=uvar.n
'set lev 'ulev.l
if(uvar.n = 'tad') ; var='dewpt(ta,hur)' ; endif
if(regrid > 0)
  ovar='re2('var'),'regrid')'
else
  ovar=var
endif

   'lats_data 'ovar
    print 'result 'result

    l=l+1
  endwhile

  n=n+1
endwhile

tau=tau+dtau
endwhile

'set_lats close 'id_file

if(batch=1); 'quit' ; endif

return
