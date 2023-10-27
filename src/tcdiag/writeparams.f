c-----7---------------------------------------------------------------72
c     subroutine writeparams
c-----7---------------------------------------------------------------72
      SUBROUTINE writeparams(luou,ierr,rmiss,imiss,imissd,
     $     nvar,diagvar,idiagvar,
     $     nvaru,udiagvar,iudiagvar,
     $     nsnd,usnd,vsnd,tsnd,rsnd,zsnd,
     $     usfc,vsfc,tsfc,rsfc,psfc)
c-----7---------------------------------------------------------------72
c     Given the dtg, model, and forecast time; return the latitude,
c      longitude, vmax and pmin
c
c     ierr returns 1 if file not read in correctly
c
c-----7---------------------------------------------------------------72
c 
      IMPLICIT NONE
c 
      integer, intent(in) :: luou
      integer, intent(in) :: imiss, imissd
      real, intent(in) :: rmiss
      integer, intent(in) :: nvar
      real, dimension(nvar), intent(in) :: diagvar
      integer, dimension(nvar), intent(in) :: idiagvar
      integer, intent(in) :: nsnd
      real, dimension(nsnd), intent(in) :: usnd, vsnd, tsnd, rsnd, zsnd
      real, intent(in) :: usfc, vsfc, tsfc, rsfc, psfc

      integer, intent(in) :: nvaru
      real, dimension(nvaru), intent(in) :: udiagvar
      integer, dimension(nvaru), intent(in) :: iudiagvar

      integer, intent(out) :: ierr
c 
c     local variables
      integer :: n
c 
c     initialize error flag
      ierr = 0
c     initialize write out format
  110    format(i6)
 
      print*,'ssssssssssssssssss ',nvar 
 
      do n=1,nvar
         write(luou,110) idiagvar(n)
      enddo
 
      !write out surface variables
      if (tsfc .le. rmiss) then
         write(luou,110) imissd
      else
         write(luou,110) nint((tsfc-273.15)*10.0)
      endif
      if (rsfc .le. rmiss) then
         write(luou,110) imissd
      else
         write(luou,110) nint(rsfc)
      endif
      if (psfc .le. rmiss) then
         write(luou,110) imissd
      else
         write(luou,110) nint(psfc/100.0)
      endif
      if (usfc .le. rmiss) then
         write(luou,110) imissd
      else
         write(luou,110) nint(usfc*10.0)
      endif
      if (vsfc .le. rmiss) then
         write(luou,110) imissd
      else
         write(luou,110) nint(vsfc*10.0)
      endif
      
c--       user diagvars          
c         
      print*,'uuuuuuuuuuuuuuuuuu ',nvaru
      do n=1,nvaru
         write(luou,110) iudiagvar(n)
      enddo

c--       write  out sounding variables
c
      do n=1,nsnd
        print*,'nnnnnnnnnnnnnnnnn ',n
         if (tsnd(n) .le. rmiss) then
            write(luou,110) imissd
         else
            write(luou,110) nint((tsnd(n)-273.15)*10.0)
         endif
         if (rsnd(n) .le. rmiss) then
            write(luou,110) imissd
         else
            write(luou,110) nint(rsnd(n))
         endif
         if (zsnd(n) .le. rmiss) then
            write(luou,110) imissd
         else
            write(luou,110) nint(zsnd(n)/10.0)
         endif
         if (usnd(n) .le. rmiss) then
            write(luou,110) imissd
         else
            write(luou,110) nint(usnd(n)*10.0)
         endif
         if (vsnd(n) .le. rmiss) then
            write(luou,110) imissd
         else
            write(luou,110) nint(vsnd(n)*10.0)
         endif
      enddo
c 
      return
c 
 1009 continue
      ierr = 1
      write(*,*) 'Parameter write failure'
      return
c 
      END SUBROUTINE writeparams
