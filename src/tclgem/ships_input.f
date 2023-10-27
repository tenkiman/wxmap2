      MODULE ships_input
c-----7---------------------------------------------------------------72
c     This module contains the procedures needed to read in the various
c     available input files for SHIPS.
c
c     Needs: ships_util.f
c            aland.f
c
c     Parameters:
c        
c     SHIPS procedures:
c        subroutine readSCard()
c        subroutine readADeck()
c        subroutine readLSDiag()
c        subroutine readModel()
c     Utility procedures:
c        ???
c
c     Created:  27 Jul 2010 by Kate Musgrave
c     Modified: 31 Aug 2010 (KM) -adjusted for variable format modeldiag
c                                in readModel()
c               28 Oct 2010 (KM) -modified readADeck to allow ADeck EOF
c               29 Oct 2010 (KM) -modified readModel to deal with
c                                 missing vortex times (patchi, imiss)
C
C         20101014 -- (mf) mike fiorino add readCARQ subroutine to support simpler input
C         of tcvitals and more options for controling input
C
c-----7---------------------------------------------------------------72
c 
      USE ships_util
      include 'dataformats.inc'
      !also uses subroutines from dataio.f
      !also uses aland.f
c      IMPLICIT NONE
c 
      !the integer and real versions of missing data
c***      integer, parameter :: imiss = 9999
c***      real, parameter :: rmiss = 9999.
c 
      CONTAINS
c 
c-----7---------------------------------------------------------------72
c     subroutine readSCard
c-----7---------------------------------------------------------------72
      SUBROUTINE readSCard(luis,ierr,isyr,isyr4,ismon,isday,istime,
     +                     ilat0,ilatm12,ilon0,ilonm12,
     +                     ivmx0,ivmxm12,ihead,ispeed,
     +                     sname,natcf,natcf8)
c     This subroutine reads basic storm information, as well as 
c      available data at t=0 and t=-12 for initial calculations.
c 
c     ierr returns 1 if file not read in correctly
c 
      IMPLICIT NONE
c 
      !list calling variables
      integer, intent(in) :: luis
      integer, intent(out) :: ierr
      integer, intent(out) :: isyr
      integer, intent(out) :: isyr4
      integer, intent(out) :: ismon
      integer, intent(out) :: isday
      integer, intent(out) :: istime
      integer, intent(out) :: ilat0
      integer, intent(out) :: ilatm12
      integer, intent(out) :: ilon0
      integer, intent(out) :: ilonm12
      integer, intent(out) :: ivmx0
      integer, intent(out) :: ivmxm12
      integer, intent(out) :: ihead
      integer, intent(out) :: ispeed
      character(*), intent(out) :: sname
      character(*), intent(out) :: natcf
      character(*), intent(out) :: natcf8
c 
      !list local variables
      character(len=80) :: iline80
c 
      ierr = 0   !initialize error flag
c 
      !Read the stormcard file first
      read(luis,'(3(i2))') isyr,ismon,isday
      read(luis,'(i2)') istime
      read(luis,*) ilat0,ilatm12
      read(luis,*) ilon0,ilonm12
      read(luis,'(a80)') iline80
      read(luis,'(a80)') iline80
      read(luis,*) ivmx0,ivmxm12
      read(luis,*) ihead
      read(luis,*) ispeed
      read(luis,'(1x,a10)') sname
      read(luis,'(a6)') natcf
c 
      !Perform some limited data manipulation of stormcard data
c 
c     Calculate 4 digit year
      call yr2to4(isyr,isyr4)
c 
c     Calculate 8 character ATCF ID (with 4 digit year)
      natcf8(1:4) = natcf(1:4)
      write(natcf8(5:8),'(i4.4)') isyr4
c 
      return
c 
 1001 continue
      ierr = 1
c      write(*,*) 'Stormcard read failure'
      return
      END SUBROUTINE readSCard
c 
c-----7---------------------------------------------------------------72
c     subroutine readADeck
c-----7---------------------------------------------------------------72
      SUBROUTINE readADeck(luad,dtg,ierr,
     +                     isyr,isyr4,ismon,isday,istime,
     +                     ilat0,ilatm12,ilon0,ilonm12,
     +                     ivmx0,ivmxm12,ihead,ispeed,iper)
c-----7---------------------------------------------------------------72
c     Given the dtg specified by the model file, read in the
c     storm adeck (iadeck.dat), and grab the relevant data for 
c     t=-12hr, t=-6hr, and t=0hr from CARQ.
c
c     Calculate initial storm speed, heading, and persistence.
c
c     ierr returns 1 if file not read in correctly
c
c
c-----7---------------------------------------------------------------72
c 
      IMPLICIT NONE
c 
      integer, intent(in) :: luad
      character(*), intent(in) :: dtg
      integer, intent(out) :: ierr
      integer, intent(out) :: isyr,isyr4,ismon,isday,istime
      integer, intent(out) :: ilat0,ilatm12,ilon0,ilonm12
      integer, intent(out) :: ivmx0,ivmxm12
      integer, intent(out) :: ihead, ispeed, iper
c 
      real, parameter :: rmiss = 9999.
      integer, parameter :: mpt = 0
      integer :: result
      real :: templl, cxt, cyt, cmagt, head
      real, dimension(-2:mpt) :: tlat = rmiss, tlon = rmiss
      real, dimension(-2:mpt) :: ttime = (/-12.0,-6.0,0.0/)
      real, dimension(-2:mpt) :: cx, cy, cmag
      type (BIG_AID_DATA) :: tempDTG
      type (AID_DATA) :: tempCARQ
      type (A_RECORD) :: tempRecord
c 
c     initialize error flags
      ierr = 0
      result = 1
c 
      !read dtg to get storm dtg variables
      read(dtg,'(i4.4,3(i2.2))') isyr4,ismon,isday,istime
c 
      !Calculate 2 digit year from 4 digit year
      if (isyr4 .gt. 2000) then
         isyr = isyr4 - 2000
      else
         isyr = isyr4 - 1900
      endif
c 
      !finds all Aid for the given DTG
      call getBigAidDTG(luad,dtg,tempDTG,result)
      if (result .eq. 0) go to 1002
c 
      !narrows down to the CARQ at the given DTG
      call getTech(tempDTG,'CARQ',tempCARQ,result)
      if (result .eq. 0) go to 1002
c 
      !pulls the CARQ for t=-12
      call getAidTAU(tempCARQ,-12,tempRecord,result)
      if (result .eq. 0) go to 1002
      !set t=-12 variables here - lat, lon, vmax
      templl=tempRecord%lat
      if (tempRecord%NS .eq. 'S') templl = templl*(-1.0)
      tlat(-2) = templl
      ilatm12 = ifix(templl*10.0)
      templl=tempRecord%lon
      tlon(-2) = templl
      if (tempRecord%EW .eq. 'W') templl = templl*(-1.0)
c      tlon(-2) = templl
      ilonm12 = ifix(templl*10.0)
      ivmxm12 = tempRecord%vmax
c 
      !pulls the CARQ for t=-6
      call getAidTAU(tempCARQ,-6,tempRecord,result)
      if (result .eq. 0) go to 1002
      !set t=-6 variables here - lat, lon
      templl=tempRecord%lat
      if (tempRecord%NS .eq. 'S') templl = templl*(-1.0)
      tlat(-1) = templl
      templl=tempRecord%lon
      tlon(-1) = templl
      if (tempRecord%EW .eq. 'W') templl = templl*(-1.0)
c      tlon(-1) = templl
c 
      !pulls the CARQ for t=0
      call getAidTAU(tempCARQ,0,tempRecord,result)
      if (result .eq. 0) go to 1002
      !set t=0 variables here - lat, lon, vmax
      templl=tempRecord%lat
      if (tempRecord%NS .eq. 'S') templl = templl*(-1.0)
      tlat(0) = templl
      ilat0 = ifix(templl*10.0)
      templl=tempRecord%lon
      tlon(0) = templl
      if (tempRecord%EW .eq. 'W') templl = templl*(-1.0)
c      tlon(0) = templl
      ilon0 = ifix(templl*10.0)
      ivmx0 = tempRecord%vmax
c 
      !calculate persistence (= vmax(t=0) - vmax(t=-12))
      iper = ivmx0 - ivmxm12
c 
      !calculate heading and speed
      ihead=0
      ispeed=0
c 
      call tspdcal(tlat,tlon,ttime,mpt,rmiss,cx,cy,cmag)
c 
      cxt = 0.0
      cyt = 0.0
      cmagt = 0.0
c 
      if (cmag(-1) .lt. rmiss) then
         cxt = cx(-1)
         cyt = cy(-1)
         cmagt = cmag(-1)
      elseif (cmag(0) .lt. rmiss) then
         cxt = cx(0)
         cyt = cy(0)
         cmagt = cmag(0)
      endif
c 
      call ctorh(cxt,cyt,templl,head)
c 
      ispeed = ifix(cmagt + 0.49)
      ihead  = ifix(head  + 0.49)
c 
      !write out ADeck info for debugging
c      write(*,*) 'ilat0, ilatm12 = ', ilat0, ilatm12
c      write(*,*) 'ilon0, ilonm12 = ', ilon0, ilonm12
c      write(*,*) 'ivmx0, ivmxm12 = ', ivmx0, ivmxm12
c      write(*,*) 'ihead, ispeed = ', ihead, ispeed
c      write(*,*) 'iper = ', iper
c 
      return
c 
 1002 continue
      ierr = 1
c      write(*,*) 'ADeck read failure'
      return
      END SUBROUTINE readADeck

      SUBROUTINE readCARQ(luad,ierr,
     +                     isyr,isyr4,ismon,isday,istime,
     +                     ilat0,ilatm12,ilon0,ilonm12,
     +                     ivmx0,ivmxm12,ihead,ispeed,iper)


c-----7---------------------------------------------------------------72
C         target output:
C
C ilat0, ilatm12 =  272 253  
C ilon0, ilonm12 =  -617 -645
C ivmx0, ivmxm12 =  75 65
C ihead, ispeed =  55 16
C iper =  10  (ivmx0 - ivmxm12)
C
c-----7---------------------------------------------------------------72
c 
      IMPLICIT NONE

      integer, intent(in) :: luad
      character dtg*10

      integer, intent(out) :: ierr
      integer, intent(out) :: isyr,isyr4,ismon,isday,istime
      integer, intent(out) :: ilat0,ilatm12,ilon0,ilonm12
      integer, intent(out) :: ivmx0,ivmxm12
      integer, intent(out) :: ihead, ispeed, iper

      integer ios

C -- initialize error flags

      ierr = 0
 
C -- read dtg to get storm dtg variables
      
      read(luad,'(a10,1x,9(i5,1x))',iostat=ios) dtg,
     $     ilat0,ilon0,ilatm12,ilonm12,ivmx0,ivmxm12,ihead,ispeed,iper
      if(ios.ne.0) goto 1002

      read(dtg,'(i4.4,3(i2.2))') isyr4,ismon,isday,istime

      !Calculate 2 digit year from 4 digit year
      if (isyr4 .gt. 2000) then
         isyr = isyr4 - 2000
      else
         isyr = isyr4 - 1900
      endif

C -- write out CARQ info for debugging

      write(*,*) 'ilat0, ilatm12 = ', ilat0, ilatm12
      write(*,*) 'ilon0, ilonm12 = ', ilon0, ilonm12
      write(*,*) 'ivmx0, ivmxm12 = ', ivmx0, ivmxm12
      write(*,*) 'ihead, ispeed = ', ihead, ispeed
      write(*,*) 'iper = ', iper
      return
 
 1002 continue

      ierr = 1
      write(*,*) 'CARQ read failure'
      return
      END SUBROUTINE readCARQ

c 
c-----7---------------------------------------------------------------72
c     subroutine readLSDiag
c-----7---------------------------------------------------------------72
      SUBROUTINE readLSDiag(luls,mft,ierr,
     +                      ilyr,ilyr4,ilmon,ilday,iltime,
     +                      sname4,ivmx,iper,irlag,
     +                      ilat,ilon,idist,ivmaxb,
     +                      iu200,it200,it250,
     +                      iz850,id200,itwac,iepos,ipslv,irefc,
     +                      irhhi,irhmd,irhlo,
     +                      ishr,ishtd,ishdc,isddc,ishgc,
     +                      isst,irsst,iasst,irhcn,iphcn,
     +                      igoes,igoesm3,igoesxx,
     +                      ipenc,ivmpi2)
c     This subroutine reads the lsdiag.dat file and returns SHIPS
c      predictors listed in and derived from the model file.
c 
c     ierr returns 1 if file not read in correctly
c 
c     Input:  luls - file unit number for lsdiag.dat file
c             mft - number of time steps
c     Output:
c     Uses:
      IMPLICIT NONE
c 
      !list calling variables
      integer, intent(in) :: luls   !input file
      integer, intent(in) :: mft    !max # time steps
      integer, intent(out) :: ierr
      integer, intent(out) :: ilyr
      integer, intent(out) :: ilyr4
      integer, intent(out) :: ilmon
      integer, intent(out) :: ilday
      integer, intent(out) :: iltime
c 
c      character(*), intent(out) :: tmname
      character(*), intent(out) :: sname4
c      character(*), intent(out) :: sname
c      character(*), intent(out) :: natcf
c      character(*), intent(out) :: natcf8
c 
      integer, intent(out) :: ivmx
      integer, intent(out) :: iper
      integer, intent(out) :: irlag
c 
      integer, intent(inout), dimension(-2:mft) :: ilat
      integer, intent(inout), dimension(-2:mft) :: ilon
      integer, intent(inout), dimension(0:mft) :: idist
      integer, intent(inout), dimension(0:mft) :: ivmaxb
c 
      integer, intent(inout), dimension(0:mft) :: iu200
      integer, intent(inout), dimension(0:mft) :: it200
      integer, intent(inout), dimension(0:mft) :: it250
c 
      integer, intent(inout), dimension(0:mft) :: iz850
      integer, intent(inout), dimension(0:mft) :: id200
      integer, intent(inout), dimension(0:mft) :: itwac
      integer, intent(inout), dimension(0:mft) :: iepos
      integer, intent(inout), dimension(0:mft) :: ipslv
      integer, intent(inout), dimension(0:mft) :: irefc
c 
      integer, intent(inout), dimension(0:mft) :: irhhi
      integer, intent(inout), dimension(0:mft) :: irhmd
      integer, intent(inout), dimension(0:mft) :: irhlo
c 
      integer, intent(inout), dimension(0:mft) :: ishr
      integer, intent(inout), dimension(0:mft) :: ishtd
c      integer, intent(inout), dimension(0:mft) :: ishrs
c      integer, intent(inout), dimension(0:mft) :: ishts
c      integer, intent(inout), dimension(0:mft) :: ishrg
c 
      integer, intent(inout), dimension(0:mft) :: ishdc
      integer, intent(inout), dimension(0:mft) :: isddc
      integer, intent(inout), dimension(0:mft) :: ishgc
c 
      integer, intent(inout), dimension(0:mft) :: isst
      integer, intent(inout), dimension(0:mft) :: irsst
      integer, intent(inout), dimension(0:mft) :: iasst
      integer, intent(inout), dimension(0:mft) :: irhcn
      integer, intent(inout), dimension(0:mft) :: iphcn
c 
      integer, intent(inout), dimension(0:mft) :: igoes
      integer, intent(inout), dimension(0:mft) :: igoesm3
      integer, intent(inout), dimension(0:mft) :: igoesxx
c 
      integer, intent(inout), dimension(0:mft) :: ipenc
      integer, intent(inout), dimension(0:mft) :: ivmpi2
c 
      !list local variables
      integer, parameter :: imiss=9999
c      real, parameter :: rmiss=9999.
c      integer, parameter :: mfx=20
      character(len=130) :: iline
      integer :: k   !counter
c 
c     Initialize variables
      ierr = 0
      iper = imiss
c 
c     Read header line
      read(luls,110) sname4,ilyr,ilmon,ilday,iltime,ivmx
  110 format(1x,a4,1x,3(i2),1x,i2,1x,i4)
c 
c     Calculate 4 digit year
      call yr2to4(ilyr,ilyr4)
c 
c     Read body section until 'LAST' line is reached
 1100 continue
      read(luls,111) iline
  111 format(a130)
c 
         select case (iline(117:120))
         case ('LAST') !finished with body, escape go to loop
            go to 1200
         !intensity-based predictors
         case ('DELV')
            read(iline,112) iper
  112       format(1x,i4)
         case ('VMAX')
            read(iline,116) (ivmaxb(k),k= 0,mft)
         !position-based predictors
         case ('LAT ')
            read(iline,114) (ilat(k),k=-2,mft)
  114       format( 1x,23(i4,1x))
         case ('LON ')
            read(iline,114) (ilon(k),k=-2,mft)
         case ('DTL ')
            read(iline,116) (idist(k),k=0,mft)
         !shear predictors
         case ('SHRD')
            read(iline,116) (ishr(k),k= 0,mft)
  116       format(11x,21(i4,1x))
         case ('SHDC')
            read(iline,116) (ishdc(k),k= 0,mft)
         case ('SDDC')
            read(iline,116) (isddc(k),k= 0,mft)
            !Convert isddc from heading to direction (save in ishtd)
            do k=0,mft
               if (isddc(k) .lt. imiss) then
                  ishtd(k) = 180 + isddc(k)
                  if (ishtd(k) .gt. 360) ishtd(k) = ishtd(k)-360
               endif
            enddo
         case ('SHGC')
            read(iline,116) (ishgc(k),k= 0,mft)
         !SST predictors
         case ('CSST')
            read(iline,116) (isst(k),k= 0,mft)
         case ('RSST')
            read(iline,117) (irsst(k),k= 0,mft),irlag
  117       format(11x,21(i4,1x),5x,i4)
         case ('AMS1')
            read(iline,117) (iasst(k),k= 0,mft)
         !ocean heat content predictors
         case ('RHCN')
            read(iline,116) (irhcn(k),k= 0,mft)
         case ('PHCN')
            read(iline,116) (iphcn(k),k= 0,mft)
         !IR predictors
         case ('IR00')
            read(iline,116) (igoes(k),k= 0,mft)
         case ('IRM3')
            read(iline,116) (igoesm3(k),k= 0,mft)
         case ('IRXX')
            read(iline,116) (igoesxx(k),k= 0,mft)
         !pressure level data predictors
         case ('U200')
            read(iline,116) (iu200(k),k= 0,mft)
         case ('T200')
            read(iline,116) (it200(k),k= 0,mft)
         case ('T250')
            read(iline,116) (it250(k),k= 0,mft)
         !storm calculated predictors
         case ('Z850')
            read(iline,116) (iz850(k),k= 0,mft)
         case ('D200')
            read(iline,116) (id200(k),k= 0,mft)
         case ('EPOS')
            read(iline,116) (iepos(k),k= 0,mft)
         case ('REFC')
            read(iline,116) (irefc(k),k= 0,mft)
         case ('PSLV')
            read(iline,116) (ipslv(k),k= 0,mft)
         case ('TWAC')
            read(iline,116) (itwac(k),k= 0,mft)
         !relative humidity predictors
         case ('RHLO')
            read(iline,116) (irhlo(k),k= 0,mft)
         case ('RHMD')
            read(iline,116) (irhmd(k),k= 0,mft)
         case ('RHHI')
            read(iline,116) (irhhi(k),k= 0,mft)
c*************** start add code, PrSEFoNe (1 FEB 2010, jpk)
         case ('PENC')
            read(iline,116) (ipenc(k),k= 0,mft)
         case ('VMPI')
            read(iline,116) (ivmpi2(k),k= 0,mft)
c*************** end add code, PrSEFoNe
         end select
c 
         go to 1100
 1200    continue
c 
      return
c 
 1004 continue
      ierr = 1
c      write(*,*) 'lsdiag read failure'
      return
      END SUBROUTINE readLSDiag
c 
c-----7---------------------------------------------------------------72
c     subroutine readModel
c-----7---------------------------------------------------------------72
      SUBROUTINE readModel(lumo,mft,ierr,
     +                     ilyr,ilyr4,ilmon,ilday,iltime,
     +                     tmname,sname4,sname,natcf,natcf8,
     +                     ivmx,
     +                     ilat,ilon,idist,ivmaxb,
     +                     iu200,it200,it250,
     +                     iz850,id200,itwac,iepos,ipslv,
     +                     irhhi,irhmd,irhlo,
     +                     ishrd,ishtd,ishrs,ishts,ishrg,
     +                     ishdc,isddc,ishgc,
     +                     isst,ihcn)
c     This subroutine reads a model diagnostic file and returns SHIPS
c      predictors listed in and derived from the model file.
c 
c     ierr returns 1 if file not read in correctly
c     ierr returns 2 if SST/OHC subroutines fail
c 
c     Input:
c     Output:
c     Uses: ships_util.f, aland.f
      IMPLICIT NONE
c 
      !list calling variables
      integer, intent(in) :: lumo   !input file
      integer, intent(in) :: mft    !max # time steps
      integer, intent(out) :: ierr  !error flag
      integer, intent(out) :: ilyr
      integer, intent(out) :: ilyr4
      integer, intent(out) :: ilmon
      integer, intent(out) :: ilday
      integer, intent(out) :: iltime
c 
      character(*), intent(out) :: tmname
      character(*), intent(out) :: sname4
      character(*), intent(out) :: sname
      character(*), intent(out) :: natcf
      character(*), intent(out) :: natcf8
c 
      integer, intent(out) :: ivmx
c 
      integer, intent(inout), dimension(-2:mft) :: ilat
      integer, intent(inout), dimension(-2:mft) :: ilon
      integer, intent(inout), dimension(0:mft) :: idist
      integer, intent(inout), dimension(0:mft) :: ivmaxb
c 
      integer, intent(inout), dimension(0:mft) :: iu200
      integer, intent(inout), dimension(0:mft) :: it200
      integer, intent(inout), dimension(0:mft) :: it250
c 
      integer, intent(inout), dimension(0:mft) :: iz850
      integer, intent(inout), dimension(0:mft) :: id200
      integer, intent(inout), dimension(0:mft) :: itwac
      integer, intent(inout), dimension(0:mft) :: iepos
      integer, intent(inout), dimension(0:mft) :: ipslv
c 
      integer, intent(inout), dimension(0:mft) :: irhhi
      integer, intent(inout), dimension(0:mft) :: irhmd
      integer, intent(inout), dimension(0:mft) :: irhlo
c 
      integer, intent(inout), dimension(0:mft) :: ishrd
      integer, intent(inout), dimension(0:mft) :: ishtd
      integer, intent(inout), dimension(0:mft) :: ishrs
      integer, intent(inout), dimension(0:mft) :: ishts
      integer, intent(inout), dimension(0:mft) :: ishrg
c 
      integer, intent(inout), dimension(0:mft) :: ishdc
      integer, intent(inout), dimension(0:mft) :: isddc
      integer, intent(inout), dimension(0:mft) :: ishgc
c 
      integer, intent(inout), dimension(0:mft) :: isst
      integer, intent(inout), dimension(0:mft) :: ihcn
c 
      !list local variables
c 
      integer, parameter :: imiss=9999
      real, parameter :: rmiss=9999.
      integer, parameter :: mfx=20
c 
      integer, parameter :: idelt = 6          !time interval
      real, parameter :: delt = float(idelt)   ! between data points
c 
      integer :: ireadsound, ireadopt !flags for sections read in
      integer :: iexmsst             !flag for whether model SST provided
      integer :: iexmhcn             !flag for whether model OHC provided
      integer :: ibas                !basin selector, 1=Atl, 2=EPac/CPac
      integer :: ierrc, ierrf        !error flag from ohcclim
      real :: chcn                   !temp holder for clim OHC at one time
      integer :: ntime
      character(len=80) :: iline80   !blank line
      character(len=142) :: ilinem   !temp line for data retrieval
                                     !142 = 6*(mft+1)+16
      character(len=13) :: cfmtstri  !format spec for int
      character(len=15) :: cfmtstrf  !format spec for real
      character(len=15) :: cfmtstrlon  !format spec for lon
      character(len=13) :: cfmtstrtmp  !format spec
      character(len=6) :: tempc
      character(len=3) :: bas          !basin file extension, 'atl' or 'pac'
c 
      real, dimension(-2:mfx) :: slat = rmiss, slon = rmiss
      integer, dimension(0:mfx) :: imsst = imiss
      real, dimension(0:mfx) :: msst = rmiss
      integer, dimension(0:mfx) :: imhcn = imiss
      real, dimension(0:mfx) :: mhcn = rmiss
c 
      !not currently sent back to ships
      integer, dimension(0:mfx) :: itime = imiss
      integer, dimension(0:mfx) :: irmw = imiss
      integer, dimension(0:mfx) :: imslp = imiss
      integer, dimension(0:mfx) :: ispd = imiss
      integer, dimension(0:mfx) :: ihdg = imiss
      integer, dimension(0:mfx) :: itpw = imiss
      integer, dimension(0:mfx) :: it150 = imiss
      integer, dimension(0:mfx) :: it000 = imiss
      integer, dimension(0:mfx) :: ir000 = imiss
      integer, dimension(0:mfx) :: iz000 = imiss
      integer, dimension(0:mfx) :: ie000 = imiss
      integer, dimension(0:mfx) :: iepss = imiss
      integer, dimension(0:mfx) :: ienss = imiss
      integer, dimension(0:mfx) :: ieneg = imiss
      integer, dimension(0:mfx) :: ipsfc = imiss
      integer, dimension(0:mfx) :: ishxu = imiss
      integer, dimension(0:mfx) :: ishxl = imiss
      integer, dimension(0:mfx) :: icsst = imiss   !need to add calc
      integer, dimension(0:mfx) :: ichcn = imiss
c      integer, dimension(0:mfx) :: iphcn = imiss   !need to add calc
      integer, dimension(0:mfx) :: iopt = imiss   !never used, dummy var
c 
      real, dimension(0:mfx) :: rtwac = rmiss
      real, dimension(0:mfx) :: rz850 = rmiss
      real, dimension(0:mfx) :: rd200 = rmiss
      real, dimension(0:mfx) :: rtpw = rmiss
      real, dimension(0:mfx) :: rshdc = rmiss
      real, dimension(0:mfx) :: rsddc = rmiss
      real, dimension(0:mfx) :: rshtd = rmiss
      real, dimension(0:mfx) :: rspd = rmiss, rhdg = rmiss
      real, dimension(-2:mfx) :: cxt = rmiss, cyt = rmiss
      real, dimension(-2:mfx) :: cmagt = rmiss, ftimec = rmiss
      real, dimension(0:mfx) :: rland = rmiss
c                                                                        
c     Variables for vertical profiles                                    
      integer, parameter :: nvp=10
      integer, parameter :: i100=1, i150=2, i200=3, i250=4, i300=5
      integer, parameter :: i400=6, i500=7, i700=8, i850=9, i000=10
      real, dimension(nvp) :: pvp=(/100.0,150.0,200.0,250.0,300.0,
     +                              400.0,500.0,700.0,850.0,1000.0/)
c                                                                        
      real, dimension(0:mfx,nvp) :: uvp = rmiss, vvp = rmiss
      real, dimension(0:mfx,nvp) :: tvp = rmiss
      real, dimension(0:mfx,nvp) :: rvp = rmiss, zvp = rmiss
      integer, dimension(0:mfx) :: irvp = imiss, izvp = imiss
      integer, dimension(0:mfx) :: itvp = imiss
      integer, dimension(0:mfx) :: iuvp = imiss, ivvp = imiss
      real, dimension(nvp) :: qvp = rmiss, wvp = rmiss
      real, dimension(nvp) :: wt1 = rmiss, wt2 = rmiss
      real, dimension(nvp) :: tevp = rmiss, tevps = rmiss
      real, dimension(nvp) :: tempu = rmiss, tempv = rmiss
c 
      real :: dpvp, deltc
      real :: olons, olats, colat, t1lat, t1lon, t2lat, t2lon
      real :: temx1, temy1, temx2, temy2, cx, cy
      real :: tkel, pmb, rh, rhs, plcl, tlcl, wmr
      real :: tempt, templon
      real :: epos, delte, epss, eneg, enss, deltes
      real :: shearx, sheary, shrd, shtd, shrs, shts, shrg
      real :: shxu, shxl
      integer :: icok, ipsprt
      real :: psfc, alpha, tvptem
      real :: ubard, vbard, pbard, ubars, vbars, pbars
c 
      integer :: k, kt, n, ll   !counters
c 
c     Initialize variables
      ierr = 0
      ivmx = imiss
      iexmsst = 0
      iexmhcn = 0
      ireadsound = 0
      ireadopt = 0
c 
c     Read in header data
c 
c      read(lumo,120) tmname,ilyr4,ilmon,ilday,iltime
c  120 format(19x,a4,2x,i4,3(i2))
c      read(lumo,121) sname4,sname
c  121 format(19x,a4,2x,a10)
c 
c***  had to alter to account for variable white space in header lines
      read(lumo,'(a80)') iline80
      n=1
 1100 continue
      if ((iline80(n:n) .eq. ' ') .or. (iline80(n:n) .eq. '*')) then
         n = n + 1
         if (n .ge. 66) then
            ierr = 1
            write(*,*) 'Error reading modeldiag header data'
            go to 1006
         endif
         go to 1100
      else
         tmname = iline80(n:n+3)
         n = n + 4
      endif
c 
 1110 continue
c--       search for start of dtg
c
      if (iline80(n:n) .eq. ' ') then
         n = n + 1
         if (n .ge. 70) then
            ierr = 1
            write(*,*) 'Error reading modeldiag header data'
            go to 1006
         endif
         go to 1110
       else
c---------------------assume dtg starts in column 19 -- allows aid names > 4 char
c--       20111103 -- not really sure it's really need -- just get 4*char names onluy         
c
ccc         if(n .ne. 19) n=19
         read (iline80(n:n+9),'(i4,3(i2))') ilyr4,ilmon,ilday,iltime
      endif
c 
      read(lumo,'(a80)') iline80
      n=1
 1120 continue
      if ((iline80(n:n) .eq. ' ') .or. (iline80(n:n) .eq. '*')) then
         n = n + 1
         if (n .ge. 66) then
            ierr = 1
            write(*,*) 'Error reading modeldiag header data'
            go to 1006
         endif
         go to 1120
      else
         sname4 = iline80(n:n+3)
         n = n + 4
      endif
c 
 1130 continue
      if (iline80(n:n) .eq. ' ') then
         n = n + 1
         if (n .ge. 70) then
            ierr = 1
            write(*,*) 'Error reading modeldiag header data'
            go to 1006
         endif
         go to 1130
      else
         sname = iline80(n:n+9)
      endif
c 
      !Perform limited data manipulation on header data
c 
c     Remove any stars from sname
      do k=1,10
         if (sname(k:k) .eq. '*') sname(k:k) = ' '
      enddo
c 
c     Calculate 2 digit year from 4 digit year
      if (ilyr4 .gt. 2000) then
         ilyr = ilyr4 - 2000
      else
         ilyr = ilyr4 - 1900
      endif
c 
c     Calculate 8 character ATCF ID (with 4 digit year)
      natcf(1:4) = sname4
      write(natcf(5:6),'(i2.2)') ilyr
      natcf8(1:4) = sname4
      write(natcf8(5:8),'(i4.4)') ilyr4
c 
      read(lumo,'(a80)') iline80   !blank line
      read(lumo,'(a80)') iline80   !Storm Data line
c 
c     Read the storm data section
c 
      !Read NTIME
      read(lumo,'(a142)') ilinem    !temp line to get ntime and value
c 
c     Check to see if blank line between heading and data
      if (ilinem(1:1) .EQ. ' ') then
         !read next line to get ntime and value
         read(lumo,'(a142)') ilinem
      endif
      if (ilinem(1:5) .eq. 'NTIME') then
         read(ilinem, '(6x,i4)') ntime
      else
         !Default to SHIPS max time if ntime is not provided
         ntime = mft + 1
c         backspace(lumo)
      endif
      !Don't read data past max SHIPS time
      if (ntime .gt. (mft + 1)) ntime = mft + 1
c 
      !set reading formats for rest of file: integer, real
      cfmtstri(1:5) = '(16x,'
      write(cfmtstri(6:8),'(i3.3)') ntime
      cfmtstri(9:13) = '(i6))'
      cfmtstrf(1:5) = '(18x,'
      write(cfmtstrf(6:8),'(i3.3)') ntime
      cfmtstrf(9:15) = '(f6.1))'
      cfmtstrlon(1:5) = '(17x,'
      write(cfmtstrlon(6:8),'(i3.3)') ntime
      cfmtstrlon(9:15) = '(f6.1))'
c**  125    format(16x,ntime(i6))
c**  126    format(16x,ntime(f6))
c 
      !Begin reading storm data
 1210 continue
c 
      read(lumo,'(a142)', iostat=ierrf) ilinem
      if (ierrf .ne. 0) go to 1220
      if (ilinem(1:1) .eq. ' ') go to 1220
      select case (ilinem(1:7))
      case ('       ')
         go to 1220
      case ('TIME   ')   !not currently used
c         write(*,*) ilinem
c         write(*,*) cfmtstri
         read(ilinem,cfmtstri) (itime(k),k= 0,ntime-1)
      case ('LAT    ','LATITUD')   !real LAT, from t=0 on
         do k=0,ntime-1
            if (k .eq. 0) then
               cfmtstrtmp ='(16x,A6)     '
            else
               cfmtstrtmp(1:5) = '(16x,'
               write(cfmtstrtmp(6:8),'(i3.3)') k*6
               cfmtstrtmp(9:13) = 'x,A6)'
            endif
            read(ilinem,cfmtstrtmp) tempc
            read(tempc,*) slat(k)
            if (slat(k) .gt. 900) slat(k) = rmiss
ccc            print*,'ssssssssssslat ',k,slat(k)
         enddo
c         write(*,*) slat(0)
      case ('LON    ','LONGITU')   !real LON, from t=0 on
c         write(*,*) ilinem
c         read(ilinem,cfmtstrlon) (slon(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (k .eq. 0) then
               cfmtstrtmp ='(16x,A6)     '
            else
               cfmtstrtmp(1:5) = '(16x,'
               write(cfmtstrtmp(6:8),'(i3.3)') k*6
               cfmtstrtmp(9:13) = 'x,A6)'
            endif
            read(ilinem,cfmtstrtmp) tempc
            read(tempc,*) slon(k)
ccc            print*,'ssssssssssslon ',k,slon(k)
            if (slon(k) .gt. 900) slon(k) = rmiss
         enddo
c         write(*,*) slon(0)
         !convert from 0-360 degrees to SHIPS lon
         do k=0,ntime-1
            if ((slon(k) .gt. 180.0) .and. (slon(k) .lt. 900)) then
               slon(k) = slon(k) - 360.0
            endif
c***        this will change as other basins added
            if ((slon(k) .gt. 0) .and. (slon(k) .lt. 900)) then
               write(*,*)'Longitude at time',k,'out of range.'
            endif
         enddo
c         write(*,*) slon(0)
      case ('MAXWIND','MAX WIN')   !int vmax in kts, VMAX
         read(ilinem,cfmtstri) (ivmaxb(k),k= 0,ntime-1)
ccc            print*,'sssssssssssivmaxb ',k,ivmaxb(k)
         ivmx=ivmaxb(0)
      case ('RMW    ')   !int rmw in km, not currently used
         read(ilinem,cfmtstri) (irmw(k),k= 0,ntime-1)
      case ('MIN_SLP','MIN SLP')   !int pmin in mb, not currently used
         read(ilinem,cfmtstri) (imslp(k),k= 0,ntime-1)
      case ('SHR_MAG','SHR MAG')   !int shear magnitude in kt, SHDC
         !actually, 850-200mb shear over 0-500km radius (w/vortex)
         read(ilinem,cfmtstri) (ishdc(k),k= 0,ntime-1)
c         write(*,*) ishdc(0)
c***     trying to track down shear error
         ishdc = ishdc*10
      case ('SHR_DIR','SHR DIR')   !int shear heading in deg, SDDC
         !actually, 850-200mb shear over 0-500km radius (w/vortex)
         read(ilinem,cfmtstri) (isddc(k),k= 0,ntime-1)
c         write(*,*) isddc(0)
         ishtd=isddc
c         write(*,*) ishtd(0)
         !Convert ishtd from heading to direction
         do k=0,mft
            if (isddc(k) .lt. imiss) then
               isddc(k) = 180 + isddc(k)
               if (isddc(k) .gt. 360) isddc(k) = isddc(k)-360
            endif
         enddo
c         write(*,*) isddc(0)
      case ('STM_SPD','STM SPD')   !int storm speed in kt
         !calculated in SHIPS already
         read(ilinem,cfmtstri) (ispd(k),k= 0,ntime-1)
      case ('STM_HDG','STM HDG')   !int storm heading in deg
         !calculated in SHIPS already
         read(ilinem,cfmtstri) (ihdg(k),k= 0,ntime-1)
      case ('SST    ')   !integer SST in 10*C
         !saved locally as msst,imsst
         read(ilinem,cfmtstri) (imsst(k),k= 0,ntime-1)
c         Code from when SST was in diag file as real, in C
c         do k=0,ntime-1
c            if (k .eq. 0) then
c               cfmtstrtmp ='(16x,A6)     '
c            else
c               cfmtstrtmp(1:5) = '(16x,'
c               write(cfmtstrtmp(6:8),'(i3.3)') k*6
c               cfmtstrtmp(9:13) = 'x,A6)'
c            endif
c            read(ilinem,cfmtstrtmp) tempc
c            read(tempc,*) msst(k)
c         enddo
         do k=0,ntime-1
            if (imsst(k) .lt. imiss) then
               iexmsst = 1
               msst(k) = float(imsst(k))/10.
            endif
         enddo
      case ('OHC    ')   !integer OHC
         !saved locally as imhcn
         read(ilinem,cfmtstri) (imhcn(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (imhcn(k) .lt. imiss) then
               iexmhcn = 1
               mhcn(k) = float(imhcn(k))
            endif
         enddo
      case ('TPW    ')   !int tpw in mm, not currently used
         read(ilinem,cfmtstri) (itpw(k),k= 0,ntime-1)
      case ('LAND   ')   !int dtl in km, DTL
         read(ilinem,cfmtstri) (idist(k),k=0,ntime-1)
      case ('850TANG')   !int twac in 10*m/s, TWAC
         read(ilinem,cfmtstri) (itwac(k),k= 0,ntime-1)
      case ('850VORT')   !int z850 in 10^7/s, Z850
         read(ilinem,cfmtstri) (iz850(k),k= 0,ntime-1)
      case ('200DVRG')   !int d200 in 10^7/s, D200
         read(ilinem,cfmtstri) (id200(k),k= 0,ntime-1)
      end select
      go to 1210
 1220 continue
c
c     Read in sounding data
c 
      !Read NLEV, LEVS
      read(lumo,'(a142)',iostat=ierrf) ilinem
      if (ilinem(1:1) .EQ. ' ') go to 1220   !test for blank/header line
c 
c     Test if Optional Data instead of Sounding data
      if (ilinem(1:4) .eq. 'NVAR') go to 1250
c 
      !Need 10 pressure levels:
      ! 100,150,200,250,300,400,500,700,850,1000
c 
c     Read in U,V,R,Z,T at each required pressure level
c      (U, V in kt; R in %; Z in dm; T in C)
c      (R and Z are ints, convert to real)
c                                                                        
 1230 continue
c 
      read(lumo,'(a142)', iostat=ierrf) ilinem
c      if (ierrf .ne. 0) then
c         write(*,*) 'ierrf= ', ierrf
c         write(*,*) 'ireadsound= ', ireadsound
c         write(*,*) 'ireadopt= ', ireadopt
c      endif
      if (ierrf .ne. 0) go to 1240
      if (ilinem(1:1) .eq. ' ') go to 1240
      select case (ilinem(1:6))
      case ('      ')
         go to 1240
c 
      case ('T_1000')   !begin 1000mb fields
         read(ilinem,cfmtstri) (itvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (itvp(k) .lt. imiss) then
               !convert 10*deg C --> deg C
               tvp(k,i000) = float(itvp(k))/10.0
            endif
         enddo
      case ('R_1000')
         read(ilinem,cfmtstri) (irvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (irvp(k) .lt. imiss) then
               rvp(k,i000) = float(irvp(k))
            endif
         enddo
      case ('Z_1000')
         read(ilinem,cfmtstri) (izvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (izvp(k) .lt. imiss) then
               !convert decimeters --> meters
               zvp(k,i000) = float(izvp(k))/10.0
            endif
         enddo
      case ('U_1000')
         read(ilinem,cfmtstri) (iuvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (iuvp(k) .lt. imiss) then
               !convert 10*kt --> kt
               uvp(k,i000) = float(iuvp(k))/10.0
            endif
         enddo
      case ('V_1000')
         read(ilinem,cfmtstri) (ivvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (ivvp(k) .lt. imiss) then
               !convert 10*kt --> kt
               vvp(k,i000) = float(ivvp(k))/10.0
            endif
         enddo
c 
      case ('T_0850')   !begin 850mb fields
         read(ilinem,cfmtstri) (itvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (itvp(k) .lt. imiss) then
               !convert 10*deg C --> deg C
               tvp(k,i850) = float(itvp(k))/10.0
            endif
         enddo
      case ('R_0850')
         read(ilinem,cfmtstri) (irvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (irvp(k) .lt. imiss) then
               rvp(k,i850) = float(irvp(k))
            endif
         enddo
      case ('Z_0850')
         read(ilinem,cfmtstri) (izvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (izvp(k) .lt. imiss) then
               !convert decimeters --> meters
               zvp(k,i850) = float(izvp(k))/10.0
            endif
         enddo
      case ('U_0850')
         read(ilinem,cfmtstri) (iuvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (iuvp(k) .lt. imiss) then
               !convert 10*kt --> kt
               uvp(k,i850) = float(iuvp(k))/10.0
            endif
         enddo
      case ('V_0850')
         read(ilinem,cfmtstri) (ivvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (ivvp(k) .lt. imiss) then
               !convert 10*kt --> kt
               vvp(k,i850) = float(ivvp(k))/10.0
            endif
         enddo
c 
      case ('T_0700')   !begin 700mb fields
         read(ilinem,cfmtstri) (itvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (itvp(k) .lt. imiss) then
               !convert 10*deg C --> deg C
               tvp(k,i700) = float(itvp(k))/10.0
            endif
         enddo
      case ('R_0700')
         read(ilinem,cfmtstri) (irvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (irvp(k) .lt. imiss) then
               rvp(k,i700) = float(irvp(k))
            endif
         enddo
      case ('Z_0700')
         read(ilinem,cfmtstri) (izvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (izvp(k) .lt. imiss) then
               !convert decimeters --> meters
               zvp(k,i700) = float(izvp(k))/10.0
            endif
         enddo
      case ('U_0700')
         read(ilinem,cfmtstri) (iuvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (iuvp(k) .lt. imiss) then
               !convert 10*kt --> kt
               uvp(k,i700) = float(iuvp(k))/10.0
            endif
         enddo
      case ('V_0700')
         read(ilinem,cfmtstri) (ivvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (ivvp(k) .lt. imiss) then
               !convert 10*kt --> kt
               vvp(k,i700) = float(ivvp(k))/10.0
            endif
         enddo
c 
      case ('T_0500')   !begin 500mb fields
         read(ilinem,cfmtstri) (itvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (itvp(k) .lt. imiss) then
               !convert 10*deg C --> deg C
               tvp(k,i500) = float(itvp(k))/10.0
            endif
         enddo
      case ('R_0500')
         read(ilinem,cfmtstri) (irvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (irvp(k) .lt. imiss) then
               rvp(k,i500) = float(irvp(k))
            endif
         enddo
      case ('Z_0500')
         read(ilinem,cfmtstri) (izvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (izvp(k) .lt. imiss) then
               !convert decimeters --> meters
               zvp(k,i500) = float(izvp(k))/10.0
            endif
         enddo
      case ('U_0500')
         read(ilinem,cfmtstri) (iuvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (iuvp(k) .lt. imiss) then
               !convert 10*kt --> kt
               uvp(k,i500) = float(iuvp(k))/10.0
            endif
         enddo
      case ('V_0500')
         read(ilinem,cfmtstri) (ivvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (ivvp(k) .lt. imiss) then
               !convert 10*kt --> kt
               vvp(k,i500) = float(ivvp(k))/10.0
            endif
         enddo
c 
      case ('T_0400')   !begin 400mb fields
         read(ilinem,cfmtstri) (itvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (itvp(k) .lt. imiss) then
               !convert 10*deg C --> deg C
               tvp(k,i400) = float(itvp(k))/10.0
            endif
         enddo
      case ('R_0400')
         read(ilinem,cfmtstri) (irvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (irvp(k) .lt. imiss) then
               rvp(k,i400) = float(irvp(k))
            endif
         enddo
      case ('Z_0400')
         read(ilinem,cfmtstri) (izvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (izvp(k) .lt. imiss) then
               !convert decimeters --> meters
               zvp(k,i400) = float(izvp(k))/10.0
            endif
         enddo
      case ('U_0400')
         read(ilinem,cfmtstri) (iuvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (iuvp(k) .lt. imiss) then
               !convert 10*kt --> kt
               uvp(k,i400) = float(iuvp(k))/10.0
            endif
         enddo
      case ('V_0400')
         read(ilinem,cfmtstri) (ivvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (ivvp(k) .lt. imiss) then
               !convert 10*kt --> kt
               vvp(k,i400) = float(ivvp(k))/10.0
            endif
         enddo
c 
      case ('T_0300')   !begin 300mb fields
         read(ilinem,cfmtstri) (itvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (itvp(k) .lt. imiss) then
               !convert 10*deg C --> deg C
               tvp(k,i300) = float(itvp(k))/10.0
            endif
         enddo
      case ('R_0300')
         read(ilinem,cfmtstri) (irvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (irvp(k) .lt. imiss) then
               rvp(k,i300) = float(irvp(k))
            endif
         enddo
      case ('Z_0300')
         read(ilinem,cfmtstri) (izvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (izvp(k) .lt. imiss) then
               !convert decimeters --> meters
               zvp(k,i300) = float(izvp(k))/10.0
            endif
         enddo
      case ('U_0300')
         read(ilinem,cfmtstri) (iuvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (iuvp(k) .lt. imiss) then
               !convert 10*kt --> kt
               uvp(k,i300) = float(iuvp(k))/10.0
            endif
         enddo
      case ('V_0300')
         read(ilinem,cfmtstri) (ivvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (ivvp(k) .lt. imiss) then
               !convert 10*kt --> kt
               vvp(k,i300) = float(ivvp(k))/10.0
            endif
         enddo
c 
      case ('T_0250')   !begin 250mb fields
         read(ilinem,cfmtstri) (itvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (itvp(k) .lt. imiss) then
               !convert 10*deg C --> deg C
               tvp(k,i250) = float(itvp(k))/10.0
            endif
         enddo
      case ('R_0250')
         read(ilinem,cfmtstri) (irvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (irvp(k) .lt. imiss) then
               rvp(k,i250) = float(irvp(k))
            endif
         enddo
      case ('Z_0250')
         read(ilinem,cfmtstri) (izvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (izvp(k) .lt. imiss) then
               !convert decimeters --> meters
               zvp(k,i250) = float(izvp(k))/10.0
            endif
         enddo
      case ('U_0250')
         read(ilinem,cfmtstri) (iuvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (iuvp(k) .lt. imiss) then
               !convert 10*kt --> kt
               uvp(k,i250) = float(iuvp(k))/10.0
            endif
         enddo
      case ('V_0250')
         read(ilinem,cfmtstri) (ivvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (ivvp(k) .lt. imiss) then
               !convert 10*kt --> kt
               vvp(k,i250) = float(ivvp(k))/10.0
            endif
         enddo
c 
      case ('T_0200')   !begin 200mb fields
         read(ilinem,cfmtstri) (itvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (itvp(k) .lt. imiss) then
               !convert 10*deg C --> deg C
               tvp(k,i200) = float(itvp(k))/10.0
            endif
         enddo
      case ('R_0200')
         read(ilinem,cfmtstri) (irvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (irvp(k) .lt. imiss) then
               rvp(k,i200) = float(irvp(k))
            endif
         enddo
      case ('Z_0200')
         read(ilinem,cfmtstri) (izvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (izvp(k) .lt. imiss) then
               !convert decimeters --> meters
               zvp(k,i200) = float(izvp(k))/10.0
            endif
         enddo
      case ('U_0200')
         read(ilinem,cfmtstri) (iuvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (iuvp(k) .lt. imiss) then
               !convert 10*kt --> kt
               uvp(k,i200) = float(iuvp(k))/10.0
            endif
         enddo
      case ('V_0200')
         read(ilinem,cfmtstri) (ivvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (ivvp(k) .lt. imiss) then
               !convert 10*kt --> kt
               vvp(k,i200) = float(ivvp(k))/10.0
            endif
         enddo
c 
      case ('T_0150')   !begin 150mb fields
         read(ilinem,cfmtstri) (itvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (itvp(k) .lt. imiss) then
               !convert 10*deg C --> deg C
               tvp(k,i150) = float(itvp(k))/10.0
            endif
         enddo
      case ('R_0150')
         read(ilinem,cfmtstri) (irvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (irvp(k) .lt. imiss) then
               rvp(k,i150) = float(irvp(k))
            endif
         enddo
      case ('Z_0150')
         read(ilinem,cfmtstri) (izvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (izvp(k) .lt. imiss) then
               !convert decimeters --> meters
               zvp(k,i150) = float(izvp(k))/10.0
            endif
         enddo
      case ('U_0150')
         read(ilinem,cfmtstri) (iuvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (iuvp(k) .lt. imiss) then
               !convert 10*kt --> kt
               uvp(k,i150) = float(iuvp(k))/10.0
            endif
         enddo
      case ('V_0150')
         read(ilinem,cfmtstri) (ivvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (ivvp(k) .lt. imiss) then
               !convert 10*kt --> kt
               vvp(k,i150) = float(ivvp(k))/10.0
            endif
         enddo
c 
      case ('T_0100')   !begin 100mb fields
         read(ilinem,cfmtstri) (itvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (itvp(k) .lt. imiss) then
               !convert 10*deg C --> deg C
               tvp(k,i100) = float(itvp(k))/10.0
            endif
         enddo
      case ('R_0100')
         read(ilinem,cfmtstri) (irvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (irvp(k) .lt. imiss) then
               rvp(k,i100) = float(irvp(k))
            endif
         enddo
      case ('Z_0100')
         read(ilinem,cfmtstri) (izvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (izvp(k) .lt. imiss) then
               !convert decimeters --> meters
               zvp(k,i100) = float(izvp(k))/10.0
            endif
         enddo
      case ('U_0100')
         read(ilinem,cfmtstri) (iuvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (iuvp(k) .lt. imiss) then
               !convert 10*kt --> kt
               uvp(k,i100) = float(iuvp(k))/10.0
            endif
         enddo
      case ('V_0100')
         read(ilinem,cfmtstri) (ivvp(k),k= 0,ntime-1)
         do k=0,ntime-1
            if (ivvp(k) .lt. imiss) then
               !convert 10*kt --> kt
               vvp(k,i100) = float(ivvp(k))/10.0
            endif
         enddo
c 
      end select
      go to 1230
 1240 continue
      ireadsound = 1
c 
c     Finished reading in sounding data, begin calculations
c 
c 
c     First patch all variables
      !slat, slon
      call patchi(slon(0:mft),rmiss,mfx)
      call patchi(slat(0:mft),rmiss,mfx)
      !storm location: ispd, ihdg, idist
      !recalculate with patched lat/lon
      do k=-2,mft
         ftimec(k) = delt*float(k)
      enddo
      call tspdcal(slat,slon,ftimec,mft,rmiss,cxt,cyt,cmagt)
      do k=0,mft
         call ctorh(cxt(k),cyt(k),rspd(k),rhdg(k))
         !could use rspd(k) instead of cmagt(k) for same result
         ispd(k) = ifix(cmagt(k) + 0.49)
         ihdg(k)  = ifix(rhdg(k)  + 0.49)
         !update land
         if ((slat(k) .lt. rmiss) .and. (slon(k) .lt. rmiss)) then
            call aland(slon(k),slat(k),rland(k))
            idist(k) = ifix(rland(k))
         else
            idist(k) = imiss
         endif
      enddo
c 
      !shear: ishdc, ishtd, isddc
      !misc storm variables: itwac, iz850, id200, itpw
      !sst, ohc - currently handled in later section
      do k=0,mft
         if (ishdc(k) .lt. imiss) rshdc(k) = float(ishdc(k))
         if (isddc(k) .lt. imiss) rsddc(k) = float(isddc(k))
         if (ishtd(k) .lt. imiss) rshtd(k) = float(ishtd(k))
         if (itwac(k) .lt. imiss) rtwac(k) = float(itwac(k))
         if (id200(k) .lt. imiss) rd200(k) = float(id200(k))
         if (iz850(k) .lt. imiss) rz850(k) = float(iz850(k))
         if (itpw(k) .lt. imiss) rtpw(k) = float(itpw(k))
      enddo
      call patchi(rshdc,rmiss,mft)
      call patchi(rsddc,rmiss,mft)
      call patchi(rshtd,rmiss,mft)
      call patchi(rtwac,rmiss,mft)
      call patchi(rd200,rmiss,mft)
      call patchi(rz850,rmiss,mft)
      call patchi(rtpw,rmiss,mft)
      !convert from real to int
      do k=0,mft
         !lat,lon
         if (slat(k) .lt. 900) then
            ilat(k) = ifix(10.0*slat(k))
         else
            ilat(k) = imiss
         endif
         if (slon(k) .lt. 900) then
            ilon(k) = ifix(-10.0*slon(k))
         else
            ilon(k) = imiss
         endif
         !shdc,sddc,shtd
         if (rshdc(k) .lt. rmiss) then
            ishdc(k) = ifix(rshdc(k))
         else
            ishdc(k) = imiss
         endif
         if (rsddc(k) .lt. rmiss) then
            isddc(k) = ifix(rsddc(k))
         else
            isddc(k) = imiss
         endif
         if (rshtd(k) .lt. rmiss) then
            ishtd(k) = ifix(rshtd(k))
         else
            ishtd(k) = imiss
         endif
         !twac, d200, z850, tpw
         if (rtwac(k) .lt. rmiss) then
            itwac(k) = ifix(rtwac(k))
         else
            itwac(k) = imiss
         endif
         if (rd200(k) .lt. rmiss) then
            id200(k) = ifix(rd200(k))
         else
            id200(k) = imiss
         endif
         if (rz850(k) .lt. rmiss) then
            iz850(k) = ifix(rz850(k))
         else
            iz850(k) = imiss
         endif
         if (rtpw(k) .lt. rmiss) then
            itpw(k) = ifix(rtpw(k))
         else
            itpw(k) = imiss
         endif
      enddo
      !the sounding variables: uvp, vvp, tvp, rvp, zvp
      do n=1,nvp
         call patchi(uvp(:,n),rmiss,mfx)
         call patchi(vvp(:,n),rmiss,mfx)
         call patchi(tvp(:,n),rmiss,mfx)
         call patchi(rvp(:,n),rmiss,mfx)
         call patchi(zvp(:,n),rmiss,mfx)
      enddo
c 
c     Calculate deep layer mean weights for each pressure level
      dpvp = pvp(nvp)-pvp(1)
c 
      wvp(  1) = 0.5*(pvp(  2)-pvp(    1))/dpvp
      wvp(nvp) = 0.5*(pvp(nvp)-pvp(nvp-1))/dpvp
c 
      do n=2,nvp-1
	 wvp(n) = ( 0.5*(pvp(n+1)-pvp(n-1)) )/dpvp
      enddo
c 
c     Proceed through each time period:
      do 5 kt=0,mft
c 
c        Save current lat,lon
         olons = slon(kt)
         olats = slat(kt)
         colat = cos(slat(kt)*3.14159265/180.0)
c 
c        Calculate x,y components of storm motion (m/s)
         if (slat(kt-2) .lt. 900.0 .and.
     +       slat(kt  ) .lt. 900.0) then
            t2lat = slat(kt)
            t2lon = slon(kt)
            t1lat = slat(kt-2)
            t1lon = slon(kt-2)
            deltc = 2.0*delt
	    icok = 1
         else
	    if (kt+2       .le. mft .and.
     +          slat(kt  ) .lt. 900.0 .and.
     +          slat(kt+2) .lt. 900.0) then
               t2lat = slat(kt+2)
               t2lon = slon(kt+2)
               t1lat = slat(kt)
               t1lon = slon(kt)
               deltc = 2.0*delt
               icok = 1
	    elseif (kt+1       .le. mft .and.
     +              slat(kt  ) .lt. 900.0 .and.
     +              slat(kt+1) .lt. 900.0) then
               t2lat = slat(kt+1)
               t2lon = slon(kt+1)
               t1lat = slat(kt)
               t1lon = slon(kt)
               deltc = 1.0*delt
               icok = 1
            else
               t2lat = slat(kt)
               t2lon = slon(kt)
               t1lat = slat(kt)
               t1lon = slon(kt)
               deltc = 1.0*delt
               icok = 0
            endif
         endif
c 
         call lltoxy(olons,olats,colat,t1lon,t1lat,temx1,temy1)
         call lltoxy(olons,olats,colat,t2lon,t2lat,temx2,temy2)
c 
         cx = 1000.0*(temx2-temx1)/(deltc*3600.0)
         cy = 1000.0*(temy2-temy1)/(deltc*3600.0)
c 
c        Calculate thetae profile
         do n=1,nvp
            tkel = tvp(kt,n) + 273.15   !convert C --> K
            pmb  = pvp(n)
            rh   = rvp(kt,n)
            if (rh .le. 0.0 .or. rh .gt. 99.9) rh = 50.0
            call thetae(tkel,pmb,rh,plcl,tlcl,wmr,tevp(n))
            qvp(n) = wmr
            rvp(kt,n) = rh
c 
            rhs= 100.0
            call thetae(tkel,pmb,rhs,plcl,tlcl,wmr,tevps(n))
         enddo
c 
c        Save annular average u at 200 mb (in knots)
         iu200(kt) = ifix(10.0*uvp(kt,i200))
c 
c        Save annular average T at 150,200 and 250 mb (in deg C)
         it150(kt) = ifix( 10.0*tvp(kt,i150) )
         it200(kt) = ifix( 10.0*tvp(kt,i200) )
         it250(kt) = ifix( 10.0*tvp(kt,i250) )
c 
c        Save annular average T,RH and Z at 1000 mb (in deg C, %, m)
         it000(kt) = ifix( 10.0*tvp(kt,i000) )
         ir000(kt) = ifix(rvp(kt,i000))
         iz000(kt) = ifix(zvp(kt,i000))
c 
c        Calculate and save sea level pressure
         tempt = tvp(kt,i000) + 273.15   !convert C to K
         call psext(tempt,zvp(kt,i000),psfc)
         ipsfc(kt) = ifix(10.0*(psfc-1000.0))
c 
c        Save annular average low-level RH
         irhlo(kt) = ifix( (rvp(kt,i700)+rvp(kt,i850))/2.0 )
c 
c        Save annular average mid-level RH
         irhmd(kt) = ifix( (rvp(kt,i500)+rvp(kt,i700))/2.0 )
c 
c        Save annular average high-level RH
         irhhi(kt) = ifix( (rvp(kt,i300)+rvp(kt,i400)+
     +                      rvp(kt,i500))/3.0 )
c 
c        Save annular average thetae at 1000 mb
         ie000(kt) = ifix( 10.0*tevp(i000) )
c 
c        Calculate and save the thetae positive area
         epos = 0.0
         eneg = 0.0
         epss = 0.0
         enss = 0.0
         do n=1,nvp
            delte = tevp(i000) - tevp(n)
            deltes= tevp(i000) - tevps(n)
            if (delte  .gt. 0.0) epos = epos + wvp(n)*delte
            if (delte  .lt. 0.0) eneg = eneg + wvp(n)*abs(delte)
            if (deltes .gt. 0.0) epss = epss + wvp(n)*deltes
            if (deltes .lt. 0.0) enss = enss + wvp(n)*abs(deltes)
         enddo
         iepos(kt) = ifix( 10.0*epos )
         ieneg(kt) = ifix( 10.0*eneg )
         iepss(kt) = ifix( 10.0*epss )
         ienss(kt) = ifix( 10.0*enss )
c 
c        Calculate and save the 850-200 mb vertical shear
         shearx = uvp(kt,i200)-uvp(kt,i850)
         sheary = vvp(kt,i200)-vvp(kt,i850)
	 call ctorh(shearx,sheary,shrd,shtd)
         ishrd(kt) = ifix(10.0*shrd)
c***     this direction is currently holding isddc converted to htd
c***         ishtd(kt) = ifix(shtd)
c 
c        Calculate and save the 850-500 mb vertical shear
         shearx = uvp(kt,i500)-uvp(kt,i850)
         sheary = vvp(kt,i500)-vvp(kt,i850)
	 call ctorh(shearx,sheary,shrs,shts)
         ishrs(kt) = ifix(10.0*shrs)
         ishts(kt) = ifix(shts)
c 
c        Calculate and save the generalized shear parameter
	 call gshear(uvp(kt,:),vvp(kt,:),wvp,nvp,shrg)
	 ishrg(kt) = ifix(10.0*shrg)
c**      Define generalized shear w/o vortex as ishrg for now
         ishgc(kt)=ishrg(kt)
c 
c        Calculate and save the maximum shear in the
c        upper and lower part of the sounding
	 call xshear(uvp(kt,:),vvp(kt,:),pvp,nvp,i150,i500,shxu)
	 ishxu(kt) = ifix(10.0*shxu)
c 
	 call xshear(uvp(kt,:),vvp(kt,:),pvp,nvp,i500,i000,shxl)
	 ishxl(kt) = ifix(10.0*shxl)
c 
         ipsprt=0
c         ipsprt=1
         if (kt .eq. 0) then
c           Calculate and save the steering pressure level PSLV
            alpha = 0.4
            if (icok .eq. 1) then
               do n=1,nvp
                  tempu(n) = uvp(kt,n)*0.51444
                  tempv(n) = vvp(kt,n)*0.51444
               enddo
               call splcal(pvp,tempu,tempv,cx,cy,
     +                     alpha,nvp,wt1,wt2,
     +                     ubard,vbard,pbard,ubars,vbars,pbars)
c 
               if (ipsprt .eq. 1) then
                  write(*,749) alpha,cxt(kt),cyt(kt),ubard,vbard,pbard,
     +                                         ubars,vbars,pbars
  749             format(/,' Steering pressure level output',
     +                   /,' alpha=',f5.1,' cx,cy: ',2(f5.1,1x),
     +                   /,' ub,vb,pb: ',3(f6.1,1x),
     +                   /,' us,vs,ps: ',3(f6.1,1x),
     +                  //,'  p     u     v     wd     ws     ws/wd',
     +                     '  T     RH    ThE    ThEs')
c 
                  do ll=1,nvp
                     tvptem = tvp(kt,ll)
c                     tvptem = tvp(kt,ll)-273.15
                     write(*,750) pvp(ll),uvp(kt,ll),vvp(kt,ll),
     +                            wt1(ll),wt2(ll),
     +                            wt2(ll)/wt1(ll),
     +                            tvptem,rvp(kt,ll),
     +                            tevp(ll),tevps(ll)
  750                format(1x,f5.0,1x,f5.1,1x,f5.1,1x,
     +                      f6.3,1x,f6.3,1x,f6.2,1x,f6.1,1x,f5.1,
     +                      1x,f5.1,1x,f5.1)
                  enddo
               endif
            else
               pbars = 525.0
            endif
            ipslv(kt) = ifix(pbars)
         endif
c 
c        Set any of the derived variables to missing if lat/lon missing
         if ((slat(kt) .ge. rmiss) .or. (slon(kt) .ge. rmiss)) then
            iu200(kt) = imiss
            it150(kt) = imiss
            it200(kt) = imiss
            it250(kt) = imiss
            it000(kt) = imiss
            ir000(kt) = imiss
            iz000(kt) = imiss
            ipsfc(kt) = imiss
            ie000(kt) = imiss
            iepos(kt) = imiss
            ieneg(kt) = imiss
            iepss(kt) = imiss
            ienss(kt) = imiss
            ishrd(kt) = imiss
            ishrs(kt) = imiss
            ishts(kt) = imiss
	    ishrg(kt) = imiss
            ishgc(kt) = imiss
            irhlo(kt) = imiss
            irhmd(kt) = imiss
            irhhi(kt) = imiss
	    ishxu(kt) = imiss
	    ishxl(kt) = imiss
         endif
c 
    5 continue
c 
c     If the optional data has already been read in, skip this section
      if (ireadopt .eq. 1) go to 1260
c 
c     Read in optional data
c 
      !Read NVAR, VAR NAMES
      read(lumo,'(a142)', iostat=ierrf) ilinem
      if (ierrf .ne. 0) go to 1260
      if (ilinem(1:1) .eq. ' ') go to 5        !test for blank/header line

      !link in for cases where optional listed before sounding data
 1250 continue
c 
      read(lumo,'(a142)',iostat=ierrf) ilinem
      if (ierrf .ne. 0) go to 1260             !test for EOF
      if (ilinem(1:1) .eq. ' ') go to 1260     !test for blank line
      select case (ilinem(1:8))
      case ('        ')
         go to 1260
c 
      case ('OPTIONAL')   !optional field
         read(ilinem,cfmtstri) (iopt(k),k= 0,ntime-1)
c 
      end select
      go to 1250
 1260 continue
      ireadopt = 1
c 
c     If the sounding data has not yet been read in, send back
      if (ireadsound .eq. 0) go to 1220
c 
c     If model SST, OHC exists, send back to iships
c     otherwise use climatological values of SST, OHC
      if (iexmsst .eq. 1) then   !model SST
         call patchi(msst,rmiss,mfx)
         do k=0,ntime-1
            if ((slat(k) .lt. 900) .and. (slon(k) .lt. 900)) then
               isst(k) = ifix(msst(k)*10.)
            else
               isst(k) = imiss
            endif
         enddo
      else                    !clim SST
         do k=0,ntime-1
            isst(k) = icsst(k)
         enddo
      endif
c      write(*,*) isst(0)
c 
      if (iexmhcn .eq. 1) then   !model OHC
         call patchi(mhcn,rmiss,mfx)
         do k=0,ntime-1
            if ((slat(k) .lt. 900) .and. (slon(k) .lt. 900)) then
               ihcn(k) = ifix(mhcn(k))
            else
               ihcn(k) = imiss
            endif
         enddo
      else                    !clim OHC
         do k=0,ntime-1
            chcn = rmiss
            ierrc = 0
c 
            if ((slat(k) .ge. 900) .or. (slon(k) .ge. 900)) go to 6
            if (idist(k) .lt. 0) then
               chcn = 0
               go to 6
            endif
            call bassel(slat(k),360.0+slon(k),ibas)
            if (ibas .eq. 1) then
               bas = 'atl'
               call ohcclim(bas,ilyr4,ilmon,ilday,slat(k),slon(k),rmiss,
     +                      chcn,ierrc)
            elseif (ibas .eq. 2) then
               bas = 'pac'
               call ohcclim(bas,ilyr4,ilmon,ilday,slat(k),slon(k),rmiss,
     +                      chcn,ierrc)
            else
               write(*,*)'Basin outside of SHIPS current operations.'
            endif
c            write(*,*) slon(k), 360.0+slon(k), bas
c 
c            if (ierrc .ne. 0) go to 1007
            if (ierrc .ne. 0) then
c               write(*,*)'Problem running ohcclim from readModel'
c               write(*,*)'ierrc = ', ierrc
               chcn = rmiss
            endif
c 
    6       continue
            ihcn(k) = ifix(chcn)
         enddo
      endif
c      write(*,*) ihcn(0)
c 
c 
c**      close(lumo)
c 
      return
 1006 continue
      ierr = 1
c      write(*,*) 'modeldiag read failure'
      return
 1007 continue
      ierr = 2
c      write(*,*) 'SST/OHC read failure'
      return
      END SUBROUTINE readModel
c 
c***********************************************************************
c     end main read subroutines, begin supporting subroutines
c***********************************************************************
c 
c-----7---------------------------------------------------------------72
c     subroutine psext
c-----7---------------------------------------------------------------72
      SUBROUTINE psext(t00,z00,psfc)
c     This routine calculates the surface pressure in hPa
c     by extrapolating from the 1000 mb height surface.
c 
c     Input: t00 = temperature (K) at 1000 mb
c            z00 = height deviation (m) of 1000 mb from the height of
c                  the standard atmosphere.
c 
c     Output: psfc = surface pressure (hPa)
c 
c     Uses: subroutine stndz()
c 
      IMPLICIT NONE
c 
      !list calling variables
      real, intent(in) ::  t00, z00
      real, intent(out) :: psfc
c 
      !list local variables
      real :: gam, aa, p00, zb00, tb00, thb00, z00t, t11
c 
      gam = 0.0065
      aa    = 9.81/(287.0*gam)
      p00 = 1000.0
      call stndz(p00,zb00,tb00,thb00)
      z00t= zb00+z00
      t11 = t00 + gam*z00t
c 
      psfc= p00*( (t11/t00)**aa )
c 
      return
      END SUBROUTINE psext
c 
c-----7---------------------------------------------------------------72
c     subroutine gshear
c-----7---------------------------------------------------------------72
      subroutine gshear(uvp,vvp,wvp,nvp,shrg)                            
c     This routine calculates a generalized shear parameter, which       
c     includes contributes from nvp pressure levels                      
c                                                                        
      dimension uvp(nvp),vvp(nvp),wvp(nvp)                               
c                                                                        
c     Calculate the vertically averaged wind                             
      ubar = 0.0                                                         
      vbar = 0.0                                                         
      do 10 n=1,nvp                                                      
	 ubar = ubar + wvp(n)*uvp(n)                                            
	 vbar = vbar + wvp(n)*vvp(n)                                            
   10 continue                                                           
c                                                                        
c     Calculate generarlized shear                                       
      shrg = 0.0                                                         
      do 20 n=1,nvp                                                      
         shrg = shrg + wvp(n)*sqrt( (uvp(n)-ubar)**2 +                   
     +                              (vvp(n)-vbar)**2 )                   
   20 continue                                                           
c                                                                        
c     Add factor to make generalized shear equal to two level shear      
c     for linear shear profiles                                          
      shrg = 4.0*shrg                                                    
c                                                                        
c     do 30 n=1,nvp                                                      
c        write(6,100) n,uvp(n),vvp(n),wvp(n),ubar,vbar,shrg              
c 100    format(1x,'n,u,v,w,ub,vb,sg: ',i2,6(f6.2,1x))                   
c  30 continue                                                           
c                                                                        
      return                                                             
      end subroutine
c 
c-----7---------------------------------------------------------------72
c     subroutine xshear
c-----7---------------------------------------------------------------72
      subroutine xshear(uvp,vvp,pvp,nvp,i1,i2,shrx)                      
c     This routine calculates the maximum shear in the layer             
c     pvp(i1) to pvp(i2). The max shear magnitude is normalized          
c     to the 850 to 200 mb layer.                                        
c                                                                        
      dimension uvp(nvp),vvp(nvp),pvp(nvp)                               
c                                                                        
c     Check input                                                        
      if (i2 .gt. i1) then                                               
	 n1 = i1                                                                
	 n2 = i2                                                                
      elseif (i2 .lt. i1) then                                           
	 n1 = i2                                                                
	 n2 = i1                                                                
      else                                                               
	 shrx = 999.9                                                           
	 return                                                                 
      endif                                                              
c                                                                        
      if (n1 .gt. nvp .or. n2 .gt. nvp) then                             
	 shrx = 999.9                                                           
	 return                                                                 
      endif                                                              
c                                                                        
      if (n1 .lt. 1 .or. n2 .lt. 1) then                                 
	 shrx = 999.9                                                           
	 return                                                                 
      endif                                                              
c                                                                        
c     Calculate the vertically averaged wind                             
      shrx = -999.9                                                      
      dpn  = (850.0-200.0)                                               
      do n=n1,n2-1                                                    
	 du = (uvp(n+1)-uvp(n))                                                 
	 dv = (vvp(n+1)-vvp(n))                                                 
	 dp = (pvp(n+1)-pvp(n))                                                 
	 shrt = sqrt(du*du + dv*dv)*dpn/dp                                      
c                                                                        
	 if (shrt .gt. shrx) shrx = shrt                                        
      enddo                                                           
c                                                                        
      return                                                             
      end subroutine
c 
c-----7---------------------------------------------------------------72
c     subroutine splcal
c-----7---------------------------------------------------------------72
      subroutine splcal(plev,u,v,cx,cy,alpha,ml,
     +                  dw,w,ubard,vbard,pbard,ubar,vbar,pbar)
c 
c     This routine calculates the weights w to determine the vertically
c     averaged horizontal wind that is as close as possible to
c     the storm motion cx,cy. The weights are used to determine the
c     pressure of the steering level.
c
c     Input:
c       plev        - 1-D array containing the pressure levels (mb)
c       u,v         - The enviromental wind at the levels plev
c       cx,cy       - The components of the storm motion vector
c       alpha       - The coefficient for contraining the steering
c                     weights so that they are not "too far" from
c                     the mass weighted average weights
c       ml          - The number of pressure levels
c
c     Output:
c       dw          - The weights for a mass-weighted average
c       w           - The weights for the optimal steering
c       ubard,vbard - The mass-weighted average horizontal wind
c       ubar,vbar   - The optimally weighted horizontal mean
c       pbard       - The mass-weighted pressure
c       pbar        - The optimally weighted pressure
c 
      dimension plev(ml),u(ml),v(ml),dw(ml),w(ml)
c
c     Local variables
      parameter (np=12,mp=2)
c 
      dimension a(np,np),b(np,mp)
c
c     Set ipen=1 for penalty in terms of (W-M) or 
c         ipen=2 for penalty in terms of (W/M-1)
      ipen=2
c
c     Make sure np is large enough
      if (ml .gt. np) then
         write(6,100)
  100    format(/,' np too small in routine wcal')
         stop
      endif
c 
      n=ml-1
c
c     Calculate deep-layer mean weights
      call dlmw(plev,dw,ml)
c
c     Calculate column matrix on the RHS of the linear system for w
      uk = u(ml)
      vk = v(ml)
      dk= dw(ml)
c 
      if (ipen .eq. 1) then
         do k=1,n
            b(k,1) = (cx-uk)*(u(k)-uk) + (cy-vk)*(v(k)-vk) +
     +               alpha*(1.0 + dw(k) - dk)
         enddo
      else
         do k=1,n
            b(k,1) = (cx-uk)*(u(k)-uk) + (cy-vk)*(v(k)-vk) +
     +               alpha*(1.0/(dk*dk) + 1.0/dw(k) - 1.0/dk)
         enddo
      endif
c
c     Calculate w coefficient matrix
      if (ipen .eq. 1) then
         do 15 j=1,n
         do 15 i=1,n
            if (i .eq. j) then
               ac = 2.0
            else
               ac = 1.0
            endif
c 
            a(i,j) = (u(i)-uk)*(u(j)-uk) +
     +               (v(i)-vk)*(v(j)-vk) + ac*alpha
   15    continue
      else
         do 16 j=1,n
         do 16 i=1,n
            if (i .eq. j) then
               ac = (1.0/dk)**2 + (1.0/dw(j))**2
            else
               ac = (1.0/dk)**2
            endif
c 
            a(i,j) = (u(i)-uk)*(u(j)-uk) +
     +               (v(i)-vk)*(v(j)-vk) + ac*alpha
   16    continue
      endif
c
c     Calculate optimal weights
      call gaussj(a,n,np,b,1,mp)
c 
      do i=1,n
         w(i) = b(i,1)
      enddo
c 
      w(ml) = 1.0
      do i=1,n
         w(ml) = w(ml) - w(i)
      enddo
c
c     Calculate vertically weighted variables
      ubard = 0.0
      vbard = 0.0
      ubar  = 0.0
      vbar  = 0.0
      pbard = 0.0
      pbar  = 0.0
      do k=1,ml
         ubard = ubard + dw(k)*u(k)
         vbard = vbard + dw(k)*v(k)
         pbard = pbard + dw(k)*plev(k)
         ubar  = ubar  +  w(k)*u(k)
         vbar  = vbar  +  w(k)*v(k)
         pbar  = pbar  +  w(k)*plev(k)
      enddo
c 
      return
      end subroutine
c 
c-----7---------------------------------------------------------------72
c     subroutine thetae
c-----7---------------------------------------------------------------72
      SUBROUTINE thetae(tk,p,rh,pl,tl,w,te)
c     This routine calculates the equivalent potential temperature
c     using the formula described in Bolton (1980) MWR
c 
c     Input: tk  - Temperature (K)
c            p   - Total pressure (hPa)
c            rh  - Relative humidity (%)
c 
c     Output: tl - Temperature (K) of the LCL
c             pl - Pressure (hPa) of the LCL
c             te - Thetae (K) 
c             w  - Mixing ratio (g/Kg)
c 
c     Note: If any input values is outside the normal 
c           atmospheric range, all output variables are set to -999.
c 
c     Check input
      if (tk .lt. 100. .or. tk .gt.  350.) go to 900
      if (p  .le.   0  .or.  p .gt. 1200.) go to 900
      if (rh .le.   0. .or. rh .gt.  100.) go to 900
c 
      ctk = 273.15
      t   = tk - ctk
c 
      es = 6.112*exp( 17.67*t/(t+243.5) )
      ws = 622.0*es/(p-es)
      w  = ws*rh/100.0
c 
      tl = 55.0 + 1.0/( 1.0/(tk-55.0) - alog(rh/100.0)/2840. )
      pl = p*(tl/tk)**(1.0/0.2854)
c 
      aa = .2854*(1.0 - .00028*w) 
      bb = ( (3.376/tl) - .00254 )*w*(1.+.00081*w)
      te = (tk*(1000.0/p)**aa)*exp(bb)
c 
      return
c 
  900 continue
      pl = -999.
      tl = -999.
      te = -999.
c 
      return
      END SUBROUTINE thetae
c 
      subroutine ohcclim(bas,ityr,itmon,itday,tlat,tlon,rmiss,
     +                 cohc,ierr)
c
c     This routine calculates the climatological values of  
c     ocean heat content.
c
c
c     Input:  bas   - 3 character basin name; atl or pac
c             ityr - 4-digit year
c             itmon  - month (1-12)
c             itday  - day (1-31)
c             tlat - TC latitude
c             tlon - TC longitude
c             rmiss - error value (real)
c
c     Output: 
c             cohc  - Climatological OHC value
c             ierr - error flag =0 for normal completion
c                               =2 for illegal itmon
c                               =3 for illegal itday
c                               =4 for problem with reading input file
c                                
c     Passed arrays/values
      character*3 bas
c
c     Array for day of month represented by each monthly mean 
c     (used for time interpolation 0=dec,1=jan,...,12=dec,13=jan)
      dimension ndmo(0:13),jdmo(0:13),kdmo(12)
c
c     Inputs: Climatological OHC
      parameter (mx=201,my=121)      
      real rlonl,rlonr,dlon
      real rlatt,rlatb,dlat,nerr
      dimension spatfc(mx,my,12)
      dimension icase(12)
      character *3 label(12)

      data luinp /77/
      character*72 fninp
c
c     Month information
      dimension ngm(12)
c 
      data kdmo /   31,28,31,30,31,30,31,31,30,31,30,31   /
      data ndmo /16,16,14,16,15,16,15,16,16,15,16,15,16,16/
c
c     Flag for file reading
      data iofread /1/
c 
      save iofread,ndmo,jdmo,kdmo,ngm
      save rlonl,rlonr,dlon,nlon,
     +     rlatt,rlatb,dlat,nlat
      save label,icase 
      save spatfc
c 
      ierr = 0
      cohc = rmiss
c
c     Calculate Julian Days of center of each month
c     for later use by time interpolation routines
      ityrt=1999
      do k=1,12
         call jdate2(k,ndmo(k),ityrt,jdmo(k))
      enddo
c 
      jdmo(13) = 365 + ndmo(13)
      jdmo (0) =     - ndmo( 0)
c 
      if (iofread .eq. 1) then
         iofread = 0
c        Open and read climatological OHC for the specified basin
         write(fninp,502) bas
  502    format('ohcclim.',a3)
         open(file=fninp,
     +        unit=luinp,form='formatted',status='old',err=900)
c
c        Read the header line
         read(luinp,505,err=900) rlonl,rlonr,dlon,nlon,
     +                           rlatb,rlatt,dlat,nlat
c 
 505     format(8x,2(3(f9.2),i6))	 
c
c        Read the clim OHC data for each month
         do m=1,12
            read(luinp,100,err=900) label(m),icase(m)
  100       format(a3,i7)
c 
            do j=1,nlat
               read(luinp,110,err=900) (spatfc(i,j,m),i=1,nlon)
  110          format(500(f6.1))
            enddo
         enddo
c 
         close(luinp)
      endif
c
c     Determine the index of the climatological OHC value
c        closest to the TC lat/lon:
      itc = nint(((tlon - rlonl)/(rlonr - rlonl))*(nlon - 1))
      jtc = nint(((tlat - rlatb)/(rlatt - rlatb))*(nlat - 1))
c 
      if ((itc .le. 0) .or. (itc .gt. nlon)) then
         ierr = 1
	 return
      endif
      
      if ((jtc .le. 0) .or. (jtc .gt. nlat)) then
         ierr = 1
	 return
      endif       
c
c     Check input dates
      if (itmon .gt. 12 .or. itmon .lt. 1) then
         ierr=2
         return
      endif
c 
      ndmax = 2*ndmo(itmon)
      if (ndmax .gt. 31) ndmax=31
      if (itmon .eq. 2 .and. mod(ityr,4) .eq. 0) ndmax=29
c 
      if (itday .gt. ndmax .or. itday .lt. 1) then
         ierr=3
         return
      endif
c
c     Calculate Julian day of requested input date
c     but under the assumption that it is not a leap year
      ityrt=1999
      itdaytm=itday
      if (itmon .eq. 2 .and. itday .eq. 29) itdaytm=28
      call jdate2(itmon,itdaytm,ityrt,ijday)
c
c     Calculate the weights for time interpolation
      if (itday .le. ndmo(itmon)) then
         im = itmon-1
         ip = itmon
      else
         im = itmon
         ip = itmon+1
      endif
      jm = jdmo(im)
      jp = jdmo(ip)
c 
      dday = float(jp-jm)
      wtm = float(jp-ijday)/dday
      wtp = float(ijday-jm)/dday
c 
      ierr=0
c
c     Adjust indices for Jan and Dec
      if (im .eq.  0) im = 12
      if (ip .eq. 13) ip= 1
c
c     Perform time interpolation
c      
      cohc = wtm*spatfc(itc,jtc,im) + wtp*spatfc(itc,jtc,ip)      
c 
      return
c 
  900 ierr=4
      return
c 
      end subroutine
c 
      subroutine bassel(rlat,rlon,ibasin)
c     This routine determines which basin a given 
c     lat/lon point is in
c
c     Input: 
c       rlat - latitude deg N
c       rlon - longitude deg E (deg W neg)
c 
c     Output
c       ibasin = 1 for Atlantic
c              = 2 for east Pacific
c              = 3 for west Pacific
c              = 4 for south Pacific
c              = 5 for Indian Ocean 
c 
      ibasin = 1
      if     (rlat                      .ge.  0.0) then
      if     (rlat                      .le.  8.0) then
        if (rlon .lt.  285.0) ibasin=2
      elseif (rlat .gt.  8.0 .and. rlat .le. 15.0) then
        if (rlon .lt.  275.0) ibasin=2
      elseif (rlat .gt. 15.0 .and. rlat .le. 17.5) then
        if (rlon .lt.  270.0) ibasin=2
      elseif (rlat .gt. 17.5                     ) then
         if (rlon .lt.  260.0) ibasin=2
      endif
      endif
c 
      if ((rlon .lt. 180) .and. (rlat .ge. 0))  ibasin=3
c 
      if ((rlon .lt. 280) .and. (rlat .lt. 0))  ibasin=4
c 
      if (rlon .lt. 100) ibasin=5
c       
      return
      end subroutine
c 
      subroutine jdate2(imon,iday,iyear,julday)
c     This routine calculates the Julian day (julday) from
c     the month (imon), day (iday), and year (iyear). The
c     appropriate correction is made for leap year.
c 
      dimension ndmon(12)
c 
c     Specify the number of days in each month
      ndmon(1)  = 31
      ndmon(2)  = 28
      ndmon(3)  = 31
      ndmon(4)  = 30
      ndmon(5)  = 31
      ndmon(6)  = 30
      ndmon(7)  = 31
      ndmon(8)  = 31
      ndmon(9)  = 30
      ndmon(10) = 31
      ndmon(11) = 30
      ndmon(12) = 31
c 
c     Correct for leap year
      if (mod(iyear,4) .eq. 0) ndmon(2)=29
c 
c     Check for illegal input
      if (imon .lt. 1 .or. imon .gt. 12) then
         julday=-1
         return
      endif
c 
      if (iday .lt. 1 .or. iday .gt. ndmon(imon)) then
         julday=-1
         return
      endif
c 
c     Calculate the Julian day
      julday = iday
      if (imon .gt. 1) then
         do 10 i=2,imon
            julday = julday + ndmon(i-1)
   10    continue
      endif
c 
      return
      end subroutine
c 
      END MODULE ships_input
