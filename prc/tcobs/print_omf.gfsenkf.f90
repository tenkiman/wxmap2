program obfits_temp
 use readconvobs
 implicit none
 character*120 datapath
 character*10 datestring
 integer num_obs_tot,nanals,i,n,doall,NARGS,IARGC,obct
 real, dimension(:), allocatable :: hx,hxnobc,hxens
 real, dimension(:), allocatable :: obs
 real, dimension(:), allocatable :: err
 real, dimension(:), allocatable :: lon
 real, dimension(:), allocatable :: lat
 real, dimension(:), allocatable :: press
 real, dimension(:), allocatable :: time
 real, dimension(:), allocatable :: errorig
 integer, dimension(:), allocatable :: qc
 real                            :: tlat,tlat0,tlat1,dx,tlon,tlon0,tlon1,tp,tp0,tp1,dp
 real                            :: ob,er,ln,lt,prs
 integer, dimension(:), allocatable :: code
 character(len=20), dimension(:), allocatable :: obtype
 character(len=10) id
 character(len=3) charanal
 character                       :: ttype*3,ttype0*3
 character                       :: chartmp*5

logical ::foundob
 NARGS = IARGC()
IF (NARGS.NE.7) THEN 
   print*,'print_omf.gfsenkf lon lat pressure dx dp type (u,v,t,q)  doall (0 for  no)'
   STOP
ENDIF
call getarg(1,chartmp)
read(chartmp,'(f5.3)') tlon
call getarg(2,chartmp)
read(chartmp,'(f5.3)') tlat
call getarg(3,chartmp)
read(chartmp,'(f5.3)') tp
call getarg(4,chartmp)
read(chartmp,'(f5.3)') dx
call getarg(5,chartmp)
read(chartmp,'(f5.3)') dp
call getarg(6,ttype0)

if(len_trim(ttype0).eq.1) ttype='  '//ttype0
if(len_trim(ttype0).eq.2) ttype=' '//ttype0
if(len_trim(ttype0).eq.3) ttype=ttype0

call getarg(7,chartmp)
read(chartmp,'(I5)') doall
 print*,tlon,tlat,dx
 nanals=60
 allocate(hxens(nanals))
 open(9,form='formatted',file='dates.dat')
 read(9,'(a10)') datestring
 id = 'ensmean'
  !datapath = "/lfs1/projects/fim/ppegion/gfsenkf/"//datestring//"/"
  !datapath = "/lfs1/projects/fim/ppegion/gfsenkf/t254/cira_winds/diag/"//datestring//"/"
  !datapath = "/lfs1/projects/fim/whitaker/gfsenkf_t254/"//datestring//"/"
  !Slocum Test
  datapath = "/mnt/lfs1/projects/fim/slocum/gfsenkf_t254/"//datestring//"/"
 call get_num_convobs(datapath,datestring,num_obs_tot,id)
 allocate(hx(num_obs_tot),obs(num_obs_tot),err(num_obs_tot),lon(num_obs_tot),&
         lat(num_obs_tot),press(num_obs_tot),time(num_obs_tot),errorig(num_obs_tot),&
         hxnobc(num_obs_tot),qc(num_obs_tot),obtype(num_obs_tot),code(num_obs_tot))
 tlon0=tlon-dx
 tlon1=tlon+dx
 tlat0=tlat-dx
 tlat1=tlat+dx
 tp0=tp-dp
 tp1=tp+dp

 
 call get_convobs_data(datapath,datestring,num_obs_tot,hx,hxnobc,obs,err, &
           lon, lat, press, time, code, errorig, qc, obtype, id)
 foundob=.FALSE.
 obct=1
 do n=1,num_obs_tot
!!!    print*,n,press(n),obs(n),obtype(n),code(n)
    IF (lon(n) .GE. tlon0 .AND. lon(n) .LE. tlon1 .AND. abs(err(n)).LT.20.AND.lat(n) .GE. tlat0 .AND. lat(n).LT. tlat1 .AND. press(n).GT.tp0.AND.press(n).LT.tp1.AND.obtype(n).EQ.ttype) THEN
        write(*,FMT='(I5,7F10.3,a,I3)'),obct,hx(n),obs(n),err(n),lon(n),lat(n),press(n),qc(n),obtype(n),code(n)
        IF (doall.EQ.obct) THEN
           ob=obs(n)
           ln=lon(n)
           lt=lat(n)
           prs=press(n)
        ENDIF
        obct=obct+1
	foundob=.TRUE.
    ENDIF
 enddo
 IF (.NOT.foundob) THEN
  print*,'did not find an ob'
  STOP
ENDIF
IF (doall.EQ.0) STOP
do i=1,nanals
   write(charanal,FMT='(I3.3)') i
   id='mem'//charanal
 call get_convobs_data(datapath,datestring,num_obs_tot,hx,hxnobc,obs,err, &
           lon, lat, press, time, code, errorig, qc, obtype, id)
 obct=1
 do n=1,num_obs_tot
    IF (lon(n) .GE. tlon0 .AND. lon(n) .LE. tlon1 .AND. abs(err(n)).LT.20.AND.lat(n) .GE. tlat0 .AND. lat(n).LT. tlat1 .AND. press(n).GT.tp0.AND.press(n).LT.tp1.AND.obtype(n).EQ.ttype) THEN
        IF (doall.EQ.obct) THEN
           write(*,FMT='(6F10.5,a)') hx(n),obs(n),err(n),lon(n),lat(n),press(n),obtype(n)
           hxens(i)=hx(n)
        ENDIF
        obct=obct+1
    ENDIF
 enddo
ENDDO
open(33,file=trim(datapath)//'selected_'//ttype0//'_omf',form='unformatted')
write(33) hxens
write(33) ob
write(33) ln
write(33) lt
write(33) prs
close(33)
end program obfits_temp
